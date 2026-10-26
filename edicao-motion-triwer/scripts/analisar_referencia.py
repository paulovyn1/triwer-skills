"""Analisa um vídeo de REFERÊNCIA de edição gastando o mínimo de tokens: tudo que dá para medir vira texto, e o que
precisa de olho vira poucas folhas de quadros rotuladas (1 leitura de imagem por ~14 s de vídeo).

Uso:  python analisar_referencia.py <video> [--saida DIR] [--fps 2] [--larg 216] [--sem-fala] [--idioma pt]

Saída (padrão <pasta do vídeo>/<nome>_analise/):
  resumo.txt        metadados, cortes secos e transições suaves (com tempos), ritmo, fala por frase com tempos,
                    palavras por minuto, densidade de transientes (proxy de efeito sonoro), loudness
  folha_NN.png      quadros a N fps; cada um com o tempo e a palavra falada naquele instante.
                    Borda vermelha = primeiro quadro depois de um corte seco; laranja = dentro de transição suave.
  fala.json         cache da transcrição (Groq whisper-large-v3; precisa de GROQ_API_KEY)

Ler primeiro o resumo.txt. Abrir as folhas só depois, na ordem, e anotar o estilo no modelo de estilos/_modelo.md.
"""
from __future__ import annotations

import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CORTE = 0.30      # score de cena acima disso = corte seco
COLS, LINHAS = 7, 4


def sh(cmd: list, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def meta(v: Path) -> dict:
    j = json.loads(sh(["ffprobe", "-v", "error", "-show_entries",
                       "format=duration:stream=codec_type,width,height,r_frame_rate", "-of", "json", str(v)]).stdout)
    vs = next(s for s in j["streams"] if s["codec_type"] == "video")
    n, d = vs["r_frame_rate"].split("/")
    return {"dur": float(j["format"]["duration"]), "w": vs["width"], "h": vs["height"], "fps": float(n) / float(d),
            "audio": any(s["codec_type"] == "audio" for s in j["streams"])}


def scores(v: Path, tmp: Path) -> list[tuple[float, float]]:
    """score de mudança de cena de TODO quadro (ffmpeg scene), em resolução baixa."""
    sh(["ffmpeg", "-v", "error", "-i", str(v), "-an", "-vf",
        "scale=160:-2,select='gte(scene,0)',metadata=print:file=scores.txt", "-f", "null", "-"], cwd=tmp)
    out, t = [], None
    for ln in (tmp / "scores.txt").read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.search(r"pts_time:([\d.]+)", ln)
        if m:
            t = float(m.group(1))
        m = re.search(r"lavfi\.scene_score=([\d.]+)", ln)
        if m and t is not None:
            out.append((t, float(m.group(1))))
    return out


def movimento(v: Path, m: dict, cortes: list[float]) -> tuple[list[tuple[float, float]], list[tuple[float, float]], float]:
    """Diferença média entre quadros (cinza, 96 px). Devolve (movimento forte sem corte, trechos parados > 0,5 s, % parado).
    O score de cena do ffmpeg só pega corte seco; câmera andando, chicote e morph aparecem aqui."""
    import numpy as np
    w = 96
    h = max(2, round(w * m["h"] / m["w"] / 2) * 2)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(v), "-an", "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    q = np.frombuffer(raw, np.uint8)[: (len(raw) // (w * h)) * w * h].reshape(-1, h, w).astype(np.int16)
    if len(q) < 3:
        return [], [], 0.0
    d = np.abs(np.diff(q, axis=0)).mean(axis=(1, 2))
    d = np.concatenate([[d[0]], d])
    t = np.arange(len(d)) / m["fps"]
    perto_corte = np.zeros(len(d), bool)
    for c in cortes:
        perto_corte |= np.abs(t - c) <= 1.5 / m["fps"]
    # quadros repetidos (vídeo 24→30 fps) zeram a diferença: média só dos quadros que mudaram, numa janela de 5
    jan = []
    for i in range(len(d)):
        x = d[max(0, i - 2): i + 3]
        x = x[x > 0.05]
        jan.append(x.mean() if len(x) else 0.0)
    jan = np.array(jan)
    limiar = max(2.5, float(np.percentile(jan[~perto_corte], 85)))
    fortes, parados, ini = [], [], None
    for i, (val, pc) in enumerate(zip(jan, perto_corte)):
        if val >= limiar and not pc:
            ini = i if ini is None else ini
        else:
            if ini is not None and i - ini >= 4:
                fortes.append((round(t[ini], 2), round(t[i - 1], 2)))
            ini = None
    ini = None
    for i, val in enumerate(jan):
        if val < 0.35:
            ini = i if ini is None else ini
        else:
            if ini is not None and (i - ini) / m["fps"] > 0.5:
                parados.append((round(t[ini], 2), round(t[i - 1], 2)))
            ini = None
    if ini is not None and (len(jan) - ini) / m["fps"] > 0.5:
        parados.append((round(t[ini], 2), round(t[-1], 2)))
    pct = sum(b - a for a, b in parados) / m["dur"] * 100
    return fortes, parados, pct


def fala(v: Path, cache: Path, idioma: str | None) -> dict | None:
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        print("aviso: GROQ_API_KEY ausente, sem transcrição")
        return None
    import requests
    with tempfile.TemporaryDirectory() as tmp:
        a = Path(tmp) / "a.flac"
        sh(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "flac", str(a)])
        data = [("model", "whisper-large-v3"), ("response_format", "verbose_json"), ("temperature", "0"),
                ("timestamp_granularities[]", "word"), ("timestamp_granularities[]", "segment")]
        if idioma:
            data.append(("language", idioma))
        with open(a, "rb") as f:
            r = requests.post("https://api.groq.com/openai/v1/audio/transcriptions",
                              headers={"Authorization": f"Bearer {key}"},
                              files={"file": ("a.flac", f, "audio/flac")}, data=data, timeout=600)
    if r.status_code != 200:
        print(f"aviso: Groq {r.status_code}: {r.text[:200]}")
        return None
    g = r.json()
    j = {"idioma": g.get("language"), "texto": g.get("text", "").strip(),
         "palavras": [{"w": w["word"].strip(), "s": round(w["start"], 2), "e": round(w["end"], 2)} for w in g.get("words", [])],
         "frases": [{"s": round(s["start"], 2), "e": round(s["end"], 2), "t": s["text"].strip()} for s in g.get("segments", [])]}
    cache.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    return j


