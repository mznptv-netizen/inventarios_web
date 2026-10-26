# INVENTARIOS IPSICOL · Servidor web para Windows

Versión Flask + Waitress + SQLite. Preparada el 26 de octubre de 2026.

## 1. Qué vas a tener

Un solo computador ejecuta INVENTARIOS_IPSICOL.exe y guarda la base SQLite y los documentos. Los demás equipos abren la aplicación en Chrome, Edge u otro navegador, sin instalar Python ni copiar la base. Puedes seguir usando Windows 10 de 64 bits.

Se conservan la paleta blanco/magenta, el logo de la caja con IPSICOL, el menú lateral, las cuatro secciones, las tablas centradas y la letra legible. Los controles están adaptados al navegador y a pantallas pequeñas; no es una ventana de CustomTkinter incrustada.

La información se guarda inmediatamente en el servidor. Las tablas y el stock de selección se consultan automáticamente cada 5 segundos, mientras la pestaña esté visible. Los formularios y listas de entrega no se borran al actualizar. Esto es actualización periódica, no transmisión instantánea: otro usuario puede tardar hasta unos 5 segundos en ver un cambio. Al guardar siempre se verifica el stock real de nuevo.

## 2. Archivos que debes subir a GitHub

Extrae el ZIP y sube su **contenido**, sin ponerlo dentro de una carpeta extra:

- `ipsicol.py` en la raíz.
- `requirements.txt` en la raíz.
- `.github/workflows/build.yml` en esa ruta exacta.
- `INICIAR_SERVIDOR.bat`, `INICIAR_TUNEL.bat`, `CAMBIAR_BASE.bat`, `RESTABLECER_ADMIN.bat`.
- `PERMITIR_RED_LOCAL.ps1`, `GUIA.md`, `LEEME_PRIMERO.txt`, `.gitignore`.
- `COMPILAR_LOCAL.bat` es opcional: solo se usa si deseas compilar en tu Windows con Python 3.12 instalado.

**Reemplaza también requirements.txt y build.yml. No sirve conservar el flujo de compilación de la aplicación de escritorio.** Ahora debe incluir Flask/Waitress y probar `web`/`http`, no `gui`.

No subas la base `.db`/`.sqlite3`, la carpeta `soportes`, contraseñas, archivos de configuración ni copias de seguridad a GitHub. `.gitignore` ayuda con Git; al subir archivos manualmente, selecciona solo los archivos de código de este paquete.

Si GitHub no muestra la carpeta `.github` al cargarla: entra a **Add file → Create new file**, escribe `.github/workflows/build.yml` como nombre y copia dentro el contenido del archivo incluido.

## 3. Descargar el ejecutable desde GitHub

1. Guarda los archivos en tu rama `main` o `master`.
2. Abre **Actions → Compilar IPSICOL Flask para Windows**.
3. La compilación se inicia al subir cambios. También puedes pulsar **Run workflow**.
4. Espera a que termine en verde.
5. Abre esa ejecución y, en **Artifacts**, descarga **INVENTARIOS_IPSICOL-FLASK-Windows-x64**.
6. Extrae el ZIP completo en una carpeta del computador servidor, por ejemplo `C:\IPSICOL_SERVIDOR`.
7. Dentro verás `INVENTARIOS_IPSICOL.exe`, los accesos `.bat` y la guía.

GitHub instala Python solo en su equipo de compilación. El servidor y los clientes no necesitan instalarlo. El EXE se compila en Windows, incluye sus dependencias y utiliza el icono integrado de la caja IPSICOL. No necesitas subir un logo adicional.

Este paquete no contiene todavía un EXE de Windows probado en tu equipo. GitHub lo construirá y ejecutará una prueba del propio EXE antes de publicarlo. La prueba usa una base temporal, inicia un puerto local de prueba y valida login, páginas, SQLite, PDF e iconos.

## 4. Preparar tu base anterior sin perder los soportes

1. Cierra la aplicación anterior en **todos** los computadores.
2. Haz una copia del archivo `.db` o `.sqlite3` y de la carpeta `soportes` que está junto a él.
3. En el computador servidor crea, por ejemplo, `C:\IPSICOL_DATOS`.
4. Copia ahí la base y la carpeta `soportes`, manteniendo los nombres de sus archivos.
5. La base debe quedar en el **disco local del servidor**, no en una ruta `\\OTRO-PC\...`, unidad de red, ni una carpeta sincronizada por OneDrive/Dropbox.
6. No abras esa base simultáneamente con el programa anterior. A partir de ahora, todos trabajan desde el navegador.

