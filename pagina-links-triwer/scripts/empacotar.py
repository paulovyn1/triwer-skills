"""Empacota a página num zip com caminhos em barra normal (abre certo em Windows e Mac).

Uso: python empacotar.py <pasta-do-projeto> <arquivo.zip>

Deixa de fora o que não vai para quem recebe: node_modules, .vercel, .git e
package-lock.json (este último porque, se a instalação foi interrompida, ele fica
incompleto; quem recebe gera um novo no npm install).

Por que não usar o Compress-Archive do Windows: no PowerShell 5.1 ele grava os
caminhos com barra invertida (src\\App.jsx), e no Mac o arquivo vira um nome só,
sem pastas.
"""
import os
import sys
import zipfile

FORA = {"node_modules", ".vercel", ".git"}
ARQUIVOS_FORA = {"package-lock.json"}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    origem, destino = sys.argv[1], sys.argv[2]
    total = 0
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for raiz, pastas, arquivos in os.walk(origem):
            pastas[:] = [p for p in pastas if p not in FORA]
            for nome in arquivos:
                if nome in ARQUIVOS_FORA:
                    continue
                caminho = os.path.join(raiz, nome)
                dentro = os.path.relpath(caminho, origem).replace(os.sep, "/")
                z.write(caminho, dentro)
                total += 1
    print(f"{total} arquivos em {destino}")


if __name__ == "__main__":
    main()
