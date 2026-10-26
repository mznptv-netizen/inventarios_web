@echo off
cd /d "%~dp0"
title IPSICOL - CLOUDFLARE TUNNEL
if exist "%~dp0cloudflared.exe" (
  "%~dp0cloudflared.exe" tunnel --url http://127.0.0.1:5000
) else (
  where cloudflared >nul 2>nul
  if errorlevel 1 (
    echo No se encontro cloudflared.exe.
    echo Descargalo desde el enlace oficial que aparece en GUIA.md.
    echo Guardalo junto a este archivo con el nombre cloudflared.exe.
    pause
    exit /b 1
  )
  cloudflared tunnel --url http://127.0.0.1:5000
)
pause
