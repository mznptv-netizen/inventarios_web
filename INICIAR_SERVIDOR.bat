@echo off
cd /d "%~dp0"
title INVENTARIOS IPSICOL - SERVIDOR WEB
if not exist "INVENTARIOS_IPSICOL.exe" (
  echo Falta INVENTARIOS_IPSICOL.exe. Descarga y extrae el resultado de GitHub Actions.
  pause
  exit /b 1
)
"%~dp0INVENTARIOS_IPSICOL.exe"
pause
