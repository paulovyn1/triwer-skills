# =============================================================
# Triwer Skills — Instalador para Windows (PowerShell)
# Instala: carrossel-triwer + cta-triwer
# =============================================================

$ErrorActionPreference = "Stop"

$REPO = "https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
$SKILLS_DIR = "$env:USERPROFILE\.claude\skills"
$CARROSSEL_DIR = "$SKILLS_DIR\carrossel-triwer"
$CTA_DIR = "$SKILLS_DIR\cta-triwer"
$VERSION_FILE_CARROSSEL = "$CARROSSEL_DIR\VERSION"
$VERSION_FILE_CTA = "$CTA_DIR\VERSION"

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
Write-Color "║     Triwer Skills — Instalador       ║" "Blue"
Write-Color "║   carrossel-triwer + cta-triwer      ║" "Blue"
Write-Color "╚══════════════════════════════════════╝" "Blue"
Write-Host ""

# Buscar versão disponível
Write-Color "→ Verificando versão disponível..." "Yellow"
try {
    $REMOTE_VERSION = (Invoke-WebRequest -Uri "$REPO/VERSION" -UseBasicParsing).Content.Trim()
} catch {
    Write-Color "✗ Não foi possível conectar ao repositório. Verifique sua conexão." "Red"
    exit 1
}

Write-Color "   Versão disponível: $REMOTE_VERSION" "Green"

# Verificar versão instalada
$INSTALLED_VERSION = ""
if (Test-Path $VERSION_FILE_CARROSSEL) {
    $INSTALLED_VERSION = (Get-Content $VERSION_FILE_CARROSSEL).Trim()
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
$folders = @(
    "$CARROSSEL_DIR\indices",
    "$CARROSSEL_DIR\modelos\mc",
    "$CARROSSEL_DIR\modelos\mh",
    "$CARROSSEL_DIR\referencias",
    "$CTA_DIR\referencias"
)
foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

# Baixar carrossel-triwer
Write-Color "→ Baixando carrossel-triwer..." "Yellow"
Download-File "carrossel-triwer/SKILL.md" "$CARROSSEL_DIR\SKILL.md"
Download-File "carrossel-triwer/indices/modelos-headline.md" "$CARROSSEL_DIR\indices\modelos-headline.md"
Download-File "carrossel-triwer/indices/modelos-carrossel.md" "$CARROSSEL_DIR\indices\modelos-carrossel.md"
Download-File "carrossel-triwer/referencias/manual-headline.md" "$CARROSSEL_DIR\referencias\manual-headline.md"
Download-File "carrossel-triwer/referencias/outliers-headline.md" "$CARROSSEL_DIR\referencias\outliers-headline.md"

Write-Color "→ Baixando modelos de carrossel (MC001–MC015)..." "Yellow"
1..15 | ForEach-Object {
    $N = $_.ToString("000")
    Download-File "carrossel-triwer/modelos/mc/MC$N.md" "$CARROSSEL_DIR\modelos\mc\MC$N.md"
}

Write-Color "→ Baixando modelos de headline (MH001–MH016)..." "Yellow"
1..16 | ForEach-Object {
    $N = $_.ToString("000")
    Download-File "carrossel-triwer/modelos/mh/MH$N.md" "$CARROSSEL_DIR\modelos\mh\MH$N.md"
}

# Baixar cta-triwer
Write-Color "→ Baixando cta-triwer..." "Yellow"
Download-File "cta-triwer/SKILL.md" "$CTA_DIR\SKILL.md"
Download-File "cta-triwer/referencias/iscas-regras.md" "$CTA_DIR\referencias\iscas-regras.md"
Download-File "cta-triwer/referencias/padroes-de-iscas.md" "$CTA_DIR\referencias\padroes-de-iscas.md"

# iscas-local.md: nunca sobrescrever se já existir
if (-not (Test-Path "$CTA_DIR\referencias\iscas-local.md")) {
    Download-File "cta-triwer/referencias/iscas-local.md" "$CTA_DIR\referencias\iscas-local.md"
    Write-Color "   ↳ iscas-local.md criado" "White"
} else {
    Write-Color "   ↳ iscas-local.md mantido (seus dados pessoais)" "White"
}

# Salvar versão instalada
Set-Content -Path $VERSION_FILE_CARROSSEL -Value $REMOTE_VERSION
Set-Content -Path $VERSION_FILE_CTA -Value $REMOTE_VERSION

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
Write-Host "  1. Conecte o Notion no Claude Desktop"
Write-Host "     Configurações → Integrações → Notion"
Write-Host ""
Write-Host "  2. Abra uma nova conversa no Claude Desktop"
Write-Color "     e digite: /carrossel-triwer" "Yellow"
Write-Host ""
Write-Host "  3. O onboarding iniciará automaticamente."
Write-Host ""
