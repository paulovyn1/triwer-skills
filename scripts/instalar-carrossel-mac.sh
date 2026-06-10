#!/bin/bash

# =============================================================
# Triwer Skills — Instalador do carrossel-triwer (Mac e Linux)
# =============================================================

set -e

REPO="https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
SKILLS_DIR="$HOME/.claude/skills"
CARROSSEL_DIR="$SKILLS_DIR/carrossel-triwer"
VERSION_URL="$REPO/carrossel-triwer/VERSION"
VERSION_FILE="$CARROSSEL_DIR/VERSION"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Triwer Skills — carrossel-triwer   ║${NC}"
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
mkdir -p "$CARROSSEL_DIR/indices"
mkdir -p "$CARROSSEL_DIR/modelos/mc"
mkdir -p "$CARROSSEL_DIR/modelos/mh"
mkdir -p "$CARROSSEL_DIR/referencias"

# Baixar arquivos principais
echo -e "${YELLOW}→ Baixando carrossel-triwer...${NC}"
download_file "carrossel-triwer/SKILL.md" "$CARROSSEL_DIR/SKILL.md"
download_file "carrossel-triwer/indices/modelos-headline.md" "$CARROSSEL_DIR/indices/modelos-headline.md"
download_file "carrossel-triwer/indices/modelos-carrossel.md" "$CARROSSEL_DIR/indices/modelos-carrossel.md"
download_file "carrossel-triwer/referencias/manual-headline.md" "$CARROSSEL_DIR/referencias/manual-headline.md"
download_file "carrossel-triwer/referencias/outliers-headline.md" "$CARROSSEL_DIR/referencias/outliers-headline.md"
download_file "carrossel-triwer/referencias/orientacoes-quem-sou-eu.md" "$CARROSSEL_DIR/referencias/orientacoes-quem-sou-eu.md"
download_file "carrossel-triwer/referencias/orientacoes-publico.md" "$CARROSSEL_DIR/referencias/orientacoes-publico.md"

echo -e "${YELLOW}→ Baixando modelos de carrossel (MC001–MC015)...${NC}"
for i in $(seq -w 1 15); do
    N=$(printf "%03d" $i)
    download_file "carrossel-triwer/modelos/mc/MC${N}.md" "$CARROSSEL_DIR/modelos/mc/MC${N}.md"
done

echo -e "${YELLOW}→ Baixando modelos de headline (MH001–MH016)...${NC}"
for i in $(seq -w 1 16); do
    N=$(printf "%03d" $i)
    download_file "carrossel-triwer/modelos/mh/MH${N}.md" "$CARROSSEL_DIR/modelos/mh/MH${N}.md"
done

# memoria.md: nunca sobrescrever se já existir
if [ ! -f "$CARROSSEL_DIR/memoria.md" ]; then
    echo -e "   ↳ memoria.md será criado no primeiro uso (onboarding)"
else
    echo -e "   ↳ memoria.md mantido (seus dados pessoais)"
fi

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
echo -e "  1. Conecte o Notion no Claude Desktop"
echo -e "     Configurações → Integrações → Notion"
echo ""
echo -e "  2. Abra uma nova conversa no Claude Desktop"
echo -e "     e digite: ${YELLOW}/carrossel-triwer${NC}"
echo ""
echo -e "  3. O onboarding iniciará automaticamente."
echo ""
