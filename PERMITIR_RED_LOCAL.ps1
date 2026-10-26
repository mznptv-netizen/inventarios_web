# Ejecutar una sola vez desde PowerShell como administrador.
# Solo permite conexiones TCP 5000 en redes Privadas desde la subred local.
$ErrorActionPreference = 'Stop'
$name = 'IPSICOL-Flask-LAN-5000'
if (-not (Get-NetFirewallRule -Name $name -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -Name $name -DisplayName 'IPSICOL - Navegadores de red local' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000 -Profile Private -RemoteAddress LocalSubnet
}
Write-Host 'Regla lista. La conexion del servidor debe estar marcada como red Privada.'
Write-Host 'No es necesario abrir puertos en el router.'
