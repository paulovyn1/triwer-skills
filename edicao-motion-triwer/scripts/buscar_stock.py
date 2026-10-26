"""Busca vídeo/foto gratuito em vários bancos e devolve UMA folha numerada com as miniaturas (1 leitura de imagem para escolher
entre 12-20 opções, em vez de abrir uma por uma). Depois baixa só os escolhidos e grava os créditos.

    python buscar_stock.py buscar "<termo em inglês>" [--fontes archive,commons,pexels,pixabay] [--tipo video|foto]
                           [--vertical] [--organico] [--n 16] [--saida edit/fontes/busca]
    python buscar_stock.py baixar <saida>/candidatos.json 3,7,12 [--destino edit/fontes]

Fontes:
  archive   Internet Archive (filmes de arquivo, cinejornais, Prelinger = domínio público). Sem chave.
  commons   Wikimedia Commons (fotos históricas, documentos, vídeos). Sem chave; licença por arquivo (CC-BY pede crédito).
  pexels    Pexels (precisa PEXELS_API_KEY, grátis em pexels.com/api). Uso comercial, sem crédito obrigatório.
  pixabay   Pixabay (precisa PIXABAY_API_KEY, grátis em pixabay.com/api/docs). Uso comercial, sem crédito obrigatório.
--organico tira resultados com cara de banco ("business", "corporate", "smiling", "teamwork"...). Dicas de termo: references/fontes-reais.md
"""
from __future__ import annotations

import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import argparse
import json
import os
import re
import sys
import urllib.parse
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

UA = {"User-Agent": "edicao-motion-triwer/0.4 (busca de material livre para edição)"}
CARA_DE_BANCO = re.compile(r"business|corporate|smil|teamwork|handshake|office meeting|success|happy team|cheerful|thumbs up", re.I)