No necesitas compartir por SMB la base ni instalar el programa en cada cliente. Los navegadores hablan con Flask; solo este servidor abre SQLite. Los datos no se envían a Supabase ni a otra base en la nube.

El código conserva las tablas y aplica actualizaciones aditivas. Guarda una copia `nombre.db.antes_flask_v1.bak` antes de la preparación web en el arranque; esa copia automática es solo de SQLite. Tu respaldo manual inicial y el respaldo descargable incluyen también `soportes`.

## 5. Primer inicio en el computador servidor

1. Abre `INVENTARIOS_IPSICOL.exe` o `INICIAR_SERVIDOR.bat`.
2. Elige **Seleccionar base existente** y busca tu `.db` o `.sqlite3` local. Si empezarás desde cero, usa **Crear una base nueva**.
3. Si hay una ruta guardada por la versión anterior, se intentará abrir. Para elegir otra, cierra el servidor y usa `CAMBIAR_BASE.bat`. Si la ruta anterior ya no existe o era de red, utiliza el selector para elegir la copia local; no se crea una base vacía sustituta.
4. Se abrirá la configuración local del administrador: elige usuario y una contraseña de al menos 12 caracteres; escríbela dos veces. El usuario sugerido es `ADMIN`, pero **no existe una contraseña predeterminada**.
5. Se abrirá el navegador en `http://127.0.0.1:5000`.
6. Entra con la cuenta que acabas de crear.
7. En **Usuarios**, crea una cuenta independiente para cada persona.

La base seleccionada se recuerda en este servidor. Los demás usuarios no eligen una base al iniciar sesión: todos acceden a la misma.

Mantén abierta la ventana del servidor; es normal que también aparezca una consola. Cerrarla detiene la aplicación para todos. Para detener de forma normal usa **Ctrl+C** en esa ventana. Si cambias de base o reinicias, avisa a los usuarios para que guarden lo que estén llenando.

## 6. Acceder desde la misma red

1. El servidor muestra una o varias direcciones como `http://192.168.1.50:5000`. Si aparecen varias, usa la IP del adaptador Wi-Fi o Ethernet que comparte red con los usuarios.
2. También puedes abrir CMD y escribir `ipconfig`; busca la **Dirección IPv4** de ese adaptador.
3. En otro equipo de la misma red abre esa dirección en Chrome o Edge.
4. Inicia sesión con su cuenta.

Si no abre:

- Comprueba primero que `http://127.0.0.1:5000` funciona en el servidor.
- En Windows marca tu red de confianza como **Privada**.
- Abre PowerShell **como administrador** y ejecuta una vez:

```powershell
New-NetFirewallRule -Name "IPSICOL-Flask-LAN-5000" -DisplayName "IPSICOL - Navegadores de red local" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000 -Profile Private -RemoteAddress LocalSubnet
```

El mismo comando está en `PERMITIR_RED_LOCAL.ps1`. Es una regla de entrada solo para la subred local y redes privadas; no abre el router. Si ya existe, no hace falta crearla de nuevo.

- Evita la red Wi-Fi de invitados: suele aislar los dispositivos.
- Si DHCP cambia la IP del servidor, usa la dirección nueva. Una reserva DHCP en el router, si puedes configurarla, facilita mantener la dirección.
- El acceso local del ejemplo usa HTTP: utiliza una red de confianza. También puedes usar el enlace HTTPS de Cloudflare desde la oficina.

## 7. Acceder desde Internet con Cloudflare

El computador servidor necesita Internet y debe permanecer encendido. Los usuarios remotos solo necesitan navegador e Internet.

1. Deja funcionando `INVENTARIOS_IPSICOL.exe`.
2. Descarga `cloudflared` para **Windows de 64 bits** desde la página oficial:
   https://developers.cloudflare.com/tunnel/downloads/
3. Si descargas el ejecutable con un nombre como `cloudflared-windows-amd64.exe`, cámbialo a **cloudflared.exe** y colócalo junto a `INICIAR_TUNEL.bat`.
4. Abre **INICIAR_TUNEL.bat**. También puedes abrir CMD en esa carpeta y ejecutar:

```bat
cloudflared.exe tunnel --url http://127.0.0.1:5000
```

