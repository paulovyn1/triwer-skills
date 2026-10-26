"""Comentários reais para compor a história (dor, frase do público, opinião), em texto: zero imagem, barato de ler.

    python buscar_comentarios.py youtube "<url do vídeo>" [--filtro "palavra|outra"] [--max 300] [--top 15]
        comentários de um vídeo (ótima fonte em português: buscar vídeos brasileiros do tema e filtrar pela dor)
    python buscar_comentarios.py hn "<termo em inglês>" [--top 10]
        comentários do Hacker News (API pública), por relevância; termo curto e específico ("freelance burnout") funciona melhor

Saída: lista "likes | data | autor anonimizado | texto | link". Para usar no vídeo: cartão de citação com o texto, a fonte
(site + data) e o autor só com iniciais. Nunca imitar o print da rede, nem expor pessoa comum.
"""
from __future__ import annotations

import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import requests


def anon(nome: str) -> str:
    partes = [p for p in re.split(r"[\s_.@-]+", nome or "") if p]
    return ".".join(p[0].upper() for p in partes[:2]) + "." if partes else "anônimo"


def youtube(a) -> None:
    exe = [shutil.which("yt-dlp")] if shutil.which("yt-dlp") else [sys.executable, "-m", "yt_dlp"]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "v"
        r = subprocess.run([*exe, "--skip-download", "--write-comments", "--no-warnings",
                            "--extractor-args", f"youtube:max_comments={a.max},all,0;comment_sort=top", "-o", str(out), a.url],
                           capture_output=True, text=True, encoding="utf-8")
        js = list(Path(tmp).glob("*.info.json"))
        if not js:
            sys.exit(f"falhou: {r.stderr[-300:]}")
        m = json.loads(js[0].read_text(encoding="utf-8"))
    pat = re.compile(a.filtro, re.I) if a.filtro else None
    cs = [c for c in m.get("comments") or [] if not pat or pat.search(c.get("text", ""))]
    cs.sort(key=lambda c: -(c.get("like_count") or 0))
    print(f"{m.get('title')} | {m.get('channel')} | {len(cs)} comentário(s) após o filtro")
    for c in cs[: a.top]:
        t = re.sub(r"\s+", " ", c.get("text", ""))[:300]
        print(f"{c.get('like_count') or 0} | {c.get('_time_text') or ''} | {anon(c.get('author', ''))} | {t} | {a.url}&lc={c.get('id')}")


def hn(a) -> None:
    r = requests.get("https://hn.algolia.com/api/v1/search", params={"query": a.termo, "tags": "comment", "hitsPerPage": 50}, timeout=30).json()
    hits = r.get("hits", [])  # já vêm por relevância (comentário quase nunca tem pontos na API)
    for h in hits[: a.top]:
        t = html.unescape(re.sub("<[^>]+>", " ", h.get("comment_text") or ""))
        t = re.sub(r"\s+", " ", t)[:320]
        print(f"{h.get('points') or 0} | {h.get('created_at', '')[:10]} | {anon(h.get('author', ''))} | {t} | https://news.ycombinator.com/item?id={h['objectID']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    y = sub.add_parser("youtube")
    y.add_argument("url")
    y.add_argument("--filtro")
    y.add_argument("--max", type=int, default=300)
    y.add_argument("--top", type=int, default=15)
    h = sub.add_parser("hn")
    h.add_argument("termo")
    h.add_argument("--top", type=int, default=10)
    a = ap.parse_args()
    youtube(a) if a.cmd == "youtube" else hn(a)


if __name__ == "__main__":
    main()
