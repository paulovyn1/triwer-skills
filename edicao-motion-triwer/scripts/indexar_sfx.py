"""Índice dos efeitos sonoros do Mixkit (todas as categorias, todas as páginas) -> biblioteca/sfx/indice_mixkit.json.

Uso (de qualquer pasta):  python indexar_sfx.py      (≈ 5-10 min, zero token; rodar de novo de tempos em tempos)
Depois: sfx.py buscar "<o que se vê na tela>" acha o som em todo o acervo; o áudio só é baixado quando usado (cache local).
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import json
import time

from _cfg import LIB
from mixkit import BASE, cartoes, get, links_categoria

SAIDA = LIB / "sfx" / "indice_mixkit.json"
RAIZ = "/free-sound-effects/"

idx = json.loads(SAIDA.read_text(encoding="utf-8")) if SAIDA.exists() else {}
n0 = len(idx)
raiz = get(BASE + RAIZ)
cats = sorted(l for l in links_categoria(raiz, RAIZ) if l.count("/") == 3)
print(f"{len(cats)} categorias", flush=True)
paginas = 0
for ci, cat in enumerate(cats, 1):
    vistos_cat = set()
    for pg in range(1, 30):
        u = BASE + cat + (f"?page={pg}" if pg > 1 else "")
        try:
            html = get(u)
        except Exception as e:
            print("falhou", u, e)
            break
        paginas += 1
        novos = 0
        for c in cartoes(html):
            if c["tipo"] != "sfx" or c["id"] in vistos_cat:
                continue
            vistos_cat.add(c["id"])
            novos += 1
            it = idx.setdefault(c["id"], {"titulo": c["titulo"], "tags": [], "dur": c["dur"]})
            for t in [cat.strip("/").split("/")[-1]] + [t[1] for t in c["tags"]]:
                if t not in it["tags"]:
                    it["tags"].append(t)
        time.sleep(0.3)
        if not novos:
            break
    if ci % 10 == 0:
        print(f"{ci}/{len(cats)} categorias, {len(idx)} efeitos", flush=True)
        SAIDA.write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
SAIDA.write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"índice de efeitos: {len(idx)} ({len(idx) - n0} novos) em {paginas} páginas -> {SAIDA}")
