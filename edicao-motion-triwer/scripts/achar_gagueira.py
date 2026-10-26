"""Candidatos a gagueira, repetição e vício de fala, cruzando duas transcrições (Groq + faster-whisper).

Uso:  python achar_gagueira.py           (rodar em edit/, depois de fw_check.py gerar transcripts/fw_small_words.json)
Imprime só candidatos com tempo; o Claude decide o que entra em corte.remover do projeto.json (janela [início, fim] no ORIGINAL).
Sinais: (1) palavra que só o faster-whisper ouviu (é/ahn/hum que o Groq normaliza); (2) palavra repetida em seguida ("eu eu",
"de de"); (3) trecho repetido (2 palavras); (4) palavra esticada (> 0,9 s, hesitação); (5) fragmento terminado em hífen.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import difflib
import json
import re

from _cfg import EDIT, cfg, fonte


def norm(s):
    return re.sub(r"[^\wà-ú]", "", s.lower())


c = cfg()
g = [w for w in json.loads((EDIT / "transcripts" / f"{fonte(c).stem}.json").read_text(encoding="utf-8"))["words"] if w["type"] == "word"]
fp = EDIT / "transcripts" / "fw_small_words.json"
f = json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else []

print("# palavras que só o faster-whisper ouviu (hesitação normalizada pelo Groq)")
sm = difflib.SequenceMatcher(a=[norm(w["text"]) for w in g], b=[norm(w["text"]) for w in f], autojunk=False)
for tag, a1, a2, b1, b2 in sm.get_opcodes():
    if tag in ("insert", "replace"):
        for w in f[b1:b2]:
            if w["end"] - w["start"] < 0.6 and len(norm(w["text"])) <= 5:
                print(f"  {w['start']:.2f}-{w['end']:.2f}  '{w['text']}'")
print("# repetições imediatas")
for i in range(1, len(g)):
    if norm(g[i]["text"]) == norm(g[i - 1]["text"]) and len(norm(g[i]["text"])) > 0:
        print(f"  {g[i - 1]['start']:.2f}-{g[i]['end']:.2f}  '{g[i - 1]['text']} {g[i]['text']}'")
for i in range(3, len(g)):
    if [norm(x["text"]) for x in g[i - 3:i - 1]] == [norm(x["text"]) for x in g[i - 1:i + 1]]:
        print(f"  {g[i - 3]['start']:.2f}-{g[i]['end']:.2f}  trecho repetido '{' '.join(x['text'] for x in g[i - 3:i + 1])}'")
print("# palavras esticadas / fragmentos")
for w in g:
    if w["end"] - w["start"] > 0.9 or w["text"].endswith("-"):
        print(f"  {w['start']:.2f}-{w['end']:.2f}  '{w['text']}'  ({w['end'] - w['start']:.2f}s)")
