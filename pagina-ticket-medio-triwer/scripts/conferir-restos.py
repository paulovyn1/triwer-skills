"""Confere o projeto antes de mostrar ou publicar: sobras do exemplo, travessão e preço fora da ancoragem.

Uso: python conferir-restos.py <pasta-do-projeto>

Varre src/, index.html, o arquivo HTML (modo HTML) e public/ e relata:
  1. pendências [entre colchetes]: texto de exemplo que ainda não foi trocado;
  2. números zerados no CONFIG (config.js ou bloco CONFIG do HTML), como CUSTO_DE: 0;
  3. travessão (— ou –), proibido em qualquer texto da página;
  4. preço (R$ ...) em lugar que não é a ancoragem, como o topo, os botões e a
     meta description.

Sai com código 1 se achar algo. As pendências entre colchetes são esperadas até
o fim do trabalho; o que sobra na hora de entregar precisa ser zero.

Por que existe: o kit é uma página que funciona de ponta a ponta, escrita só com
texto de exemplo entre colchetes. É mais rápido trocar o texto de uma página pronta
do que escrever do zero, e o risco é um [colchete] ou uma frase de exemplo
sobreviver na página do aluno. Este script pega isso antes do aluno.
"""
import os
import re
import sys

# O console do Windows (cp1252) quebra com acento e símbolo: imprima sempre em UTF-8.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXT = {".jsx", ".js", ".css", ".html", ".json", ".md"}
IGNORAR = {"node_modules", "dist", ".vercel", ".git"}
COLCHETE = re.compile(r"\[[^\]\n]{2,90}\]")
# Pendência = texto em colchetes (começa com letra ou @, sem sinais de código). Array JS, índice,
# chamada de função e data attribute não contam.
TEXTO = re.compile(r"^\[[A-Za-zÀ-ÿ@][^()=\{\}<>\[\]]*\]$")
PRECO = re.compile(r"R\$\s?\d")
ZERADO = re.compile(r"\b(CUSTO_DE|CUSTO_PARA)\b\s*[:=]\s*0\b")
# trechos onde preço é permitido: ancoragem, conta do custo e valores de mercado
SECOES_COM_PRECO = ("Oferta", "Custo", "recap", "preco", "oferta", "custo", "PRECO", "PARCELA")


def arquivos(raiz):
    for pasta, subs, nomes in os.walk(raiz):
        subs[:] = [s for s in subs if s not in IGNORAR]
        for n in nomes:
            if os.path.splitext(n)[1].lower() in EXT and n != "package-lock.json":
                yield os.path.join(pasta, n)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    raiz = sys.argv[1]
    achados = 0
    for f in arquivos(raiz):
        rel = os.path.relpath(f, raiz)
        if rel.endswith("styles.css") or rel.endswith("LEIA-ME.md"):
            continue
        codigo = f.endswith((".js", ".jsx", ".html"))
        with open(f, encoding="utf-8", errors="ignore") as fh:
            linhas = fh.readlines()
        dentro_ancoragem = False
        for i, linha in enumerate(linhas, 1):
            if any(k in linha for k in ('id="oferta"', "export function Oferta", "export function Custo", 'class="panel center">\n')):
                dentro_ancoragem = "oferta" in linha or "Oferta" in linha or "Custo" in linha
            motivos = []
            if codigo:
                for m in COLCHETE.finditer(linha):
                    c = m.group(0)
                    if TEXTO.match(c) and (c[1].isupper() or c[1] == "@" or (" " in c and "," not in c)):
                        motivos.append(f"pendência {c}")
                        break
                if ZERADO.search(linha):
                    motivos.append("número zerado no CONFIG")
            if "—" in linha or "–" in linha:
                motivos.append("travessão")
            if codigo and PRECO.search(linha) and not any(k in linha for k in SECOES_COM_PRECO) and not dentro_ancoragem:
                if "meta" in linha or "<title" in linha or "cta" in linha.lower():
                    motivos.append("preço em botão, título ou meta description")
            if motivos:
                achados += 1
                print(f"{rel}:{i}: {'; '.join(motivos)} | {linha.strip()[:110]}")
    print(f"\n{achados} ocorrência(s). Pendências entre colchetes são esperadas até o fim; na entrega, o total precisa ser 0.")
    sys.exit(1 if achados else 0)


if __name__ == "__main__":
    main()
