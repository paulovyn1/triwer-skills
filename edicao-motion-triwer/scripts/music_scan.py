"""Varre trilhas: BPM, tom (Camelot), modo, energia por janela e "pulso" (força de onset).
Depois cruza pares tensão→virada compatíveis em andamento (±7%, ou 2:1) e tom (Camelot igual/vizinho/relativo).
Saída: music_cand2/scan.json e ranking no stdout."""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import json
import sys
from pathlib import Path

import librosa
import numpy as np

D = Path(sys.argv[1])
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
NOTES = "C C# D D# E F F# G G# A A# B".split()
# Camelot: número por tônica
CAM_MAJ = {0: 8, 7: 9, 2: 10, 9: 11, 4: 12, 11: 1, 6: 2, 1: 3, 8: 4, 3: 5, 10: 6, 5: 7}
CAM_MIN = {9: 8, 4: 9, 11: 10, 6: 11, 1: 12, 8: 1, 3: 2, 10: 3, 5: 4, 0: 5, 7: 6, 2: 7}

res = {}
for p in sorted(D.glob("*.mp3"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0):
    y, sr = librosa.load(str(p), sr=22050, mono=True, duration=150)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = float(np.atleast_1d(librosa.feature.tempo(onset_envelope=onset_env, sr=sr, start_bpm=110))[0])
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr).mean(axis=1)
    best = max([(np.corrcoef(np.roll(MAJ, k), chroma)[0, 1], k, "B") for k in range(12)] +
               [(np.corrcoef(np.roll(MIN, k), chroma)[0, 1], k, "A") for k in range(12)])
    conf, k, m = best
    cam = (CAM_MAJ if m == "B" else CAM_MIN)[k]
    rms = librosa.feature.rms(y=y, hop_length=2048)[0]
    sec = 2048 / sr
    win = lambda a, b: float(20 * np.log10(rms[int(a / sec):int(b / sec)].mean() + 1e-9))
    pulse = float(onset_env.mean())
    res[p.stem] = {"bpm": round(tempo, 1), "key": f"{NOTES[k]} {'maior' if m == 'B' else 'menor'}", "cam": f"{cam}{m}",
                   "conf": round(float(conf), 2), "e0_8": round(win(0, 8), 1), "e8_30": round(win(8, 30), 1),
                   "e30_90": round(win(30, 90), 1), "pulse": round(pulse, 2), "dur": round(len(y) / sr)}
    print(p.stem, res[p.stem], flush=True)
(D / "scan.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
