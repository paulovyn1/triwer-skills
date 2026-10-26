"""Etapa 4: limpeza e equalização da voz (work/voz_cortada.wav -> work/voz_limpa.wav) e relatório antes/depois.

Cadeia padrão (testada em voz de celular ao ar livre): passa-alta 85 Hz, redução de ruído FFT leve, -6 dB em 60 Hz (zumbido),
-3 dB em 320 Hz (caixa/boxy), +4,5 dB em 3,2 kHz (presença), shelf +4 dB em 7,5 kHz (ar), de-esser, compressor 3:1, limitador.
Ruído pesado (ventilador, rua): subir nr (afftdn) até 20 ou trocar por  arnndn=m=<modelo rnnn>.  Ver references/audio.md.
Uso: python limpar_voz.py [--nr 12] [--filtro "<cadeia ffmpeg completa>"]
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import argparse
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import welch

from _cfg import WORK, sync_public

ap = argparse.ArgumentParser()
ap.add_argument("--nr", type=float, default=12)
ap.add_argument("--filtro", default=None)
a = ap.parse_args()
chain = a.filtro or (
    f"highpass=f=85:poles=2,afftdn=nr={a.nr}:nf=-62:tn=1,equalizer=f=60:t=q:w=1:g=-6,equalizer=f=320:t=q:w=1.1:g=-3,"
    "equalizer=f=3200:t=q:w=1.3:g=4.5,highshelf=f=7500:g=4,deesser=i=0.35:m=0.5:f=0.5,"
    "acompressor=threshold=-22dB:ratio=3:attack=6:release=90:knee=4:makeup=3,alimiter=limit=0.89:level=false")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(WORK / "voz_cortada.wav"), "-af", chain,
                "-ar", "48000", "-c:a", "pcm_s24le", str(WORK / "voz_limpa.wav")], check=True)


def bands(fn):
    y, sr = sf.read(str(WORK / fn))
    f = int(0.02 * sr)
    n = len(y) // f
    fr = y[: n * f].reshape(n, f)
    db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-12)
    out = []
    for name, m in (("pausa", (db > -75) & (db < -40)), ("fala", db > -18)):
        if m.sum() < 5:
            continue
        fq, p = welch(fr[m].ravel(), sr, nperseg=4096)
        pdb = 10 * np.log10(p + 1e-20)
        out.append(name + " " + " ".join(f"{lo}-{hi}:{pdb[(fq >= lo) & (fq < hi)].mean():.0f}"
                                          for lo, hi in ((20, 80), (80, 200), (200, 500), (1000, 2000), (2000, 4000), (4000, 8000))))
    return " | ".join(out)


print("antes :", bands("voz_cortada.wav"))
print("depois:", bands("voz_limpa.wav"))
m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(WORK / "voz_limpa.wav"), "-af", "ebur128=peak=true", "-f", "null", "-"],
                   capture_output=True, text=True, encoding="utf-8", errors="ignore").stderr
print([ln.strip() for ln in m.splitlines() if ln.strip().startswith(("I:", "Peak:"))][-2:])
sync_public("voz_limpa.wav")
