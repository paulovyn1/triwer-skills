"""Mede a mixagem: efeito vs voz (janela 200 ms em volta de cada evento) e música vs voz.

Uso (de dentro de edit/, depois de mix.py <opção>):  python medir_mix.py A
Aprova se: nenhum efeito pontual > 0 dB sobre a voz (exceto clímax) e música ~ -17 dB abaixo da voz.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import json
import sys

import numpy as np
import soundfile as sf

from _cfg import EDIT, WORK, cfg

opt = sys.argv[1] if len(sys.argv) > 1 else "A"
FPS = cfg().get("fps", 30)
cache = EDIT / "audio" / "_cache"
v, sr = sf.read(str(WORK / "voz_limpa.wav"))
v = v if v.ndim == 1 else v.mean(1)
s = sf.read(str(cache / f"stem_sfx_{opt}.wav"))[0].mean(1)
m = sf.read(str(cache / f"stem_music_{opt}.wav"))[0].mean(1)
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
rows = []
for e in json.loads((EDIT / "audio" / "sfx.json").read_text(encoding="utf-8"))["events"]:
    t = e["at"] / FPS
    a, b = int(max(0, t - 0.05) * sr), int((t + 0.15) * sr)
    rows.append((db(s[a:b]) - db(v[max(0, a - int(0.3 * sr)): b + int(0.3 * sr)]), e["note"]))
rows.sort(reverse=True)
print("efeito vs voz (dB) — 8 mais altos:")
for r, n in rows[:8]:
    print(f"  {r:+.1f}  {n}")
print("música vs voz (média):", round(db(m) - db(v[: len(m)]), 1), "dB")
