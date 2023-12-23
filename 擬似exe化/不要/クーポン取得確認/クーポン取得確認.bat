@echo off

if not "%~0"=="%~dp0.\%~nx0" (
	start /min cmd /c,"%~dp0.\%~nx0" %*
	exit
)

call C:\Users\YUTANAO\PycharmProjects\PythonScripts\venv\Scripts\activate.bat

for /f %%a in (py_dir.txt) do (
	set py_dir=%%a
)
Python %py_dir%

pause