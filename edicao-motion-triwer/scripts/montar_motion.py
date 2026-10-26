"""Monta (ou completa) o projeto Remotion do vídeo em UM comando, sem sobrescrever o que já foi gerado.

Uso (de dentro de edit/):
    python montar_motion.py [--kit "<pasta do kit do cliente>"] [--paineis P05,P10:paineis-c3/P12-x.tsx] [--novos P14,P15,P16:overlay] [--sem-npm]

1. copia template/remotion -> edit/motion (só arquivos que ainda não existem: words.json, cuts.json, captions.ts, timeline.ts,
   painéis e tudo que você editou ficam intactos; pode rodar de novo à vontade)
2. copia work/base.mp4 e work/voz_limpa.wav para motion/public (de novo quando mudarem; extract_base/limpar_voz também fazem isso)
3. --kit: assets/theme.tsx -> src/theme.tsx, assets/fotos -> public/img, assets/logos -> public/logos; grava o caminho em projeto.json -> kit
4. --paineis: cada item Pnn busca Pnn*.tsx em kit/paineis-*/ (a pasta mais nova ganha); "Pnn:pasta/arquivo.tsx" força um arquivo
5. --novos: cria o STUB de cada painel inédito (Pnn[:top|cover|overlay]) para o timeline.ts compilar enquanto os subagentes trabalham
   em paralelo (cada um substitui só o seu arquivo)
6. npm install (TEMP/TMP num disco com espaço) se node_modules não existir
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import os
import shutil
import subprocess
import sys
from pathlib import Path

from _cfg import EDIT, SKILL, cfg, salvar_cfg, sync_public

TEMPLATE = SKILL / "template" / "remotion"
MOTION = EDIT / "motion"


def arg(nome, default=None):
    for i, a in enumerate(sys.argv):
        if a == nome and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def copiar_sem_sobrescrever(src: Path, dst: Path) -> int:
    n = 0
    for f in src.rglob("*"):
        if f.is_dir() or "node_modules" in f.parts or "__pycache__" in f.parts:
            continue
        alvo = dst / f.relative_to(src)
        if alvo.exists():
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, alvo)
        n += 1
    return n


n = copiar_sem_sobrescrever(TEMPLATE, MOTION)
print(f"template: {n} arquivo(s) novo(s) em {MOTION}")
(MOTION / "public").mkdir(exist_ok=True)
sync_public()
pub = MOTION / "public"

kit = arg("--kit")
if kit:
    kit = Path(kit).resolve()
    try:
        c = cfg()
        if c.get("kit") != str(kit):
            c["kit"] = str(kit)
            salvar_cfg(c)
    except SystemExit:
        pass
    tema = kit / "assets" / "theme.tsx"
    if tema.exists():
        shutil.copy2(tema, MOTION / "src" / "theme.tsx")
        print("tema do cliente:", tema)
    for sub, dest in (("fotos", "img"), ("logos", "logos")):
        d = kit / "assets" / sub
        if d.exists():
            (pub / dest).mkdir(exist_ok=True)
            for f in d.iterdir():
                if f.is_file() and not (pub / dest / f.name).exists():
                    shutil.copy2(f, pub / dest / f.name)
    for item in [p for p in arg("--paineis", "").split(",") if p]:
        pid, _, rel = item.partition(":")
        if rel:
            origem = kit / rel
        else:
            achados = sorted(kit.glob(f"paineis-*/{pid}*.tsx"), key=lambda p: p.parent.stat().st_mtime)
            origem = achados[-1] if achados else None
        if not origem or not origem.exists():
            print(f"AVISO: painel {pid} não encontrado no kit")
            continue
        (MOTION / "src" / "panels").mkdir(parents=True, exist_ok=True)
        destino = MOTION / "src" / "panels" / f"{pid}.tsx"
        if destino.exists():
            print(f"painel {pid}: já existe, mantido")
            continue
        shutil.copy2(origem, destino)
        print(f"painel {pid} <- {origem.relative_to(kit)}")

for item in [p for p in arg("--novos", "").split(",") if p]:
    pid, _, tipo = item.partition(":")
    destino = MOTION / "src" / "panels" / f"{pid}.tsx"
    if destino.exists():
        continue
    destino.parent.mkdir(parents=True, exist_ok=True)
    corpo = "<></>" if tipo == "overlay" else "<PanelBg />"
    imp = "" if tipo == "overlay" else 'import { PanelBg } from "../theme";\n'
    destino.write_text(f"// STUB: o subagente do painel substitui este arquivo inteiro (template/BRIEF_PAINEL.md)\nimport React from \"react\";\n{imp}"
                       f"export const {pid}: React.FC = () => {corpo};\n", encoding="utf-8")
    print(f"stub {pid} ({tipo or 'top'})")

if "--sem-npm" not in sys.argv and not (MOTION / "node_modules").exists():
    tmp = EDIT / "_tmp"
    tmp.mkdir(exist_ok=True)
    print("npm install (≈ 2 min)...")
    subprocess.run("npm install --no-audit --no-fund", cwd=MOTION, shell=True, check=True,
                   env={**os.environ, "TEMP": str(tmp), "TMP": str(tmp)})
print("projeto Remotion pronto em", MOTION)
