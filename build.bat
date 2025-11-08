@echo off
echo Building Campus Gadget System Executables...
echo.

:: Build Desktop Application
echo Building Desktop App...
pyinstaller --onefile --windowed --name "CampusGadgetDesktop" --icon=assets/icon.ico main.py

:: Build Web Server
echo Building Web Server...
pyinstaller --onefile --console --name "CampusGadgetServer" production_server.py

echo.
echo ✅ Build completed! Check 'dist' folder for executables.
pause