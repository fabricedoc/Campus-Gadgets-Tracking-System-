# launch.py - User-friendly launcher
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'customtkinter',
        'pillow', 
        'pandas',
        'requests',
        'matplotlib'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def install_dependencies(missing_packages):
    """Install missing packages"""
    try:
        for package in missing_packages:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

def main():
    print("🚀 Campus Gadget System Launcher")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        response = messagebox.askyesno(
            "Install Dependencies", 
            f"The following packages are missing:\n{', '.join(missing)}\n\nInstall them automatically?"
        )
        
        if response:
            if install_dependencies(missing):
                messagebox.showinfo("Success", "Dependencies installed successfully!")
            else:
                messagebox.showerror("Error", "Failed to install dependencies.")
                return
        else:
            return
    
    # Launch main application
    try:
        from main import CampusGadgetSystem
        app = CampusGadgetSystem()
        app.run()
    except Exception as e:
        messagebox.showerror("Launch Error", f"Failed to start application:\n{str(e)}")

if __name__ == "__main__":
    main()