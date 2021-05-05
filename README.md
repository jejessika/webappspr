# Web-based Surface Plasmon Resonance (SPR) Signal Processing System for Fast Analyte Analysis

## Summary
We introduce a web-based application for SPR sample data analysis with Python’s Matplotlib and Bokeh as the primary tools. Users can directly upload and analyze the SPR data output, where the data are stored in the Firebase cloud storage. The web application is embedded with several features, including the graph label, tooltips, and interactive legend. With this application, SPR sample analysis only needs to be run within minutes, and the system is made portable by implementing Python virtual environment. The PDF version of the manual is available here [https://github.com/jejessika/webappspr/blob/main/Web%20App%20Manual%20Book_Final.pdf].

## Getting Started
### Installing Python
1. Go to www.python.org/downloads/.
2. Click the download button and choose which one is suitable for your operating system (Windows or Linux or Mac OS).
3. Run the Python installer once downloaded.
4. Follow all the instructions (including select install launcher for all users and add Python 3.8 to PATH checkboxes).
5. The next dialog will prompt you to select whether to disable path length limit. Select it to enable Python to use long path names.
6. Verify the newly installed Python on your Windows by running command prompt (CTRL+R then type “cmd” and click OK) as follows.
7. Type “python” and click enter. The output will be similar as follows. It can be verified that the downloaded Python 3.8.5 is successfully installed.
8. Verify whether pip is also installed. Pip is a powerful package management system for Python software packages. Run command prompt again and type “pip -V” as shown below. The output tells us that pip is successfully installed.
9. To prevent error from too long path, open registry editor by typing “regedit’ on windows search bar and open Registry Editor
10. Go to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem, then select “LongPathEnabled”
11. Change the value data from “0” to “1”
### Activate Virtual Environment
The developed Python program for building web application comprises of several packages to support the operations needed for SPR data processing. All the needed packages can be
installed in a virtual environment. Therefore, you do not need to install each packages one by one using pip via command prompt. Instead, run the Python program in our virtual environment. Here are some steps to activate the virtual environment.
1. Go to the Web App Directory (where you extract the Web App.zip file).
2. Go to the following directory: Web App > env > Scripts by typing “cd [Web App Folder]\env\Scripts”.
3. Edit the “activate.bat” file using notepad, wordpad, or notepad++
4. Change the “set VIRTUAL_ENV” variable value into the correct directory in your computer.
5. Click enter and type “activate.bat” to activate the virtual environment.
5. Click enter and then “(env)” will show up on the left side indicating the virtual environment is successfully activated.
6. Back to the directory of Web App where the Python web app program is located by typing “cd..”, click enter, and do it one more time until the Command Prompt directs to the Web App folder directory.
7. Run the program by typing “python app.py” and click enter. Wait until your command prompt look like the above picture. Copy the http://127.0.0.1:5000/ and open it on your web browser.
### ANALYTE CONCENTRATION INPUT LIMIT
The developed Python algorithm for this program has user input feature to label the visualized graph result. On the ‘Input Sample’ column, input 1 for IBV, 2 for RBD, 3 for Non-specific Sample, and 4 for Unknown Sample. On the ‘Input Concentration’ column, input the analyte’s concentration in ng/mL unit. The analyte’s concentration can’t be more than 10 ng/mL due to this program’s algorithm.