def chave(nome: str) -> str | None:
    if os.environ.get(nome):
        return os.environ[nome]
    for env in (Path.cwd() / ".env", Path.cwd().parent / ".env", Path.home() / ".env"):
        if env.exists():
            m = re.search(rf"^{nome}=(.+)$", env.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m:
                return m.group(1).strip().strip('"')
    return None


def archive(q: str, tipo: str, n: int, **_) -> list[dict]:
    mt = "movies" if tipo == "video" else "image"
    r = requests.get("https://archive.org/advancedsearch.php", headers=UA, timeout=30, params={
        "q": f"({q}) AND mediatype:({mt})", "fl[]": ["identifier", "title", "licenseurl", "year", "creator"],
        "rows": n, "output": "json", "sort[]": "downloads desc"})
    out = []
    for d in r.json().get("response", {}).get("docs", []):
        i = d["identifier"]
        out.append({"fonte": "archive", "id": i, "titulo": str(d.get("title", ""))[:80], "autor": str(d.get("creator", ""))[:40],
                    "licenca": d.get("licenseurl") or "ver página (muitos são domínio público)", "ano": d.get("year"),
                    "thumb": f"https://archive.org/services/img/{i}", "pagina": f"https://archive.org/details/{i}", "arquivo": None})
    return out


def commons(q: str, tipo: str, n: int, **_) -> list[dict]:
    ft = "filetype:video" if tipo == "video" else "filetype:bitmap"
    r = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=30, params={
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} {ft}", "gsrnamespace": 6, "gsrlimit": n,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 320})
    out = []
    for p in (r.json().get("query", {}).get("pages", {}) or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        autor = re.sub("<[^>]+>", "", md.get("Artist", {}).get("value", ""))[:40]
        out.append({"fonte": "commons", "id": p["title"], "titulo": p["title"].replace("File:", "")[:80], "autor": autor,
                    "licenca": md.get("LicenseShortName", {}).get("value", "?"), "thumb": ii.get("thumburl"),
                    "pagina": ii.get("descriptionurl"), "arquivo": ii.get("url"), "w": ii.get("width"), "h": ii.get("height")})
    return out


def pexels(q: str, tipo: str, n: int, vertical: bool = False, **_) -> list[dict]:
    k = chave("PEXELS_API_KEY")
    if not k:
        print("pexels: sem PEXELS_API_KEY (grátis em pexels.com/api), pulando")
        return []
    url = "https://api.pexels.com/videos/search" if tipo == "video" else "https://api.pexels.com/v1/search"
    p = {"query": q, "per_page": n, **({"orientation": "portrait"} if vertical else {})}
    r = requests.get(url, headers={"Authorization": k, **UA}, params=p, timeout=30).json()
    out = []
    for it in r.get("videos" if tipo == "video" else "photos", []):
        if tipo == "video":
            fs = sorted([f for f in it["video_files"] if f.get("file_type") == "video/mp4" and (f.get("height") or 0) <= 1920],
                        key=lambda f: -(f.get("height") or 0))
            arq, thumb, dur = (fs[0]["link"] if fs else None), it.get("image"), it.get("duration")
        else:
            arq, thumb, dur = it["src"]["original"], it["src"]["medium"], None
        out.append({"fonte": "pexels", "id": str(it["id"]), "titulo": it.get("url", "").rstrip("/").split("/")[-1][:80],
                    "autor": (it.get("user") or {}).get("name") or it.get("photographer", ""), "licenca": "Pexels (livre, sem crédito obrigatório)",
                    "thumb": thumb, "pagina": it.get("url"), "arquivo": arq, "dur": dur, "w": it.get("width"), "h": it.get("height")})
    return out


def pixabay(q: str, tipo: str, n: int, vertical: bool = False, **_) -> list[dict]:
    k = chave("PIXABAY_API_KEY")
    if not k:
        print("pixabay: sem PIXABAY_API_KEY (grátis em pixabay.com/api/docs), pulando")
        return []
    url = "https://pixabay.com/api/videos/" if tipo == "video" else "https://pixabay.com/api/"
    p = {"key": k, "q": q, "per_page": max(3, n), "safesearch": "true", **({"orientation": "vertical"} if vertical and tipo == "foto" else {})}
    r = requests.get(url, params=p, headers=UA, timeout=30).json()
    out = []
    for it in r.get("hits", []):
        if tipo == "video":
            v = it["videos"].get("large") or it["videos"].get("medium") or {}
            arq, thumb, w, h = v.get("url"), v.get("thumbnail"), v.get("width"), v.get("height")
        else:
            arq, thumb, w, h = it.get("largeImageURL"), it.get("webformatURL"), it.get("imageWidth"), it.get("imageHeight")
        out.append({"fonte": "pixabay", "id": str(it["id"]), "titulo": it.get("tags", "")[:80], "autor": it.get("user", ""),
                    "licenca": "Pixabay (livre, sem crédito obrigatório)", "thumb": thumb, "pagina": it.get("pageURL"), "arquivo": arq,
                    "dur": it.get("duration"), "w": w, "h": h})
    return out


FONTES = {"archive": archive, "commons": commons, "pexels": pexels, "pixabay": pixabay}


def fonte_txt(px: int):
    for p in ("C:/Windows/Fonts/arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(p).exists():
            return ImageFont.truetype(p, px)
    return ImageFont.load_default()


def folha(cands: list[dict], out: Path) -> None:
    W, H, BAR, COLS = 300, 230, 44, 5
    rows = (len(cands) + COLS - 1) // COLS
    sh = Image.new("RGB", (COLS * W, rows * (H + BAR)), (24, 24, 28))
    d = ImageDraw.Draw(sh)
    f1, f2 = fonte_txt(22), fonte_txt(13)
    for k, c in enumerate(cands):
        x, y = (k % COLS) * W, (k // COLS) * (H + BAR)
        try:
            im = Image.open(BytesIO(requests.get(c["thumb"], headers=UA, timeout=20).content)).convert("RGB")
            im.thumbnail((W - 6, H - 6))
            sh.paste(im, (x + (W - im.width) // 2, y + (H - im.height) // 2))
        except Exception:  # noqa: BLE001
            d.text((x + 10, y + 100), "sem miniatura", font=f2, fill=(150, 150, 150))
        d.rectangle([x, y, x + 44, y + 30], fill=(255, 220, 0))
        d.text((x + 6, y + 3), f"#{k + 1}", font=f1, fill=(0, 0, 0))
        info = f"{c['fonte']} · {str(c.get('licenca'))[:22]}" + (f" · {c['dur']}s" if c.get("dur") else "")
        d.text((x + 6, y + H + 4), info, font=f2, fill=(255, 235, 120))
        d.text((x + 6, y + H + 22), str(c.get("titulo"))[:40], font=f2, fill=(210, 210, 210))
    sh.save(out)


def buscar(a) -> None:
    out = Path(a.saida or f"fontes/busca_{re.sub(r'[^a-z0-9]+', '_', a.termo.lower())[:40]}").resolve()
    out.mkdir(parents=True, exist_ok=True)
    cands = []
    for nome in a.fontes.split(","):
        try:
            cands += FONTES[nome.strip()](a.termo, a.tipo, a.n, vertical=a.vertical)
        except Exception as ex:  # noqa: BLE001
            print(f"{nome}: falhou ({str(ex)[:120]})")
    if a.organico:
        cands = [c for c in cands if not CARA_DE_BANCO.search(f"{c.get('titulo')} {c.get('pagina')}")]
    cands = [c for c in cands if c.get("thumb")][: a.n * 2]
    (out / "candidatos.json").write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    folha(cands, out / "folha.png")
    for k, c in enumerate(cands, 1):
        print(f"#{k:<3} {c['fonte']:8} {str(c.get('licenca'))[:28]:28} {c.get('titulo', '')[:60]}")
    print(f"\nfolha: {out / 'folha.png'}  ({len(cands)} candidatos)\nbaixar: python buscar_stock.py baixar \"{out / 'candidatos.json'}\" 1,4")


def arquivo_archive(ident: str) -> str | None:
    m = requests.get(f"https://archive.org/metadata/{ident}", headers=UA, timeout=30).json()
    fs = [f for f in m.get("files", []) if f.get("name", "").lower().endswith((".mp4", ".jpg", ".png"))]
    fs.sort(key=lambda f: (not f["name"].lower().endswith(".mp4"), -int(f.get("size", 0) or 0)))
    mp4 = [f for f in fs if f["name"].lower().endswith(".mp4") and int(f.get("size", 0) or 0) < 600e6]
    f = (mp4 or fs or [None])[0]
    return f"https://archive.org/download/{ident}/{urllib.parse.quote(f['name'])}" if f else None


def baixar(a) -> None:
    cands = json.loads(Path(a.json).read_text(encoding="utf-8"))
    dest = Path(a.destino).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    cred_p = dest / "creditos.json"
    cred = json.loads(cred_p.read_text(encoding="utf-8")) if cred_p.exists() else []
    for n in [int(x) for x in a.numeros.split(",") if x.strip()]:
        c = cands[n - 1]
        url = c.get("arquivo") or (arquivo_archive(c["id"]) if c["fonte"] == "archive" else None)
        if not url:
            print(f"#{n}: sem arquivo direto; abrir {c.get('pagina')}")
            continue
        ext = Path(urllib.parse.urlparse(url).path).suffix or ".mp4"
        alvo = dest / f"{c['fonte']}_{re.sub(r'[^A-Za-z0-9]+', '_', c['id'])[:40]}{ext}"
        with requests.get(url, headers=UA, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(alvo, "wb") as fh:
                for ch in r.iter_content(1 << 20):
                    fh.write(ch)
        cred.append({"arquivo": alvo.name, "fonte": c["fonte"], "titulo": c.get("titulo"), "autor": c.get("autor"),
                     "licenca": c.get("licenca"), "pagina": c.get("pagina")})
        print(f"#{n}: {alvo} ({alvo.stat().st_size / 1e6:.1f} MB)")
    cred_p.write_text(json.dumps(cred, ensure_ascii=False, indent=1), encoding="utf-8")
    print("créditos:", cred_p)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("buscar")
    b.add_argument("termo")
    b.add_argument("--fontes", default="archive,commons,pexels,pixabay")
    b.add_argument("--tipo", default="video", choices=["video", "foto"])
    b.add_argument("--vertical", action="store_true")
    b.add_argument("--organico", action="store_true")
    b.add_argument("--n", type=int, default=8, help="por fonte")
    b.add_argument("--saida")
    d = sub.add_parser("baixar")
    d.add_argument("json")
    d.add_argument("numeros")
    d.add_argument("--destino", default="fontes")
    a = ap.parse_args()
    buscar(a) if a.cmd == "buscar" else baixar(a)


if __name__ == "__main__":
    sys.exit(main())
