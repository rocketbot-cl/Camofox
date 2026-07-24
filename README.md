



# Camofox
  
Module to interact with Camofox Browser Server from Rocketbot through its REST API. It allows checking the server, creating tabs, navigating, getting snapshots, clicking, typing text and taking screenshots.  

*Read this in other languages: [English](README.md), [Português](README.pr.md), [Español](README.es.md)*

## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  


## Overview


1. Start Server  
Start the Camofox Browser Server in background.

2. Health Check  
Check if the Camofox server is running and reachable.

3. Create Tab  
Create a new Camofox tab and open the provided URL.

4. Navigate  
Navigate an existing Camofox tab to a new URL.

5. Get Snapshot  
Get the accessibility snapshot of a Camofox tab.

6. Click  
Click an element by its snapshot reference.

7. Type Text  
Type text into an element by its snapshot reference.

8. Screenshot  
Take a screenshot of a Camofox tab.

9. Stop Server  
Stop the Camofox Browser Server using the process PID.

10. Download File   
Monitors and captures downloads natively in CamoFox's temporary folder in Excel, PDF, TXT, and ZIP formats.

11. Evaluate JS  
Execute a JavaScript expression in the current tab.

12. Hover  
Move the mouse over an element using its snapshot reference or a CSS selector.

13. Scroll  
Scroll the active page in Camofox according to the number of pixels indicated.  




----
### OS

- windows

### Dependencies

### License
  
![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)  
[MIT](http://opensource.org/licenses/mit-license.ph)