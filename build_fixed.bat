@echo off
echo Building Campus Gadget System with Fixed Configuration...
echo.

:: Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "CampusGadgetDesktop.spec" del "CampusGadgetDesktop.spec"
if exist "CampusGadgetServer.spec" del "CampusGadgetServer.spec"

:: Build Desktop Application with hidden imports
echo Building Desktop App...
pyinstaller --onefile --windowed ^
--name "CampusGadgetDesktop" ^
--add-data "*.py;." ^
--hidden-import "customtkinter" ^
--hidden-import "PIL" ^
--hidden-import "PIL._tkinter_finder" ^
--hidden-import "pandas" ^
--hidden-import "matplotlib.backends.backend_tkagg" ^
--hidden-import "sqlite3" ^
--collect-all "customtkinter" ^
--collect-all "PIL" ^
main.py

:: Build Web Server
echo Building Web Server...
pyinstaller --onefile --console ^
--name "CampusGadgetServer" ^
--add-data "*.py;." ^
--hidden-import "flask" ^
--hidden-import "waitress" ^
--hidden-import "sqlite3" ^
production_server.py

echo.
echo ✅ Build completed! Check 'dist' folder.
pause