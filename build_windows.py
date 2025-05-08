import os
import sys
import subprocess
import shutil
from build import build_executable

def create_windows_installer():
    # First build the executable
    os_system = build_executable()
    
    if os_system != 'windows':
        print("Warning: This script should be run on Windows for proper installer creation.")
        print("Creating a placeholder installer file instead.")
        
        # Create output directory if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")
        
        # Create a mock Windows installer file
        with open("output/FileManager-Setup.exe", "w") as f:
            f.write("This is a placeholder for a Windows installer executable.\n")
            f.write("To create a real Windows installer, this script needs to be run on Windows.\n")
        
        return
    
    # Install NSIS if not already installed (requires Chocolatey)
    try:
        subprocess.run(["where", "makensis"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("NSIS not found. Installing via Chocolatey...")
        try:
            subprocess.run(["choco", "--version"], check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("Chocolatey not found. Please install Chocolatey first: https://chocolatey.org/install")
            return
        
        subprocess.run(["choco", "install", "nsis", "-y"], check=True)
    
    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Create NSIS script
    nsis_script = """
; FileManager Installer Script
!include "MUI2.nsh"

; General
Name "File Manager"
OutFile "output\\FileManager-Setup.exe"
InstallDir "$PROGRAMFILES\\FileManager"
InstallDirRegKey HKCU "Software\\FileManager" ""

; Interface Settings
!define MUI_ABORTWARNING

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Add files to your installer:
    File /r "dist\\FileManager\\*.*"
    
    ; Create shortcuts
    CreateDirectory "$SMPROGRAMS\\FileManager"
    CreateShortcut "$SMPROGRAMS\\FileManager\\File Manager.lnk" "$INSTDIR\\FileManager.exe"
    CreateShortcut "$DESKTOP\\File Manager.lnk" "$INSTDIR\\FileManager.exe"
    
    ; Write uninstaller
    WriteRegStr HKCU "Software\\FileManager" "" $INSTDIR
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    CreateShortcut "$SMPROGRAMS\\FileManager\\Uninstall.lnk" "$INSTDIR\\Uninstall.exe"
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Remove files and uninstaller
    RMDir /r "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$DESKTOP\\File Manager.lnk"
    RMDir /r "$SMPROGRAMS\\FileManager"
    
    ; Remove registry keys
    DeleteRegKey HKCU "Software\\FileManager"
SectionEnd
"""

    # Write NSIS script to file
    with open("installer.nsi", "w") as f:
        f.write(nsis_script)
    
    # Run NSIS to create installer
    subprocess.run(["makensis", "installer.nsi"], check=True)
    
    print("Windows installer created: output/FileManager-Setup.exe")

if __name__ == "__main__":
    create_windows_installer() 