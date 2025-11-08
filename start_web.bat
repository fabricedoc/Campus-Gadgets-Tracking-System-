@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
python production_server.py
pause