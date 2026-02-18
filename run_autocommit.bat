@echo off 
REM Switch to the folder where this .bat file is located 
cd /d "%~dp0" 
set LOG=log_%date:~10,4%%date:~4,2%%date:~7,2%.txt 
echo ==== Run at %date% %time% ==== >> %LOG% 
"C:\Users\goddt\AppData\Local\Programs\Python\Python314\python.exe" autocommit.py >> %LOG% 2>&1 
echo ---- Script Finished ---- >> %LOG%