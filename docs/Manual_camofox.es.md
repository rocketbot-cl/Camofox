



# Camofox
  
Modulo para interactuar con Camofox Browser Server desde Rocketbot mediante API REST. Permite verificar el servidor, crear pestanas, navegar, obtener snapshots, hacer click, escribir texto y tomar screenshots.  

*Read this in other languages: [English](Manual_camofox.md), [Português](Manual_camofox.pr.md), [Español](Manual_camofox.es.md)*
  
![banner](imgs/Camofox_modulo.jpg)
## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  


## Descripción de los comandos

### Iniciar Servidor
  
Inicia el servidor de Camofox Browser en segundo plano.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base|URL del servidor Camofox. Por defecto http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|Ruta del servidor|Carpeta desde donde se iniciara el proceso de Camofox. Si se usa npm start, indicar la carpeta del repositorio camofox-browser.|C:\Users\pc\Downloads|
|Comando de inicio|Comando utilizado para iniciar Camofox. Por defecto npx -y @askjo/camofox-browser|npx -y @askjo/camofox-browser|
|Segundos de espera||20|
|Asignar resultado a variable||resultado|

### Verificar Servidor
  
Verifica si el servidor de Camofox esta activo y accesible.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base|URL del servidor Camofox. Por defecto http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|Asignar resultado a variable||resultado|

### Crear Pestana
  
Crea una nueva pestana de Camofox y abre la URL indicada.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|URL||https://example.com|
|Clave de sesion||default|
|Timeout de solicitud (segundos)||60|
|Asignar resultado a variable||resultado|

### Navegar
  
Navega una pestana existente de Camofox hacia una nueva URL.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID de pestana||tabId|
|URL||https://example.com|
|Asignar resultado a variable||resultado|

### Obtener Snapshot
  
Obtiene el snapshot accesible de una pestana de Camofox.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID de pestana||tabId|
|Asignar resultado a variable||resultado|

### Click
  
Hace click en un elemento usando su referencia del snapshot.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID de pestana||tabId|
|Referencia del elemento||e1|
|Asignar resultado a variable||resultado|

### Escribir Texto
  
Escribe texto en un elemento usando su referencia del snapshot.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID de pestana||tabId|
|Referencia del elemento||e1|
|Texto||Text to type|
|Presionar Enter despues de escribir|||
|Asignar resultado a variable||resultado|

### Screenshot
  
Obtiene una captura de pantalla de una pestana de Camofox.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID de pestana||tabId|
|Ruta de guardado (opcional)||C:\tmp\camofox_capture.png|
|Asignar resultado a variable||resultado|

### Detener Servidor
  
Detiene el servidor de Camofox Browser usando el PID del proceso.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|PID|PID devuelto por el comando Iniciar Servidor.|12345|
|Asignar resultado a variable||resultado|

### Descargar Archivo
  
Monitorea y captura descargas de forma nativa en la carpeta temporal de CamoFox en formatos Excel, PDF o TXT.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base|URL del servidor Camofox. Por defecto http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|ID Pestana|ID de la pestaña de CamoFox desde donde se ejecuta la descarga.|tab_1|
|Ruta de guardado|Ruta donde se guardará el archivo. Si no se especifica, por defecto se creará en el directorio actual con la extensión del formato elegido.|C:\Users\Downloads\cartola.xlsx|
|Tipo de Archivo|Formato a descargar Excel, PDF o TXT.||
|Sobrescribir si existe|||
|Asignar resultado a variable||resultado|

### Ejecutar JS
  
Ejecuta una expresion JavaScript en la pestana actual.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID de pestana||tabId|
|Expresion JS||JavaScript expression|
|Timeout de request||30|
|Asignar resultado a variable||resultado|

### Hover
  
Mueve el mouse sobre un elemento usando su referencia del snapshot o un selector CSS.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|URL base|URL del servidor Camofox. Por defecto http//localhost9377|http://localhost:9377|
|User ID|User ID utilizado al crear la pestana.|rb-test|
|ID de pestana||tabId|
|Referencia del elemento|Referencia del snapshot, por ejemplo e13. Usar referencia o selector.|e13|
|Selector CSS|Selector CSS. Se usa solo si no se informa referencia.|button.download|
|Asignar resultado a variable||resultado|
