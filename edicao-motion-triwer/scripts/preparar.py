"""Etapa 0: prepara a pasta edit/, extrai o áudio, transcreve palavra a palavra e imprime a LEITURA do vídeo.

Uso:  cd "<pasta do vídeo>" && python <skill>/scripts/preparar.py "<video.mp4>"
Cria edit/{work,verify,audio,transcripts,entrega} e edit/projeto.json (modelo), extrai work/orig.wav (48k mono 24-bit),
transcreve com Groq whisper-large-v3 (GROQ_API_KEY; cacheado), roda o faster-whisper (relógio preciso) e imprime: texto com tempo de
cada palavra e as pausas >= 0,12 s, tomadas repetidas, a mesma janela segundo o faster-whisper quando há várias tomadas, e silêncios.
É a ÚNICA saída que o Claude precisa ler pra decidir cortes e legenda: não abrir o JSON cru.
"""
from __future__ import annotations

import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
video = Path(sys.argv[1]).resolve()
edit = (video.parent / "edit")
for d in ("work", "verify", "audio", "transcripts", "entrega"):
    (edit / d).mkdir(parents=True, exist_ok=True)

proj = edit / "projeto.json"
if not proj.exists():
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(video)],
                                     capture_output=True, text=True).stdout)
    dur = float(info["format"]["duration"])
    proj.write_text(json.dumps({
        "nome": video.stem, "cliente": "", "fonte": str(video), "fps": 30,
        "corte": {"inicio": 0.0, "fim": round(dur, 2), "min_pausa": 0.13, "mantem_depois": 0.07, "mantem_antes": 0.05,
                  "limiar_db_abaixo_da_fala": 16, "pausas_dramaticas": {}, "remover": []},
        "texto": {"correcoes": {}, "descartar": [], "retempo": []},
        "musica": {"candidatas": "music_cand", "lufs_musica": -23.0, "trechos": [], "versoes": {}},
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"criado {proj} (ajuste corte.inicio/fim depois de ler a transcrição)")

orig = edit / "work" / "orig.wav"
if not orig.exists():
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "48000",
                    "-c:a", "pcm_s24le", str(orig)], check=True)

env = {**__import__("os").environ, "EDIT_DIR": str(edit), "PYTHONUTF8": "1"}
subprocess.run([sys.executable, str(HERE / "transcribe_groq.py"), str(video), "--edit-dir", str(edit)], check=True, env=env)

# segunda opinião de timing (faster-whisper, CPU, ≈ 40 s, cacheado): words_out.py usa quando bate com o Groq
fw = edit / "transcripts" / "fw_small_words.json"
if not fw.exists():
    r = subprocess.run([sys.executable, str(HERE / "fw_check.py"), str(orig), "small", str(fw)], env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    if not fw.exists():
        print("AVISO: fw_check.py falhou (sem faster-whisper: tempos só do Groq). Últimas linhas do erro:\n  "
              + "\n  ".join((r.stderr or "").strip().splitlines()[-3:]), file=sys.stderr)

tr = json.loads((edit / "transcripts" / f"{video.stem}.json").read_text(encoding="utf-8"))
words = [w for w in tr["words"] if w["type"] == "word"]
desordem = sum(1 for a, b in zip(words, words[1:]) if b["start"] < a["start"] - 0.05)
words.sort(key=lambda w: w["start"])
out = []
for i, w in enumerate(words):
    gap = w["start"] - (words[i - 1]["end"] if i else 0.0)
    if gap >= 0.12:
        out.append(f"<{gap:.2f}>")
    out.append(f"{w['text']}[{w['start']:.2f}]")
dur = tr.get("duration", 0) or words[-1]["end"]
linhas = [f"{len(words)} palavras · duração {dur:.1f}s", "", " ".join(out), ""]

# tomadas repetidas: trecho de 3 palavras que reaparece > 2,5 s depois = a pessoa regravou a frase; ficar com a ÚLTIMA/mais limpa
norm = lambda s: re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())
tri: dict = {}
for i in range(len(words) - 2):
    k = " ".join(norm(w["text"]) for w in words[i:i + 3])
    tri.setdefault(k, []).append((words[i]["start"], " ".join(w["text"] for w in words[i:i + 3])))
rep = []
for k, v in tri.items():
    ts = [x[0] for x in v]
    if len(v) >= 2 and ts[-1] - ts[0] > 2.5 and len(k) > 8:
        rep.append((len(v), ts, v[0][1]))
rep.sort(key=lambda r: (-r[0], r[1][0]))
if rep:
    linhas.append("POSSÍVEIS TOMADAS REPETIDAS (frase dita mais de uma vez; decida corte.remover, ficando com a tomada mais limpa):")
    for n, ts, txt in rep[:8]:
        linhas.append(f"  \"{txt}\" em " + ", ".join(f"{x:.1f}s" for x in ts))
if desordem:
    linhas.append(f"AVISO: {desordem} palavras do Groq com tempo fora de ordem (trecho com várias tomadas): use a janela do faster-whisper abaixo.")
if (rep or desordem) and fw.exists():
    fwl = json.loads(fw.read_text(encoding="utf-8"))
    ini = min(min(r[1]) for r in rep) - 3 if rep else 0
    jan = [w for w in fwl if w["start"] >= ini]
    linhas += ["", f"JANELA DAS TOMADAS segundo o faster-whisper (relógio mais preciso; texto pode errar palavra) a partir de {ini:.1f}s:",
               " ".join(f"{w['text']}[{w['start']:.2f}-{w['end']:.2f}]" for w in jan)]
g = subprocess.run([sys.executable, str(HERE / "gaps.py"), str(orig), "0.4"], capture_output=True, text=True, env=env).stdout.strip()
linhas += ["", "SILÊNCIOS >= 0,4 s (início - fim):", g,
           "", "Bordas de corte com folga certa: python bordas.py <t1> <t2> ... (energia a cada 30 ms em volta de cada tempo)"]
saida = "\n".join(linhas)
(edit / "work" / "leitura.txt").write_text(saida, encoding="utf-8")
print(saida)
print("\n(leitura gravada em edit/work/leitura.txt)")
