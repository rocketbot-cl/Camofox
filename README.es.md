



# Camofox
  
Modulo para interactuar con Camofox Browser Server desde Rocketbot mediante API REST. Permite verificar el servidor, crear pestanas, navegar, obtener snapshots, hacer click, escribir texto y tomar screenshots.  

*Read this in other languages: [English](README.md), [Português](README.pr.md), [Español](README.es.md)*

## Como instalar este módulo
  
Para instalar el módulo en Rocketbot Studio, se puede hacer de dos formas:
1. Manual: __Descargar__ el archivo .zip y descomprimirlo en la carpeta modules. El nombre de la carpeta debe ser el mismo al del módulo y dentro debe tener los siguientes archivos y carpetas: \__init__.py, package.json, docs, example y libs. Si tiene abierta la aplicación, refresca el navegador para poder utilizar el nuevo modulo.
2. Automática: Al ingresar a Rocketbot Studio sobre el margen derecho encontrara la sección de **Addons**, seleccionar **Install Mods**, buscar el modulo deseado y presionar install.  


## Overview


1. Iniciar Servidor  
Inicia el servidor de Camofox Browser en segundo plano.

2. Verificar Servidor  
Verifica si el servidor de Camofox esta activo y accesible.

3. Crear Pestana  
Crea una nueva pestana de Camofox y abre la URL indicada.

4. Navegar  
Navega una pestana existente de Camofox hacia una nueva URL.

5. Obtener Snapshot  
Obtiene el snapshot accesible de una pestana de Camofox.

6. Click  
Hace click en un elemento usando su referencia del snapshot.

7. Escribir Texto  
Escribe texto en un elemento usando su referencia del snapshot.

8. Screenshot  
Obtiene una captura de pantalla de una pestana de Camofox.

9. Detener Servidor  
Detiene el servidor de Camofox Browser usando el PID del proceso.

10. Descargar Archivo  
Monitorea y captura descargas de forma nativa en la carpeta temporal de CamoFox en formatos Excel, PDF, TXT Y ZIP.

11. Ejecutar JS  
Ejecuta una expresion JavaScript en la pestana actual.

12. Hover  
Mueve el mouse sobre un elemento usando su referencia del snapshot o un selector CSS.

13. Scroll  
Desplaza la página activa en Camofox según la cantidad de píxeles indicada.  




----
### OS

- windows

### Dependencies

### License
  
![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)  
[MIT](http://opensource.org/licenses/mit-license.ph)