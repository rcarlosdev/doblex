@echo off
title Doblex SMU - Backend Keep Alive Worker
cd /d "%~dp0"

echo =======================================================
echo    DOBLEX SMU - INICIANDO TRABAJADOR KEEP-ALIVE
echo =======================================================
echo.

if exist "backend\.venv\Scripts\python.exe" (
    set "PY_BIN=backend\.venv\Scripts\python.exe"
) else (
    set "PY_BIN=python"
)

echo Usando ejecutable: %PY_BIN%
echo.

"%PY_BIN%" backend\scripts\keep_alive.py --interval 600

pause
