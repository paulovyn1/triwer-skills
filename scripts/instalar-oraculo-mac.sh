#!/bin/bash

# =============================================================
# Triwer Skills — Instalador do oraculo-triwer (Mac e Linux)
# =============================================================
#
# O que este script faz (leia antes de rodar):
#   - Baixa arquivos de texto (.md, VERSION) do repositório público
#     https://github.com/paulovyn1/triwer-skills para ~/.claude/skills/
#   - Não coleta credenciais nem envia dados para lugar nenhum; não executa
#     nada além de gravar esses arquivos em disco.
#   - Nunca sobrescreve memoria.md (seus dados pessoais ficam intactos).
#   - Rodar de novo só baixa de novo o que tiver versão nova.

set -e

REPO="https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
SKILLS_DIR="$HOME/.claude/skills"
ORACULO_DIR="$SKILLS_DIR/oraculo-triwer"
VERSION_URL="$REPO/oraculo-triwer/VERSION"
VERSION_FILE="$ORACULO_DIR/VERSION"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Triwer Skills — oraculo-triwer     ║${NC}"
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
    echo -e "   Versão instalada:  ${GREEN}$INSTALLED_VERSION${NC} (já é a mais recente)"
    echo -e "${YELLOW}→ Conferindo arquivos...${NC}"
    UPDATE=true
elif [ -n "$INSTALLED_VERSION" ]; then
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
mkdir -p "$ORACULO_DIR/referencias"

# Baixar arquivos principais
echo -e "${YELLOW}→ Baixando oraculo-triwer...${NC}"
download_file "oraculo-triwer/SKILL.md" "$ORACULO_DIR/SKILL.md"
download_file "oraculo-triwer/referencias/orientacoes-publico.md" "$ORACULO_DIR/referencias/orientacoes-publico.md"

# memoria.md: nunca sobrescrever se já existir
if [ ! -f "$ORACULO_DIR/memoria.md" ]; then
    echo -e "   ↳ memoria.md será criado no primeiro uso"
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
echo -e "  1. Complete o /onboarding-triwer antes, se ainda não fez"
echo ""
echo -e "  2. Abra uma nova conversa"
echo -e "     e digite: ${YELLOW}/oraculo-triwer${NC}"
echo ""
echo -e "  3. Tenha em mãos, se possível, uma planilha (.xlsx/.csv) de"
echo -e "     pesquisa com alunos/clientes."
echo ""
