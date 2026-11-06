@echo off
cd /d "%~dp0"
title Atualizar Pacote de Distribuicao Slayin PS Vita
echo ========================================================
echo   Slayin PS Vita - Atualizador do Pacote de Lancamento
echo ========================================================
echo.
python dev_update.py
if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu uma falha ao atualizar o pacote.
    pause
    exit /b 1
)
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
