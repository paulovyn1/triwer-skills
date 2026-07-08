# =============================================================
# Triwer Skills — Instalador completo do ecossistema (Windows/PowerShell)
# =============================================================
#
# Instala (ou atualiza) todas as skills Triwer de uma vez só, na ordem
# recomendada. Cada skill mantém seu próprio instalador — este script só
# encadeia todos, para quem quer instalar tudo com um comando.
#
# Rodar de novo a qualquer momento atualiza só o que tiver versão nova
# (mesmo comportamento dos instaladores individuais). memoria.md pessoal de
# cada skill nunca é sobrescrito.

$ErrorActionPreference = "Stop"

$REPO = "https://raw.githubusercontent.com/paulovyn1/triwer-skills"

function Write-Color($text, $color = "White") {
    Write-Host $text -ForegroundColor $color
}

Write-Host ""
Write-Color "╔════════════════════════════════════════════╗" "Blue"
Write-Color "║   Triwer Skills — Instalação completa      ║" "Blue"
Write-Color "╚════════════════════════════════════════════╝" "Blue"
Write-Host ""
Write-Host "Isso vai instalar (ou atualizar) todas as skills do ecossistema Triwer,"
Write-Host "na ordem recomendada de uso."
Write-Host ""

$INSTALLERS = @(
    @{ Name = "Onboarding"; Path = "main/scripts/instalar-onboarding-windows.ps1" },
    @{ Name = "Estilo Forge"; Path = "main/estilo-forge/scripts/instalar-windows.ps1" },
    @{ Name = "Dr. House (avaliação)"; Path = "main/scripts/instalar-drhouse-windows.ps1" },
    @{ Name = "Oráculo (público)"; Path = "main/scripts/instalar-oraculo-windows.ps1" },
    @{ Name = "Sexy (promessa)"; Path = "main/scripts/instalar-sexy-windows.ps1" },
    @{ Name = "Prisma (viés/posicionamento)"; Path = "main/scripts/instalar-prisma-windows.ps1" },
    @{ Name = "Histórias"; Path = "main/scripts/instalar-historias-windows.ps1" },
    @{ Name = "MDI"; Path = "main/scripts/instalar-mdi-windows.ps1" },
    @{ Name = "Carrossel"; Path = "main/scripts/instalar-carrossel-windows.ps1" },
    @{ Name = "CTA"; Path = "main/scripts/instalar-cta-windows.ps1" },
    @{ Name = "Notion Zettelkasten"; Path = "main/scripts/instalar-zettelkasten-windows.ps1" }
)

$TOTAL = $INSTALLERS.Count
$CURRENT = 0
$FAILED = @()

foreach ($installer in $INSTALLERS) {
    $CURRENT++
    Write-Color "[$CURRENT/$TOTAL] $($installer.Name)" "Blue"

    # Cada instalador individual roda num processo powershell.exe FILHO, isolado,
    # via -EncodedCommand (Base64 de UTF-16). Isso evita tres problemas reais:
    # (1) rodar via Invoke-Expression no mesmo escopo fazia cada instalador
    # redefinir $REPO com um valor diferente do deste script, "vazando" para as
    # iteracoes seguintes do loop e quebrando as URLs de download; (2) um
    # "exit 0"/"exit 1" dentro do instalador individual (ex.: quando a skill ja
    # esta na versao mais recente) encerraria este script inteiro, nao so
    # aquele item do loop; (3) gravar o script baixado num arquivo .ps1 em
    # disco e rodar via -File exige que o PowerShell 5.1 detecte a codificacao
    # certa (sem BOM ele assume o codepage ANSI do sistema, corrompendo
    # caracteres especiais e ate quebrando o parser) -- -EncodedCommand evita
    # esse problema por completo, sem tocar em disco.
    try {
        $scriptContent = (Invoke-WebRequest -Uri "$REPO/$($installer.Path)" -UseBasicParsing).Content
        # Os .ps1 individuais sao salvos com BOM (necessario para rodarem sozinhos
        # via -File, ver comentario acima). Aqui o BOM sobrevive dentro da string
        # e, colado direto no inicio do -EncodedCommand, faz o parser tentar
        # executar "<BOM>#" como comando antes de reconhecer o comentario --
        # remover antes de codificar.
        $scriptContent = $scriptContent.TrimStart([char]0xFEFF)
        $encodedCommand = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($scriptContent))

        & powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand $encodedCommand
        if ($LASTEXITCODE -ne 0) {
            throw "instalador retornou codigo $LASTEXITCODE"
        }
        Write-Host ""
    } catch {
        Write-Color "Falha ao instalar: $($installer.Name) - $($_.Exception.Message)" "Red"
        Write-Host ""
        $FAILED += $installer.Name
    }
}

Write-Host ""
if ($FAILED.Count -eq 0) {
    Write-Color "╔════════════════════════════════════════════╗" "Green"
    Write-Color "║   ✓ Instalação completa concluída!         ║" "Green"
    Write-Color "╚════════════════════════════════════════════╝" "Green"
} else {
    Write-Color "╔════════════════════════════════════════════╗" "Yellow"
    Write-Color "║   ⚠ Concluído com pendências               ║" "Yellow"
    Write-Color "╚════════════════════════════════════════════╝" "Yellow"
}
Write-Host ""

if ($FAILED.Count -gt 0) {
    Write-Color "Não foi possível instalar:" "Yellow"
    foreach ($f in $FAILED) {
        Write-Host "  - $f"
    }
    Write-Host ""
}

Write-Color "Próximos passos:" "Blue"
Write-Host "  1. Abra uma nova conversa"
Write-Color "     e digite: /onboarding-triwer" "Yellow"
Write-Host ""
Write-Host "  2. Siga o fluxo — ele configura seu Notion e libera as outras skills"
Write-Host ""
Write-Host "  3. Ordem recomendada de uso depois do onboarding:"
Write-Host "     estilo-forge -> dr-house-triwer -> oraculo-triwer -> sexy-triwer ->"
Write-Host "     prisma-triwer -> historias-triwer (continua) -> mdi-triwer ->"
Write-Host "     carrossel-triwer -> cta-triwer"
Write-Host ""
