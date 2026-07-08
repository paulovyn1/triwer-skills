# =============================================================
# Triwer Skills — Instalador do sexy-triwer (Windows/PowerShell)
# =============================================================

$ErrorActionPreference = "Stop"

$REPO = "https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
$SKILLS_DIR = "$env:USERPROFILE\.claude\skills"
$SEXY_DIR = "$SKILLS_DIR\sexy-triwer"
$VERSION_FILE = "$SEXY_DIR\VERSION"

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
Write-Color "║   Triwer Skills — sexy-triwer        ║" "Blue"
Write-Color "╚══════════════════════════════════════╝" "Blue"
Write-Host ""

# Buscar versão disponível
Write-Color "→ Verificando versão disponível..." "Yellow"
try {
    $REMOTE_VERSION = (Invoke-WebRequest -Uri "$REPO/sexy-triwer/VERSION" -UseBasicParsing).Content.Trim()
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
New-Item -ItemType Directory -Force -Path "$SEXY_DIR\references\pilares-do-desejo","$SEXY_DIR\references\tipos-de-produto","$SEXY_DIR\assets" | Out-Null

# Baixar arquivos principais
Write-Color "→ Baixando sexy-triwer..." "Yellow"
Download-File "sexy-triwer/SKILL.md" "$SEXY_DIR\SKILL.md"
Download-File "sexy-triwer/assets/template-oportunidade-sexy.html" "$SEXY_DIR\assets\template-oportunidade-sexy.html"
Download-File "sexy-triwer/references/manual-headline.md" "$SEXY_DIR\references\manual-headline.md"
Download-File "sexy-triwer/references/notion-setup.md" "$SEXY_DIR\references\notion-setup.md"
Download-File "sexy-triwer/references/pilares-do-desejo/INDEX.md" "$SEXY_DIR\references\pilares-do-desejo\INDEX.md"
Download-File "sexy-triwer/references/pilares-do-desejo/01-gula.md" "$SEXY_DIR\references\pilares-do-desejo\01-gula.md"
Download-File "sexy-triwer/references/pilares-do-desejo/02-inveja.md" "$SEXY_DIR\references\pilares-do-desejo\02-inveja.md"
Download-File "sexy-triwer/references/pilares-do-desejo/03-ira.md" "$SEXY_DIR\references\pilares-do-desejo\03-ira.md"
Download-File "sexy-triwer/references/pilares-do-desejo/04-luxuria.md" "$SEXY_DIR\references\pilares-do-desejo\04-luxuria.md"
Download-File "sexy-triwer/references/pilares-do-desejo/05-preguica.md" "$SEXY_DIR\references\pilares-do-desejo\05-preguica.md"
Download-File "sexy-triwer/references/pilares-do-desejo/06-soberba.md" "$SEXY_DIR\references\pilares-do-desejo\06-soberba.md"
Download-File "sexy-triwer/references/pilares-do-desejo/07-avareza.md" "$SEXY_DIR\references\pilares-do-desejo\07-avareza.md"
Download-File "sexy-triwer/references/tipos-de-produto/INDEX.md" "$SEXY_DIR\references\tipos-de-produto\INDEX.md"
Download-File "sexy-triwer/references/tipos-de-produto/comunidade.md" "$SEXY_DIR\references\tipos-de-produto\comunidade.md"
Download-File "sexy-triwer/references/tipos-de-produto/consultoria.md" "$SEXY_DIR\references\tipos-de-produto\consultoria.md"
Download-File "sexy-triwer/references/tipos-de-produto/curso.md" "$SEXY_DIR\references\tipos-de-produto\curso.md"
Download-File "sexy-triwer/references/tipos-de-produto/desafio.md" "$SEXY_DIR\references\tipos-de-produto\desafio.md"
Download-File "sexy-triwer/references/tipos-de-produto/ebook.md" "$SEXY_DIR\references\tipos-de-produto\ebook.md"
Download-File "sexy-triwer/references/tipos-de-produto/ferramenta.md" "$SEXY_DIR\references\tipos-de-produto\ferramenta.md"
Download-File "sexy-triwer/references/tipos-de-produto/formacao.md" "$SEXY_DIR\references\tipos-de-produto\formacao.md"
Download-File "sexy-triwer/references/tipos-de-produto/mentoria-grupo.md" "$SEXY_DIR\references\tipos-de-produto\mentoria-grupo.md"
Download-File "sexy-triwer/references/tipos-de-produto/mentoria-individual.md" "$SEXY_DIR\references\tipos-de-produto\mentoria-individual.md"
Download-File "sexy-triwer/references/tipos-de-produto/pacotes.md" "$SEXY_DIR\references\tipos-de-produto\pacotes.md"

# memoria.md: nunca sobrescrever se já existir
if (-not (Test-Path "$SEXY_DIR\memoria.md")) {
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
Write-Color "     e digite: /sexy-triwer" "Yellow"
Write-Host ""
Write-Host "  3. Se possível, rode /oraculo-triwer antes — a investigação fica"
Write-Host "     mais rápida com 'Meu Público' já mapeado."
Write-Host ""
