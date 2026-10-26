"""Mixagem final: voz + trilha (1 a N faixas, trocando conforme a emoção da fala) + efeitos sonoros + master.

Trilha (projeto.json -> musica.versoes[X].faixas, gerado por escolher_musica.py; o formato antigo musica.pares + marcos ainda funciona):
  cada faixa tem `de` (segundo de saída em que começa a entrar) e `entrada`:
  - dj      transição de DJ: a anterior é abafada (passa-baixa) e baixa; a nova entra sem grave (passa-alta) por baixo e, no primeiro tempo
            forte da anterior ~1,3-3,6 s depois, acontece a troca de grave; a nova é esticada (rubberband, sem mudar o tom) para o andamento
            da anterior quando a diferença é <= 8%; riser discreto cola a troca;
  - respiro a anterior abafa e some em 1,2 s; a nova entra num tempo forte dela em `de` (mudança de clima sem casar andamento);
  - corte   troca seca no `de` com impacto grave (virada brusca de emoção: usar pouco).
  Cada faixa começa num tempo forte e no trecho da música com a energia da intensidade pedida (1 calma, 2 média, 3 forte).
Ducking por sidechain (voz + efeitos, máx. 6 dB), efeitos com envelope e pico no frame, barramento de efeitos com corte em 2,8 kHz,
master em -14 LUFS / -1 dBTP (loudnorm 2 passadas).

Efeitos (audio/sfx.json): `file` = nome do catálogo (biblioteca/sfx/<nome>.mp3|wav) ou "mixkit:<id>" (qualquer efeito do Mixkit, baixado
para o cache na hora; buscar com sfx.py buscar "..."). `rajada_ok: true` tira o evento do aviso de rajada (ex.: camadas do knock).

Uso: python mix.py A|B|C   →  motion/public/mix_<opt>.wav  e  edit/audio/mix_<opt>.mp3
"""
from __future__ import annotations

import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import json
import re
import subprocess
import sys
from pathlib import Path

import librosa
import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
from _cfg import CACHE_LIB, EDIT, LIB, MOTION, cfg  # noqa: E402
from mixkit import baixar, url_musica, url_sfx  # noqa: E402

C = cfg()
MC = C["musica"]
FPS_ = C.get("fps", 30)
TOTAL = json.loads((EDIT / "edl.json").read_text(encoding="utf-8"))["total_duration_s"]
N = int(round(TOTAL * SR))
SFX_DIR = LIB / "sfx"
CAND = EDIT / MC.get("candidatas", "music_cand")
CACHE = EDIT / "audio" / "_cache"
CACHE.mkdir(parents=True, exist_ok=True)
(MOTION / "public").mkdir(parents=True, exist_ok=True)
MUSIC_LUFS = MC.get("lufs_musica", -23.0)  # pré-ducking; música bem baixinha, ambiência
T_END_FADE = MC.get("marcos", {}).get("fim_fade", TOTAL - 0.6)


def db2lin(d):
    return 10 ** (np.asarray(d) / 20)


def env_at(keys, t):
    ks = sorted(keys, key=lambda k: k[0])
    xs, ys, last = [], [], None
    for x, y in ks:  # eixo estritamente crescente (antes, tempos fixos do C2 deixavam a curva fora de ordem em outros vídeos)
        if last is not None and x <= last:
            x = last + 1e-4
        xs.append(x)
        ys.append(y)
        last = x
    return np.interp(t, xs, ys)


def load(path: Path, sr=SR) -> np.ndarray:
    y, _ = librosa.load(str(path), sr=sr, mono=False)
    if y.ndim == 1:
        y = np.stack([y, y])
    return y.astype(np.float32)


def lufs(y: np.ndarray) -> float:
    v = pyln.Meter(SR).integrated_loudness(y.T.astype(np.float64))
    return v if np.isfinite(v) else -70.0


