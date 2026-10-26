@echo off
cd /d "%~dp0"
echo Cierra primero la ventana del servidor anterior.
echo Los usuarios se desconectaran durante el cambio de base.
pause
"%~dp0INVENTARIOS_IPSICOL.exe" --choose-db
pause
