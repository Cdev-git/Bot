@echo off
title Liquid Client installer
echo ========================================
echo  Liquid Client installer!
echo ========================================
echo.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Run this file as Administrator
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
$ErrorActionPreference = 'Stop'; ^
$repo = 'sigmaclient123-droid/LIQUID.CLIENT'; ^
Write-Host 'fetching latest release...' -ForegroundColor Cyan; ^
$latest = Invoke-RestMethod -Uri \"https://api.github.com/repos/$repo/releases/latest\" -Headers @{'User-Agent'='LIQUID-Downloader'}; ^
$dllAsset = $latest.assets ^| Where-Object { $_.name -like '*.dll' } ^| Select-Object -First 1; ^
if (-not $dllAsset) { Write-Host 'no .dll found in latest release' -ForegroundColor Red; exit 1 }; ^
$downloadUrl = $dllAsset.browser_download_url; ^
$fileName = $dllAsset.name; ^
Write-Host \"Found: $fileName\" -ForegroundColor Green; ^
Write-Host 'Downloading...' -ForegroundColor Cyan; ^
Invoke-WebRequest -Uri $downloadUrl -OutFile $fileName -UserAgent 'LIQUID-Downloader'; ^
Write-Host 'Download complete!' -ForegroundColor Green; ^
$target = 'C:\Program Files (x86)\Steam\steamapps\common\Gorilla Tag\BepInEx\plugins'; ^
if (!(Test-Path $target)) { New-Item -ItemType Directory -Path $target -Force ^| Out-Null }; ^
Move-Item -Path $fileName -Destination (Join-Path $target $fileName) -Force; ^
Write-Host \"Installed to: $target\$fileName\" -ForegroundColor Green

echo.
echo SUCCESS! dll is now in your plugins folder
echo Open GTAG to have the menu
echo Dm me on discord if there are errors
pause
