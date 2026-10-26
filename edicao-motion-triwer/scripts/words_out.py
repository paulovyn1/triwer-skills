"""Palavras na linha do tempo de SAÍDA (legenda): texto do Groq + tempo do faster-whisper onde as palavras batem.

Lê projeto.json -> texto.correcoes {"está": "tá"} (ajusta o texto ao que foi dito),
texto.descartar [[palavra, tempo_original_Groq]] (falsa largada que sobrou em trecho mantido) e
texto.retempo [[palavra, tempo_Groq, novo_tempo]] (Groq com tempo trocado). Grava motion/public/words.json.

Automático (antes era manual, 9 entradas no C3):
- descarta palavra cujo tempo do Groq OU do faster-whisper cai dentro de `corte.remover` (falsa largada/tomada descartada);
- palavra do Groq fora de ordem (trecho com várias tomadas) sem par no faster-whisper: procura a mesma palavra no FW a ±1,5 s e usa o tempo dele;
- números por extenso batem com algarismos ("cinco" = "5") no alinhamento.
Imprime as correções automáticas e a lista final "palavra@quadro" (base do roteiro em motion/src/captions.ts).
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import difflib
import json
import re

from _cfg import EDIT, MOTION, WORK, cfg, fonte

c = cfg()
g = [w for w in json.loads((EDIT / "transcripts" / f"{fonte(c).stem}.json").read_text(encoding="utf-8"))["words"] if w["type"] == "word"]
fp = EDIT / "transcripts" / "fw_small_words.json"
f = json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else []
cmap = json.loads((WORK / "cuts_map.json").read_text(encoding="utf-8"))
T = c.get("texto", {})
FIX = T.get("correcoes", {})
FPS = c.get("fps", 30)
REMOVER = [tuple(r) for r in c.get("corte", {}).get("remover", [])]
NUM = {"zero": "0", "um": "1", "uma": "1", "dois": "2", "duas": "2", "tres": "3", "quatro": "4", "cinco": "5", "seis": "6", "sete": "7",
       "oito": "8", "nove": "9", "dez": "10", "onze": "11", "doze": "12", "vinte": "20", "trinta": "30", "cem": "100"}


ALIAS = {"pra": "para", "pro": "para", "ta": "esta", "to": "estou", "ce": "voce", "tu": "voce", "teu": "seu", "tua": "sua"}


def norm(s):
    s = re.sub(r"[^\wà-ú]", "", s.lower())
    s = s.translate(str.maketrans("áàâãéêíóôõúç", "aaaaeeiooouc"))
    s = ALIAS.get(s, s)  # fala informal x faster-whisper formal ("pra" x "para", "tu" x "você")
    return NUM.get(s, s)


timed = [None] * len(g)
usados = set()
if f:
    sm = difflib.SequenceMatcher(a=[norm(w["text"]) for w in g], b=[norm(w["text"]) for w in f], autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            fw = f[blk.b + k]
            if abs(fw["start"] - g[blk.a + k]["start"]) < 0.8:  # guarda: FW fora de sincronia com o Groq é ignorado
                timed[blk.a + k] = (fw["start"], fw["end"])
                usados.add(blk.b + k)

auto = []
# Groq fora de ordem e sem par: mesma palavra no FW a ±1,5 s
for i, w in enumerate(g):
    if timed[i] or not f:
        continue
    prev_s = max((timed[j][0] if timed[j] else g[j]["start"]) for j in range(i)) if i else -1
    nxt = [timed[j][0] if timed[j] else g[j]["start"] for j in range(i + 1, min(len(g), i + 3))]
    fora = w["start"] < prev_s - 0.05 or (nxt and w["start"] > min(nxt) + 0.05)
    if not fora:
        continue
    cands = [(abs(x["start"] - w["start"]), k) for k, x in enumerate(f)
             if k not in usados and norm(x["text"]) == norm(w["text"]) and abs(x["start"] - w["start"]) <= 1.5 and x["start"] > prev_s]
    if cands:
        _, k = min(cands)
        timed[i] = (f[k]["start"], f[k]["end"])
        usados.add(k)
        auto.append(f'retempo "{w["text"]}" {w["start"]:.2f} -> {f[k]["start"]:.2f} (Groq fora de ordem)')
    elif w["start"] < prev_s - 0.05 and i:
        # sem par no FW (ele ouviu outra palavra): logo depois do fim da anterior
        j = i - 1
        fim_ant = min(timed[j][1] if timed[j] else g[j]["end"], (timed[j][0] if timed[j] else g[j]["start"]) + 0.6)
        dur = max(0.12, w["end"] - w["start"])
        timed[i] = (fim_ant + 0.02, fim_ant + 0.02 + dur)
        auto.append(f'retempo "{w["text"]}" {w["start"]:.2f} -> {fim_ant + 0.02:.2f} (Groq fora de ordem, sem par no FW: depois da anterior; conferir)')

words = []
for i, w in enumerate(g):
    s, e = timed[i] if timed[i] else (w["start"], w["end"])
    words.append({"text": FIX.get(w["text"], w["text"]), "s": s, "e": e, "gs": w["start"]})
for a, b in zip(words, words[1:]):
    a["e"] = min(a["e"], b["s"])


def to_out(t):
    for m in cmap:
        if m["src_start"] - 0.25 <= t < m["src_end"]:
            return round(max(t, m["src_start"]) - m["src_start"] + m["out_start"], 3)
    for m in cmap:
        if t < m["src_start"]:
            return m["out_start"]
    return cmap[-1]["out_start"] + cmap[-1]["src_end"] - cmap[-1]["src_start"]


def mantida(t):
    return any(m["src_start"] - 0.15 <= t < m["src_end"] + 0.30 for m in cmap)


def removida(t, folga=0.0):
    return any(a - 0.02 + folga <= t <= b - 0.06 - folga for a, b in REMOVER)


DESC = T.get("descartar", [])
final = []
for w in words:
    if any(w["text"] == d[0] and abs(w["gs"] - d[1]) < 0.06 for d in DESC):
        continue
    # tempo do Groq dentro de `remover`, ou o do FW BEM dentro (> 0,3 s das bordas: perto da borda o FW pode ter pego a respiração)
    if removida(w["gs"]) or (w["s"] != w["gs"] and removida(w["s"], 0.3)):
        if mantida(w["s"]) or mantida(w["gs"]):  # só avisa o que antes vazava para a legenda (borda de remover)
            auto.append(f'descarta "{w["text"]}" {w["gs"]:.2f} (dentro de corte.remover)')
        continue
    if not (mantida(w["s"]) or mantida(w["gs"])):
        continue
    final.append(w)
words = final
for w in words:
    for r in T.get("retempo", []):
        if w["text"] == r[0] and abs(w["gs"] - r[1]) < 0.06:
            w["e"] = r[2] + (w["e"] - w["s"])
            w["s"] = r[2]
out = [{"text": w["text"], "start": to_out(w["s"]), "end": to_out(min(w["e"], w["s"] + 1.2)), "src": round(w["s"], 2)} for w in words]
# palavras que caíram em trecho cortado grudam no próximo corte: tempo mínimo crescente
for a, b in zip(out, out[1:]):
    b["start"] = max(b["start"], round(a["start"] + 0.04, 3))
for a, b in zip(out, out[1:]):
    a["end"] = max(a["start"] + 0.05, min(a["end"], b["start"]))
dst = MOTION / "public"
dst.mkdir(parents=True, exist_ok=True)
(dst / "words.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for a in auto:
    print("auto:", a)
print(len(out), "palavras;", sum(1 for t in timed if t is None), "sem tempo do faster-whisper" + ("" if f else " (fw_small_words.json ausente)"))
print(" ".join(f"{w['text']}@{round(w['start'] * FPS)}" for w in out))
