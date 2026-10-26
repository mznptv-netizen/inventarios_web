@echo off
cd /d "%~dp0"
echo Cierra primero la ventana del servidor anterior.
echo Esta opcion recupera el acceso administrador desde este computador.
pause
"%~dp0INVENTARIOS_IPSICOL.exe" --reset-admin
pause
