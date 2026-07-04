#!/bin/bash

# =============================================================
# estilo-forge — Instalador (Mac e Linux)
# =============================================================

set -e

REPO="https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
SKILLS_DIR="$HOME/.claude/skills"
FORGE_DIR="$SKILLS_DIR/estilo-forge"
VERSION_URL="$REPO/estilo-forge/VERSION"
VERSION_FILE="$FORGE_DIR/VERSION"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          estilo-forge                ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
echo ""

# Verificar curl
if ! command -v curl &> /dev/null; then
    echo -e "${RED}✗ curl não encontrado. Instale o curl e tente novamente.${NC}"
    exit 1
fi

# Buscar versão disponível no repositório
echo -e "${YELLOW}→ Verificando versão disponível...${NC}"
REMOTE_VERSION=$(curl -fsSL "$VERSION_URL" 2>/dev/null || echo "")

if [ -z "$REMOTE_VERSION" ]; then
    echo -e "${RED}✗ Não foi possível conectar ao repositório. Verifique sua conexão.${NC}"
    exit 1
fi

echo -e "   Versão disponível: ${GREEN}$REMOTE_VERSION${NC}"

# Verificar versão instalada
INSTALLED_VERSION=""
if [ -f "$VERSION_FILE" ]; then
    INSTALLED_VERSION=$(cat "$VERSION_FILE")
fi

if [ "$INSTALLED_VERSION" = "$REMOTE_VERSION" ]; then
    echo ""
    echo -e "${GREEN}✓ Você já tem a versão mais recente instalada ($INSTALLED_VERSION).${NC}"
    echo ""
    exit 0
fi

if [ -n "$INSTALLED_VERSION" ]; then
    echo -e "   Versão instalada:  ${YELLOW}$INSTALLED_VERSION${NC}"
    echo -e "${YELLOW}→ Atualizando para $REMOTE_VERSION...${NC}"
    UPDATE=true
else
    echo -e "   Nenhuma versão instalada."
    echo -e "${YELLOW}→ Instalando versão $REMOTE_VERSION...${NC}"
    UPDATE=false
fi

echo ""

# Função para baixar arquivo
download_file() {
    local remote_path="$1"
    local local_path="$2"
    local dir=$(dirname "$local_path")
    mkdir -p "$dir"
    curl -fsSL "$REPO/$remote_path" -o "$local_path"
}

# Criar estrutura de pastas
echo -e "${YELLOW}→ Criando pastas...${NC}"
mkdir -p "$FORGE_DIR/references"

# Baixar arquivos
echo -e "${YELLOW}→ Baixando estilo-forge...${NC}"
download_file "estilo-forge/SKILL.md" "$FORGE_DIR/SKILL.md"
download_file "estilo-forge/references/analysis-framework.md" "$FORGE_DIR/references/analysis-framework.md"
download_file "estilo-forge/references/skill-template.md" "$FORGE_DIR/references/skill-template.md"
download_file "estilo-forge/references/universal-anti-ia.md" "$FORGE_DIR/references/universal-anti-ia.md"

# Salvar versão instalada
echo "$REMOTE_VERSION" > "$VERSION_FILE"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
if [ "$UPDATE" = true ]; then
    echo -e "${GREEN}║   ✓ Atualização concluída!           ║${NC}"
else
    echo -e "${GREEN}║   ✓ Instalação concluída!            ║${NC}"
fi
echo -e "${GREEN}║   Versão: $REMOTE_VERSION$(printf '%*s' $((29 - ${#REMOTE_VERSION})) '')║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BLUE}Próximos passos:${NC}"
echo -e "  1. Abra uma nova conversa no Claude Code ou Claude Desktop"
echo -e "     e digite: ${YELLOW}/estilo-forge${NC}"
echo ""
echo -e "  2. O onboarding iniciará automaticamente e vai te guiar"
echo -e "     na criação da sua skill de estilo personalizada."
echo ""
echo -e "  As skills geradas (estilo-[nome]) ficam em ~/.claude/skills/"
echo -e "  e nunca são alteradas por atualizações do estilo-forge."
echo ""
