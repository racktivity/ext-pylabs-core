@echo off
set QBASE=%~dp0
set PYTHONHOME=%~dp0\lib\python27
rem rem set PYTHONUNBUFFERED=True
rem set IPYTHONDIR=%~dp0\lib\python31\_ipython
path %CD%\bin;%CD%\lib\Python27;%windir%;%windir%\system
rem ;%windir%\system32
mode con cp select=437 >nul 2>nul
rem set HOME=%QBASE%\cfg\home
rem SET SVN_EDITOR=%QBASE%\bin\scite.bat
rem SET GIT_EDITOR=%QBASE%\bin\scite.bat
rem SET git_install_root=%QBASE%\apps\git
rem @set path=%git_install_root%\bin;%git_install_root%\mingw\bin;%PATH%
