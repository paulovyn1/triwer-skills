"""Entrega em UM comando: render (opcional) + muxagem + checagens + folha de amostra + revisão de efeitos + registro da música + limpeza.

Uso (de dentro de edit/):
    python entregar.py <A|B|C|all> "<nome base>" [--render] [--sem-revisao] [--manter-tmp]
      --render       roda o `remotion render` antes (≈ 5 min, CPU; chame em segundo plano: run_in_background)
Entrada:  work/video_full.mp4 (render sem áudio) + motion/public/mix_<opção>.wav (mix.py)
Saída:    ../entrega/<nome base> - trilha <opção>.mp4 (AAC 320k, faststart, SEM -shortest: ele comia 2 quadros) e um relatório:
          quadros (== total de cuts.json), loudness e pico, auditoria de quadros parados/saltos (verificar.py final),
          verify/final_sheet.png (12 quadros do arquivo final: 1 leitura de imagem) e, por padrão, o vídeo de efeitos numerados +
          a página de escuta (revisar_sfx.py). Registra as faixas entregues em ~/.claude/edicao-motion-triwer/musicas_usadas.json
          (o escolher_musica.py evita repetir música para o mesmo cliente) e apaga edit/_tmp (passava de 9 GB).
"""
import _cfg  # noqa: F401  (reexecuta no venv de ferramentas; precisa vir ANTES de librosa/cv2/numpy)
import datetime
import json
import os
import shutil
import subprocess
import sys

from _cfg import EDIT, MOTION, WORK, cfg, sync_public
from registro import registrar_musicas

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opcoes, nome = args[0], args[1]
opts = ["A", "B", "C"] if opcoes.lower() == "all" else [opcoes.upper()]
opts = [o for o in opts if (MOTION / "public" / f"mix_{o}.wav").exists()] or opts
out_dir = EDIT.parent / "entrega"
out_dir.mkdir(exist_ok=True)
video = WORK / "video_full.mp4"
total = json.loads((MOTION / "public" / "cuts.json").read_text(encoding="utf-8"))["total"]
sync_public()
tmp = EDIT / "_tmp"

if "--render" in sys.argv or not video.exists():
    tmp.mkdir(exist_ok=True)
    env = {**os.environ, "TEMP": str(tmp), "TMP": str(tmp)}
    print("renderizando (≈ 5 min)...", flush=True)
    subprocess.run("npx remotion render Criativo ../work/video_full.mp4 --muted --codec=h264 --crf=16 --x264-preset=slow",
                   cwd=MOTION, shell=True, check=True, env=env)


def frames(path) -> int:
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip().strip(",")
    return int(r)


ok = frames(video) == total
print(f"render: {frames(video)} quadros (esperado {total}) {'ok' if ok else 'DIFERENTE: não entregar'}")
finais = []
for o in opts:
    out = out_dir / f"{nome} - trilha {o}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(MOTION / "public" / f"mix_{o}.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
                    "-movflags", "+faststart", str(out)], check=True)
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore").stderr
    lin = [ln.strip() for ln in m.splitlines() if ln.strip().startswith(("I:", "Peak:"))][-2:]
    n = frames(out)
    print(f"{out.name}: {n} quadros {'ok' if n == total else 'DIFERENTE'} | {lin}")
    finais.append(out)

amostra = EDIT / "verify" / "final"
amostra.mkdir(parents=True, exist_ok=True)
imgs = []
for k in range(12):
    f = int((k + 0.5) * total / 12)
    p = amostra / f"m{f:04d}.png"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{f / 30:.3f}", "-i", str(finais[0]), "-frames:v", "1",
                    "-vf", "scale=270:-1", str(p)], check=True)
    imgs.append(str(p))
here = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(here, "contact.py"), str(EDIT / "verify" / "final_sheet.png"), "4", "270", *imgs], check=True)
print("amostra do arquivo final:", EDIT / "verify" / "final_sheet.png")
subprocess.run([sys.executable, os.path.join(here, "verificar.py"), "final", str(video)], check=False)

c = cfg()
for o in opts:
    registrar_musicas(c, o, datetime.date.today().isoformat())
if "--sem-revisao" not in sys.argv and (EDIT / "audio" / "sfx.json").exists():
    subprocess.run([sys.executable, os.path.join(here, "revisar_sfx.py"), str(finais[0])], check=False)
if ok and "--manter-tmp" not in sys.argv and tmp.exists():
    shutil.rmtree(tmp, ignore_errors=True)
    print("limpo: edit/_tmp")
