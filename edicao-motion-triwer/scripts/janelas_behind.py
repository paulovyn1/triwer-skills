"""Lista as janelas (frames de saída) em que a pessoa recortada precisa aparecer: cues `behind` (texto atrás) e `ghost`.

Uso:  python janelas_behind.py            (de dentro de edit/)  -> imprime e grava work/janelas_behind.json
Lê motion/src/captions.ts (SCRIPT) + motion/public/words.json; mesma regra do Pessoa.tsx: janela = [início do cue - PRE, hold ou
fim do cue], com margem de 3 quadros. O recorte é gerado SÓ nessas janelas (PNG com alfa por quadro), não no vídeo todo.
`cues()` também é usado por verificar.py (lint/stills) e montar_sfx.py (efeitos da legenda).
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import json
import re

from _cfg import EDIT

PRE = 6  # igual ao Pessoa.tsx
MARGEM = 3
FPS = 30


def cues():
    """todos os cues do SCRIPT: mode, text, start, end, hold, ghost (frames de saída) e palavras [{texto, quadro, linha}]"""
    caps = (EDIT / "motion" / "src" / "captions.ts").read_text(encoding="utf-8")
    words = json.loads((EDIT / "motion" / "public" / "words.json").read_text(encoding="utf-8"))
    body = caps[caps.index("const SCRIPT"):]
    body = body[: body.index("\n];")]
    cues, k = [], 0
    for m in re.finditer(r'^\s*\[\s*"(\w+)"\s*,\s*"([^"]*)"\s*(?:,\s*\{([^}]*)\})?\s*\]', body, re.M):
        mode, text, opt = m.group(1), m.group(2), m.group(3) or ""
        toks = [t for t in text.split(" ") if t]
        palavras, linha = [], 0
        for t in toks:
            if t == "|":
                linha += 1
                continue
            palavras.append({"texto": t.lstrip("*#^"), "quadro": round(words[k + len(palavras)]["start"] * FPS), "linha": linha})
        n = len(palavras)
        start = round(words[k]["start"] * FPS)
        endw = round(words[k + n - 1]["end"] * FPS)
        hold = re.search(r"hold:\s*(\d+)", opt)
        cues.append({"mode": mode, "text": text, "start": start, "end": endw, "hold": int(hold.group(1)) if hold else None,
                     "ghost": "ghost" in opt, "palavras": palavras})
        k += n
    for i, c in enumerate(cues):  # cada cue fica até o próximo começar (mesma regra do resolver)
        c["end"] = cues[i + 1]["start"] if i + 1 < len(cues) else c["end"] + 15
    return cues


def janelas():
    out = []
    for c in cues():
        if c["mode"] == "behind" or c["ghost"]:
            a = c["start"] - PRE - MARGEM
            b = (c["hold"] if c["hold"] is not None else c["end"]) + MARGEM
            out.append([max(0, a), b])
    out.sort()
    merged = []
    for a, b in out:
        if merged and a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged


if __name__ == "__main__":
    w = janelas()
    (EDIT / "work").mkdir(exist_ok=True)
    (EDIT / "work" / "janelas_behind.json").write_text(json.dumps(w), encoding="utf-8")
    print("janelas do recorte (frames):", w, "| total", sum(b - a + 1 for a, b in w), "quadros")
