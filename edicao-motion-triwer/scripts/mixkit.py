"""Leitura do catálogo público do Mixkit (música e efeitos): cartões das páginas de listagem -> id, título, tags, duração.

Licenças (conferidas em mixkit.co): Stock Music Free License (anúncio online ok, sem crédito; não CD/DVD/jogo/TV/rádio) e
Sound Effects Free License (uso comercial, sem crédito). Módulo usado por indexar_musicas.py, indexar_sfx.py e sfx.py.
"""
import html
import re
import time
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (edicao-motion-triwer)"}
BASE = "https://mixkit.co"
CARD = re.compile(r'data-audio-player-item-id-value="(\d+)"\s+data-audio-player-item-type-value="(\w+)"')


def get(url: str, tentativas: int = 3) -> str:
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore")
        except Exception:
            if k == tentativas - 1:
                raise
            time.sleep(2 * (k + 1))
    return ""


def baixar(url: str, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists() or destino.stat().st_size < 1000:
        req = urllib.request.Request(url, headers=UA)
        destino.write_bytes(urllib.request.urlopen(req, timeout=90).read())
    return destino


def url_musica(i: str) -> str:
    return f"https://assets.mixkit.co/music/{i}/{i}.mp3"


def url_sfx(i: str) -> str:
    return f"https://assets.mixkit.co/active_storage/sfx/{i}/{i}-preview.mp3"


def sfx_catalogo(nome: str, pasta_sfx: Path, cache: Path) -> Path | None:
    """Som do CATALOGO.md pelo nome. Usa o arquivo da pasta se existir; senão baixa do Mixkit pelo id da tabela para o cache
    (a skill compartilhada não leva os .mp3: a licença do Mixkit não permite redistribuir o arquivo) ou gera o som "gerado"."""
    for ext in ("wav", "mp3"):
        if (pasta_sfx / f"{nome}.{ext}").exists():
            return pasta_sfx / f"{nome}.{ext}"
    cat = pasta_sfx / "CATALOGO.md"
    if not cat.exists():
        return None
    for ln in cat.read_text(encoding="utf-8").splitlines():
        cols = [c.strip().strip("`") for c in ln.split("|")]
        if len(cols) > 3 and cols[1] == nome:
            if cols[2].isdigit():
                return baixar(url_sfx(cols[2]), cache / "sfx" / f"{cols[2]}.mp3")
            m = re.search(r"seno (\d+) kHz, ([\d,]+) s", cols[2])
            if m:  # efeito sintetizado (ex.: flatline)
                import subprocess
                out = cache / "sfx" / f"{nome}.wav"
                out.parent.mkdir(parents=True, exist_ok=True)
                if not out.exists():
                    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                                    f"sine=frequency={int(m.group(1)) * 1000}:duration={m.group(2).replace(',', '.')}",
                                    "-af", "volume=0.5", str(out)], check=True)
                return out
    return None


def dur_s(txt: str):
    p = [int(x) for x in txt.strip().split(":") if x.isdigit()]
    return p[0] * 60 + p[1] if len(p) == 2 else (p[0] if p else None)


def cartoes(pagina: str) -> list:
    """cada item da grade: id, tipo (music|sfx), título, tags [(tipo, slug, nome)], duração em s (quando a página mostra)"""
    achados = list(CARD.finditer(pagina))
    out = []
    for i, m in enumerate(achados):
        fim = achados[i + 1].start() if i + 1 < len(achados) else m.end() + 8000
        bloco = pagina[m.end():fim]
        t = re.search(r'item-grid-card__title">\s*([^<]+?)\s*</h2>', bloco)
        if not t:
            continue
        tags = []
        for href, nome in re.findall(r'class="meta-links__link"[^>]*href="(/free-[^"]+)">([^<]+)</a>', bloco):
            partes = [p for p in href.strip("/").split("/") if p]
            if len(partes) >= 3:
                tipo, slug = partes[1], partes[2]
            else:
                tipo, slug = ("genre" if partes[0] == "free-stock-music" else "categoria"), partes[-1]
            tags.append((tipo, slug, html.unescape(nome.strip())))
        d = re.search(r'data-test-id="duration">\s*([\d:]+)', bloco)
        out.append({"id": m.group(1), "tipo": m.group(2), "titulo": html.unescape(t.group(1)), "tags": tags,
                    "dur": dur_s(d.group(1)) if d else None})
    return out


def links_categoria(pagina: str, raiz: str) -> set:
    """links de categoria (/free-stock-music/mood/x/, /free-sound-effects/x/ ...) encontrados na página"""
    pad = re.escape(raiz) + r"[a-z0-9-]+/(?:[a-z0-9-]+/)?"
    return set(re.findall(r'href="(' + pad + r')"', pagina))
