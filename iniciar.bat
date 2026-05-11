@echo off
title Atlas Voice
echo.
echo  ╔══════════════════════════════╗
echo  ║       ATLAS VOICE v1.0       ║
echo  ╚══════════════════════════════╝
echo.
echo  Iniciando servidor...

call conda activate atlasvoice

start "" http://127.0.0.1:8000/dashboard

cd /d "%~dp0"
uvicorn api:app --port 8000