def audio(v: Path) -> dict:
    r = {}
    e = sh(["ffmpeg", "-v", "info", "-nostats", "-i", str(v), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    if m:
        r["lufs"] = float(m[-1])
    m = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
    if m:
        r["pico"] = float(m[-1])
    try:
        import librosa
        import numpy as np
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.wav"
            sh(["ffmpeg", "-y", "-v", "error", "-i", str(v), "-vn", "-ac", "1", "-ar", "22050", str(a)])
            y, sr = librosa.load(a, sr=None)
        env = librosa.onset.onset_strength(y=y, sr=sr)
        on = librosa.onset.onset_detect(onset_envelope=env, sr=sr, units="time", delta=0.25)  # só transientes fortes
        r["transientes_fortes"] = [round(float(t), 2) for t in on]
        tempo = librosa.beat.beat_track(onset_envelope=env, sr=sr)[0]
        r["bpm_estimado"] = round(float(np.atleast_1d(tempo)[0]))
    except Exception as ex:  # noqa: BLE001
        r["erro_librosa"] = str(ex)[:120]
    return r


def fonte(px: int):
    for p in ("C:/Windows/Fonts/arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, px)
    return ImageFont.load_default()


def palavra_em(t: float, f: dict | None) -> str:
    if not f:
        return ""
    for w in f["palavras"]:
        if w["s"] - 0.05 <= t <= w["e"] + 0.05:
            return w["w"]
    return "·"


def folhas(v: Path, out: Path, fps_folha: float, larg: int, cortes, suaves, f) -> list[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        sh(["ffmpeg", "-v", "error", "-i", str(v), "-vf", f"fps={fps_folha},scale={larg}:-2", str(Path(tmp) / "q%04d.jpg")])
        qs = sorted(Path(tmp).glob("q*.jpg"))
        ims = [Image.open(q).convert("RGB") for q in qs]
    if not ims:
        return []
    fn, fs = fonte(15), fonte(13)
    h = ims[0].height
    barra = 36
    cel = []
    for i, im in enumerate(ims):
        t = i / fps_folha
        tp = (i - 1) / fps_folha
        cor = None
        if any(tp < c <= t + 1e-3 for c in cortes):
            cor = (230, 30, 30)
        elif any(a - 0.05 <= t <= b + 0.05 for a, b in suaves):
            cor = (255, 150, 0)
        c = Image.new("RGB", (larg, h + barra), (14, 14, 18))
        c.paste(im, (0, 0))
        d = ImageDraw.Draw(c)
        if cor:
            d.rectangle([0, 0, larg - 1, h - 1], outline=cor, width=5)
        d.text((5, h + 2), f"{t:5.1f}s", font=fn, fill=(255, 235, 0))
        d.text((5, h + 19), palavra_em(t, f)[:22], font=fs, fill=(220, 220, 220))
        cel.append(c)
    por = COLS * LINHAS
    saidas = []
    for k in range(0, len(cel), por):
        bloco = cel[k:k + por]
        linhas = (len(bloco) + COLS - 1) // COLS
        fl = Image.new("RGB", (COLS * larg, linhas * (h + barra)), (40, 40, 46))
        for j, c in enumerate(bloco):
            fl.paste(c, ((j % COLS) * larg, (j // COLS) * (h + barra)))
        p = out / f"folha_{k // por + 1:02d}.png"
        fl.save(p)
        saidas.append(p)
    return saidas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--saida", type=Path)
    ap.add_argument("--fps", type=float, default=2.0, help="quadros por segundo nas folhas")
    ap.add_argument("--larg", type=int, default=216, help="largura da miniatura")
    ap.add_argument("--sem-fala", action="store_true")
    ap.add_argument("--idioma", default=None, help="pt, en... (padrão: detectar)")
    a = ap.parse_args()
    v = a.video.resolve()
    out = (a.saida or v.parent / f"{v.stem}_analise").resolve()
    out.mkdir(parents=True, exist_ok=True)
    m = meta(v)
    with tempfile.TemporaryDirectory() as tmp:
        sc = scores(v, Path(tmp))
    cortes = [t for t, s in sc if s >= CORTE]
    suaves, parados, pct_parado = movimento(v, m, cortes)
    f = None if a.sem_fala or not m["audio"] else fala(v, out / "fala.json", a.idioma)
    au = audio(v) if m["audio"] else {}
    fl = folhas(v, out, a.fps, a.larg, cortes, suaves, f)

    planos = [0.0] + cortes + [m["dur"]]
    dur_planos = [round(b - a_, 2) for a_, b in zip(planos, planos[1:]) if b - a_ > 0.04]
    L = [f"# {v.name}",
         f"{m['dur']:.1f} s | {m['w']}x{m['h']} | {m['fps']:.0f} fps | áudio: {'sim' if m['audio'] else 'não'}",
         "",
         f"## Ritmo visual",
         f"cortes secos: {len(cortes)} ({len(cortes) / m['dur'] * 60:.0f}/min) | plano médio {sum(dur_planos) / len(dur_planos):.2f} s"
         f" | mais longo {max(dur_planos):.2f} s | mais curto {min(dur_planos):.2f} s",
         "cortes em: " + ", ".join(f"{t:.2f}" for t in cortes),
         f"movimento forte sem corte ({len(suaves)}; câmera andando, chicote, morph = transições suaves): "
         + ", ".join(f"{a_:.2f}-{b:.2f}" for a_, b in suaves),
         f"parado: {pct_parado:.0f}% do vídeo em trechos > 0,5 s" + (": " + ", ".join(f"{a_:.1f}-{b:.1f}" for a_, b in parados) if parados else ""),
         "(muito movimento forte e poucos cortes = cenas emendadas por motion; conferir nas folhas, borda laranja)",
         ""]
    if f:
        ws = f["palavras"]
        falado, fim = 0.0, -1.0  # união dos intervalos (palavras do Whisper se sobrepõem)
        for w in sorted(ws, key=lambda w: w["s"]):
            ini_w = max(w["s"], fim)
            if w["e"] > ini_w:
                falado += w["e"] - ini_w
            fim = max(fim, w["e"])
        ppm = len(ws) / (ws[-1]["e"] - ws[0]["s"]) * 60 if len(ws) > 1 else 0
        L += [f"## Fala ({f.get('idioma')})",
              f"{len(ws)} palavras | {ppm:.0f} palavras/min | fala cobre {min(100, falado / m['dur'] * 100):.0f}% do vídeo"
              f" | primeira palavra em {ws[0]['s'] if ws else '-'} s",
              *[f"[{fr['s']:5.1f}-{fr['e']:5.1f}] {fr['t']}" for fr in f["frases"]], ""]
    if au:
        tr = au.get("transientes_fortes", [])
        L += ["## Áudio",
              f"loudness {au.get('lufs', '?')} LUFS | pico {au.get('pico', '?')} dBFS | BPM estimado {au.get('bpm_estimado', '?')}",
              f"transientes fortes (golpes, impactos, cliques; inclui consoantes da fala): {len(tr)}"
              f" ({len(tr) / m['dur']:.1f}/s)",
              "em: " + ", ".join(f"{t:.1f}" for t in tr[:80]), ""]
        coinc = sum(1 for c in cortes if any(abs(c - t) <= 0.08 for t in tr))
        if cortes:
            L.append(f"cortes com golpe de áudio a ±80 ms: {coinc}/{len(cortes)}")
    L += ["", "## Folhas", *[str(p.name) for p in fl]]
    (out / "resumo.txt").write_text("\n".join(L), encoding="utf-8")
    print(out / "resumo.txt", f"| {len(fl)} folha(s)")


if __name__ == "__main__":
    main()
