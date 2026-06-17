@echo off
title Atlas Voice
cd /d C:\Users\Gleida\Desktop\atlas-voice-v1
call conda activate atlasvoice

echo.
echo  ██████████████████████████████████████
echo   ATLAS VOICE — Iniciando...
echo  ██████████████████████████████████████
echo.

start "" "http://127.0.0.1:8000/dashboard"

:loop
echo [Atlas] Backend iniciando...
uvicorn api:app --host 0.0.0.0 --port 8000
echo.
echo [Atlas] Backend caiu. Reiniciando em 3 segundos...
timeout /t 3 /nobreak >nul
goto loop
