@echo off
echo Installing Campus Gadget Tracking System...
echo.

:: Create virtual environment
python -m venv campus_env
call campus_env\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Create necessary directories
mkdir reports
mkdir student_photos
mkdir web_uploads
mkdir logs

echo.
echo ✅ Installation completed!
echo.
echo 🚀 To start the system:
echo 1. Run desktop app: python main.py
echo 2. Run web server: python production_server.py
echo.
pause