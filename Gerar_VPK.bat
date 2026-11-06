@echo off
cd /d "%~dp0"
title Slayin PS Vita - Gerador de VPK
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0patcher.ps1"
if errorlevel 1 (
    echo.
    echo Pressione qualquer tecla para sair...
    pause >nul
    exit /b 1
)
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul
