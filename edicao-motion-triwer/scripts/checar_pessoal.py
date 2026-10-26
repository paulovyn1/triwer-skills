"""Antes de compartilhar a skill (alunos, outra equipe): procura dado pessoal dentro da pasta da skill.

    python checar_pessoal.py [--termos "Fulano,Marca X"]

Termos = os de <dados>/termos_pessoais.txt (um por linha) + --termos + padrões fixos (e-mail, telefone, caminho de usuário,
chave de API). Varre todos os arquivos de texto da skill (menos bibliotecas geradas). Sai com código 1 se achar algo.
Preferências, estilos próprios, músicas usadas e referências do usuário já moram fora da skill (_dados.py); não precisam sair.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dados import DADOS  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
TEXTO = {".md", ".py", ".ts", ".tsx", ".mjs", ".js", ".json", ".sh", ".txt", ".yml", ".yaml", ".toml"}
IGNORAR = {"node_modules", "__pycache__", ".git"}
GERADOS = {"indice.json", "analise.json", "indice_mixkit.json", "scan_mixkit_40.json", "mixkit_index.txt"}
FIXOS = {
    "e-mail": r"[\w.+-]+@[A-Za-z][\w-]*\.[A-Za-z]{2,}",
    "telefone": r"\b\d{2}\s?9\d{4}-?\d{4}\b|\+55\s?\d{2}",
    "caminho de usuário": r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+|/home/[a-z_][^/\s]*|/Users/[A-Za-z][^/\s]*",
    "chave de API": r"\b(sk|gsk|pk|rk)_[A-Za-z0-9]{16,}",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--termos", default="")
    a = ap.parse_args()
    termos = [t.strip() for t in a.termos.split(",") if t.strip()]
    tp = DADOS / "termos_pessoais.txt"
    if tp.exists():
        termos += [ln.strip() for ln in tp.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    pads = {f"termo '{t}'": rf"(?<![\w]){re.escape(t)}(?![\w])" for t in termos} | FIXOS
    achados = 0
    for p in sorted(SKILL.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in TEXTO or IGNORAR & set(p.parts) or p.name in GERADOS:
            continue
        for n, ln in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for nome, rx in pads.items():
                if re.search(rx, ln, re.I if nome.startswith("termo") else 0):
                    achados += 1
                    print(f"{p.relative_to(SKILL)}:{n}: {nome}: {ln.strip()[:140]}")
    print(f"\n{achados} ocorrência(s); termos verificados: {len(termos)} + padrões fixos")
    if not termos:
        print(f"aviso: nenhum termo pessoal cadastrado ({tp}); só os padrões fixos foram verificados")
    sys.exit(1 if achados else 0)


if __name__ == "__main__":
    main()
