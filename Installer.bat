@echo off
title Campus Gadget System Installer
color 0A

echo ========================================
echo    CAMPUS GADGET SYSTEM INSTALLER
echo ========================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Please run as Administrator!
    echo Right-click -> Run as Administrator
    pause
    exit /b 1
)

:: Set installation directory
set "INSTALL_DIR=%PROGRAMFILES%\CampusGadgetSystem"
set "DESKTOP_DIR=%USERPROFILE%\Desktop"

echo 📁 Installation directory: %INSTALL_DIR%
echo.

:: Create installation directory
if exist "%INSTALL_DIR%" (
    echo ⚠️  Existing installation found. Overwriting...
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"
mkdir "%INSTALL_DIR%\data"
mkdir "%INSTALL_DIR%\reports"
mkdir "%INSTALL_DIR%\backups"
mkdir "%INSTALL_DIR%\logs"

echo ✅ Created installation directories...

:: Copy files
echo 📦 Copying system files...
copy "CampusGadgetDesktop.exe" "%INSTALL_DIR%\"
copy "CampusGadgetServer.exe" "%INSTALL_DIR%\"
copy "*.py" "%INSTALL_DIR%\"
copy "requirements.txt" "%INSTALL_DIR%\"

:: Copy assets
if exist "assets" (
    xcopy "assets" "%INSTALL_DIR%\assets\" /E /I /Y
)

:: Create database
echo 🗃️  Creating database...
cd "%INSTALL_DIR%"
python -c "from database import Database; db = Database()" >nul 2>&1
if errorlevel 1 (
    :: If Python method fails, use executable
    echo 📊 Initializing database...
    start /wait "" CampusGadgetServer.exe
    timeout /t 3
    taskkill /f /im CampusGadgetServer.exe >nul 2>&1
)

:: Create desktop shortcuts
echo 🔗 Creating shortcuts...
set "SHORTCUT_SCRIPT=%TEMP%\create_shortcuts.vbs"

echo Set WshShell = WScript.CreateObject("WScript.Shell") > "%SHORTCUT_SCRIPT%"
echo set oShellLink = WshShell.CreateShortcut("%DESKTOP_DIR%\Campus Gadget System.lnk") >> "%SHORTCUT_SCRIPT%"
echo oShellLink.TargetPath = "%INSTALL_DIR%\CampusGadgetDesktop.exe" >> "%SHORTCUT_SCRIPT%"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%SHORTCUT_SCRIPT%"
echo oShellLink.Description = "Campus Gadget Tracking System" >> "%SHORTCUT_SCRIPT%"
echo oShellLink.Save >> "%SHORTCUT_SCRIPT%"

echo set oShellLink = WshShell.CreateShortcut("%DESKTOP_DIR%\Campus Web Server.lnk") >> "%SHORTCUT_SCRIPT%"
echo oShellLink.TargetPath = "%INSTALL_DIR%\CampusGadgetServer.exe" >> "%SHORTCUT_SCRIPT%"
echo oShellLink.WorkingDirectory = "%INSTALL_DIR%" >> "%SHORTCUT_SCRIPT%"
echo oShellLink.Description = "Campus Gadget Web Server" >> "%SHORTCUT_SCRIPT%"
echo oShellLink.Save >> "%SHORTCUT_SCRIPT%"

cscript //nologo "%SHORTCUT_SCRIPT%"
del "%SHORTCUT_SCRIPT%"

:: Create start menu entries
powershell -Command " 
$s=(New-Object -COM WScript.Shell).CreateShortcut('$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Campus Gadget System.lnk');
$s.TargetPath='%INSTALL_DIR%\CampusGadgetDesktop.exe';
$s.WorkingDirectory='%INSTALL_DIR%';
$s.Save();
"

:: Create auto-start entry for web server (optional)
echo 📝 Creating startup entries...
reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "CampusGadgetWebServer" /t REG_SZ /d "\"%INSTALL_DIR%\CampusGadgetServer.exe\"" /f

:: Create uninstaller
echo 🗑️  Creating uninstaller...
set "UNINSTALL_SCRIPT=%INSTALL_DIR%\uninstall.bat"

echo @echo off > "%UNINSTALL_SCRIPT%"
echo echo Uninstalling Campus Gadget System... >> "%UNINSTALL_SCRIPT%"
echo. >> "%UNINSTALL_SCRIPT%"
echo :: Remove shortcuts >> "%UNINSTALL_SCRIPT%"
echo del "%DESKTOP_DIR%\Campus Gadget System.lnk" >> "%UNINSTALL_SCRIPT%"
echo del "%DESKTOP_DIR%\Campus Web Server.lnk" >> "%UNINSTALL_SCRIPT%"
echo rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Campus Gadget System" >> "%UNINSTALL_SCRIPT%"
echo. >> "%UNINSTALL_SCRIPT%"
echo :: Remove registry entries >> "%UNINSTALL_SCRIPT%"
echo reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "CampusGadgetWebServer" /f ^>nul 2^>^&1 >> "%UNINSTALL_SCRIPT%"
echo. >> "%UNINSTALL_SCRIPT%"
echo :: Remove installation directory >> "%UNINSTALL_SCRIPT%"
echo rmdir /s /q "%INSTALL_DIR%" >> "%UNINSTALL_SCRIPT%"
echo. >> "%UNINSTALL_SCRIPT%"
echo echo ✅ Uninstallation completed! >> "%UNINSTALL_SCRIPT%"
echo pause >> "%UNINSTALL_SCRIPT%"

:: Register uninstaller
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\CampusGadgetSystem" /v "DisplayName" /t REG_SZ /d "Campus Gadget Tracking System" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\CampusGadgetSystem" /v "UninstallString" /t REG_SZ /d "\"%UNINSTALL_SCRIPT%\"" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\CampusGadgetSystem" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f

echo.
echo ========================================
echo        INSTALLATION COMPLETED!
echo ========================================
echo.
echo ✅ Campus Gadget System installed successfully!
echo.
echo 🚀 Quick Start:
echo   1. Double-click 'Campus Gadget System' on desktop
echo   2. Double-click 'Campus Web Server' on desktop
echo   3. Login with: admin / admin123
echo.
echo 📍 Files installed to: %INSTALL_DIR%
echo 🔗 Desktop shortcuts created
echo 🗑️  Uninstall via: Control Panel -> Programs
echo.
echo Press any key to finish...
pause >nul