@echo off
cd /d "%~dp0"
echo Starting Campus Gadget System...
start "Campus Desktop" start_desktop.bat
timeout /t 3
start "Campus Web Server" start_web.bat