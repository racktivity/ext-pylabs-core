@echo off
rem set OLDPATH=%PATH%
call "%~dp0_settings.bat"
rem path %~dp0;%~dp0bin;%~dp0Python25
rem ;C:\WINDOWS\SYSTEM32
"%~dp0\lib\python27\python" "%~dp0utils/Shell.py" %*
rem set PATH=%OLDPATH%
rem path %OLDPATH%
