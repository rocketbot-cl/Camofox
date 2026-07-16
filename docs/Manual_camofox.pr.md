



# Camofox
  
Modulo para interagir com o Camofox Browser Server a partir do Rocketbot por meio da API REST. Permite verificar o servidor, criar abas, navegar, obter snapshots, clicar, digitar texto e capturar screenshots.  

*Read this in other languages: [English](Manual_camofox.md), [Português](Manual_camofox.pr.md), [Español](Manual_camofox.es.md)*
  
![banner](imgs/Camofox_modulo.jpg)
## Como instalar este módulo
  
Para instalar o módulo no Rocketbot Studio, pode ser feito de duas formas:
1. Manual: __Baixe__ o arquivo .zip e descompacte-o na pasta módulos. O nome da pasta deve ser o mesmo do módulo e dentro dela devem ter os seguintes arquivos e pastas: \__init__.py, package.json, docs, example e libs. Se você tiver o aplicativo aberto, atualize seu navegador para poder usar o novo módulo.
2. Automático: Ao entrar no Rocketbot Studio na margem direita você encontrará a seção **Addons**, selecione **Install Mods**, procure o módulo desejado e aperte instalar.  


## Como usar este módulo
Este módulo é uma alternativa a outros módulos web como o WebPro. Ele utiliza um navegador baseado no Firefox, voltado para automação e técnicas anti-detecção, que roda em segundo plano.

1. Para usar este módulo, você precisa instalar o Node.js em sua máquina, bem como instalar o pacote Camoufox a partir do console (CMD ou terminal) com o seguinte comando: `npx -y @askjo/camofox-browser`.

2. O módulo opera em modo headless (em segundo plano), portanto, uma instância do navegador não é renderizada visualmente. A validação do estado da página deve ser realizada usando o comando `capture`.

3. Para obter os elementos com os quais você deseja interagir neste módulo, use o comando `get snapshot`. Este comando retorna uma árvore estruturada da página (baseada no DOM), onde cada elemento é representado por identificadores internos como `[e1], [e2], [e3]`, correspondentes à aba aberta no Camoufox.

4. Os downloads realizados com o módulo são gerados em segundo plano
 e inicialmente armazenados na pasta Temp do sistema. No entanto, usando o comando "baixar arquivo", é possível mover o arquivo desse local temporário para o caminho desejado, por exemplo, a pasta Downloads do Windows ou outro local personalizado definido pelo usuário.

5. O módulo pode apresentar variações no tempo de resposta, portanto, a criação de abas ou outras ações pode demorar um pouco para aparecer ou pode não ser executada imediatamente. Recomenda-se verificar cada ação antes de prosseguir para a próxima.

6. Durante a execução em um ambiente de desenvolvimento, a sessão pode ser perdida se houver inatividade ou atrasos entre as ações, o que pode resultar no erro: "Falha ao estabelecer uma nova conexão: [WinError 10061]", indicando que o servidor precisa ser reiniciado para restabelecer a conexão.

7.Devido às técnicas de evasão de deteção (anti-bot) utilizadas pelo Camoufox, o navegador pode alterar dinamicamente a resolução, o tamanho da janela de visualização (viewport) ou
 simular diferentes dispositivos em cada sessão. Consequentemente, as capturas de ecrã tiradas em segundo plano podem ser renderizadas com dimensões variáveis ou apresentadas de forma incompleta.



## Descrição do comando

### Iniciar Servidor
  
Inicia o servidor Camofox Browser em segundo plano.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base|URL do servidor Camofox. Padrao http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|Caminho do servidor|Pasta de onde o processo Camofox sera iniciado. Se usar npm start, informe a pasta do repositorio camofox-browser.|C:/Users/pc/Downloads|
|Comando de inicio|Comando usado para iniciar o Camofox. Padrao npx -y @askjo/camofox-browser|npx -y @askjo/camofox-browser|
|Segundos de espera||20|
|Atribuir resultado a variavel||resultado|

### Verificar Servidor
  
Verifica se o servidor Camofox esta ativo e acessivel.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base|URL do servidor Camofox. Padrao http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|Atribuir resultado a variavel||resultado|

### Criar Aba
  
Cria uma nova aba no Camofox e abre a URL informada.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|URL||https://example.com|
|Chave da sessao||default|
|Timeout da requisicao (segundos)||60|
|Atribuir resultado a variavel||resultado|

### Navegar
  
Navega uma aba existente do Camofox para uma nova URL.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID da aba||tabId|
|URL||https://example.com|
|Atribuir resultado a variavel||resultado|

### Obter Snapshot
  
Obtem o snapshot acessivel de uma aba do Camofox.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID da aba||tabId|
|Atribuir resultado a variavel||resultado|

### Click
  
Clica em um elemento usando sua referencia do snapshot.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID da aba||tabId|
|Referencia do elemento||e1|
|Atribuir resultado a variavel||resultado|

### Digitar Texto
  
Digita texto em um elemento usando sua referencia do snapshot.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID da aba||tabId|
|Referencia do elemento||e1|
|Texto||Text to type|
|Pressionar Enter depois de digitar|||
|Atribuir resultado a variavel||resultado|

### Screenshot
  
Obtem uma captura de tela de uma aba do Camofox.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID da aba||tabId|
|Caminho para salvar (opcional)||C:\tmp\camofox_capture.png|
|Atribuir resultado a variavel||resultado|

### Parar Servidor
  
Para o servidor Camofox Browser usando o PID do processo.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|PID|PID retornado pelo comando Iniciar Servidor.|12345|
|Atribuir resultado a variavel||resultado|

### Baixar Arquivo
  
Monitora e captura downloads nativamente na pasta temporária do CamoFox nos formatos Excel, PDF, TXT e ZIP.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base|URL do servidor Camofox. Padrao http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|ID Aba|ID da aba do CamoFox de onde o download é executado.|tab_1|
|Caminho de salvamento|Caminho onde o arquivo será salvo. Se não especificado, por padrão será criado no diretório atual com a extensão do formato escolhido.|C:\Users\Downloads\cartola.xlsx|
|Tipo de Arquivo|Formato para baixar Excel, PDF,TXT ou ZIP.||
|Sobrescrever se existir|||
|Atribuir resultado a variavel||resultado|

### Executar JS
  
Executa uma expressao JavaScript na aba atual.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base||http://localhost:9377|
|User ID||rb-test|
|ID da aba||tabId|
|Expressao JS||JavaScript expression|
|Timeout da requisicao||30|
|Atribuir resultado a variavel||resultado|

### Hover
  
Move o mouse sobre um elemento usando sua referencia do snapshot ou um seletor CSS.
|Parâmetros|Descrição|exemplo|
| --- | --- | --- |
|URL base|URL do servidor Camofox. Padrao http//localhost9377|http://localhost:9377|
|User ID|User ID usado ao criar a aba.|rb-test|
|ID da aba||tabId|
|Referencia do elemento|Referencia do snapshot, por exemplo e13. Use referencia ou seletor.|e13|
|Seletor CSS|Seletor CSS. Usado somente se nenhuma referencia for informada.|button.download|
|Atribuir resultado a variavel||resultado|
