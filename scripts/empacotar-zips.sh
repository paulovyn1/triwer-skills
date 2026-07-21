#!/bin/bash

# =============================================================
# Triwer Skills — Empacota cada skill em um .zip para upload manual
# (uso do mantenedor — gera dist/, não é para o aluno rodar)
# =============================================================
#
# Cada .zip contém a pasta da skill pronta para upload na tela de Skills
# do claude.ai (Settings -> Capabilities -> Skills -> Upload skill).
# Formato exato aceito pelo claude.ai ainda não foi confirmado na prática
# (Bloco 9.2 do plano de arquitetura) -- ajustar este script se o claude.ai
# esperar uma estrutura diferente (ex: zip sem pasta-raiz, ou só o SKILL.md).

set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"

SKILLS=(
    "onboarding-triwer"
    "estilo-forge"
    "dr-house-triwer"
    "oraculo-triwer"
    "sexy-triwer"
    "prisma-triwer"
    "historias-triwer"
    "mdi-triwer"
    "carrossel-triwer"
    "cta-triwer"
    "notion-zettelkasten-si"
)

echo ""
echo "Empacotando skills para upload manual (claude.ai)..."
echo ""

rm -rf "$DIST"
mkdir -p "$DIST"

for skill in "${SKILLS[@]}"; do
    skill_path="$ROOT/$skill"
    if [ ! -d "$skill_path" ]; then
        echo "  pulando $skill (pasta não encontrada)"
        continue
    fi

    zip_path="$DIST/$skill.zip"
    temp_dir=$(mktemp -d)

    # Copia excluindo dados pessoais (memoria.md) e scripts próprios (não
    # fazem sentido dentro do zip de upload manual).
    rsync -a --exclude 'memoria.md' --exclude 'scripts' --exclude '.git' --exclude '_draft-redesign' \
        "$skill_path/" "$temp_dir/" 2>/dev/null || \
        cp -r "$skill_path/." "$temp_dir/"
    rm -rf "$temp_dir/_draft-redesign"

    (cd "$temp_dir" && zip -rq "$zip_path" .)
    rm -rf "$temp_dir"

    echo "  ✓ $skill.zip"
done

echo ""
echo "Pronto. Arquivos em: $DIST"
echo "Suba esses .zip numa Release do GitHub (ou na pasta dist/ versionada)"
echo "para os alunos baixarem e importarem manualmente no claude.ai."
echo ""
