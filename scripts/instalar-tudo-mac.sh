#!/bin/bash

# =============================================================
# Triwer Skills — Instalador completo do ecossistema (Mac e Linux)
# =============================================================
#
# Instala (ou atualiza) todas as skills Triwer de uma vez só, na ordem
# recomendada. Cada skill mantém seu próprio instalador — este script só
# encadeia todos, para quem quer instalar tudo com um comando.
#
# Rodar de novo a qualquer momento atualiza só o que tiver versão nova
# (mesmo comportamento dos instaladores individuais). memoria.md pessoal de
# cada skill nunca é sobrescrito.
#
# O que este script faz (leia antes de rodar):
#   - Baixa, um de cada vez, os 11 instaladores individuais abaixo do
#     repositório público https://github.com/paulovyn1/triwer-skills e
#     salva cada um num arquivo temporário antes de rodar -- nada é
#     executado sem primeiro existir em disco, então dá pra abrir e ler
#     qualquer um deles antes ou durante a instalação.
#   - Cada instalador baixado só grava arquivos de texto (.md, VERSION) em
#     ~/.claude/skills/<skill>/. Não coleta credenciais, não envia dados
#     para lugar nenhum.
#   - Nunca sobrescreve memoria.md (seus dados pessoais ficam intactos).

set -e

REPO="https://raw.githubusercontent.com/paulovyn1/triwer-skills"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Triwer Skills — Instalação completa      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""
echo "Isso vai instalar (ou atualizar) todas as skills do ecossistema Triwer,"
echo "na ordem recomendada de uso."
echo ""

if ! command -v curl &> /dev/null; then
    echo -e "${RED}✗ curl não encontrado. Instale o curl e tente novamente.${NC}"
    exit 1
fi

# Nome de exibição | caminho do instalador individual (relativo ao repo)
INSTALLERS=(
    "Onboarding|main/scripts/instalar-onboarding-mac.sh"
    "Estilo Forge|main/estilo-forge/scripts/instalar-mac.sh"
    "Dr. House (avaliação)|main/scripts/instalar-drhouse-mac.sh"
    "Oráculo (público)|main/scripts/instalar-oraculo-mac.sh"
    "Sexy (promessa)|main/scripts/instalar-sexy-mac.sh"
    "Prisma (viés/posicionamento)|main/scripts/instalar-prisma-mac.sh"
    "Histórias|main/scripts/instalar-historias-mac.sh"
    "MDI|main/scripts/instalar-mdi-mac.sh"
    "Carrossel|main/scripts/instalar-carrossel-mac.sh"
    "CTA|main/scripts/instalar-cta-mac.sh"
    "Notion Zettelkasten|main/scripts/instalar-zettelkasten-mac.sh"
)

TOTAL=${#INSTALLERS[@]}
CURRENT=0
FAILED=()

for entry in "${INSTALLERS[@]}"; do
    CURRENT=$((CURRENT + 1))
    NAME="${entry%%|*}"
    PATH_SUFFIX="${entry#*|}"

    echo -e "${BLUE}[$CURRENT/$TOTAL] $NAME${NC}"

    # Baixa o instalador individual para um arquivo temporário real antes de
    # rodar (em vez de "bash <(curl ...)"), para que o conteúdo possa ser
    # aberto e lido a qualquer momento durante a instalação.
    TMP_SCRIPT=$(mktemp)
    if curl -fsSL "$REPO/$PATH_SUFFIX" -o "$TMP_SCRIPT" && bash "$TMP_SCRIPT"; then
        echo ""
    else
        echo -e "${RED}✗ Falha ao instalar: $NAME${NC}"
        echo ""
        FAILED+=("$NAME")
    fi
    rm -f "$TMP_SCRIPT"
done

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
if [ ${#FAILED[@]} -eq 0 ]; then
    echo -e "${GREEN}║   ✓ Instalação completa concluída!         ║${NC}"
else
    echo -e "${YELLOW}║   ⚠ Concluído com pendências               ║${NC}"
fi
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""

if [ ${#FAILED[@]} -gt 0 ]; then
    echo -e "${YELLOW}Não foi possível instalar:${NC}"
    for f in "${FAILED[@]}"; do
        echo "  - $f"
    done
    echo ""
fi

echo -e "${BLUE}Próximos passos:${NC}"
echo "  1. Abra uma nova conversa"
echo -e "     e digite: ${YELLOW}/onboarding-triwer${NC}"
echo ""
echo "  2. Siga o fluxo — ele configura seu Notion e libera as outras skills"
echo ""
echo "  3. Ordem recomendada de uso depois do onboarding:"
echo "     estilo-forge → dr-house-triwer → oraculo-triwer → sexy-triwer →"
echo "     prisma-triwer → historias-triwer (contínua) → mdi-triwer →"
echo "     carrossel-triwer → cta-triwer"
echo ""
