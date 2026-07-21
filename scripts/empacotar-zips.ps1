# =============================================================
# Triwer Skills — Empacota cada skill em um .zip para upload manual
# (uso do mantenedor — gera dist/, não é para o aluno rodar)
# =============================================================
#
# Cada .zip contém a pasta da skill pronta para upload na tela de Skills
# do claude.ai (Settings -> Capabilities -> Skills -> Upload skill).
# Formato exato aceito pelo claude.ai ainda não foi confirmado na prática
# (Bloco 9.2 do plano de arquitetura) -- ajustar este script se o claude.ai
# esperar uma estrutura diferente (ex: zip sem pasta-raiz, ou só o SKILL.md).

$ErrorActionPreference = "Stop"

$ROOT = Split-Path -Parent $PSScriptRoot
$DIST = Join-Path $ROOT "dist"

$SKILLS = @(
    "onboarding-triwer",
    "estilo-forge",
    "dr-house-triwer",
    "oraculo-triwer",
    "sexy-triwer",
    "prisma-triwer",
    "historias-triwer",
    "mdi-triwer",
    "carrossel-triwer",
    "cta-triwer",
    "notion-zettelkasten-si"
)

Write-Host ""
Write-Host "Empacotando skills para upload manual (claude.ai)..." -ForegroundColor Blue
Write-Host ""

if (Test-Path $DIST) {
    Remove-Item -Recurse -Force $DIST
}
New-Item -ItemType Directory -Force -Path $DIST | Out-Null

foreach ($skill in $SKILLS) {
    $skillPath = Join-Path $ROOT $skill
    if (-not (Test-Path $skillPath)) {
        Write-Host "  pulando $skill (pasta não encontrada)" -ForegroundColor Yellow
        continue
    }

    $zipPath = Join-Path $DIST "$skill.zip"

    # Copia para uma pasta temporária excluindo dados pessoais (memoria.md)
    # e scripts próprios (não fazem sentido dentro do zip de upload manual).
    $tempDir = Join-Path $env:TEMP "triwer-pack-$skill"
    if (Test-Path $tempDir) { Remove-Item -Recurse -Force $tempDir }
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

    Copy-Item -Path "$skillPath\*" -Destination $tempDir -Recurse -Force `
        -Exclude @("memoria.md", "scripts", ".git", "*.zip", "_draft-redesign")

    # Compress-Archive grava os caminhos internos do zip com "\" (separador do
    # Windows) em vez de "/" (exigido pelo formato ZIP) -- o validador de
    # upload do claude.ai rejeita isso como "path with invalid characters".
    # Por isso montamos o zip manualmente via System.IO.Compression, forçando
    # "/" em cada nome de entrada.
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $fs = [System.IO.File]::Open($zipPath, [System.IO.FileMode]::Create)
    $archive = New-Object System.IO.Compression.ZipArchive($fs, [System.IO.Compression.ZipArchiveMode]::Create)
    Get-ChildItem -Path $tempDir -Recurse -File | ForEach-Object {
        $relPath = $_.FullName.Substring($tempDir.Length + 1).Replace([char]92, [char]47)
        $entry = $archive.CreateEntry($relPath, [System.IO.Compression.CompressionLevel]::Optimal)
        $entryStream = $entry.Open()
        $fileStream = [System.IO.File]::OpenRead($_.FullName)
        $fileStream.CopyTo($entryStream)
        $fileStream.Dispose()
        $entryStream.Dispose()
    }
    $archive.Dispose()
    $fs.Dispose()

    Remove-Item -Recurse -Force $tempDir

    Write-Host "  ✓ $skill.zip" -ForegroundColor Green
}

Write-Host ""
Write-Host "Pronto. Arquivos em: $DIST" -ForegroundColor Blue
Write-Host "Suba esses .zip numa Release do GitHub (ou na pasta dist/ versionada)" -ForegroundColor Blue
Write-Host "para os alunos baixarem e importarem manualmente no claude.ai." -ForegroundColor Blue
Write-Host ""
