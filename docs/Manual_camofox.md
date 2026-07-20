



# Camofox
  
Module to interact with Camofox Browser Server from Rocketbot through its REST API. It allows checking the server, creating tabs, navigating, getting snapshots, clicking, typing text and taking screenshots.  

*Read this in other languages: [English](Manual_camofox.md), [Português](Manual_camofox.pr.md), [Español](Manual_camofox.es.md)*
  
![banner](imgs/Camofox_modulo.jpg)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  

## How to use this Module
This module is an alternative to other web modules like WebPro. It uses a Firefox-based browser geared towards automation and anti-detection techniques, running in the background.

1. To use this module, you need to install Node.js on your machine, as well as install the Camoufox package from the console (CMD or terminal) with this command: `npx -y @askjo/camofox-browser`.

2. The module operates in headless mode (background), so a browser instance is not visually rendered. Page state validation must be performed using the `capture` command.

3. To obtain the elements you want to interact with in this module, use the `get snapshot` command. This command returns a structured tree of the page (based on the DOM), where each element is represented by internal identifiers such as `[e1], [e2], [e3],` corresponding to the open tab in Camoufox.

4. Downloads performed with the module are generated in the background and initially stored in the system's Temp folder. 
However, using the "download file" command, it is possible to move the file from this temporary location to the desired path, for example, the Windows Downloads folder or another custom location defined by the user.

5. The module may exhibit variations in response time, so the creation of tabs or other actions may take some time to appear or may not execute immediately. It is recommended to verify each action before proceeding to the next.

6. During execution in a development environment, the session may be lost if there is inactivity or delays between actions, which may result in the error: "Failed to establish a new connection: [WinError 10061]", indicating that the server needs to be restarted to re-establish the connection.

7. Due to the detection-evasion (anti-bot) techniques used by Camoufox, the browser may dynamically alter the resolution or viewport size, or simulate different devices during each session. As a result, screenshots taken in the background may be rendered with
 varying dimensions or appear incomplete.

8. If it is not possible to start the server using the procedure described in point 1, use the following alternative method: 
    - Clone the repository instead of running the server using npx: 
        - git clone https://github.com/jo-inc/camofox-browser 
        - cd camofox-browser 
        - npm install 
    - Once the installation is complete, start the server by executing: 
        - npm start

9. If the server does not finish correctly and processes are still running, it is possible to release them from the console. To do so, execute the following commands: 
    - netstat -year | findstr :9377 (What returns the PID of the process associated with port 9377) 
    - taskkill /PID {PID} /F( Replace <PID> with the process identifier obtained in the previous step)


## Description of the commands

### Start Server
  
Start the Camofox Browser Server in background.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL|Camofox server URL. Default http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|Server path|Folder where the Camofox process will be started. If using npm start, use the camofox-browser repository folder.|C:/Users/pc/Downloads|
|Start command|Command used to start Camofox. Default npx -y @askjo/camofox-browser|npx -y @askjo/camofox-browser|
|Wait seconds||20|
|Assign result to variable||result|

### Health Check
  
Check if the Camofox server is running and reachable.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL|Camofox server URL. Default http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|Assign result to variable||result|

### Create Tab
  
Create a new Camofox tab and open the provided URL.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL||http://localhost:9377|
|User ID||rb-test|
|URL||https://example.com|
|Session key||default|
|Request timeout (seconds)||60|
|Assign result to variable||result|

### Navigate
  
Navigate an existing Camofox tab to a new URL.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL||http://localhost:9377|
|User ID||rb-test|
|Tab ID||tabId|
|URL||https://example.com|
|Assign result to variable||result|

### Get Snapshot
  
Get the accessibility snapshot of a Camofox tab.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL||http://localhost:9377|
|User ID||rb-test|
|Tab ID||tabId|
|Assign result to variable||result|

### Click
  
Click an element by its snapshot reference.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL||http://localhost:9377|
|User ID||rb-test|
|Tab ID||tabId|
|Element reference||e1|
|Assign result to variable||result|

### Type Text
  
Type text into an element by its snapshot reference.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL||http://localhost:9377|
|User ID||rb-test|
|Tab ID||tabId|
|Element reference||e1|
|Text||Text to type|
|Press Enter after typing|||
|Assign result to variable||result|

### Screenshot
  
Take a screenshot of a Camofox tab.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL||http://localhost:9377|
|User ID||rb-test|
|Tab ID||tabId|
|Save path (optional)||C:\tmp\camofox_capture.png|
|Assign result to variable||result|

### Stop Server
  
Stop the Camofox Browser Server using the process PID.
|Parameters|Description|example|
| --- | --- | --- |
|PID|PID returned by the Start Server command.|12345|
|Assign result to variable||result|

### Download File 
  
Monitors and captures downloads natively in CamoFox's temporary folder in Excel, PDF, TXT, and ZIP formats.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL|Camofox server URL. Default http//localhost9377|http://localhost:9377|
|User ID||rb-test|
|Tab ID|Tab ID of CamoFox where the download is triggered.|tab_1|
|Save path|Path to save the file. If not specified, it defaults to 'archivo_descargado' with the chosen format extension in the current directory.|C:\Users\Downloads\cartola.xlsx|
|File Type|Format to download Excel, PDF,TXT or ZIP.||
|Overwrite file if exists|||
|Assign result to variable||result|

### Evaluate JS
  
Execute a JavaScript expression in the current tab.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL||http://localhost:9377|
|User ID||rb-test|
|Tab ID||tabId|
|Expression||JavaScript expression|
|Request timeout||30|
|Assign result to variable||result|

### Hover
  
Move the mouse over an element using its snapshot reference or a CSS selector.
|Parameters|Description|example|
| --- | --- | --- |
|Base URL|Camofox server URL. Default http//localhost9377|http://localhost:9377|
|User ID|User ID used when creating the tab.|rb-test|
|Tab ID||tabId|
|Element reference|Snapshot reference, for example e13. Use either reference or selector.|e13|
|CSS selector|CSS selector. Used only if no reference is provided.|button.download|
|Assign result to variable||result|