5. Espera hasta que aparezca una URL con formato `https://...trycloudflare.com`.
6. Copia esa URL completa y entrégala a las personas autorizadas, junto con sus cuentas individuales.
7. Comprueba el acceso desde el celular con datos móviles, sin Wi-Fi, para verificar que realmente funciona desde fuera.

No abras el puerto 5000 en el router. No apuntes el túnel a archivos de la base: su destino es el servidor HTTP de la aplicación. Los documentos y PDF también requieren sesión.

**Debes mantener abiertas las dos ventanas:** IPSICOL y Cloudflare. El enlace deja de servir al cerrar el túnel, apagar el servidor o suspender el computador.

### Qué permite el enlace gratuito temporal

Quick Tunnel no requiere un dominio propio ni una cuenta Cloudflare para la prueba básica. La URL cambia cada vez que creas el túnel. No tiene garantía de disponibilidad, tiene un límite de 200 solicitudes simultáneas en curso y no admite SSE. Esta aplicación usa consultas periódicas HTTP, así que no depende de SSE.

Cloudflare indica que Quick Tunnels son para pruebas y desarrollo. Para un enlace estable de uso diario, configura un túnel permanente con un hostname que controles; el dominio puede tener un costo aparte. El programa es compatible con ambos: el servicio debe seguir apuntando a `http://127.0.0.1:5000`.

Si cloudflared ya estaba configurado y no inicia un túnel rápido, revisa su archivo de configuración y los mensajes de esa ventana; no borres configuraciones anteriores sin respaldarlas. La aplicación no instala ni modifica Cloudflare automáticamente.

## 8. Funciones del inventario

- **Crear inventario = ingreso:** incluye nombre, regional, fecha, responsable, destino/taller, varios proveedores, NIT y documentos. Genera número independiente de ingreso y código por proveedor.
- **Añadir productos:** quedan dentro del mismo ingreso, sin crear una factura distinta por cada producto.
- **Editar inventario:** permite cambiar nombre y regional, manteniendo productos y cantidades. Si otro usuario lo modifica antes de guardar, pide recargar.
- **Datos del ingreso:** permite completar destino, responsable, fecha y proveedores conservando los ya registrados. También detecta ediciones simultáneas.
- **Mayúsculas:** nombres, responsables, destinos y motivos se guardan en mayúsculas; las contraseñas y rutas conservan sus caracteres.
- **Eliminar productos/inventarios:** retira existencias activas, conservando salidas y documentos históricos; solicita confirmación.
- **Salidas múltiples:** añade productos de varios inventarios, revisa cantidades y registra la entrega completa.
- **Añadir todo el inventario:** llena la lista con el stock disponible. Repetir el botón reemplaza las cantidades de ese inventario y conserva los productos de los demás; no acumula duplicados. Aún debes confirmar la entrega.
- **Validación de stock:** SQLite valida y descuenta toda la entrega en una transacción. Si una línea falla, no se guarda ninguna. Cada reintento de la misma entrega utiliza una clave para impedir otro descuento, incluso si el servidor reinicia.
- **Consultas:** filtros por regional, inventario, producto, ubicación, fechas, estado, persona, destino y número de factura. Hasta 100 filas por página y tabla alta.
- **Devolver:** en Ver detalle, elige solo ese producto o todos los productos vigentes de la entrega, incluso de diferentes inventarios. La devolución restaura las existencias una sola vez.
- **Eliminar anuladas:** selecciona una o varias anuladas en Consultas y confirma el borrado definitivo. No descuenta ni aumenta otra vez el stock. No permite borrar salidas vigentes.
- **Adjuntar factura posterior:** abre la salida → Ver detalle → elige archivo → Guardar documento. Permite PDF e imágenes, máximo 25 MB cada uno. Se guarda una copia interna.
- **Imprimir:** abre la factura o la constancia del inventario, elige cada firma opcional y descarga el PDF. Abre el PDF y usa Ctrl+P. Incluye únicamente el logo IPSICOL y cuatro líneas de observaciones para esfero. Sin marcas de firma no aparecen espacios de firma.
- **Documentos originales:** se descargan desde su registro. Las salidas de una misma entrega pueden tener documentos distintos; también se permite adjuntar a la factura del grupo.

Los documentos denominados “facturas” en la interfaz son **constancias internas de inventario**. La aplicación no emite ni valida facturación electrónica DIAN.

## 9. Usuarios, respaldo y recuperación

**Roles:**

