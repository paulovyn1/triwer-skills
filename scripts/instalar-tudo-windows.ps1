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
#
# O que este script faz (leia antes de rodar):
#   - Baixa, um de cada vez, os 12 instaladores individuais abaixo do
#     repositório público https://github.com/paulovyn1/triwer-skills e
#     salva cada um em arquivo temporário (%TEMP%) antes de rodar -- nada
#     é executado sem primeiro existir em disco, então dá pra abrir e ler
#     qualquer um deles antes ou durante a instalação.
#   - Cada instalador baixado só grava arquivos de texto (.md, VERSION) em
#     %USERPROFILE%\.claude\skills\<skill>\. Não coleta credenciais, não
#     envia dados para lugar nenhum.
#   - Nunca sobrescreve memoria.md (seus dados pessoais ficam intactos).

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
    @{ Name = "Notion Zettelkasten"; Path = "main/scripts/instalar-zettelkasten-windows.ps1" },
    @{ Name = "Leitura Ativa"; Path = "main/scripts/instalar-leitura-ativa-windows.ps1" }
)

$TOTAL = $INSTALLERS.Count
$CURRENT = 0
$FAILED = @()

foreach ($installer in $INSTALLERS) {
    $CURRENT++
    Write-Color "[$CURRENT/$TOTAL] $($installer.Name)" "Blue"

    # Cada instalador individual e baixado para um arquivo .ps1 real em
    # %TEMP% (os .ps1 do repo ja sao salvos com BOM, entao o PowerShell 5.1
    # detecta a codificacao certa via -File sem precisar de -EncodedCommand).
    # Rodar via "powershell.exe -File" num processo FILHO ainda garante que:
    # (1) $REPO definido dentro do instalador nao vaza para as proximas
    # iteracoes deste loop, porque cada processo filho tem seu proprio escopo;
    # (2) um "exit 0"/"exit 1" dentro do instalador individual encerra so o
    # processo filho, nao este script inteiro.
    $tempScript = Join-Path $env:TEMP "triwer-instalador-$($installer.Name -replace '[^a-zA-Z0-9]', '')-$PID.ps1"
    try {
        Invoke-WebRequest -Uri "$REPO/$($installer.Path)" -OutFile $tempScript -UseBasicParsing

        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $tempScript
        if ($LASTEXITCODE -ne 0) {
            throw "instalador retornou codigo $LASTEXITCODE"
        }
        Write-Host ""
    } catch {
        Write-Color "Falha ao instalar: $($installer.Name) - $($_.Exception.Message)" "Red"
        Write-Host ""
        $FAILED += $installer.Name
    } finally {
        if (Test-Path $tempScript) {
            Remove-Item $tempScript -Force -ErrorAction SilentlyContinue
        }
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
