# Slayin PS Vita - Construtor do VPK Oficial
# Requisitos: Apenas Windows padrao (PowerShell). Sem SDK, sem Python, sem instalacoes.

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "         SLAYIN PS VITA - GERADOR DE PACOTE VPK            " -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 1. Localizar o APK
$apkFile = $null
$candidates = @("Slayin.apk", "slayin.apk", "Slayin_v1.0.apk")
foreach ($c in $candidates) {
    if (Test-Path (Join-Path $ScriptDir $c)) {
        $apkFile = Join-Path $ScriptDir $c
        break
    }
}

if (-not $apkFile) {
    # Procura qualquer .apk na pasta
    $anyApk = Get-ChildItem -Path $ScriptDir -Filter "*.apk" -File | Select-Object -First 1
    if ($anyApk) {
        $apkFile = $anyApk.FullName
    }
}

if (-not $apkFile) {
    Write-Host "[ERRO] Arquivo 'Slayin.apk' nao encontrado nesta pasta!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instrucoes:" -ForegroundColor White
    Write-Host "1. Copie o arquivo 'Slayin.apk' original do seu Android para esta mesma pasta." -ForegroundColor Gray
    Write-Host "2. Execute o 'Gerar_VPK.bat' novamente." -ForegroundColor Gray
    Write-Host ""
    Exit 1
}

$encFile = Join-Path $ScriptDir "assets.enc"
$baseDir = Join-Path $ScriptDir "base"
$outputVpk = Join-Path $ScriptDir "Slayin.vpk"

if (-not (Test-Path $encFile)) {
    Write-Host "[ERRO] Arquivo 'assets.enc' nao encontrado!" -ForegroundColor Red
    Exit 1
}

if (-not (Test-Path $baseDir)) {
    Write-Host "[ERRO] Pasta 'base' com os binarios da engine nao encontrada!" -ForegroundColor Red
    Exit 1
}

Write-Host "[1/4] Lendo e verificando '$([System.IO.Path]::GetFileName($apkFile))'..." -ForegroundColor Green
$apkBytes = [System.IO.File]::ReadAllBytes($apkFile)
$sha = [System.Security.Cryptography.SHA256]::Create()
$key = $sha.ComputeHash($apkBytes)
$hashHex = ([System.BitConverter]::ToString($key) -replace "-","").ToLower()

Write-Host "      Chave SHA-256: $hashHex" -ForegroundColor Gray

# 2. Descriptografar assets.enc
Write-Host "[2/4] Descriptografando assets com AES-256..." -ForegroundColor Green
$allEnc = [System.IO.File]::ReadAllBytes($encFile)
if ($allEnc.Length -le 16) {
    Write-Host "[ERRO] Arquivo assets.enc corrompido!" -ForegroundColor Red
    Exit 1
}

$iv = New-Object byte[] 16
[System.Array]::Copy($allEnc, 0, $iv, 0, 16)
$cipherLen = $allEnc.Length - 16
$cipherBytes = New-Object byte[] $cipherLen
[System.Array]::Copy($allEnc, 16, $cipherBytes, 0, $cipherLen)

$plainBytes = $null
try {
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.KeySize = 256
    $aes.BlockSize = 128
    $aes.Key = $key
    $aes.IV = $iv
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7

    $decryptor = $aes.CreateDecryptor()
    $plainBytes = $decryptor.TransformFinalBlock($cipherBytes, 0, $cipherLen)
    $decryptor.Dispose()
    $aes.Dispose()
} catch {
    Write-Host ""
    Write-Host "[ERRO] Falha na descriptografia!" -ForegroundColor Red
    Write-Host "O APK fornecido nao corresponde a versao original esperada de Slayin." -ForegroundColor Yellow
    Write-Host "Certifique-se de estar usando o APK oficial intacto." -ForegroundColor Yellow
    Exit 1
}

Write-Host "      Assets descriptografados com sucesso ($([math]::Round($plainBytes.Length / 1MB, 2)) MB)!" -ForegroundColor Gray

# 3. Montar o Slayin.vpk
Write-Host "[3/4] Empacotando 'Slayin.vpk' compativel com VitaShell..." -ForegroundColor Green
if (Test-Path $outputVpk) {
    Remove-Item -Path $outputVpk -Force
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

# Abre o VPK como ZIP para escrita
$vpkZip = [System.IO.Compression.ZipFile]::Open($outputVpk, [System.IO.Compression.ZipArchiveMode]::Create)

# Adiciona arquivos da pasta base/
$baseFiles = Get-ChildItem -Path $baseDir -Recurse -File
foreach ($bf in $baseFiles) {
    $relPath = $bf.FullName.Substring($baseDir.Length).TrimStart("\", "/")
    # OBRIGATORIO: Barras POSIX / para VitaShell nao dar erro 0xFFFFFFFE
    $zipEntryPath = $relPath.Replace("\", "/")
    
    $entry = $vpkZip.CreateEntry($zipEntryPath, [System.IO.Compression.CompressionLevel]::Optimal)
    $entryStream = $entry.Open()
    $fileStream = [System.IO.File]::OpenRead($bf.FullName)
    $fileStream.CopyTo($entryStream)
    $fileStream.Dispose()
    $entryStream.Dispose()
}

# Descompacta e adiciona os assets descriptografados
$assetMemStream = New-Object System.IO.MemoryStream(,$plainBytes)
$assetZip = New-Object System.IO.Compression.ZipArchive($assetMemStream, [System.IO.Compression.ZipArchiveMode]::Read)

foreach ($assetEntry in $assetZip.Entries) {
    if ([string]::IsNullOrEmpty($assetEntry.Name)) { continue } # ignora diretorios
    $entryPath = $assetEntry.FullName.Replace("\", "/")
    
    $targetEntry = $vpkZip.CreateEntry($entryPath, [System.IO.Compression.CompressionLevel]::Optimal)
    $targetStream = $targetEntry.Open()
    $srcStream = $assetEntry.Open()
    $srcStream.CopyTo($targetStream)
    $srcStream.Dispose()
    $targetStream.Dispose()
}

$assetZip.Dispose()
$assetMemStream.Dispose()
$vpkZip.Dispose()

$finalSize = (Get-Item $outputVpk).Length
Write-Host "[4/4] Slayin.vpk gerado com sucesso! ($([math]::Round($finalSize / 1MB, 2)) MB)" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  TUDO PRONTO! O ARQUIVO 'Slayin.vpk' ESTA PRONTO." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Proximos passos:" -ForegroundColor White
Write-Host "1. Conecte seu PS Vita ao PC pelo VitaShell (USB ou FTP)." -ForegroundColor Gray
Write-Host "2. Copie o arquivo 'Slayin.vpk' para qualquer pasta do cartao (ex: ux0:download/)." -ForegroundColor Gray
Write-Host "3. No VitaShell, aperte X no 'Slayin.vpk' para instalar." -ForegroundColor Gray
Write-Host "4. Bom jogo a 60 FPS!" -ForegroundColor Green
Write-Host ""
