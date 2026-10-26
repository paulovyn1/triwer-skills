"""Baixa trilhas do Mixkit pelos IDs do índice (biblioteca/musica/mixkit_index.txt). Licença Mixkit: uso comercial e
anúncio online liberados, sem crédito; proibido em CD/DVD/jogo/TV/rádio.

Uso (de dentro de edit/):  python baixar_musica.py 568 34 605 963        -> edit/music_cand/<id>.mp3
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import sys
import urllib.request

from _cfg import EDIT, cfg

c = cfg()
d = EDIT / c["musica"].get("candidatas", "music_cand")
d.mkdir(exist_ok=True)
for i in sys.argv[1:]:
    out = d / f"{i}.mp3"
    if out.exists():
        print("cache", out.name)
        continue
    req = urllib.request.Request(f"https://assets.mixkit.co/music/{i}/{i}.mp3", headers={"User-Agent": "Mozilla/5.0"})
    out.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    print("baixou", out.name, f"{out.stat().st_size / 1e6:.1f} MB")
