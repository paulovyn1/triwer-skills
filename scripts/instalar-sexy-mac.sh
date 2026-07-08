#!/bin/bash

# =============================================================
# Triwer Skills — Instalador do sexy-triwer (Mac e Linux)
# =============================================================

set -e

REPO="https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
SKILLS_DIR="$HOME/.claude/skills"
SEXY_DIR="$SKILLS_DIR/sexy-triwer"
VERSION_URL="$REPO/sexy-triwer/VERSION"
VERSION_FILE="$SEXY_DIR/VERSION"

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Triwer Skills — sexy-triwer        ║${NC}"
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
mkdir -p "$SEXY_DIR/references/pilares-do-desejo" "$SEXY_DIR/references/tipos-de-produto" "$SEXY_DIR/assets"

# Baixar arquivos principais
echo -e "${YELLOW}→ Baixando sexy-triwer...${NC}"
download_file "sexy-triwer/SKILL.md" "$SEXY_DIR/SKILL.md"
download_file "sexy-triwer/assets/template-oportunidade-sexy.html" "$SEXY_DIR/assets/template-oportunidade-sexy.html"
download_file "sexy-triwer/references/manual-headline.md" "$SEXY_DIR/references/manual-headline.md"
download_file "sexy-triwer/references/notion-setup.md" "$SEXY_DIR/references/notion-setup.md"
download_file "sexy-triwer/references/pilares-do-desejo/INDEX.md" "$SEXY_DIR/references/pilares-do-desejo/INDEX.md"
download_file "sexy-triwer/references/pilares-do-desejo/01-gula.md" "$SEXY_DIR/references/pilares-do-desejo/01-gula.md"
download_file "sexy-triwer/references/pilares-do-desejo/02-inveja.md" "$SEXY_DIR/references/pilares-do-desejo/02-inveja.md"
download_file "sexy-triwer/references/pilares-do-desejo/03-ira.md" "$SEXY_DIR/references/pilares-do-desejo/03-ira.md"
download_file "sexy-triwer/references/pilares-do-desejo/04-luxuria.md" "$SEXY_DIR/references/pilares-do-desejo/04-luxuria.md"
download_file "sexy-triwer/references/pilares-do-desejo/05-preguica.md" "$SEXY_DIR/references/pilares-do-desejo/05-preguica.md"
download_file "sexy-triwer/references/pilares-do-desejo/06-soberba.md" "$SEXY_DIR/references/pilares-do-desejo/06-soberba.md"
download_file "sexy-triwer/references/pilares-do-desejo/07-avareza.md" "$SEXY_DIR/references/pilares-do-desejo/07-avareza.md"
download_file "sexy-triwer/references/tipos-de-produto/INDEX.md" "$SEXY_DIR/references/tipos-de-produto/INDEX.md"
download_file "sexy-triwer/references/tipos-de-produto/comunidade.md" "$SEXY_DIR/references/tipos-de-produto/comunidade.md"
download_file "sexy-triwer/references/tipos-de-produto/consultoria.md" "$SEXY_DIR/references/tipos-de-produto/consultoria.md"
download_file "sexy-triwer/references/tipos-de-produto/curso.md" "$SEXY_DIR/references/tipos-de-produto/curso.md"
download_file "sexy-triwer/references/tipos-de-produto/desafio.md" "$SEXY_DIR/references/tipos-de-produto/desafio.md"
download_file "sexy-triwer/references/tipos-de-produto/ebook.md" "$SEXY_DIR/references/tipos-de-produto/ebook.md"
download_file "sexy-triwer/references/tipos-de-produto/ferramenta.md" "$SEXY_DIR/references/tipos-de-produto/ferramenta.md"
download_file "sexy-triwer/references/tipos-de-produto/formacao.md" "$SEXY_DIR/references/tipos-de-produto/formacao.md"
download_file "sexy-triwer/references/tipos-de-produto/mentoria-grupo.md" "$SEXY_DIR/references/tipos-de-produto/mentoria-grupo.md"
download_file "sexy-triwer/references/tipos-de-produto/mentoria-individual.md" "$SEXY_DIR/references/tipos-de-produto/mentoria-individual.md"
download_file "sexy-triwer/references/tipos-de-produto/pacotes.md" "$SEXY_DIR/references/tipos-de-produto/pacotes.md"

# memoria.md: nunca sobrescrever se já existir
if [ ! -f "$SEXY_DIR/memoria.md" ]; then
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
echo -e "     e digite: ${YELLOW}/sexy-triwer${NC}"
echo ""
echo -e "  3. Se possível, rode /oraculo-triwer antes — a investigação fica"
echo -e "     mais rápida com 'Meu Público' já mapeado."
echo ""
