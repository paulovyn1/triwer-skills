"""Rascunho do audio/sfx.json a partir do que já está decidido: painéis (+ o que cada subagente de painel pediu), legenda e golpes de zoom.

Uso (de dentro de edit/):  python montar_sfx.py [--sobrescrever]
Fontes:
  - motion/src/panels/<ID>.sfx.json   escrito pelo subagente do painel (ver template/BRIEF_PAINEL.md):
        {"eventos": [{"palavra": "fora", "nth": 0, "off": 1, "file": "mixkit:2364", "gain": -8, "note": "tampa da lixeira bate"},
                     {"local": 23, "file": "door_shut", "gain": -8, "note": "..."}]}
  - timeline.ts: entrada de cada painel (top: swoosh, cover: whoosh de ar, overlay: pop) e PUNCH (golpe seco >= 1,2 -> zoom_impact);
  - captions.ts: slam (zoom_impact), behind (whoosh_fast), ghost (glitch_break), knock (2 batimentos + impacto grave + linha reta).
Regras: nada sem `note` (gatilho visível); camadas no mesmo quadro contam 1; densidade-alvo <= 0,95 por segundo (corta primeiro as
entradas de painel colado no anterior). Sem --sobrescrever, se audio/sfx.json existir grava audio/sfx_rascunho.json.
Zero token: o Claude só revisa o resultado (e o usuário, depois, pelo revisar_sfx.py).
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import json
import re
import sys
import unicodedata

from _cfg import EDIT, MOTION, cfg
from janelas_behind import cues

FPS = cfg().get("fps", 30)
words = json.loads((MOTION / "public" / "words.json").read_text(encoding="utf-8"))
tl = (MOTION / "src" / "timeline.ts").read_text(encoding="utf-8")
total = json.loads((MOTION / "public" / "cuts.json").read_text(encoding="utf-8"))["total"]
paineis = [(m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)) for m in
           re.finditer(r'^\s*\{\s*id:\s*"(\w+)",\s*from:\s*(\d+),\s*to:\s*(\d+),\s*kind:\s*"(\w+)"', tl, re.M)]
punch_blk = tl[tl.index("PUNCH"):] if "PUNCH" in tl else ""
punch_blk = punch_blk[: punch_blk.index("];")] if "];" in punch_blk else ""
punch = [(int(a), float(b), int(c), int(d)) for a, b, c, d in re.findall(r"^\s*\[(\d+),\s*([\d.]+),\s*(\d+),\s*(\d+)\]", punch_blk, re.M)]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode())


def quadro_palavra(p: str, nth: int = 0) -> int:
    hits = [w for w in words if norm(w["text"]) == norm(p)]
    if len(hits) <= nth:
        raise SystemExit(f'palavra "{p}" (ocorrência {nth}) não está em words.json')
    return round(hits[nth]["start"] * FPS)


ev = []  # (prioridade: 1 painel/legenda/clímax, 2 golpe, 3 entrada de painel)


def add(at, file, gain, note, prio, **kw):
    ev.append({"at": int(at), "file": file, "gain": gain, "note": note, "_p": prio, **kw})


ant_to = -99
for pid, a, b, kind in paineis:
    colado = abs(a - ant_to) <= 1
    if kind == "top":
        add(a + 5, "swoosh_small", -14, f"{pid} entra", 3 if colado else 2, hp=200, pan=[0.4, -0.2])
    elif kind == "cover":
        add(a + 4, "whoosh_air", -12, f"{pid} tela cheia entra", 2, max=1.6, hp=120, pan=[-0.4, 0.4])
    else:
        add(a + 2, "pop_whoosh", -12, f"{pid} entra", 2, hp=200)
    ant_to = b
    side = MOTION / "src" / "panels" / f"{pid}.sfx.json"
    if side.exists():
        for e in json.loads(side.read_text(encoding="utf-8")).get("eventos", []):
            at = (quadro_palavra(e["palavra"], e.get("nth", 0)) + e.get("off", 0)) if "palavra" in e else a + int(e["local"])
            extra = {k: v for k, v in e.items() if k not in ("palavra", "nth", "off", "local", "file", "gain", "note")}
            add(at, e["file"], e.get("gain", -12), f"{pid} {e.get('note', '')}".strip(), 1, **extra)

def txt(t):
    return re.sub(r"\s+", " ", re.sub(r"[|*#^]", " ", t)).strip().upper()


for c in cues():
    s = c["start"]
    if c["mode"] == "slam":
        add(s, "zoom_impact", -6, f"slam {txt(c['text'])}", 1, max=1.0)
    elif c["mode"] == "behind" and c["ghost"]:
        add(s, "glitch_break", -9, f"fantasma {txt(c['text'])}", 1, max=0.7, hp=120)
    elif c["mode"] == "behind":
        add(s, "whoosh_fast", -10, f"{txt(c['text'])} sobe atrás", 1, max=1.2, hp=150, pan=[-0.5, 0.4])
    elif c["mode"] == "knock":
        l1 = [p["quadro"] for p in c["palavras"] if p["linha"] == 1] or [s + 18]
        hit = l1[0]
        add(min(s + 2, hit - 12), "heartbeat", -9, "knock: batimento 1", 1, max=0.6, rajada_ok=True)
        add(min(s + 10, hit - 4), "heartbeat", -10.5, "knock: batimento 2", 1, max=0.6, rajada_ok=True)
        add(hit, "impact_deep", -8, "knock: linha grande pousa", 1, max=2.2, rajada_ok=True)
        add(hit, "flatline", -8, "knock: linha reta", 1, rajada_ok=True)

for f, pico, _, ataque in punch:
    if ataque == 0 and pico >= 1.2 and not any(abs(e["at"] - f) <= 6 and e["_p"] == 1 for e in ev):
        add(f, "zoom_impact", -7, f"golpe de zoom (quadro {f})", 2, max=1.0, rajada_ok=any(c["mode"] == "knock" and abs(c["start"] - f) < 60 for c in cues()))

ev.sort(key=lambda e: (e["at"], e["_p"]))
limpo = []
for e in ev:
    if any(x["file"] == e["file"] and abs(x["at"] - e["at"]) <= 4 for x in limpo):
        continue
    limpo.append(e)
dur = total / FPS
while len({e["at"] for e in limpo}) / dur > 0.95:
    pior = max((e for e in limpo if e["_p"] > 1), key=lambda e: (e["_p"], e["at"]), default=None)
    if not pior:
        break
    limpo.remove(pior)
for i, e in enumerate(limpo, 1):
    e["n"] = i
    e.pop("_p")
destino = EDIT / "audio" / ("sfx.json" if "--sobrescrever" in sys.argv or not (EDIT / "audio" / "sfx.json").exists() else "sfx_rascunho.json")
destino.parent.mkdir(exist_ok=True)
destino.write_text(json.dumps({"_doc": "at = quadro do evento visível (pico do som nesse quadro); file = catálogo ou mixkit:<id>; n = número na revisão",
                               "events": limpo}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(limpo)} eventos ({len({e['at'] for e in limpo}) / dur:.2f}/s) -> {destino}")
for e in limpo:
    print(f"  #{e['n']:<3} {e['at']:>5}  {e['file']:<16} {e['gain']:>6}  {e['note']}")
