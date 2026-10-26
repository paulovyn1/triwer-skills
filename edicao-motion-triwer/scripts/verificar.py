"""Verificação visual e técnica em UM comando.

Uso (de dentro de edit/):
    python verificar.py lint                              # regras de legibilidade do roteiro (sem render, instantâneo)
    python verificar.py stills [--escala 0.3]             # quadros de pouso escolhidos sozinho, 1 lote, folhas de contato
    python verificar.py stills --quadros 222,271,615      # só esses quadros (rodada de correção), 1 folha
    python verificar.py final [video.mp4] [--offset=N]    # quadros parados (recorte/painel) e saltos secos; sem caminho = .mp4 mais novo de ../entrega

`stills` escolhe: 1º e último quadro; de cada painel 2 quadros (35% e fim-8); de cada slam/stack/knock o quadro start+8; de cada
behind o início+12 e o fim-4 (pior caso de zoom). Folhas de 12 quadros (4 colunas): LEIA SÓ AS FOLHAS (verify/sheet_N.png),
ou passe as folhas para um subagente Sonnet de QA (references/paineis.md) e leia só a lista de defeitos.
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import os
import re
import subprocess
import sys
from pathlib import Path

from _cfg import EDIT, sync_public
from janelas_behind import cues

MOTION = EDIT / "motion"
HERE = Path(__file__).resolve().parent
# larguras aproximadas (Outfit 900 maiúsculo ≈ 0,62 em por letra) dos modos da legenda; área útil ≈ 980 px
LARG = {"slam0": 84 * 3.1, "stack": 108, "stack_serif": 108 * 2.3 * 0.75, "build": 84}


def painéis():
    src = (MOTION / "src" / "timeline.ts").read_text(encoding="utf-8")
    return [(m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)) for m in
            re.finditer(r'\{\s*id:\s*"(\w+)",\s*from:\s*(\d+),\s*to:\s*(\d+),\s*kind:\s*"(\w+)"', src)]


def largura(linha: str, base: float, serif: float | None = None) -> float:
    tot = 0.0
    for tok in linha.split():
        letras = len(re.sub(r"[^\wÀ-ú]", "", tok))
        tot += letras * 0.62 * (serif if (serif and tok.startswith("*")) else base) + 0.26 * base
    return tot


def lint() -> int:
    avisos = []
    for c in cues():
        linhas = [l.strip() for l in c["text"].split("|")]
        limpas = [re.sub(r"[*#^.,]", "", l).strip() for l in linhas]
        palavras = [t for t in c["text"].replace("|", " ").split() if t]
        if c["mode"] == "behind" and not c["ghost"]:
            if len(limpas) == 1 and len(limpas[0]) <= 10:
                avisos.append(f'behind "{c["text"]}" (quadro {c["start"]}): 1 linha com ≤ 10 letras fica coberta pela cabeça ("NÃ▮ ▮XISTE"); '
                              f'use 2 linhas com " | " (texto acima da cabeça) ou slam')
            for l in limpas:
                if len(l) > 11:
                    avisos.append(f'behind "{l}" (quadro {c["start"]}): linha com {len(l)} letras estoura a tela com zoom; quebre com " | " (ideal ≤ 9)')
        if c["mode"] == "knock" and len(linhas) < 3:
            avisos.append(f'knock "{c["text"]}": use "cabeçalho | linha grande | linha grande" (1 fileira por linha)')
        if c["mode"] == "slam":
            if len(palavras) > 4:
                avisos.append(f'slam "{c["text"]}": {len(palavras)} palavras perde impacto (ideal ≤ 3)')
            w0 = largura(linhas[0], LARG["slam0"])
            if w0 > 980:
                avisos.append(f'slam "{c["text"]}" (quadro {c["start"]}): 1ª linha com ≈ {w0:.0f} px (gigante, 3,1×) estoura 980 px; '
                              f'use palavra de até ~5 letras na 1ª linha ou troque por stack com #faixa')
        if c["mode"] == "stack":
            for l in linhas:
                w = largura(l, LARG["stack"], LARG["stack_serif"])
                if w > 980:
                    avisos.append(f'stack "{l}" (quadro {c["start"]}): ≈ {w:.0f} px estoura 980 px; quebre a linha ou tire o serif (*)')
        if c["mode"] == "build" and len(palavras) > 5:
            avisos.append(f'build "{c["text"]}" (quadro {c["start"]}): cue longo; quebre em 2-3 palavras')
    modos = [c["mode"] for c in cues()]
    if modos.count("knock") > 1:
        avisos.append("mais de 1 knock: perde força (usar no clímax emocional uma vez)")
    if modos.count("behind") > 4:
        avisos.append("mais de 4 behind: cansa")
    for a in avisos:
        print("AVISO:", a)
    if not avisos:
        print("lint do roteiro: ok")
    return len(avisos)


def render_stills(frames: list, escala: str, out: Path, comp: str = "Criativo") -> None:
    out.mkdir(parents=True, exist_ok=True)
    tmp = EDIT / "_tmp"
    tmp.mkdir(exist_ok=True)
    env = {**os.environ, "TEMP": str(tmp), "TMP": str(tmp)}
    args = ["node", "stills.mjs", str(out), escala] + (["--comp", comp] if comp != "Criativo" else []) + [str(f) for f in frames]
    subprocess.run(args, cwd=MOTION, check=True, env=env)


def folhas(frames: list, pasta: Path, prefixo: str) -> list:
    saida = []
    for i in range(0, len(frames), 12):
        lote = frames[i:i + 12]
        sheet = EDIT / "verify" / f"{prefixo}_{i // 12 + 1}.png"
        subprocess.run([sys.executable, str(HERE / "contact.py"), str(sheet), "4", "270", *[str(pasta / f"m{f:04d}.png") for f in lote]], check=True)
        saida.append(sheet)
    return saida


def stills(escala: str, quadros: list | None) -> None:
    sync_public()
    total = int(re.search(r'"total":\s*(\d+)', (MOTION / "public" / "cuts.json").read_text(encoding="utf-8")).group(1))
    if quadros:
        frames = sorted(f for f in quadros if 0 <= f < total)
        pasta, prefixo = EDIT / "verify" / "pontual", "sheet_pontual"
    else:
        fr = {3, total - 3}
        for _, a, b, kind in painéis():
            if kind == "overlay":
                fr.add(a + 28)
            else:
                fr.add(a + round((b - a) * 0.35))
                fr.add(b - 8)
        for c in cues():
            if c["mode"] in ("slam", "stack", "knock"):
                fr.add(c["start"] + 8)
            if c["mode"] == "behind":
                fr.add(c["start"] + 12)
                fr.add((c["hold"] or c["end"]) - 4)
        frames = sorted(f for f in fr if 0 <= f < total)
        pasta, prefixo = EDIT / "verify" / "auto", "sheet"
    print(f"{len(frames)} quadros:", frames)
    render_stills(frames, escala, pasta)
    print("folhas:", ", ".join(str(p) for p in folhas(frames, pasta, prefixo)))


def final(video: str | None) -> None:
    if not video:
        cands = sorted((EDIT.parent / "entrega").glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
        cands = [p for p in cands if "efeitos numerados" not in p.name]
        if not cands:
            raise SystemExit("nenhum .mp4 em ../entrega: passe o caminho do vídeo")
        video = str(cands[0])
        print("vídeo:", video)
    extra = [a for a in sys.argv if a.startswith("--offset=")]
    subprocess.run([sys.executable, str(HERE / "congelado.py"), video], check=False)
    subprocess.run([sys.executable, str(HERE / "auditar_movimento.py"), video, *extra], check=False)
    print("Referência (C2): painel com 0% de quadros parados; maior trecho parado ≤ 3; recorte sem sequência parada (o knock em tela preta é normal).")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "lint"
    if modo == "lint":
        sys.exit(1 if lint() else 0)
    elif modo == "stills":
        esc = sys.argv[sys.argv.index("--escala") + 1] if "--escala" in sys.argv else "0.3"
        q = [int(x) for x in sys.argv[sys.argv.index("--quadros") + 1].split(",")] if "--quadros" in sys.argv else None
        if not q:
            lint()
        stills(esc, q)
    elif modo == "final":
        pos = [a for a in sys.argv[2:] if not a.startswith("--")]
        final(pos[0] if pos else None)
    else:
        print(__doc__)
