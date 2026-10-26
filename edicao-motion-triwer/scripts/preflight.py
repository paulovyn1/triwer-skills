"""Checagem de ambiente em 1 comando. Imprime OK/FALTA com a correção exata. Rodar uma vez por sessão, antes de tudo.

    python preflight.py          (qualquer Python)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dados import DADOS, ambiente  # noqa: E402

HOME = Path.home()
AMB = ambiente()
TOOLS = HOME / "Developer" / "video-tools"
VUSE = HOME / "Developer" / "video-use"
PY = Path(AMB.get("venv_python") or TOOLS / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
ok = True


def say(good, msg, fix=""):
    global ok
    ok &= good
    print(("OK    " if good else "FALTA ") + msg + (f"\n        -> {fix}" if not good and fix else ""))


for exe in ("ffmpeg", "ffprobe", "node", "npm", "uv"):
    say(shutil.which(exe) is not None, exe, {"ffmpeg": "winget install Gyan.FFmpeg", "ffprobe": "vem com o ffmpeg",
        "node": "instalar Node 20+ (nodejs.org)", "npm": "vem com o Node", "uv": "pip install uv"}[exe])
if shutil.which("node"):
    v = subprocess.run(["node", "-v"], capture_output=True, text=True).stdout.strip()
    say(int(v.lstrip("v").split(".")[0]) >= 20, f"node {v} (precisa >= 20)")
say(PY.exists(), f"venv de ferramentas {TOOLS}",
    f'mkdir -p "{TOOLS}" && cd "{TOOLS}" && uv init --python 3.12 --no-readme --name video-tools . && '
    "uv add onnxruntime opencv-python-headless numpy soundfile noisereduce scipy librosa pyloudnorm")
if PY.exists():
    r = subprocess.run([str(PY), "-c", "import librosa,onnxruntime,cv2,soundfile,scipy,pyloudnorm"], capture_output=True, text=True)
    say(r.returncode == 0, "librosa/onnxruntime/cv2/soundfile/scipy/pyloudnorm no venv", f'cd "{TOOLS}" && uv add librosa onnxruntime opencv-python-headless soundfile scipy pyloudnorm')
say(bool(os.environ.get("GROQ_API_KEY")), "GROQ_API_KEY no ambiente (transcrição)", "setar a variável de usuário GROQ_API_KEY (console.groq.com)")
say(VUSE.exists(), f"video-use em {VUSE} (timeline_view.py = forma de onda)", f'git clone https://github.com/browser-use/video-use "{VUSE}" && cd "{VUSE}" && uv sync --python 3.12')
say(shutil.which("yt-dlp") is not None, "yt-dlp (trechos de vídeo do YouTube: baixar_trecho.py)", "pip install -U yt-dlp")
say((DADOS / "preferencias.md").exists(), f"pasta de dados do usuário {DADOS}", "python preferencias.py iniciar --nome \"<nome>\"")
tmp = Path(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp")
livre = shutil.disk_usage(tmp.anchor or "/").free / 1e9
say(livre > 3 or bool(AMB.get("temp_render")), f"disco do TEMP ({tmp.anchor}) com {livre:.1f} GB livres",
    "renders do Remotion copiam public/ para o TEMP: apontar temp_render no ambiente.json para um disco com espaço")
print("\nLembrete: PYTHONUTF8=1 em todo comando Python; TEMP/TMP com espaço nos renders do Remotion; scripts rodam de dentro de edit/.")
sys.exit(0 if ok else 1)
