"""Efeitos sonoros: buscar no Mixkit inteiro (não só no catálogo), promover ao catálogo e ajustar o sfx.json pelo número do evento.

Uso:
    python sfx.py buscar "tampa de lixeira batendo" [--n 10]   # catálogo local + índice do Mixkit (busca em português, traduz termos)
    python sfx.py catalogar mixkit:1489 woosh_ar "vento curto, passagem de tela"   # baixa, mede e acrescenta ao CATALOGO.md
    (de dentro de edit/, depois do revisar_sfx.py, com os números que o usuário viu no vídeo de revisão:)
    python sfx.py trocar 12 b            # alternativa b da página de revisão (ou: trocar 12 mixkit:2364 / trocar 12 door_shut)
    python sfx.py remover 20
    python sfx.py ganho 33 -3            # dB relativos
    python sfx.py mover 7 -4             # quadros relativos
No sfx.json, `file` aceita nome do catálogo ou "mixkit:<id>" (o mix.py baixa na hora). Índice do Mixkit: indexar_sfx.py.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas)
import json
import re
import sys
import unicodedata

from _cfg import CACHE_LIB, EDIT, LIB

SFX = LIB / "sfx"
IDX = SFX / "indice_mixkit.json"

PT_EN = {
    "porta": "door", "fechar": "close shut slam", "fecha": "close shut slam", "batendo": "slam hit knock", "bater": "hit knock slam",
    "abrir": "open", "gaveta": "drawer", "armario": "cabinet locker", "lixeira": "trash bin can", "lixo": "trash garbage", "tampa": "lid",
    "papel": "paper", "folha": "paper page", "amassar": "crumple paper", "rasgar": "tear rip paper",
    # o Mixkit não tem impressora nem carimbo: cair no parente mais próximo (máquina de escrever, batida seca de mesa)
    "impressora": "printer print typewriter typing", "imprimir": "printer print typewriter typing", "cupom": "receipt typewriter cash register",
    "nota": "receipt cash", "carimbo": "stamp thud punch desk hit", "dinheiro": "money cash coins",
    "moeda": "coin coins", "caixa": "cash register box", "registradora": "cash register", "compra": "purchase cash register",
    "teclado": "keyboard typing", "digitar": "typing keyboard", "maquina": "typewriter machine", "escrever": "typewriter writing pencil",
    "caneta": "pen pencil writing", "lapis": "pencil", "mouse": "mouse click", "clique": "click", "click": "click", "botao": "button click",
    "toque": "tap click touch", "notificacao": "notification", "mensagem": "message notification", "alerta": "alert alarm warning",
    "alarme": "alarm", "erro": "error glitch fail", "falha": "fail error", "sucesso": "success win correct", "acerto": "correct success",
    "check": "check correct", "certo": "correct check", "errado": "wrong error", "vitoria": "win victory", "conquista": "achievement win",
    "premio": "reward win bonus", "sino": "bell chime", "campainha": "bell doorbell", "relogio": "clock tick", "tique": "tick clock",
    "cronometro": "stopwatch timer tick", "contagem": "countdown tick", "coracao": "heartbeat heart", "batimento": "heartbeat",
    "monitor": "monitor beep hospital", "bip": "beep", "vidro": "glass", "quebrar": "break shatter crash", "quebra": "break shatter",
    "explosao": "explosion boom", "impacto": "impact hit", "pancada": "punch hit", "soco": "punch", "golpe": "hit punch impact",
    "grave": "bass boom low", "trovao": "thunder", "vento": "wind whoosh air", "passagem": "whoosh swoosh transition", "transicao": "transition whoosh",
    "zoom": "zoom whoosh", "voar": "whoosh fly", "rapido": "fast quick", "subir": "rise riser up", "subida": "rise riser", "descer": "down fall drop",
    "queda": "fall drop", "cair": "fall drop", "pop": "pop bubble", "bolha": "bubble pop", "estalo": "snap click pop", "estalar": "snap finger",
    "dedo": "finger snap", "aplauso": "applause clap", "palmas": "applause clap", "risada": "laugh laughter", "multidao": "crowd",
    "plateia": "audience crowd applause", "escritorio": "office", "reuniao": "office meeting", "cadeira": "chair", "mesa": "table desk",
    "passos": "footsteps steps", "andar": "footsteps walk", "carro": "car", "caminhao": "truck", "motor": "engine motor", "buzina": "horn",
    "freio": "brake", "empilhadeira": "forklift", "armazem": "warehouse", "caixa de papelao": "cardboard box", "fita": "tape",
    "camera": "camera shutter photo", "foto": "camera shutter photo", "telefone": "phone ring", "celular": "phone notification",
    "vibrar": "vibration phone", "mola": "spring boing", "cartoon": "cartoon", "magia": "magic sparkle shimmer", "brilho": "sparkle shimmer shine",
    "estrela": "sparkle star", "suspense": "suspense tension", "tensao": "tension suspense", "terror": "horror scary", "misterio": "mystery",
    "drone": "drone ambience", "ambiente": "ambience room", "silencio": "silence room tone", "agua": "water splash", "gota": "drop water",
    "fogo": "fire", "espada": "sword metal", "metal": "metal clang", "corrente": "chain metal", "cadeado": "lock padlock", "chave": "key keys",
    "trancar": "lock", "destrancar": "unlock", "reverso": "reverse", "glitch": "glitch", "digital": "digital electronic", "robo": "robot",
    "laser": "laser", "game": "game arcade", "moeda de jogo": "arcade coin", "nivel": "level up", "subir de nivel": "level up",
    "virar": "flip page", "pagina": "page flip book", "livro": "book page", "carta": "letter envelope paper", "envelope": "envelope paper",
}


def norm(s: str) -> str:
    return unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()


def termos(q: str) -> set:
    q = norm(q)
    out = set(re.findall(r"[a-z0-9]+", q))
    for k, v in PT_EN.items():
        if k in q:
            out |= set(v.split())
    return {t for t in out if len(t) > 2 and t not in ("que", "com", "pra", "para", "uma", "dos", "das", "the")}


def catalogo() -> list:
    rows = []
    for ln in (SFX / "CATALOGO.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*`([\w-]+)`\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|", ln)
        if m:
            rows.append({"nome": m.group(1), "id": m.group(2).strip(), "dur": m.group(3).strip(), "uso": m.group(5).strip()})
    return rows


PARE = {"que", "com", "pra", "para", "uma", "dos", "das", "the", "and", "som", "efeito", "quando", "sobre", "entra", "painel"}


def conceitos(q: str) -> list:
    """cada palavra da busca vira um conceito = {palavra} ∪ traduções; um item pontua 1 vez por conceito (sinônimo não soma)"""
    qn = norm(q)
    out = []
    for w in re.findall(r"[a-z0-9]+", qn):
        if len(w) <= 2 or w in PARE:
            continue
        c = {w} | set(PT_EN.get(w, "").split())
        for k, v in PT_EN.items():  # prefixo: "fechando" -> "fechar"/"fecha"
            if " " not in k and len(k) >= 4 and (w.startswith(k[:-1]) or k.startswith(w[:-1])):
                c |= set(v.split())
        out.append(c)
    for k, v in PT_EN.items():
        if " " in k and k in qn:
            out.append(set(v.split()))
    return out


def pontua(cs: list, titulo: set, tags: set) -> float:
    return sum(2.0 if c & titulo else (1.2 if c & tags else 0.0) for c in cs)


def buscar(q: str, n: int = 10, excluir: set | None = None) -> list:
    """[(score, ref, título, tags, dur)] ref = nome do catálogo ou mixkit:<id>"""
    excluir = excluir or set()
    cs = conceitos(q)
    res = []
    for r in catalogo():
        if r["nome"] in excluir:
            continue
        txt = set(re.findall(r"[a-z0-9]+", norm(r["nome"].replace("_", " ") + " " + r["uso"])))
        txt |= {e for t in list(txt) for e in PT_EN.get(t, "").split()}
        sc = pontua(cs, txt, set()) * 1.15  # catálogo = sons já aprovados: leve preferência no empate
        if sc:
            res.append((sc + 0.2, r["nome"], r["uso"][:50], "catálogo", r["dur"]))
    if IDX.exists():
        for i, it in json.loads(IDX.read_text(encoding="utf-8")).items():
            ref = f"mixkit:{i}"
            if ref in excluir:
                continue
            tw = set(re.findall(r"[a-z0-9]+", norm(it["titulo"])))
            tg = {t for tag in it.get("tags", []) for t in re.findall(r"[a-z0-9]+", norm(tag))}
            sc = pontua(cs, tw, tg)
            if sc:
                res.append((sc, ref, it["titulo"], ", ".join(it.get("tags", [])[:4]), it.get("dur") or ""))
    res.sort(key=lambda x: (-x[0], len(str(x[2]))))
    return res[:n]


def evento(n: int):
    p = EDIT / "audio" / "sfx.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    for e in d["events"]:
        if e.get("n") == n:
            return p, d, e
    raise SystemExit(f"evento #{n} não existe (rode revisar_sfx.py para numerar)")


def catalogar(ref: str, nome: str, uso: str) -> None:
    import shutil
    import numpy as np
    import librosa
    from mixkit import baixar, url_sfx
    i = ref.split(":", 1)[1]
    src = baixar(url_sfx(i), CACHE_LIB / "sfx" / f"{i}.mp3")
    dst = SFX / f"{nome}.mp3"
    shutil.copy2(src, dst)
    y, sr = librosa.load(str(dst), sr=48000, mono=True)
    sm = np.convolve(np.abs(y), np.ones(240) / 240, mode="same")
    br = lambda x: f"{x:.2f}".replace(".", ",")
    linha = f"| `{nome}` | {i} | {br(len(y) / sr)} s | {br(np.argmax(sm) / sr)} | {uso} |"
    cat = (SFX / "CATALOGO.md").read_text(encoding="utf-8").rstrip("\n").split("\n")
    pos = max(k for k, ln in enumerate(cat) if ln.startswith("| `")) + 1
    cat.insert(pos, linha)
    (SFX / "CATALOGO.md").write_text("\n".join(cat) + "\n", encoding="utf-8")
    print("catalogado:", linha)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "buscar":
        n = int(a[a.index("--n") + 1]) if "--n" in a else 10
        for sc, ref, tit, tags, dur in buscar(a[1], n):
            print(f"{ref:<16} {str(tit)[:44]:<44} [{tags}] {dur}")
    elif a[0] == "catalogar":
        catalogar(a[1], a[2], a[3] if len(a) > 3 else "")
    elif a[0] in ("trocar", "remover", "ganho", "mover"):
        p, d, e = evento(int(a[1]))
        if a[0] == "trocar":
            novo = a[2]
            if len(novo) == 1:
                alt = json.loads((EDIT / "revisao" / "alternativas.json").read_text(encoding="utf-8"))
                novo = alt[str(e["n"])][novo]
            print(f"#{e['n']}: {e['file']} -> {novo}")
            e["file"] = novo
            e.pop("max", None)  # o corte de cauda era do som antigo; o mix aplica fade padrão
        elif a[0] == "remover":
            d["events"] = [x for x in d["events"] if x is not e]
            print(f"#{e['n']} removido ({e['file']}, {e.get('note')})")
        elif a[0] == "ganho":
            e["gain"] = round(e["gain"] + float(a[2]), 1)
            print(f"#{e['n']}: ganho {e['gain']} dB")
        else:
            e["at"] = int(e["at"] + int(a[2]))
            print(f"#{e['n']}: quadro {e['at']}")
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        print(__doc__)
