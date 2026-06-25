## How to use this Module
This module is an alternative to other web modules like WebPro. It uses a Firefox-based browser geared towards automation and anti-detection techniques, running in the background.

1. To use this module, you need to install Node.js on your machine, as well as install the Camoufox package from the console (CMD or terminal) with this command: `npx -y @askjo/camofox-browser`.

2. The module operates in headless mode (background), so a browser instance is not visually rendered. Page state validation must be performed using the `capture` command.

3. To obtain the elements you want to interact with in this module, use the `get snapshot` command. This command returns a structured tree of the page (based on the DOM), where each element is represented by internal identifiers such as `[e1], [e2], [e3],` corresponding to the open tab in Camoufox.

4. Downloads performed with the module are generated in the background and initially stored in the system's Temp folder. However, using the "download file" command, it is possible to move the file from this temporary location to the desired path, for example, the Windows Downloads folder or another custom location defined by the user.

5. The module may exhibit variations in response time, so the creation of tabs or other actions may take some time to appear or may not execute immediately. It is recommended to verify each action before proceeding to the next.

6. During execution in a development environment, the session may be lost if there is inactivity or delays between actions, which may result in the error: "Failed to establish a new connection: [WinError 10061]", indicating that the server needs to be restarted to re-establish the connection.

---

## Como usar este modulo
Este módulo es una alternativa a otros módulos web como WebPro. Utiliza un navegador basado en Firefox orientado a automatización y técnicas anti-detección, ejecutándose en segundo plano. 

1. Para poder ocupar este modulo es necesario instalar Node.js en la maquina,asi como, instalar el paquete de Camoufox desde la consola (CMD o terminal) con este comando `npx -y @askjo/camofox-browser`.

2. El módulo opera en modo headless (segundo plano), por lo que no se renderiza visualmente una instancia del navegador.
La validación del estado de la página debe realizarse mediante el uso del comando de captura de pantalla.

3.Para obtener los elementos con los que se desea interactuar en este módulo, se debe utilizar el comando obtener snapshot.Este comando devuelve un árbol estructurado de la página (basado en el DOM), donde cada elemento se representa mediante identificadores internos como [e1], [e2], [e3], correspondientes a la pestaña abierta en Camoufox.

4. Las descargas realizadas con el módulo se generan en segundo plano y se almacenan inicialmente en la carpeta Temp del sistema.Sin embargo, mediante el comando “descargar archivo”, es posible mover el archivo desde esta ubicación temporal hacia la ruta deseada, por ejemplo, la carpeta de Descargas de Windows u otra ubicación personalizada definida por el usuario.

5. El módulo puede presentar variaciones en el tiempo de respuesta, por lo que la creación de pestañas u otras acciones pueden tardar en reflejarse o no ejecutarse de forma inmediata. Se recomienda validar cada acción antes de continuar con la siguiente.

6. Durante la ejecución en entorno de desarrollo, la sesión puede perderse si existe inactividad o demoras entre acciones, lo que puede provocar el error:
Failed to establish a new connection: [WinError 10061], lo que indica que es necesario reiniciar el servidor para restablecer la conexión.

---
## Como usar este módulo
Este módulo é uma alternativa a outros módulos web como o WebPro. Ele utiliza um navegador baseado no Firefox, voltado para automação e técnicas anti-detecção, que roda em segundo plano.

1. Para usar este módulo, você precisa instalar o Node.js em sua máquina, bem como instalar o pacote Camoufox a partir do console (CMD ou terminal) com o seguinte comando: `npx -y @askjo/camofox-browser`.

2. O módulo opera em modo headless (em segundo plano), portanto, uma instância do navegador não é renderizada visualmente. A validação do estado da página deve ser realizada usando o comando `capture`.

3. Para obter os elementos com os quais você deseja interagir neste módulo, use o comando `get snapshot`. Este comando retorna uma árvore estruturada da página (baseada no DOM), onde cada elemento é representado por identificadores internos como `[e1], [e2], [e3]`, correspondentes à aba aberta no Camoufox.

4. Os downloads realizados com o módulo são gerados em segundo plano e inicialmente armazenados na pasta Temp do sistema. No entanto, usando o comando "baixar arquivo", é possível mover o arquivo desse local temporário para o caminho desejado, por exemplo, a pasta Downloads do Windows ou outro local personalizado definido pelo usuário.

5. O módulo pode apresentar variações no tempo de resposta, portanto, a criação de abas ou outras ações pode demorar um pouco para aparecer ou pode não ser executada imediatamente. Recomenda-se verificar cada ação antes de prosseguir para a próxima.

6. Durante a execução em um ambiente de desenvolvimento, a sessão pode ser perdida se houver inatividade ou atrasos entre as ações, o que pode resultar no erro: "Falha ao estabelecer uma nova conexão: [WinError 10061]", indicando que o servidor precisa ser reiniciado para restabelecer a conexão.


