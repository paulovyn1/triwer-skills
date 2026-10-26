"""Etapa 3: base cortada com timing exato de frame.

Vídeo: cada segmento com -frames:v exato (cortes já na grade de frames) -> concat -c copy (work/base.mp4).
Áudio: corte por amostra no WAV 48k, fades de 30 ms nas bordas (sem estalo) -> work/voz_cortada.wav.
Não usar o render.py do video-use pra isso: ele acumula frames a mais (+8 em 23 segmentos) e desalinha a legenda.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import json
import subprocess

import numpy as np
import soundfile as sf

from _cfg import EDIT, WORK, cfg, sync_public

FPS = cfg().get("fps", 30)
edl = json.loads((EDIT / "edl.json").read_text(encoding="utf-8"))
src = next(iter(edl["sources"].values()))
seg_dir = EDIT / "clips_graded"
seg_dir.mkdir(exist_ok=True)
for old in seg_dir.glob("*.mp4"):
    old.unlink()

paths = []
for i, r in enumerate(edl["ranges"]):
    n = round((r["end"] - r["start"]) * FPS)
    p = seg_dir / f"seg_{i:02d}.mp4"
    subprocess.run(["ffmpeg", "-y", "-ss", f"{r['start']:.4f}", "-i", src, "-frames:v", str(n), "-an", "-c:v", "libx264",
                    "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-r", str(FPS), "-video_track_timescale", "15360", str(p)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    paths.append(p)
lst = WORK / "_concat.txt"
lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in paths), encoding="utf-8")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(WORK / "base.mp4")],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
lst.unlink()

y, sr = sf.read(str(WORK / "orig.wav"), always_2d=True)
y = y.mean(axis=1)
fade = int(0.03 * sr)
ramp = np.linspace(0, 1, fade)
parts = []
for r in edl["ranges"]:
    n = round((r["end"] - r["start"]) * FPS)
    s0 = round(r["start"] * sr)
    seg = y[s0:s0 + round(n / FPS * sr)].copy()
    seg[:fade] *= ramp
    seg[-fade:] *= ramp[::-1]
    parts.append(seg)
sf.write(str(WORK / "voz_cortada.wav"), np.concatenate(parts), sr, subtype="PCM_24")
print("frames esperados:", sum(round((r["end"] - r["start"]) * FPS) for r in edl["ranges"]))
sync_public("base.mp4")
