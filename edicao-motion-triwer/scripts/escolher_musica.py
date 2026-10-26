"""Escolhe a trilha pela EMOÇÃO de cada trecho da fala: 1 faixa ou várias, trocando quando a emoção muda.

Entrada (projeto.json -> musica.trechos, escrito pelo Claude no portão 1, junto com a estratégia):
    "trechos": [
      {"de": 0,         "emocao": "tensao",    "intensidade": 2, "nota": "gancho: MBA caro"},
      {"de": "Eu@747",  "emocao": "esperanca", "intensidade": 2, "nota": "virada: o caso do Daniel"},
      {"de": "O@1064",  "emocao": "motivacao", "intensidade": 3, "entrada": "corte", "nota": "método"}
    ]
  `de` = segundos de SAÍDA ou "palavra@quadro" (formato do words_out). Emoções: ver emocoes.py (tensao, misterio, dor, reflexao,
  confianca, esperanca, motivacao, triunfo, urgencia, leveza, neutro). intensidade 1-3. `entrada` (opcional): dj | respiro | corte;
  sem ela, o script escolhe dj quando andamento e tom casam e respiro quando não.
Saída: projeto.json -> musica.versoes {A, B, C} (faixas diferentes entre si) e as faixas em edit/music_cand/. Depois: mix.py A|B|C.

Regras: trecho < musica.min_trecho (5 s) é fundido ao vizinho (troca rápida demais soa como erro) salvo entrada "corte";
faixa já usada pelo MESMO cliente perde muito ponto (vídeos diferentes, músicas diferentes; registro.py, gravado pelo entregar.py);
a mesma faixa não se repete dentro do vídeo; 2-3 versões com faixas distintas para o usuário escolher de ouvido.
Uso (de dentro de edit/):  python escolher_musica.py [--versoes 3] [--sem-baixar]
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import json
import shutil
import sys

from _cfg import CACHE_LIB, EDIT, LIB, cfg, quadro, salvar_cfg
from emocoes import EMOCOES, alvo_energia, pontuar
from mixkit import baixar, url_musica
from registro import carregar

c = cfg()
MC = c.setdefault("musica", {})
TOTAL = json.loads((EDIT / "edl.json").read_text(encoding="utf-8"))["total_duration_s"]
DIR = LIB / "musica"
idx = json.loads((DIR / "indice.json").read_text(encoding="utf-8"))
an = json.loads((DIR / "analise.json").read_text(encoding="utf-8")) if (DIR / "analise.json").exists() else {}
usadas = carregar()
cliente = (c.get("cliente") or "").strip()
NVERS = int(sys.argv[sys.argv.index("--versoes") + 1]) if "--versoes" in sys.argv else 3
MIN_T = float(MC.get("min_trecho", 5.0))

# ---------- trechos ----------
tr = []
for t in MC.get("trechos", []):
    if t.get("emocao") not in EMOCOES:
        raise SystemExit(f'emoção desconhecida: {t.get("emocao")!r}; use uma de: {", ".join(EMOCOES)}')
    tr.append({"ini": quadro(t.get("de", 0)), "emocao": t["emocao"], "int": int(t.get("intensidade", 2)), "entrada": t.get("entrada"),
               "nota": t.get("nota", "")})
if not tr:
    raise SystemExit("musica.trechos vazio: escreva o mapa emocional (ver o docstring)")
tr.sort(key=lambda x: x["ini"])
tr[0]["ini"] = 0.0
for i, t in enumerate(tr):
    t["fim"] = tr[i + 1]["ini"] if i + 1 < len(tr) else TOTAL
fund = []
for t in tr:
    if fund and t["emocao"] == fund[-1]["emocao"] and t["int"] == fund[-1]["int"] and t["entrada"] != "corte":
        fund[-1]["fim"] = t["fim"]
        continue
    if fund and t["fim"] - t["ini"] < MIN_T and t["entrada"] != "corte":
        print(f'AVISO: trecho "{t["nota"] or t["emocao"]}" tem {t["fim"] - t["ini"]:.1f} s (< {MIN_T} s): fundido ao anterior')
        fund[-1]["fim"] = t["fim"]
        continue
    fund.append(dict(t))
if len(fund) > 1 and fund[0]["fim"] - fund[0]["ini"] < MIN_T:
    fund[1]["ini"] = 0.0
    fund.pop(0)
tr = fund

# ---------- candidatas por trecho ----------
ok_ids = [i for i in idx if i in an and an[i].get("bpm")]
if len(ok_ids) < 30:
    print(f"AVISO: só {len(ok_ids)} faixas analisadas; rode indexar_musicas.py --analisar (segundo plano) para ampliar a escolha")
energias = sorted(an[i]["e8_30"] for i in ok_ids)
pct = lambda p: energias[min(len(energias) - 1, int(p * len(energias)))]
PCT = (pct(0.2), pct(0.5), pct(0.8))
ja = {}
for cli, lst in usadas.items():
    for v in lst:
        for i in v.get("ids", []):
            ja.setdefault(i, set()).add(cli)


def janela(a: dict, L: float, alvo: float):
    """melhor janela de L s na curva de energia: (aderência 0..1, offset sugerido em s)"""
    cv = a.get("curva5s")
    if not cv:
        e = a.get("e8_30", -25)
        return max(0.0, 1 - abs(e - alvo) / 8), 8.0
    n = max(1, int(round(L / 5)))
    best = (0.0, 0.0)
    for k in range(0, max(1, len(cv) - n)):
        m = sum(cv[k:k + n]) / n
        fit = max(0.0, 1 - abs(m - alvo) / 8)
        if fit > best[0] + 1e-6:
            best = (fit, k * 5.0)
    return best


cands = []
for t in tr:
    L = t["fim"] - t["ini"]
    alvo = alvo_energia(t["int"], PCT)
    lst = []
    for i in ok_ids:
        a = an[i]
        if (a.get("dur") or 0) < L + 6:
            continue
        emo = pontuar(idx[i], a)[t["emocao"]]
        if emo < 0.25:
            continue
        fit, off = janela(a, L, alvo)
        pen = -0.6 if cliente and cliente in ja.get(i, set()) else (-0.15 if i in ja else 0.0)
        lst.append({"id": i, "s": 1.6 * emo + 0.8 * fit + pen, "emo": emo, "fit": fit, "off": off, "usada": bool(pen)})
    lst.sort(key=lambda x: -x["s"])
    if not lst:
        raise SystemExit(f'nenhuma faixa para "{t["emocao"]}" com {L:.0f} s: amplie a biblioteca (indexar_musicas.py --analisar)')
    cands.append(lst[:18])


def cam_ok(a: str, b: str) -> bool:
    na, la, nb, lb = int(a[:-1]), a[-1], int(b[:-1]), b[-1]
    return (na == nb) or (la == lb and min((na - nb) % 12, (nb - na) % 12) == 1)


def bpm_ok(a: float, b: float) -> bool:
    r = b / a
    while r > 1.4:
        r /= 2
    while r < 0.7:
        r *= 2
    return abs(r - 1) <= 0.07


def entrada(t: dict, a: str, b: str):
    if t["entrada"]:
        return t["entrada"], 0.0
    A, B = an[a], an[b]
    if bpm_ok(A["bpm"], B["bpm"]):
        return "dj", (0.3 if cam_ok(A["cam"], B["cam"]) else 0.05)
    return "respiro", -0.1


def busca(proibidas: set, max_comum: int, base: list):
    beam = [([], 0.0)]
    for k, t in enumerate(tr):
        nb = []
        for chain, sc in beam:
            for cnd in cands[k]:
                i = cnd["id"]
                if i in chain:
                    continue
                comum = sum(1 for x in chain + [i] if x in proibidas)
                if comum > max_comum:
                    continue
                add = cnd["s"]
                if chain:
                    _, bon = entrada(t, chain[-1], i)
                    add += bon
                nb.append((chain + [i], sc + add))
        nb.sort(key=lambda x: -x[1])
        beam = nb[:80]
    return beam[0][0] if beam else None


versoes, usadas_aqui = {}, set()
for v in "ABC"[:NVERS]:
    ch = busca(usadas_aqui, 0 if v != "A" else 99, []) or busca(usadas_aqui, 1, [])
    if not ch:
        break
    usadas_aqui |= set(ch)
    faixas = []
    for k, (t, i) in enumerate(zip(tr, ch)):
        ent, _ = entrada(t, ch[k - 1], i) if k else ("inicio", 0)
        cnd = next(x for x in cands[k] if x["id"] == i)
        faixas.append({"id": i, "titulo": idx[i]["titulo"], "de": round(t["ini"], 2), "ate": round(t["fim"], 2), "emocao": t["emocao"],
                       "intensidade": t["int"], "entrada": ent, "offset_sugerido": cnd["off"], "nota": t["nota"]})
    versoes[v] = {"faixas": faixas}

MC["versoes"] = versoes
salvar_cfg(c)
cand_dir = EDIT / MC.get("candidatas", "music_cand")
for v, d in versoes.items():
    print(f"\n== versão {v} ==")
    for f in d["faixas"]:
        a = an[f["id"]]
        moods = ", ".join(t[2] for t in idx[f["id"]]["tags"] if t[0] in ("mood", "tag"))[:60]
        print(f'  {f["de"]:5.1f}-{f["ate"]:5.1f}s  {f["emocao"]:<10} i{f["intensidade"]}  {f["entrada"]:<7} {f["id"]:>5} {f["titulo"][:28]:<28} '
              f'{a["bpm"]:>5} bpm {a["cam"]:>3}  [{moods}]' + ("  (já usada)" if f["id"] in ja else ""))
        if "--sem-baixar" not in sys.argv:
            p = cand_dir / f'{f["id"]}.mp3'
            if not p.exists():
                cache = CACHE_LIB / "musica" / f'{f["id"]}.mp3'
                baixar(url_musica(f["id"]), cache)
                cand_dir.mkdir(exist_ok=True)
                shutil.copy2(cache, p)
print("\ngravado em projeto.json -> musica.versoes; próximo: python mix.py A (e B, C)")
