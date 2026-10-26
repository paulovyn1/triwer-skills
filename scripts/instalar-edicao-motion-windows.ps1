# =============================================================
# Triwer Skills — Instalador do edicao-motion-triwer (Windows/PowerShell)
# =============================================================
#
# O que este script faz (leia antes de rodar):
#   - Baixa todos os arquivos da pasta edicao-motion-triwer do repositório público
#     https://github.com/paulovyn1/triwer-skills para
#     %USERPROFILE%\.claude\skills\ (SKILL.md, estilos, references, scripts, template).
#     A lista de arquivos vem da API pública do GitHub, então arquivo novo
#     entra sozinho.
#   - Não coleta credenciais nem envia dados para lugar nenhum; não executa
#     nada além de gravar esses arquivos em disco.
#   - Não instala programas (ffmpeg, Node, Python/uv): a skill confere isso no
#     primeiro uso e mostra o comando de cada um.
#   - Suas preferências ficam fora da pasta da skill (%USERPROFILE%\.claude\edicao-motion-triwer\)
#     e nunca são apagadas por uma atualização.
#   - Rodar de novo atualiza para a versão mais recente.

$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$SKILL = "edicao-motion-triwer"
$REPO = "https://raw.githubusercontent.com/paulovyn1/triwer-skills/main"
$TREE_URL = "https://api.github.com/repos/paulovyn1/triwer-skills/git/trees/main?recursive=1"
$SKILLS_DIR = if ($env:TRIWER_SKILLS_DIR) { $env:TRIWER_SKILLS_DIR } else { "$env:USERPROFILE\.claude\skills" }
$SKILL_DIR = "$SKILLS_DIR\$SKILL"
$VERSION_FILE = "$SKILL_DIR\VERSION"

function Write-Color($text, $color = "White") {
    Write-Host $text -ForegroundColor $color
}

Write-Host ""
Write-Color "╔══════════════════════════════════════╗" "Blue"
Write-Color "║   Triwer Skills — edicao-motion-triwer" "Blue"
Write-Color "╚══════════════════════════════════════╝" "Blue"
Write-Host ""

Write-Color "→ Verificando versão disponível..." "Yellow"
try {
    $REMOTE_VERSION = (Invoke-WebRequest -Uri "$REPO/$SKILL/VERSION" -UseBasicParsing).Content.Trim()
} catch {
    Write-Color "✗ Não foi possível conectar ao repositório. Verifique sua conexão." "Red"
    exit 1
}
Write-Color "   Versão disponível: $REMOTE_VERSION" "Green"

$INSTALLED_VERSION = ""
if (Test-Path $VERSION_FILE) {
    $INSTALLED_VERSION = (Get-Content $VERSION_FILE -Raw).Trim()
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

# Lista de arquivos da skill no repositório
Write-Color "→ Listando arquivos da skill..." "Yellow"
try {
    $tree = Invoke-RestMethod -Uri $TREE_URL -UseBasicParsing
} catch {
    Write-Color "✗ Não consegui listar os arquivos da skill. Tente de novo em alguns minutos." "Red"
    exit 1
}
$files = @($tree.tree | Where-Object { $_.type -eq "blob" -and $_.path.StartsWith("$SKILL/") })
if ($files.Count -eq 0) {
    Write-Color "✗ Nenhum arquivo encontrado para $SKILL." "Red"
    exit 1
}

Write-Color "→ Baixando $SKILL..." "Yellow"
$count = 0
foreach ($f in $files) {
    $rel = $f.path.Substring($SKILL.Length + 1)
    $dest = Join-Path $SKILL_DIR ($rel -replace "/", "\")
    # memoria.md é dado pessoal: nunca sobrescrever
    if ($rel -eq "memoria.md" -and (Test-Path $dest)) {
        Write-Color "   ↳ memoria.md mantido (seus dados pessoais)" "White"
        continue
    }
    $dir = Split-Path $dest
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    try {
        Invoke-WebRequest -Uri "$REPO/$($f.path)" -OutFile $dest -UseBasicParsing
    } catch {
        Write-Color "  ERRO ao baixar: $($f.path)" "Red"
        throw
    }
    $count++
}
Write-Color "   ↳ $count arquivos baixados" "White"

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
Write-Host "  1. Esta skill funciona no Claude Code (não no chat do Claude Desktop nem no claude.ai)."
Write-Host "  2. Abra o Claude Code na pasta do seu vídeo e peça, por exemplo:"
Write-Color "     edita esse vídeo no estilo Fala Dinâmica" "Yellow"
Write-Host "  3. No primeiro uso ela confere ffmpeg, Node, Python/uv e a chave do Groq"
Write-Host "     e mostra o comando de instalação do que faltar."
Write-Host ""
