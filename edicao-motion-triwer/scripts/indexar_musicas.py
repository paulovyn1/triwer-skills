"""Índice da biblioteca de música (Mixkit): títulos, tags de humor/gênero/instrumento e análise de áudio de cada faixa.

Uso (de qualquer pasta; não depende de edit/):
    python indexar_musicas.py                    # varre as páginas de categoria do Mixkit -> biblioteca/musica/indice.json (≈ 3 min)
    python indexar_musicas.py --analisar [--limite N] [--manter]
        baixa cada faixa ainda não analisada para o cache (ambiente.json → cache, pasta musica/), mede BPM, tom (Camelot), energia (curva a cada 5 s),
        pulso e brilho -> biblioteca/musica/analise.json (incremental; rode em segundo plano: ≈ 4 s por faixa). Sem --manter, apaga o
        mp3 depois de medir (o mix baixa de novo só as escolhidas).
Rodar de novo de tempos em tempos pega faixas novas do site. Zero token: é o que deixa o escolher_musica.py trabalhar sozinho.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import json
import sys
import time

from _cfg import CACHE_LIB, LIB
from mixkit import BASE, baixar, cartoes, get, links_categoria, url_musica

DIR = LIB / "musica"
INDICE = DIR / "indice.json"
ANALISE = DIR / "analise.json"
RAIZ = "/free-stock-music/"


def varrer() -> None:
    idx = json.loads(INDICE.read_text(encoding="utf-8")) if INDICE.exists() else {}
    fila, vistos, n0 = [RAIZ], set(), len(idx)
    while fila and len(vistos) < 450:
        u = fila.pop(0)
        if u in vistos:
            continue
        vistos.add(u)
        try:
            pag = get(BASE + u)
        except Exception as e:
            print("falhou", u, e)
            continue
        for c in cartoes(pag):
            if c["tipo"] != "music":
                continue
            atual = idx.setdefault(c["id"], {"titulo": c["titulo"], "dur": c["dur"], "tags": []})
            atual["titulo"] = c["titulo"] or atual["titulo"]
            atual["dur"] = c["dur"] or atual.get("dur")
            for t in c["tags"]:
                if list(t) not in atual["tags"]:
                    atual["tags"].append(list(t))
        for l in sorted(links_categoria(pag, RAIZ)):
            if l not in vistos and l not in fila and not any(x in l for x in ("/search", "/author", "/discover")):
                fila.append(l)
        time.sleep(0.35)
        if len(vistos) % 25 == 0:
            print(f"{len(vistos)} páginas, {len(idx)} faixas", flush=True)
    INDICE.write_text(json.dumps(idx, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"índice: {len(idx)} faixas ({len(idx) - n0} novas) em {len(vistos)} páginas -> {INDICE}")


MAJ = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MIN = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
NOTES = "C C# D D# E F F# G G# A A# B".split()
CAM_MAJ = {0: 8, 7: 9, 2: 10, 9: 11, 4: 12, 11: 1, 6: 2, 1: 3, 8: 4, 3: 5, 10: 6, 5: 7}
CAM_MIN = {9: 8, 4: 9, 11: 10, 6: 11, 1: 12, 8: 1, 3: 2, 10: 3, 5: 4, 0: 5, 7: 6, 2: 7}


def medir(path) -> dict:
    import librosa
    import numpy as np
    y, sr = librosa.load(str(path), sr=22050, mono=True)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = float(np.atleast_1d(librosa.feature.tempo(onset_envelope=onset, sr=sr, start_bpm=110))[0])
    chroma = librosa.feature.chroma_cqt(y=y[: sr * 120], sr=sr).mean(axis=1)
    conf, k, m = max([(np.corrcoef(np.roll(MAJ, k), chroma)[0, 1], k, "B") for k in range(12)] +
                     [(np.corrcoef(np.roll(MIN, k), chroma)[0, 1], k, "A") for k in range(12)])
    cam = (CAM_MAJ if m == "B" else CAM_MIN)[k]
    hop = 2048
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    sec = hop / sr
    win = lambda a, b: float(20 * np.log10(rms[int(a / sec):max(int(a / sec) + 1, int(b / sec))].mean() + 1e-9))
    dur = len(y) / sr
    curva = [round(win(a, a + 5), 1) for a in np.arange(0, max(5, dur - 5), 5)]
    cent = float(librosa.feature.spectral_centroid(y=y[: sr * 90], sr=sr).mean())
    return {"bpm": round(tempo, 1), "key": f"{NOTES[k]} {'maior' if m == 'B' else 'menor'}", "cam": f"{cam}{m}", "conf": round(float(conf), 2),
            "e0_8": round(win(0, 8), 1), "e8_30": round(win(8, 30), 1), "e30_90": round(win(30, 90), 1), "curva5s": curva,
            "pulso": round(float(onset.mean()), 2), "brilho": round(cent), "dur": round(dur, 1)}


def analisar(limite: int, manter: bool) -> None:
    idx = json.loads(INDICE.read_text(encoding="utf-8"))
    an = json.loads(ANALISE.read_text(encoding="utf-8")) if ANALISE.exists() else {}
    falta = [i for i in idx if i not in an and (idx[i].get("dur") or 999) >= 45][:limite]
    print(f"{len(falta)} faixas para analisar (já analisadas: {len(an)})", flush=True)
    cache = CACHE_LIB / "musica"
    for n, i in enumerate(falta, 1):
        p = cache / f"{i}.mp3"
        try:
            baixar(url_musica(i), p)
            an[i] = medir(p)
        except Exception as e:
            print("falhou", i, e, flush=True)
            continue
        finally:
            if not manter and p.exists():
                p.unlink()
        if n % 10 == 0 or n == len(falta):
            ANALISE.write_text(json.dumps(an, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            print(f"{n}/{len(falta)} analisadas", flush=True)
    ANALISE.write_text(json.dumps(an, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    if "--analisar" in sys.argv:
        lim = int(sys.argv[sys.argv.index("--limite") + 1]) if "--limite" in sys.argv else 10 ** 6
        analisar(lim, "--manter" in sys.argv)
    else:
        varrer()
