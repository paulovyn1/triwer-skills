"""Procura trechos CONGELADOS no vídeo final (rosto/tronco da pessoa) comparando com o base. Pegou o bug do recorte em webm.
Uso (de dentro de edit/):  python congelado.py <video_final.mp4> [ini:fim ...]      (sem janelas = vídeo inteiro)
Imprime, por janela, a diferença média entre quadros consecutivos da região central (final x base) e marca sequências de >= 2
quadros com diferença ~0 no final enquanto o base se mexe (indício de recorte/frame parado)."""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import re
import subprocess
import sys

import numpy as np

from _cfg import EDIT
from janelas_behind import cues

final = sys.argv[1]
wins = [tuple(map(int, a.split(":"))) for a in sys.argv[2:] if ":" in a] or [(0, 10 ** 6)]
W, H = 270, 480


def frames(path, a, b):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", path, "-vf",
                        f"select='between(n,{a},{b})',scale={W}:{H},format=gray", "-vsync", "0", "-f", "rawvideo", "-"],
                       capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.int16)


# cenas em que a região baixa é estática por projeto: cover (tela cheia) e knock (tela preta)
IGNORAR = []
try:
    tl = (EDIT / "motion" / "src" / "timeline.ts").read_text(encoding="utf-8")
    IGNORAR += [(int(m[1]), int(m[2])) for m in re.findall(r'id:\s*"(\w+)",\s*from:\s*(\d+),\s*to:\s*(\d+),\s*kind:\s*"cover"', tl)]
    IGNORAR += [(c["start"] - 2, c["end"] + 4) for c in cues() if c["mode"] == "knock"]
except Exception:
    pass
REGIONS = {"centro": (slice(int(H * 0.32), int(H * 0.78)), slice(int(W * 0.25), int(W * 0.75))),
           "baixo": (slice(int(H * 0.62), int(H * 0.95)), slice(int(W * 0.15), int(W * 0.85)))}
for a, b in wins:
    fv = frames(final, a, b)
    bv = frames(str(EDIT / "work" / "base.mp4"), a, b)
    b = min(b, a + len(fv) - 1)
    print(f"janela {a}:{b} | final {len(fv)} quadros, base {len(bv)}")
    for name, sl in REGIONS.items():
        df = [float(np.abs(fv[i][sl] - fv[i - 1][sl]).mean()) for i in range(1, len(fv))]
        db = [float(np.abs(bv[i][sl] - bv[i - 1][sl]).mean()) for i in range(1, len(bv))]
        stuck = [a + 1 + i for i in range(len(df)) if df[i] < 0.25 and db[i] > 0.9 and not any(x <= a + 1 + i <= y for x, y in IGNORAR)]
        runs, cur = [], []
        for s in stuck:
            if cur and s == cur[-1] + 1:
                cur.append(s)
            else:
                if len(cur) >= 2:
                    runs.append((cur[0], cur[-1]))
                cur = [s]
        if len(cur) >= 2:
            runs.append((cur[0], cur[-1]))
        print(f"  [{name}] quadros parados: {len(stuck)} | sequências >= 2: {runs}" + ("  <- SUSPEITO: pessoa parada enquanto o base se mexe" if runs else "  ok"))
