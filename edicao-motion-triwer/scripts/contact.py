"""Folha de contato numerada: vários quadros numa imagem só (1 leitura de imagem em vez de 20).

Uso:  python contact.py <saida.png> <colunas> <largura_miniatura> <img1> <img2> ...
Cada miniatura recebe o rótulo do nome do arquivo (ex.: m0452) no canto, pra saber qual frame é qual.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import sys
from pathlib import Path

from PIL import Image, ImageDraw

out, cols, w = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
files = [Path(p) for p in sys.argv[4:]]
ims = []
for p in files:
    im = Image.open(p).convert("RGB")
    h = round(im.height * w / im.width)
    im = im.resize((w, h))
    ImageDraw.Draw(im).text((6, 6), p.stem, fill=(255, 235, 0))
    ims.append(im)
rows = (len(ims) + cols - 1) // cols
H = max(i.height for i in ims)
sheet = Image.new("RGB", (cols * w, rows * H), (12, 12, 16))
for k, im in enumerate(ims):
    sheet.paste(im, ((k % cols) * w, (k // cols) * H))
sheet.save(out)
print(out, sheet.size)
