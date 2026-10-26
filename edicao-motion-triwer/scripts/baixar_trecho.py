"""Trecho de fala real do YouTube (entrevista, palestra, podcast): acha a frase pela legenda e baixa SÓ aquele pedaço.

    python baixar_trecho.py achar "<url>" "<frase ou palavras-chave>" [--idioma pt]
        lê a legenda (manual ou automática) sem baixar o vídeo e mostra os 3 trechos mais parecidos, com tempo de início e fim
    python baixar_trecho.py baixar "<url>" --de 83.2 --ate 91.5 [--nome entrevista_x] [--destino fontes] [--folga 0.3]
        baixa só [de-folga, ate+folga] em mp4 (yt-dlp --download-sections, cortes em keyframe forçado) e grava os créditos

Regras (detalhe em references/fontes-reais.md):
  - conteúdo orgânico: trecho curto (até ~10 s), com crédito na tela (nome + fonte), comentando/contextualizando.
  - anúncio pago: NÃO usar imagem/voz de pessoa famosa (sugere endosso; direito de imagem; a plataforma reprova).
  - nunca mudar o sentido da fala com corte.
"""
from __future__ import annotations

import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import argparse
import difflib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

import requests


def ytdlp() -> list[str]:
    exe = shutil.which("yt-dlp")
    return [exe] if exe else [sys.executable, "-m", "yt_dlp"]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def info(url: str) -> dict:
    r = subprocess.run([*ytdlp(), "--dump-json", "--skip-download", "--no-warnings", url], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        sys.exit(f"yt-dlp falhou: {r.stderr[-400:]}")
    return json.loads(r.stdout)


def legenda(meta: dict, idioma: str) -> list[tuple[float, float, str]]:
    man, auto = meta.get("subtitles") or {}, meta.get("automatic_captions") or {}
    do_idioma = lambda pool: [k for k in pool if k == idioma or k.startswith(idioma + "-")]  # noqa: E731
    # ordem: manual no idioma pedido → automática no idioma pedido (a "-orig" é a da fala original) → qualquer outra
    ordem = [(man, k) for k in do_idioma(man)] + [(auto, k) for k in sorted(do_idioma(auto), key=lambda k: not k.endswith("-orig"))]
    ordem += [(man, k) for k in man if (man, k) not in ordem] + [(auto, k) for k in auto if k.endswith("-orig")]
    pools = [man, auto]
    for pool, lang in ordem:
        fmts = pool.get(lang)
        if fmts:
            j3 = next((f for f in fmts if f.get("ext") == "json3"), None)
            if not j3:
                continue
            ev = requests.get(j3["url"], timeout=30).json().get("events", [])
            out = []
            for e in ev:
                txt = "".join(s.get("utf8", "") for s in e.get("segs", []) or []).replace("\n", " ").strip()
                if txt:
                    ini = e.get("tStartMs", 0) / 1000
                    out.append((ini, ini + e.get("dDurationMs", 0) / 1000, txt))
            if out:
                print(f"legenda: {lang} ({'manual' if pool is pools[0] else 'automática'}), {len(out)} trechos")
                return out
    sys.exit("vídeo sem legenda: transcrever um pedaço baixado com o Whisper (transcribe_groq.py) para achar a frase")


def achar(a) -> None:
    m = info(a.url)
    print(f"{m.get('title')} | {m.get('channel')} | {m.get('upload_date')} | {m.get('duration')} s")
    leg = legenda(m, a.idioma)
    alvo = norm(a.frase)
    n = max(1, len(alvo.split()) // 6 + 1)
    melhores = []
    palavras = set(alvo.split())
    for i in range(len(leg)):
        for k in range(1, n + 3):  # janelas de 1 a n+2 trechos; a mais curta que cobre a frase ganha
            bloco = leg[i:i + k]
            if len(bloco) < k:
                break
            txt = " ".join(t for _, _, t in bloco)
            r = difflib.SequenceMatcher(None, alvo, norm(txt)).ratio()
            cobre = len(palavras & set(norm(txt).split())) / max(1, len(palavras))
            melhores.append((0.5 * r + 0.5 * cobre - 0.02 * k, bloco[0][0], bloco[-1][1], txt))
    melhores.sort(reverse=True)
    vistos = []
    for nota, ini, fim, txt in melhores:
        if any(abs(ini - v) < 4 for v in vistos):
            continue
        vistos.append(ini)
        print(f"\n[{nota:.2f}] {ini:.1f}-{fim:.1f} s  →  {txt[:220]}")
        if len(vistos) == 3:
            break
    print("\nbaixar: python baixar_trecho.py baixar \"<url>\" --de <ini> --ate <fim>  (ajustar a borda ouvindo; legenda automática tem folga de ~0,5 s)")


def baixar(a) -> None:
    m = info(a.url)
    dest = Path(a.destino).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    nome = a.nome or re.sub(r"[^a-z0-9]+", "_", norm(m.get("title", "trecho")))[:40]
    de, ate = max(0.0, a.de - a.folga), a.ate + a.folga
    saida = dest / f"{nome}_{int(de)}-{int(ate)}.mp4"
    cmd = [*ytdlp(), "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b", "--merge-output-format", "mp4",
           "--download-sections", f"*{de:.2f}-{ate:.2f}", "--force-keyframes-at-cuts", "--no-playlist", "-o", str(saida), a.url]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode or not saida.exists():
        sys.exit(f"falhou: {r.stderr[-500:]}")
    cred_p = dest / "creditos.json"
    cred = json.loads(cred_p.read_text(encoding="utf-8")) if cred_p.exists() else []
    cred.append({"arquivo": saida.name, "fonte": "youtube", "titulo": m.get("title"), "canal": m.get("channel"),
                 "data": m.get("upload_date"), "url": a.url, "trecho": [round(de, 2), round(ate, 2)],
                 "uso": "orgânico com crédito na tela; anúncio pago: não usar pessoa famosa"})
    cred_p.write_text(json.dumps(cred, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{saida} ({saida.stat().st_size / 1e6:.1f} MB) | crédito: {m.get('channel')} — {m.get('title')}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("achar")
    c.add_argument("url")
    c.add_argument("frase")
    c.add_argument("--idioma", default="pt")
    b = sub.add_parser("baixar")
    b.add_argument("url")
    b.add_argument("--de", type=float, required=True)
    b.add_argument("--ate", type=float, required=True)
    b.add_argument("--nome")
    b.add_argument("--destino", default="fontes")
    b.add_argument("--folga", type=float, default=0.3)
    a = ap.parse_args()
    achar(a) if a.cmd == "achar" else baixar(a)


if __name__ == "__main__":
    main()
