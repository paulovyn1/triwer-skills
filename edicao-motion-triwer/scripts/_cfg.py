"""Ambiente comum dos scripts. Rodar sempre de DENTRO da pasta edit/ do vídeo (ou definir EDIT_DIR).

    cd "<pasta do vídeo>/edit" && python <skill>/scripts/make_edl.py
"""
import json
import os
import subprocess
import sys
from pathlib import Path

# Um interpretador só: o venv de ferramentas (librosa, onnxruntime, cv2, faster-whisper, requests, PIL...). Qualquer script desta pasta
# se reexecuta nele se for chamado com outro Python (o do sistema não tem as bibliotecas). Desligar: EDICAO_SEM_VENV=1.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dados import DADOS, ambiente  # noqa: E402,F401  (pasta de dados do usuário, fora da skill)

AMB = ambiente()
VENV_PY = Path(AMB.get("venv_python") or Path.home() / "Developer" / "video-tools" / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
if VENV_PY.exists() and not os.environ.get("EDICAO_SEM_VENV") and Path(sys.executable).resolve() != VENV_PY.resolve():
    sys.exit(subprocess.call([str(VENV_PY), *sys.argv], env={**os.environ, "EDICAO_SEM_VENV": "1", "PYTHONUTF8": "1"}))
os.environ.setdefault("PYTHONUTF8", "1")

EDIT = Path(os.environ.get("EDIT_DIR") or Path.cwd()).resolve()
SKILL = Path(__file__).resolve().parent.parent
LIB = SKILL / "biblioteca"
WORK = EDIT / "work"
MOTION = EDIT / "motion"
# áudio baixado (músicas e efeitos do Mixkit) fica fora do repo; o lugar vem do ambiente.json do usuário (disco com espaço)
CACHE_LIB = Path(os.environ.get("EDICAO_CACHE") or AMB.get("cache") or Path.home() / ".cache" / "edicao-motion-triwer")
TEMP_RENDER = AMB.get("temp_render")  # pasta para TEMP/TMP dos renders (Remotion copia public/ para o TEMP)


def cfg() -> dict:
    p = EDIT / "projeto.json"
    if not p.exists():
        raise SystemExit(f"projeto.json não existe em {EDIT}. Rode preparar.py primeiro (ele cria o modelo).")
    return json.loads(p.read_text(encoding="utf-8"))


def salvar_cfg(c: dict) -> None:
    (EDIT / "projeto.json").write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding="utf-8")


def fonte(c: dict | None = None) -> Path:
    c = c or cfg()
    p = Path(c["fonte"])
    if not p.is_absolute():
        p = (EDIT / p).resolve()
    return p


def sync_public(*nomes: str) -> list:
    """Põe work/<nome> em motion/public/ quando o projeto Remotion já existe e a cópia falta ou está velha.
    Chamado por extract_base, limpar_voz, verificar e entregar: a ordem das etapas deixa de importar."""
    import shutil
    pub = MOTION / "public"
    if not pub.exists():
        return []
    feitos = []
    for n in nomes or ("base.mp4", "voz_limpa.wav"):
        s, d = WORK / n, pub / n
        if s.exists() and (not d.exists() or d.stat().st_mtime < s.stat().st_mtime or d.stat().st_size != s.stat().st_size):
            shutil.copy2(s, d)
            feitos.append(n)
    if feitos:
        print("motion/public atualizado:", ", ".join(feitos))
    return feitos


def quadro(x, words: list | None = None, fps: int = 30) -> float:
    """aceita segundos (24.75), "quadro:747" ou "palavra@747" (formato do words_out) -> segundos de saída"""
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if "@" in s:
        return int(s.rsplit("@", 1)[1]) / fps
    if s.startswith("quadro:"):
        return int(s.split(":", 1)[1]) / fps
    return float(s.replace(",", "."))
