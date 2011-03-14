@echo off
path %CD%;%CD%\bin;%CD%\Python25;%path%
call "%CD%\_settings.bat"
call python25\python.exe utils\configure.py -q unstable -a 172.17.1.5 -p 8000

if not "%1"=="-q" pause