"""Auditoria de movimento dos painéis no vídeo final: mede a diferença entre quadros consecutivos na metade de cima (painel)
e aponta (a) trechos PARADOS (painel "morto": diferença ~0 por >= 10 quadros), (b) saltos secos (um quadro com diferença
muito acima da mediana local = elemento que "pula" em vez de animar).
Uso (de dentro de edit/):  python auditar_movimento.py <video_final.mp4>      (lê PANELS de motion/src/timeline.ts)
Baseline: painéis do C2 (P10/P12) têm ~0 a 5% de quadros parados e saltos só nas entradas."""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import re
import subprocess
import sys

import numpy as np

from _cfg import EDIT

video = sys.argv[1]
OFF = int(next((a.split("=")[1] for a in sys.argv if a.startswith("--offset=")), 0))  # frame da composição em que o vídeo parcial começa
src = (EDIT / "motion" / "src" / "timeline.ts").read_text(encoding="utf-8")
panels = [(m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)) for m in
          re.finditer(r'\{\s*id:\s*"(\w+)",\s*from:\s*(\d+),\s*to:\s*(\d+),\s*kind:\s*"(\w+)"', src)]
W, H = 270, 480
for pid, a, b, kind in panels:
    if kind == "overlay":
        continue
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", video, "-vf",
                        f"select='between(n,{a - OFF},{b - OFF})',scale={W}:{H},format=gray", "-vsync", "0", "-f", "rawvideo", "-"],
                       capture_output=True)
    fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.int16)
    reg = slice(0, H // 2) if kind == "top" else slice(0, H)
    d = np.array([np.abs(fr[i][reg] - fr[i - 1][reg]).mean() for i in range(1, len(fr))])
    still = d < 0.12
    run = best = 0
    for s in still:
        run = run + 1 if s else 0
        best = max(best, run)
    med = np.median(d[d > 0.12]) if (d > 0.12).any() else 0
    spikes = [a + 1 + i for i in range(1, len(d) - 1) if d[i] > max(6 * med, 3.0) and d[i] > 2.5 * max(d[i - 1], d[i + 1])]
    print(f"{pid} {a}-{b} ({kind}): parados {100 * still.mean():.0f}% | maior trecho parado {best} quadros | mediana {med:.2f} | saltos secos {spikes[:12]}")
