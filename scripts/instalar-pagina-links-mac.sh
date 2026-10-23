#!/bin/bash

# =============================================================
# Triwer Skills — Instalador do pagina-links-triwer (Mac e Linux)
# =============================================================
#
# O que este script faz (leia antes de rodar):
#   - Baixa todos os arquivos da pasta pagina-links-triwer do repositório público
#     https://github.com/paulovyn1/triwer-skills para ~/.claude/skills/
#     (SKILL.md, references, assets, scripts). A lista de arquivos vem da
#     API pública do GitHub, então arquivo novo entra sozinho.
#   - Não coleta credenciais nem envia dados para lugar nenhum; não executa
#     nada além de gravar esses arquivos em disco.
#   - Nunca sobrescreve memoria.md (seus dados pessoais ficam intactos).
#   - Rodar de novo atualiza para a versão mais recente.

set -e

SKILL="pagina-links-triwer"
REPO="https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
TREE_URL="https://api.github.com/repos/paulovyn1/triwer-skills/git/trees/main?recursive=1"
SKILLS_DIR="${TRIWER_SKILLS_DIR:-$HOME/.claude/skills}"
SKILL_DIR="$SKILLS_DIR/$SKILL"
VERSION_FILE="$SKILL_DIR/VERSION"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Triwer Skills — pagina-links-triwer${NC}"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
echo ""

if ! command -v curl &> /dev/null; then
    echo -e "${RED}✗ curl não encontrado. Instale o curl e tente novamente.${NC}"
    exit 1
fi

echo -e "${YELLOW}→ Verificando versão disponível...${NC}"
REMOTE_VERSION=$(curl -fsSL --retry 4 --retry-delay 2 --retry-all-errors "$REPO/$SKILL/VERSION" 2>/dev/null | tr -d '\r\n ' || echo "")

if [ -z "$REMOTE_VERSION" ]; then
    echo -e "${RED}✗ Não foi possível conectar ao repositório. Verifique sua conexão.${NC}"
    exit 1
fi
echo -e "   Versão disponível: ${GREEN}$REMOTE_VERSION${NC}"

INSTALLED_VERSION=""
if [ -f "$VERSION_FILE" ]; then
    INSTALLED_VERSION=$(tr -d '\r\n ' < "$VERSION_FILE")
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

# Lista de arquivos da skill no repositório
echo -e "${YELLOW}→ Listando arquivos da skill...${NC}"
FILES=$(curl -fsSL --retry 4 --retry-delay 2 --retry-all-errors "$TREE_URL" 2>/dev/null | tr -d '\n ' | grep -o "\"path\":\"$SKILL/[^\"]*\",\"mode\":\"[0-9]*\",\"type\":\"blob\"" | sed 's/^"path":"//; s/","mode".*$//' || true)

if [ -z "$FILES" ]; then
    echo -e "${RED}✗ Não consegui listar os arquivos da skill. Tente de novo em alguns minutos.${NC}"
    exit 1
fi

echo -e "${YELLOW}→ Baixando $SKILL...${NC}"
COUNT=0
while IFS= read -r remote_path; do
    [ -z "$remote_path" ] && continue
    rel="${remote_path#"$SKILL"/}"
    # memoria.md é dado pessoal: nunca sobrescrever
    if [ "$rel" = "memoria.md" ] && [ -f "$SKILL_DIR/memoria.md" ]; then
        echo -e "   ↳ memoria.md mantido (seus dados pessoais)"
        continue
    fi
    mkdir -p "$(dirname "$SKILL_DIR/$rel")"
    curl -fsSL --retry 4 --retry-delay 2 --retry-all-errors "$REPO/$remote_path" -o "$SKILL_DIR/$rel"
    COUNT=$((COUNT + 1))
done <<< "$FILES"
echo -e "   ↳ $COUNT arquivos baixados"

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
echo -e "  1. Abra uma nova conversa"
echo -e "     e digite: ${YELLOW}/pagina-links-triwer${NC}"
echo ""
