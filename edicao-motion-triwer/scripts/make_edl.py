"""Etapa 2: lista de cortes (edl.json) removendo pausas, respirações e trechos marcados, alinhada à grade de frames.

Lê projeto.json → corte:
  inicio/fim              janela útil do original (s)
  min_pausa               pausa mínima que vira corte (0,13)
  mantem_depois/antes     quanto da pausa fica depois da fala e antes da próxima (0,07 / 0,05)
  limiar_db_abaixo_da_fala  energia (dB abaixo do P70 da fala) que conta como "baixa": 16 pega silêncio + respiração
  pausas_dramaticas       {"tempo_no_original": pausa_total_mantida_s}  respiros que ficam maiores de propósito
  remover                 [[ini, fim], ...] janelas do ORIGINAL a tirar (gagueira, repetição, fala errada); alinhar em
                          limites de palavra com ~50 ms de folga (use achar_gagueira.py + transcrição)
Gera: edl.json, work/cuts_map.json e (se existir motion/) motion/public/cuts.json com o frame de cada corte e o total.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import json

import librosa
import numpy as np

from _cfg import EDIT, MOTION, WORK, cfg, fonte

c = cfg()
k = c["corte"]
FPS = c.get("fps", 30)
SRC = fonte(c)
MIN_GAP = k.get("min_pausa", 0.13)
KEEP_A, KEEP_B = k.get("mantem_depois", 0.07), k.get("mantem_antes", 0.05)
HEAD, TAIL = k["inicio"], k["fim"]
BEATS = {float(t): v for t, v in k.get("pausas_dramaticas", {}).items()}
REMOVER = [tuple(r) for r in k.get("remover", [])]
DROP = k.get("limiar_db_abaixo_da_fala", 16.0)

y, sr = librosa.load(str(WORK / "orig.wav"), sr=16000, mono=True)
hop = 160
db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=400, hop_length=hop)[0] + 1e-9)
speech = np.percentile(db, 70)
thr = speech - DROP
t = np.arange(len(db)) * hop / sr
low = db < thr

regions, i = [], 0
while i < len(low):
    if low[i]:
        j = i
        while j < len(low) and low[j]:
            j += 1
        regions.append([t[i], t[min(j, len(t) - 1)]])
        i = j
    else:
        i += 1
merged = []
for r in regions:
    if merged and r[0] - merged[-1][1] < 0.05:
        merged[-1][1] = r[1]
    else:
        merged.append(r)
gaps = [r for r in merged if r[1] - r[0] >= MIN_GAP and r[0] > HEAD + 0.2 and r[1] < TAIL - 0.1]


def snap(x):
    return round(x * FPS) / FPS


ranges, cur = [], HEAD
for a, b in gaps:
    keep_total = KEEP_A + KEEP_B
    for bt, kt in BEATS.items():
        if a - 0.3 <= bt <= b + 0.3:
            keep_total = kt
    if (b - a) - keep_total < 0.12:
        continue
    ka = keep_total * (KEEP_A / (KEEP_A + KEEP_B))
    end_keep, next_start = snap(a + ka), snap(b - (keep_total - ka))
    if next_start - end_keep < 2 / FPS:
        continue
    ranges.append([snap(cur), end_keep])
    cur = next_start
ranges.append([snap(cur), snap(TAIL)])

for ra, rb in REMOVER:  # tira janelas marcadas
    new = []
    for s, e in ranges:
        if rb <= s or ra >= e:
            new.append([s, e])
            continue
        if ra - s >= 2 / FPS:
            new.append([s, snap(ra)])
        if e - rb >= 2 / FPS:
            new.append([snap(rb), e])
    ranges = new

edl = {"version": 1, "sources": {"V": str(SRC)}, "ranges": [{"source": "V", "start": round(a, 4), "end": round(b, 4)} for a, b in ranges],
       "grade": "none"}
out_t, cmap = 0.0, []
for a, b in ranges:
    cmap.append({"src_start": a, "src_end": b, "out_start": round(out_t, 4)})
    out_t += b - a
edl["total_duration_s"] = round(out_t, 3)
(EDIT / "edl.json").write_text(json.dumps(edl, indent=2, ensure_ascii=False), encoding="utf-8")
(WORK / "cuts_map.json").write_text(json.dumps(cmap, indent=2), encoding="utf-8")
if MOTION.exists():
    pub = MOTION / "public"
    pub.mkdir(exist_ok=True)
    (pub / "cuts.json").write_text(json.dumps({"total": round(out_t * FPS), "cuts": [round(m["out_start"] * FPS) for m in cmap]}), encoding="utf-8")
print(f"{len(ranges)} segmentos, {out_t:.2f}s ({round(out_t * FPS)} frames) a partir de {TAIL - HEAD:.2f}s úteis; limiar {thr:.1f} dB")
for (a, b), m in zip(ranges, cmap):
    print(f"  {a:6.2f}-{b:6.2f} ({b - a:5.2f}s) -> saída {m['out_start']:6.2f}s (frame {round(m['out_start'] * FPS)})")
