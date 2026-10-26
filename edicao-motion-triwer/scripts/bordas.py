"""Bordas de corte: para cada tempo do ORIGINAL, mostra onde a fala termina/começa (energia a cada 30 ms) e sugere o valor
com a folga certa (50-60 ms) para `corte.remover`. Substitui o "olhar a forma de onda" e os scripts soltos de energia.

Uso (de dentro de edit/):  python bordas.py 52.4 54.95 57.6 80.9
Para cada tempo: varre ±0,45 s, acha a transição fala->silêncio (fim de palavra) mais próxima antes e a silêncio->fala (começo) depois.
Respiração (−28 a −40 dB) conta como silêncio; o limiar é o mesmo do make_edl (P70 da fala − 16 dB).
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import sys

import numpy as np
import soundfile as sf

from _cfg import WORK, cfg

y, sr = sf.read(str(WORK / "orig.wav"), always_2d=True)
y = y.mean(axis=1)
H = int(0.03 * sr)
n = len(y) // H
db = 20 * np.log10(np.sqrt((y[: n * H].reshape(n, H) ** 2).mean(axis=1)) + 1e-9)
fala = db[db > np.percentile(db, 40)]
thr = float(np.percentile(fala, 70)) - cfg()["corte"].get("limiar_db_abaixo_da_fala", 16)
voz = db > thr


def t2i(t):
    return int(round(t / 0.03))


for arg in sys.argv[1:]:
    t = float(arg.replace(",", "."))
    i0, i1 = max(1, t2i(t - 0.45)), min(n - 1, t2i(t + 0.45))
    fins = [i for i in range(i0, i1) if voz[i - 1] and not voz[i]]  # fala acabou no começo do bloco i
    comecos = [i for i in range(i0, i1) if not voz[i - 1] and voz[i]]  # fala começa no bloco i
    perfil = " ".join(f"{k * 0.03:.2f}:{db[k]:.0f}" for k in range(t2i(t - 0.24), t2i(t + 0.25)))
    f = max([i for i in fins if i <= t2i(t) + 2], default=None)
    c = min([i for i in comecos if i >= t2i(t) - 2], default=None)
    sug = []
    if f is not None:
        sug.append(f"fala termina ≈ {f * 0.03:.2f} → início de remoção {f * 0.03 + 0.05:.2f}")
    if c is not None:
        sug.append(f"fala volta ≈ {c * 0.03:.2f} → fim de remoção {c * 0.03 - 0.06:.2f}")
    print(f"{t:.2f}s (limiar {thr:.0f} dB): " + ("; ".join(sug) or "sem transição em ±0,45 s"))
    print("   ", perfil)
