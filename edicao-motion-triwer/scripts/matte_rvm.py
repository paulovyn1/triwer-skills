"""Recorte da pessoa (Robust Video Matting, ONNX/CPU) em PNG com alfa, SÓ nos quadros em que há texto atrás dela.

Uso (de dentro de edit/):  python matte_rvm.py                 # janelas dos cues behind/ghost (janelas_behind.py)
                           python matte_rvm.py 1099:1137 ...   # janelas manuais (frames de saída)
Saída: motion/public/fg/<quadro>.png (RGBA, nome = frame de saída com 5 dígitos). O Pessoa.tsx desenha cada quadro com <Img>,
sem decodificar vídeo: o recorte fica exato (o webm com alfa lido por OffthreadVideo repetia quadros e a pessoa "congelava").
Cada janela aquece o RVM com 12 quadros antes (estado recorrente), então 100-200 quadros custam ~20-40 s em vez de 4 min.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import sys
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort

from _cfg import EDIT

MODEL = Path.home() / "Developer" / "video-tools" / "models" / "rvm_mobilenetv3_fp32.onnx"
if not MODEL.exists():
    import urllib.request
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve("https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx", MODEL)

WARM = 12
wins = [tuple(map(int, a.split(":"))) for a in sys.argv[1:] if ":" in a]
if not wins:
    from janelas_behind import janelas
    wins = [tuple(w) for w in janelas()]
if not wins:
    print("nenhum cue behind/ghost no roteiro: recorte não necessário")
    sys.exit(0)

out = EDIT / "motion" / "public" / "fg"
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("*.png"):
    old.unlink()

so = ort.SessionOptions()
so.intra_op_num_threads = 8
sess = ort.InferenceSession(str(MODEL), so, providers=["CPUExecutionProvider"])
cap = cv2.VideoCapture(str(EDIT / "work" / "base.mp4"))
N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
ratio = np.array([0.3], np.float32)
total = 0
for a, b in wins:
    a, b = max(0, a), min(N - 1, b)
    start = max(0, a - WARM)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
    for n in range(start, b + 1):
        ok, fr = cap.read()
        if not ok:
            break
        x = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB).astype(np.float32).transpose(2, 0, 1)[None] / 255.0
        _, pha, *rec = sess.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": ratio})
        if n < a:
            continue
        alpha = cv2.GaussianBlur((pha[0, 0] * 255).clip(0, 255).astype(np.uint8), (0, 0), 0.8)
        rgba = np.dstack([fr, alpha])
        ok, buf = cv2.imencode(".png", rgba, [cv2.IMWRITE_PNG_COMPRESSION, 3])
        buf.tofile(str(out / f"{n:05d}.png"))
        total += 1
print(f"recorte ok: {total} quadros em {len(wins)} janela(s) -> {out}")
