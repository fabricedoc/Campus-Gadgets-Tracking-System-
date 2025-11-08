@echo off
echo Creating Distribution Package...
echo.

:: Create distribution folder
set "DIST_DIR=CampusGadgetSystem_v1.0"
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%DIST_DIR%"

:: Build executables
call build.bat

:: Copy files to distribution
echo 📦 Packaging files...
copy "dist\CampusGadgetDesktop.exe" "%DIST_DIR%\"
copy "dist\CampusGadgetServer.exe" "%DIST_DIR%\"
copy "*.py" "%DIST_DIR%\"
copy "requirements.txt" "%DIST_DIR%\"
copy "Installer.bat" "%DIST_DIR%\"

:: Create assets folder
mkdir "%DIST_DIR%\assets"
:: You can add your icon files here

:: Create docs
mkdir "%DIST_DIR%\docs"
echo Campus Gadget Tracking System > "%DIST_DIR%\docs\README.txt"
echo Version 1.0 >> "%DIST_DIR%\docs\README.txt"
echo. >> "%DIST_DIR%\docs\README.txt"
echo INSTALLATION: >> "%DIST_DIR%\docs\README.txt"
echo 1. Run Installer.bat as Administrator >> "%DIST_DIR%\docs\README.txt"
echo 2. Follow on-screen instructions >> "%DIST_DIR%\docs\README.txt"
echo. >> "%DIST_DIR%\docs\README.txt"
echo DEFAULT LOGIN: >> "%DIST_DIR%\docs\README.txt"
echo Username: admin >> "%DIST_DIR%\docs\README.txt"
echo Password: admin123 >> "%DIST_DIR%\docs\README.txt"

:: Create zip package
powershell -Command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath '%DIST_DIR%.zip' -Force"

echo.
echo ✅ Distribution package created: %DIST_DIR%.zip
echo 📦 Size: 
dir "%DIST_DIR%.zip" | find "File(s)"
echo.
echo 🚀 Ready for distribution!
pause