- Administrador: funciones del inventario, usuarios y respaldo completo.
- Operador: inventarios, ingresos, salidas, devoluciones, adjuntos y PDF.
- Consulta: lectura, documentos y PDF; sin cambios de existencias.

Las contraseñas se almacenan como hashes con sal, no como texto plano. No hay cuentas secretas ni credenciales hardcodeadas de producción. Las credenciales visibles en el código de pruebas solo crean cuentas dentro de carpetas temporales.

Las sesiones duran hasta 8 horas desde el acceso. Un cambio/restablecimiento de contraseña o una desactivación invalida sus sesiones anteriores. Tras 8 intentos fallidos se bloquea temporalmente el usuario por 5 minutos. Los formularios incluyen protección CSRF.

**Respaldo:** entra como administrador en **Servidor y respaldo → Descargar respaldo completo**. El ZIP contiene una copia coherente de la base y sus soportes. Descárgalo con frecuencia a otro disco. No es un respaldo automático programado.

**Restaurar:** detén servidor y túnel, extrae el respaldo en una carpeta local y usa `CAMBIAR_BASE.bat` para seleccionarlo. Mantén base y `soportes` juntos. Los respaldos contienen usuarios y hashes de contraseña; no los publiques.

**Olvidé la contraseña:** cierra el servidor y ejecuta `RESTABLECER_ADMIN.bat` físicamente en ese computador. Crea o restablece el administrador y vuelve a iniciar. No existe una ruta de recuperación pública por Internet.

**Configuración y errores:** `%LOCALAPPDATA%\INVENTARIOS_IPSICOL` contiene `configuracion.json`, `servidor_secret.key` e `ipsicol_servidor.log`. La base y los soportes están en la carpeta local que elegiste. No borres la clave mientras el servidor funciona; cambiarla invalida las sesiones.

## 10. Operación diaria y diagnóstico

- Evita que el servidor entre en suspensión mientras otras personas trabajan. Apagar solamente el monitor no afecta al servidor.
- No ejecutes dos copias del servidor sobre la misma base. El programa detecta ese caso.
- Para actualizar el EXE: guarda un respaldo, detén el servidor, reemplaza el ejecutable y vuelve a abrirlo. No reemplaces la base ni los soportes por los de pruebas.
- Si el puerto 5000 está ocupado, cierra el programa que lo utiliza. Como alternativa técnica puedes arrancar con `INVENTARIOS_IPSICOL.exe --port 5001`, pero deberás cambiar también el puerto en la URL, la regla de firewall y el túnel.
- Si la base está ocupada, se devuelve un mensaje para reintentar; no se acepta una entrega parcial.
- Si dice “sesión vencida”, vuelve a iniciar sesión. Si la red se corta, el indicador mostrará que no está conectado.
- Las listas de entrega están en memoria de la pestaña: guarda o termina el trabajo antes de cerrarla. No se comparten borradores entre usuarios ni se guardan contraseñas en el navegador por parte de la aplicación.
- En redes lentas, una descarga grande puede tardar. La copia completa incluye todos los soportes y necesita memoria proporcional a su tamaño en el servidor.
- SQLite permite múltiples lectores y serializa las escrituras. Es adecuado para este servidor pequeño; no es una solución de alta disponibilidad. Si crecen mucho los usuarios o el volumen, se puede migrar posteriormente a PostgreSQL.

## 11. Validación y límites de esta entrega

Se ejecutaron las pruebas del núcleo y de las rutas web, además de un flujo real en Chromium con dos sesiones. Se revisaron PDF con/sin firmas, proveedores, NIT, destino y observaciones a mano. Se comprobó que no se pierden los datos del formulario al actualizar las tablas.

La comprobación disponible se realizó en Linux. El EXE de Windows y los permisos de firewall deben comprobarse en GitHub y después en tu computador. No se configuró una cuenta Cloudflare ni se publicó un túnel real desde tu red. No se incluyeron tus datos reales ni se abrió ningún puerto en tu equipo.

## Referencias oficiales

- Flask/Waitress para Windows: https://flask.palletsprojects.com/en/stable/deploying/waitress/
- Cloudflare: descarga oficial: https://developers.cloudflare.com/tunnel/downloads/
- Cloudflare Quick Tunnels: https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/
- SQLite y acceso por red: https://www.sqlite.org/useovernet.html
- Artefactos de GitHub Actions: https://github.com/actions/upload-artifact
