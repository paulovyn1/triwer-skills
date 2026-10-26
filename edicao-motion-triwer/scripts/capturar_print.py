"""Print de página pública (matéria, artigo, post aberto) com o Chrome headless, sem login e sem extensão.

    python capturar_print.py "<url>" <saida.png> [--largura 1080] [--altura 1600] [--espera 9000] [--escala 1]

- --escala 2 deixa o texto nítido para recortar trecho e dar zoom no vídeo.
- Sites com bloqueio de robô (alguns paywalls, redes sociais) voltam vazios ou com aviso: abrir a folha antes de usar. Nesse caso,
  usar outra fonte da mesma notícia ou o modo leitura (`https://r.jina.ai/<url>` dá o texto puro, para recriar o recorte com o
  texto exato, nome do veículo e data).
- Pessoa comum (não pública) que aparecer: borrar nome e foto antes de usar no vídeo.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


def chrome() -> str:
    cands = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        shutil.which("google-chrome") or "",
        shutil.which("chromium") or "",
        shutil.which("chrome") or "",
    ]
    for c in cands:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome não encontrado")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("saida", type=Path)
    ap.add_argument("--largura", type=int, default=1080)
    ap.add_argument("--altura", type=int, default=1600)
    ap.add_argument("--espera", type=int, default=9000, help="ms de tempo virtual para a página carregar")
    ap.add_argument("--escala", type=float, default=1.0)
    a = ap.parse_args()
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as perfil:
        cmd = [chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={perfil}", f"--user-agent={UA}",
               f"--window-size={a.largura},{a.altura}", f"--virtual-time-budget={a.espera}", f"--force-device-scale-factor={a.escala}",
               "--lang=pt-BR", f"--screenshot={a.saida.resolve()}", a.url]
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            p.wait(timeout=70)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
            else:
                p.kill()
            print("aviso: a página não terminou de carregar em 70 s (print pode estar incompleto)")
    ok = a.saida.exists() and a.saida.stat().st_size > 5000
    print(a.saida, f"{a.saida.stat().st_size / 1e3:.0f} kB" if a.saida.exists() else "NÃO GERADO", "" if ok else "(conferir: pode estar vazio/bloqueado)")


if __name__ == "__main__":
    main()