def grid(path: Path):
    """BPM, batidas e tempos fortes (fase do compasso pelo onset de grave)."""
    y, sr = librosa.load(str(path), sr=22050, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time", start_bpm=110, tightness=300)
    low = librosa.onset.onset_strength(y=y, sr=sr, fmax=180, n_mels=32)
    tl = librosa.times_like(low, sr=sr)
    s = np.interp(beats, tl, low)
    phase = max(range(4), key=lambda p: s[p::4].mean() if s[p::4].size else -1)
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    tr = librosa.times_like(rms, sr=sr, hop_length=512)
    edb = 20 * np.log10(rms + 1e-9)
    energy = lambda a, b: float(edb[(tr >= a) & (tr < b)].mean()) if b > a and ((tr >= a) & (tr < b)).any() else -99.0
    return float(np.atleast_1d(tempo)[0]), beats, beats[phase::4], energy, len(y) / sr, edb


def stretched(src: Path, ratio: float) -> Path:
    if abs(ratio - 1) < 0.004:
        return src
    out = CACHE / f"{src.stem}_x{ratio:.4f}.wav"
    if not out.exists():
        subprocess.run(["ffmpeg", "-y", "-i", str(src), "-af", f"rubberband=tempo={ratio:.5f}:pitchq=quality",
                        "-ar", str(SR), str(out)], check=True, capture_output=True)
    return out


def tv_filter(y: np.ndarray, cut: np.ndarray, kind: str, block=256) -> np.ndarray:
    """filtro Butterworth 2ª ordem com corte variando no tempo (por bloco, estado contínuo)."""
    out = np.empty_like(y)
    zi = np.zeros((1, 2, y.shape[0]))
    for a in range(0, y.shape[1], block):
        b = min(a + block, y.shape[1])
        fc = float(np.clip(cut[(a + b) // 2], 20, SR / 2 * 0.95))
        sos = butter(2, fc, btype=kind, fs=SR, output="sos")
        seg, zi = sosfilt(sos, y[:, a:b].T, axis=0, zi=zi)
        out[:, a:b] = seg.T
    return out


def peaking(f0, gain_db, q=1.0):
    A = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / SR
    al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]
    a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return np.array([[b[0] / a[0], b[1] / a[0], b[2] / a[0], 1, a[1] / a[0], a[2] / a[0]]])


def arquivo_musica(i: str) -> Path:
    p = CAND / f"{i}.mp3"
    if not p.exists():
        cache = baixar(url_musica(i), CACHE_LIB / "musica" / f"{i}.mp3")
        CAND.mkdir(exist_ok=True)
        p.write_bytes(cache.read_bytes())
    return p


def versao(opt: str):
    """lista de faixas [{id, de, entrada, int, off, extra_db, dim, muff}] + nome; aceita o formato novo e o antigo (pares + marcos)"""
    if opt in MC.get("versoes", {}):
        v = MC["versoes"][opt]
        fx = [{"id": str(f["id"]), "de": float(f["de"]), "entrada": f.get("entrada", "dj") if k else "inicio", "int": int(f.get("intensidade", 2)),
               "off": f.get("offset_sugerido"), "extra_db": float(f.get("ganho_db", 0)), "titulo": f.get("titulo", "")}
              for k, f in enumerate(v["faixas"])]
        return fx, v.get("nome") or " → ".join(f["titulo"] or f["id"] for f in fx)
    p = MC["pares"][opt]
    M = MC.get("marcos", {})
    dim = M.get("dim", TOTAL * 0.585)
    muff = M.get("muff", dim + 0.55)
    entra = M.get("entra", muff + 0.2)
    fx = [{"id": str(p["tensao"]), "de": 0.0, "entrada": "inicio", "int": 2, "off": None, "extra_db": 0.0},
          {"id": str(p["virada"]), "de": entra, "entrada": "dj", "int": 2, "off": None, "extra_db": 1.0, "dim": dim, "muff": muff}]
    return fx, p.get("nome", opt)


def escolhe_inicio(g: dict, need: float, intensidade: int, sugestao, lead: float = 0.0) -> float:
    """tempo forte de início: energia da intensidade pedida no trecho e sem buraco no começo; lead = s antes do tempo forte"""
    _, _, downs, energy, length, edb = g["bpm"], None, g["downs"], g["energy"], g["len"], g["edb"]
    alvo = np.percentile(edb[edb > -60], {1: 30, 2: 60, 3: 90}.get(intensidade, 60)) if (edb > -60).any() else -20
    best, bscore = None, -1e9
    for d in downs:
        if d - lead < 0.5 or d + need > length - 0.5:
            continue
        e = energy(d, d + min(need, 16))
        sc = -abs(e - alvo) + 0.6 * min(0.0, energy(d, d + 3) - e + 2) + 0.4 * (energy(d, d + 4) - energy(d - 2, d))
        if sugestao is not None and abs(d - float(sugestao)) < 8:
            sc += 0.8
        if sc > bscore:
            best, bscore = d, sc
    if best is None:
        best = float(downs[0]) if len(downs) else lead + 0.5
    return float(best)


def music_bed(opt: str, report: dict):
    faixas, nome = versao(opt)
    n = len(faixas)
    info, prev_bpm = [], None
    for k, f in enumerate(faixas):
        p = arquivo_musica(f["id"])
        bpm0 = grid(p)[0]
        ratio = 1.0
        if k and f["entrada"] == "dj" and prev_bpm:
            ratio = prev_bpm / bpm0
            while ratio > 1.4:
                ratio /= 2
            while ratio < 0.7:
                ratio *= 2
            if abs(ratio - 1) > 0.08:
                ratio, f["entrada"] = 1.0, "respiro"
                print(f"AVISO: faixa {f['id']} longe do andamento da anterior: entrada trocada de dj para respiro", file=sys.stderr)
        p2 = stretched(p, ratio)
        bpm, _, downs, energy, length, edb = grid(p2)
        info.append({"p": p2, "bpm": bpm, "bpm0": bpm0, "ratio": ratio, "downs": np.asarray(downs), "energy": energy, "len": length, "edb": edb})
        prev_bpm = bpm

    B = [f["de"] for f in faixas]
    off, swap = [0.0] * n, [0.0] * n
    for k, f in enumerate(faixas):
        g = info[k]
        fim_aprox = (B[k + 1] + 4.5) if k + 1 < n else TOTAL
        if k == 0:
            off[0] = escolhe_inicio(g, fim_aprox + 1, f["int"], f["off"])
            swap[0] = 0.0
            continue
        prev_downs_out = info[k - 1]["downs"] - off[k - 1] + B[k - 1]
        if f["entrada"] == "dj":
            ok = prev_downs_out[(prev_downs_out >= B[k] + 1.3) & (prev_downs_out <= B[k] + 3.6)]
            swap[k] = float(ok[0]) if ok.size else float(prev_downs_out[np.argmin(np.abs(prev_downs_out - (B[k] + 1.8)))])
            lead = swap[k] - B[k]
            L = escolhe_inicio(g, fim_aprox - swap[k] + 1, f["int"], f["off"], lead=lead)
            off[k] = L - lead
        else:
            swap[k] = B[k]
            off[k] = escolhe_inicio(g, fim_aprox - B[k] + 1, f["int"], f["off"])

    t = np.arange(N) / SR
    bed = np.zeros((2, N), np.float32)
    riser = load(arquivo_sfx("riser"))
    rp = int(np.argmax(np.abs(riser).mean(axis=0)))
    riser = sosfilt(butter(2, 300, btype="high", fs=SR, output="sos"), riser, axis=1) * db2lin(-23)
    tr_rep = []
    for k, f in enumerate(faixas):
        g = info[k]
        y = load(g["p"])
        pre = min(0.35, off[k]) if (k and f["entrada"] == "respiro") else 0.0  # respiro: a nova já soa baixinho antes do `de` (sem vão)
        a0 = int((B[k] - pre) * SR)
        s0 = int((off[k] - pre) * SR)
        seg = y[:, s0: s0 + (N - a0)]
        full = np.zeros((2, N), np.float32)
        full[:, a0:a0 + seg.shape[1]] = seg
        prot_ini = swap[k]
        prot_fim = B[k + 1] if k + 1 < n else TOTAL
        ref = full[:, int(prot_ini * SR): max(int(prot_ini * SR) + SR * 2, int(prot_fim * SR))]
        gain = MUSIC_LUFS + (f["int"] - 2) * 1.5 + f["extra_db"] - lufs(ref)
        full *= db2lin(gain)

        keys = [(0, -90.0)]
        hp_keys, lp_keys = [(0, 22.0)], [(0, 19000.0)]
        # entrada
        if k == 0:
            keys += [(0, -40.0), (0.06, 0.0)]
        elif f["entrada"] == "dj":
            s = swap[k]
            keys += [(B[k] - 0.01, -90.0), (B[k], -40.0), (B[k] + 0.3, -14.0), (min(B[k] + 0.7, s - 0.6), -6.0),
                     (min(B[k] + 1.3, s - 0.4), -2.0), (s - 0.05, -1.0), (s, 0.0)]
            hp_keys = [(0, 260.0), (s - 0.04, 260.0), (s + 0.22, 22.0)]
        elif f["entrada"] == "respiro":
            keys += [(B[k] - pre - 0.01, -90.0), (B[k] - pre, -18.0), (B[k] + 0.35, 0.0)]
        else:  # corte
            keys += [(B[k] - 0.01, -90.0), (B[k], -40.0), (B[k] + 0.01, 0.0)]
        # saída para a próxima
        if k + 1 < n:
            nx, Bn, sn = faixas[k + 1], B[k + 1], swap[k + 1]
            if nx["entrada"] == "dj":
                dim = nx.get("dim") or Bn - 0.75
                muff = nx.get("muff") or Bn - 0.2
                lp_keys = [(0, 19000.0), (dim, 19000.0), (muff, 650.0)]
                keys += [(dim, 0.0), (muff, -3.0)] + ([(Bn + 1.3, -6.0)] if Bn + 1.3 < sn - 0.2 else []) + \
                        [(sn - 0.2, -9.0), (sn + 0.12, -40.0), (sn + 0.45, -90.0), (TOTAL, -90.0)]
                if 0 < int(sn * SR) - rp < N:
                    i0 = int(sn * SR) - rp
                    bed[:, i0: i0 + riser.shape[1]] += riser[:, : N - i0]
            elif nx["entrada"] == "respiro":
                lp_keys = [(0, 19000.0), (Bn - 1.2, 19000.0), (Bn + 0.2, 900.0)]
                keys += [(Bn - 1.2, 0.0), (Bn - 0.3, -4.0), (Bn + 0.1, -12.0), (Bn + 0.45, -90.0), (TOTAL, -90.0)]
            else:
                keys += [(Bn - 0.04, 0.0), (Bn, -90.0), (TOTAL, -90.0)]
        else:
            keys += [(T_END_FADE, 0.0), (TOTAL, -30.0)]
        if len(hp_keys) > 1:
            full = tv_filter(full, env_at(hp_keys, t), "high")
        if len(lp_keys) > 1:
            full = tv_filter(full, np.exp(env_at([(x, np.log(v)) for x, v in lp_keys], t)), "low")
        full *= db2lin(env_at(keys, t))
        bed += full
        if k and f["entrada"] == "corte":
            imp = load(arquivo_sfx("impact_deep"))[:, : int(1.4 * SR)] * db2lin(-17)
            ip = int(np.argmax(np.abs(imp).mean(axis=0)))
            i0 = int(B[k] * SR) - ip
            bed[:, max(0, i0): i0 + imp.shape[1]] += imp[:, max(0, -i0): N - i0]
        tr_rep.append({"id": f["id"], "de": round(B[k], 2), "entrada": f["entrada"], "troca_s": round(swap[k], 2), "inicio_na_faixa_s": round(off[k], 2),
                       "bpm": round(info[k]["bpm0"], 1), "esticada": round(info[k]["ratio"], 4), "ganho_db": round(gain, 1)})
    # preenchimento: na janela de cada troca a trilha não cai mais que 6 dB abaixo da mediana de antes (expansor para cima, suave).
    # Faixas diferentes têm energia diferente; a curva fixa sozinha deixava vãos de 9-12 dB (a troca aprovada do C2 tinha ≈ 6).
    h = int(0.05 * SR)
    nh = N // h
    pisos = {}
    for _passada in range(2):  # 2 passadas: a suavização de 250 ms deixa sobrar parte dos vãos curtos na 1ª
        e50 = 20 * np.log10(np.sqrt((bed.mean(axis=0)[: nh * h].reshape(nh, h) ** 2).mean(axis=1)) + 1e-9)
        comp = np.zeros(nh)
        for k in range(1, n):
            r0, r1 = max(0, int((B[k] - 3) / 0.05)), max(1, int((B[k] - 0.8) / 0.05))
            if r1 <= r0:
                continue
            piso = pisos.setdefault(k, float(np.median(e50[r0:r1])) - 5.5)
            a, b = max(0, int((B[k] - 0.8) / 0.05)), min(nh, int((swap[k] + 0.6) / 0.05) + 1)
            comp[a:b] = np.maximum(comp[a:b], np.clip(piso - e50[a:b], 0, 9))
        if not comp.any():
            break
        comp = np.convolve(comp, np.ones(5) / 5, mode="same")  # 250 ms: sem "bombear"
        g = np.interp(np.arange(N), np.arange(nh) * h + h / 2, comp)
        bed *= db2lin(g)[None, :].astype(np.float32)
    # vão de volume em cada troca, na trilha ANTES do ducking (janelas de 200 ms): referência = mediana de [de-3, de-0,8]
    H = int(0.2 * SR)
    nb = N // H
    edb = 20 * np.log10(np.sqrt((bed.mean(axis=0)[: nb * H].reshape(nb, H) ** 2).mean(axis=1)) + 1e-9)
    for k in range(1, n):
        ref = edb[max(0, int((B[k] - 3) / 0.2)): max(1, int((B[k] - 0.8) / 0.2))]
        jan = edb[int((B[k] - 0.3) / 0.2): int((swap[k] + 0.6) / 0.2) + 1]
        if ref.size and jan.size:
            vao = float(np.median(ref) - jan.min())
            tr_rep[k]["vao_db"] = round(vao, 1)
            if vao > 8:
                print(f"AVISO: troca {k} ({faixas[k]['id']}, {faixas[k]['entrada']}) com vão de {vao:.1f} dB na trilha (> 8)", file=sys.stderr)
    report.update(name=nome, faixas=tr_rep)
    return bed


def arquivo_sfx(nome: str) -> Path:
    if nome.startswith("mixkit:"):
        i = nome.split(":", 1)[1]
        return baixar(url_sfx(i), CACHE_LIB / "sfx" / f"{i}.mp3")
    from mixkit import sfx_catalogo
    p = sfx_catalogo(nome, SFX_DIR, CACHE_LIB)
    if p:
        return p
    raise SystemExit(f"efeito '{nome}' não existe no catálogo (biblioteca/sfx); use 'mixkit:<id>' (sfx.py buscar)")


def lint_sfx(ev: list, report: dict) -> None:
    """Efeito sem propósito atrapalha mais que ajuda (aprendido nos testes): avisa excesso, rajadas e eventos sem gatilho.
    Camadas no mesmo quadro contam como 1 evento; `rajada_ok` exclui o evento da conta de rajada (knock, clímax desenhado)."""
    avisos = []
    dur = N / SR
    quadros = sorted({e["at"] for e in ev})
    if len(quadros) / dur > 1.0:
        avisos.append(f"densidade {len(quadros) / dur:.2f} efeitos/s (> 1,0): corte os que não têm gatilho visível")
    at = sorted({e["at"] for e in ev if not e.get("rajada_ok")})
    for i in range(len(at)):
        nq = sum(1 for a in at[i:] if a - at[i] <= 90)
        if nq > 4:
            avisos.append(f"{nq} efeitos em 3 s a partir do quadro {at[i]}: rajada (se for desenhado, marque rajada_ok)")
            break
    for e in ev:
        if not e.get("note"):
            avisos.append(f"quadro {e['at']} ({e['file']}) sem 'note' (qual elemento visível dispara?)")
    so = sorted(ev, key=lambda x: x["at"])
    same = [(a["at"], b["at"], a["file"]) for a, b in zip(so, so[1:])
            if a["file"] == b["file"] and 0 < b["at"] - a["at"] < 12 and a["file"] in ("pop_whoosh", "pop_hard", "click_ui", "swoosh_small")]
    if len(same) > 4:
        avisos.append(f"{len(same)} repetições do mesmo efeito de UI em < 12 quadros (ex.: {same[:3]}): reduzir")
    report["sfx_avisos"] = avisos
    for a in avisos:
        print("AVISO sfx:", a, file=sys.stderr)


def sfx_bus(report: dict) -> np.ndarray:
    ev = json.loads((EDIT / "audio" / "sfx.json").read_text(encoding="utf-8"))["events"]
    lint_sfx(ev, report)
    bus = np.zeros((2, N), np.float32)
    cache: dict[str, np.ndarray] = {}
    for e in ev:
        name = e["file"]
        if name not in cache:
            cache[name] = load(arquivo_sfx(name))
        y = cache[name].copy()
        if e.get("pitch"):
            y = librosa.resample(y, orig_sr=SR, target_sr=int(SR / 2 ** (e["pitch"] / 12)))
        if e.get("hp"):
            y = sosfilt(butter(2, e["hp"], btype="high", fs=SR, output="sos"), y, axis=1)
        mono = np.abs(y).mean(axis=0)
        sm = np.convolve(mono, np.ones(240) / 240, mode="same")
        peak = int(np.argmax(sm))
        if e.get("max"):
            m = int(e["max"] * SR)
            if y.shape[1] > m:
                y = y[:, :m]
        fo = int(min(0.3, 0.3 * y.shape[1] / SR) * SR)
        if fo > 8:
            y[:, -fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
        fi = int(0.003 * SR)
        y[:, :fi] *= np.linspace(0, 1, fi)
        if "pan" in e:
            pan = e["pan"]
            p = np.linspace(pan[0], pan[1], y.shape[1]) if isinstance(pan, list) else np.full(y.shape[1], pan)
            th = (p + 1) * np.pi / 4
            mid = y.mean(axis=0)
            y = np.stack([mid * np.cos(th), mid * np.sin(th)]) * np.sqrt(2)
        y *= db2lin(e["gain"])
        start = int(round(e["at"] / FPS_ * SR)) - min(peak, y.shape[1] - 1)
        a, b = max(0, start), min(N, start + y.shape[1])
        if b > a:
            bus[:, a:b] += y[:, a - start: b - start]
    bus = sosfilt(peaking(2800, -3.0, 1.0), bus, axis=1).astype(np.float32)
    report["sfx_events"] = len(ev)
    return bus


def follower(x_db: np.ndarray, rate: float, att: float, rel: float) -> np.ndarray:
    ka, kr = np.exp(-1 / (att * rate)), np.exp(-1 / (rel * rate))
    out = np.empty_like(x_db)
    v = x_db[0]
    for i, x in enumerate(x_db):
        k = ka if x > v else kr
        v = k * v + (1 - k) * x
        out[i] = v
    return out


def duck(music: np.ndarray, key: np.ndarray, report: dict) -> np.ndarray:
    hop = 48  # 1 ms
    n = key.shape[0] // hop
    rms = np.sqrt((key[: n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    kdb = 20 * np.log10(rms)
    envd = follower(kdb, 1000, 0.010, 0.250)
    active = envd[envd > -45]
    thr = float(np.median(active)) - 10 if active.size else -35
    gr = np.clip((envd - thr) * (1 - 1 / 2.5), 0, 6.0)
    gr = follower(gr, 1000, 0.040, 0.400)
    g = np.interp(np.arange(music.shape[1]), np.arange(n) * hop, -gr)
    report.update(duck_threshold_db=round(thr, 1), duck_mean_db=round(float(-gr.mean()), 1))
    return music * db2lin(g)[None, :]


def main(opt: str):
    report: dict = {"opt": opt}
    voice, _ = sf.read(str(EDIT / "work" / "voz_limpa.wav"), always_2d=True, dtype="float32")
    voice = voice.mean(axis=1)[:N]
    voice = np.pad(voice, (0, N - voice.shape[0]))
    v2 = np.stack([voice, voice])
    music = music_bed(opt, report)
    sfx = sfx_bus(report)
    music = duck(music, voice + 0.5 * sfx.mean(axis=0), report)
    mix = v2 + music + sfx
    sf.write(str(CACHE / f"stem_music_{opt}.wav"), music.T, SR, subtype="FLOAT")
    sf.write(str(CACHE / f"stem_sfx_{opt}.wav"), sfx.T, SR, subtype="FLOAT")
    raw = CACHE / f"mix_{opt}_raw.wav"
    sf.write(str(raw), mix.T, SR, subtype="FLOAT")
    report["lufs_voice"] = round(lufs(v2), 1)
    report["lufs_music"] = round(lufs(music), 1)
    report["lufs_sfx"] = round(lufs(sfx), 1)
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    js = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", m.stderr, re.S).group(0))
    filt = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
            f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    out = MOTION / "public" / f"mix_{opt}.wav"
    subprocess.run(["ffmpeg", "-y", "-i", str(raw), "-af", filt, "-ar", str(SR), "-c:a", "pcm_s24le", str(out)],
                   check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(out), "-b:a", "256k", str(EDIT / "audio" / f"mix_{opt}.mp3")],
                   check=True, capture_output=True)
    chk = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="ignore").stderr
    report["final_I"] = re.findall(r"I:\s+(-?[\d.]+) LUFS", chk)[-1]
    report["final_TP"] = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", chk)[-1]
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
