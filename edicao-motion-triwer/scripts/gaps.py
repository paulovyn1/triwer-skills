"""Envelope RMS (10 ms) e lista de trechos de baixa energia >= min_dur, com limiar adaptativo."""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import sys
import numpy as np
import librosa

path = sys.argv[1]
min_dur = float(sys.argv[2]) if len(sys.argv) > 2 else 0.12
y, sr = librosa.load(path, sr=16000, mono=True)
hop = 160
rms = librosa.feature.rms(y=y, frame_length=400, hop_length=hop)[0]
db = 20 * np.log10(rms + 1e-9)
floor = np.percentile(db, 8)
speech = np.percentile(db, 70)
thr = floor + 0.35 * (speech - floor)
print(f"floor {floor:.1f} dB  speech {speech:.1f} dB  thr {thr:.1f} dB")
low = db < thr
t = np.arange(len(db)) * hop / sr
i = 0
while i < len(low):
    if low[i]:
        j = i
        while j < len(low) and low[j]:
            j += 1
        d = (j - i) * hop / sr
        if d >= min_dur:
            print(f"  {t[i]:6.2f} - {t[min(j, len(t) - 1)]:6.2f}  ({d:.2f}s)  min {db[i:j].min():.1f}")
        i = j
    else:
        i += 1
