#!/usr/bin/env python3
"""
Build script for campus-portal-autologin standalone executable
Creates a "download and run" Windows executable with all dependencies bundled
"""

import os
import subprocess
import sys
import shutil

def print_step(step, message):
    """Print formatted step message"""
    print(f"[{step}/4] {message}")

def run_command(cmd, description):
    """Run command and handle errors"""
    print(f"Running: {description}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Building campus-portal-autologin standalone executable")
    print("=" * 60)
    print()

    # Clean previous build
    if os.path.exists("build"):
        print_step(1, "Cleaning previous build")
        shutil.rmtree("build")
    if os.path.exists("dist"):
        print_step(2, "Cleaning previous dist")
        shutil.rmtree("dist")

    # Install dependencies
    print_step(3, "Installing Python dependencies")
    if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                   "pip install -r requirements.txt"):
        sys.exit(1)

    # Install Playwright browsers in bundled mode
    print_step(4, "Installing Playwright browsers (bundled mode)")
    if not run_command([sys.executable, "-m", "playwright", "install", "chromium"], 
                   "playwright install chromium"):
        sys.exit(1)

    # Build with PyInstaller
    print_step(5, "Building standalone executable with PyInstaller")
    if not run_command([sys.executable, "-m", "PyInstaller", 
                      "--clean", 
                      "--name=CampusPortalAutologin", 
                      "--onedir", 
                      "--console", 
                      "--add-data=config.json.template:.",
                      "--add-data=install_task.py:.",
                      "--add-data=remove_task_scheduler.bat:.",
                      "--add-data=run_hidden.vbs:.",
                      "--hidden-import=playwright",
                      "--hidden-import=playwright.sync_api",
                      "--hidden-import=playwright._impl._api_types",
                      "src/campus_auto_connect_browser.py"], 
                   "pyinstaller build"):
        sys.exit(1)

    print()
    print("=" * 60)
    print("✓ Build completed successfully!")
    print("=" * 60)
    print()
    print("Output directory: dist/CampusPortalAutologin/")
    print()
    print("To test the executable:")
    print("  cd dist/CampusPortalAutologin")
    print("  ./CampusPortalAutologin.exe")
    print()
    print("Or run directly:")
    print("  dist/CampusPortalAutologin/CampusPortalAutologin.exe")

if __name__ == "__main__":
    main()
