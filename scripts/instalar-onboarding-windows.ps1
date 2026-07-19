# =============================================================
# Triwer Skills — Instalador do onboarding-triwer (Windows/PowerShell)
# =============================================================
#
# O que este script faz (leia antes de rodar):
#   - Baixa arquivos de texto (.md, VERSION) do repositório público
#     https://github.com/paulovyn1/triwer-skills para
#     %USERPROFILE%\.claude\skills\
#   - Não coleta credenciais nem envia dados para lugar nenhum; não executa
#     nada além de gravar esses arquivos em disco.
#   - Nunca sobrescreve memoria.md (seus dados pessoais ficam intactos).
#   - Rodar de novo só baixa de novo o que tiver versão nova.

$ErrorActionPreference = "Stop"

$REPO = "https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
$SKILLS_DIR = "$env:USERPROFILE\.claude\skills"
$ONBOARDING_DIR = "$SKILLS_DIR\onboarding-triwer"
$VERSION_FILE = "$ONBOARDING_DIR\VERSION"

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
Write-Color "║   Triwer Skills — onboarding-triwer  ║" "Blue"
Write-Color "╚══════════════════════════════════════╝" "Blue"
Write-Host ""

# Buscar versão disponível
Write-Color "→ Verificando versão disponível..." "Yellow"
try {
    $REMOTE_VERSION = (Invoke-WebRequest -Uri "$REPO/onboarding-triwer/VERSION" -UseBasicParsing).Content.Trim()
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
    Write-Color "   Versão instalada:  $INSTALLED_VERSION (já é a mais recente)" "Green"
    Write-Color "→ Conferindo arquivos..." "Yellow"
    $UPDATE = $true
} elseif ($INSTALLED_VERSION -ne "") {
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
New-Item -ItemType Directory -Force -Path $ONBOARDING_DIR | Out-Null

# Baixar arquivos principais
Write-Color "→ Baixando onboarding-triwer..." "Yellow"
Download-File "onboarding-triwer/SKILL.md" "$ONBOARDING_DIR\SKILL.md"

# memoria.md: nunca sobrescrever se já existir
if (-not (Test-Path "$ONBOARDING_DIR\memoria.md")) {
    Write-Color "   ↳ memoria.md será criado no primeiro uso (onboarding)" "White"
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
Write-Host "  1. Conecte o Notion no seu cliente Claude (instruções dentro da"
Write-Host "     própria skill, ela te orienta se detectar que falta)"
Write-Host ""
Write-Host "  2. Abra uma nova conversa"
Write-Color "     e digite: /onboarding-triwer" "Yellow"
Write-Host ""
Write-Host "  3. Siga o fluxo — leva de 5 a 10 minutos."
Write-Host ""
