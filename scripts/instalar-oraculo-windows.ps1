# =============================================================
# Triwer Skills — Instalador do oraculo-triwer (Windows/PowerShell)
# =============================================================

$ErrorActionPreference = "Stop"

$REPO = "https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
$SKILLS_DIR = "$env:USERPROFILE\.claude\skills"
$ORACULO_DIR = "$SKILLS_DIR\oraculo-triwer"
$VERSION_FILE = "$ORACULO_DIR\VERSION"

function Write-Color($text, $color = "White") {
    Write-Host $text -ForegroundColor $color
}

function Download-File($remotePath, $localPath) {
    $dir = Split-Path $localPath
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    try {
        Invoke-WebRequest -Uri "$REPO/$remotePath" -OutFile $localPath -UseBasicParsing
    } catch {
        Write-Color "  ERRO ao baixar: $remotePath" "Red"
        throw
    }
}

Write-Host ""
Write-Color "╔══════════════════════════════════════╗" "Blue"
Write-Color "║   Triwer Skills — oraculo-triwer     ║" "Blue"
Write-Color "╚══════════════════════════════════════╝" "Blue"
Write-Host ""

# Buscar versão disponível
Write-Color "→ Verificando versão disponível..." "Yellow"
try {
    $REMOTE_VERSION = (Invoke-WebRequest -Uri "$REPO/oraculo-triwer/VERSION" -UseBasicParsing).Content.Trim()
} catch {
    Write-Color "✗ Não foi possível conectar ao repositório. Verifique sua conexão." "Red"
    exit 1
}

Write-Color "   Versão disponível: $REMOTE_VERSION" "Green"

# Verificar versão instalada
$INSTALLED_VERSION = ""
if (Test-Path $VERSION_FILE) {
    $INSTALLED_VERSION = (Get-Content $VERSION_FILE).Trim()
}

if ($INSTALLED_VERSION -eq $REMOTE_VERSION) {
    Write-Host ""
    Write-Color "✓ Você já tem a versão mais recente instalada ($INSTALLED_VERSION)." "Green"
    Write-Host ""
    exit 0
}

if ($INSTALLED_VERSION -ne "") {
    Write-Color "   Versão instalada:  $INSTALLED_VERSION" "Yellow"
    Write-Color "→ Atualizando para $REMOTE_VERSION..." "Yellow"
    $UPDATE = $true
} else {
    Write-Color "   Nenhuma versão instalada." "White"
    Write-Color "→ Instalando versão $REMOTE_VERSION..." "Yellow"
    $UPDATE = $false
}

Write-Host ""

# Criar estrutura de pastas
Write-Color "→ Criando pastas..." "Yellow"
New-Item -ItemType Directory -Force -Path "$ORACULO_DIR\referencias" | Out-Null

# Baixar arquivos principais
Write-Color "→ Baixando oraculo-triwer..." "Yellow"
Download-File "oraculo-triwer/SKILL.md" "$ORACULO_DIR\SKILL.md"
Download-File "oraculo-triwer/referencias/orientacoes-publico.md" "$ORACULO_DIR\referencias\orientacoes-publico.md"

# memoria.md: nunca sobrescrever se já existir
if (-not (Test-Path "$ORACULO_DIR\memoria.md")) {
    Write-Color "   ↳ memoria.md será criado no primeiro uso" "White"
} else {
    Write-Color "   ↳ memoria.md mantido (seus dados pessoais)" "White"
}

# Salvar versão instalada
Set-Content -Path $VERSION_FILE -Value $REMOTE_VERSION

Write-Host ""
Write-Color "╔══════════════════════════════════════╗" "Green"
if ($UPDATE) {
    Write-Color "║   ✓ Atualização concluída!           ║" "Green"
} else {
    Write-Color "║   ✓ Instalação concluída!            ║" "Green"
}
Write-Color "║   Versão: $REMOTE_VERSION" "Green"
Write-Color "╚══════════════════════════════════════╝" "Green"
Write-Host ""
Write-Color "  Próximos passos:" "Blue"
Write-Host "  1. Complete o /onboarding-triwer antes, se ainda não fez"
Write-Host ""
Write-Host "  2. Abra uma nova conversa"
Write-Color "     e digite: /oraculo-triwer" "Yellow"
Write-Host ""
Write-Host "  3. Tenha em mãos, se possível, uma planilha (.xlsx/.csv) de"
Write-Host "     pesquisa com alunos/clientes."
Write-Host ""
