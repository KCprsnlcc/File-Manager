#!/usr/bin/env python3
import os
import platform
import sys

def check_installers():
    """Check which installers are real and which are placeholders."""
    
    print("File Manager Installer Status Check")
    print("==================================\n")
    
    # Determine the current OS
    current_os = platform.system().lower()
    if current_os == 'darwin':
        current_os = 'macos'
    
    print(f"Current platform: {current_os.upper()}\n")
    
    # Check if output directory exists
    if not os.path.exists("output"):
        print("No installers found. Please run the build scripts first.")
        return
    
    # List of expected installers
    installers = {
        "windows": "output/FileManager-Setup.exe",
        "macos": "output/FileManager.dmg",
        "linux": "output/filemanager_1.0.0_amd64.deb"
    }
    
    # Check each installer
    for os_name, installer_path in installers.items():
        if os.path.exists(installer_path):
            # Check if it's likely a placeholder (very small file)
            file_size = os.path.getsize(installer_path)
            if file_size < 10000:  # Less than 10KB is likely a placeholder
                status = "⚠️  PLACEHOLDER (must be built on {})".format(os_name.upper())
            else:
                if os_name == current_os:
                    status = "✅  READY FOR USE"
                else:
                    status = "⚠️  LIKELY PLACEHOLDER (built on {}, should be built on {})".format(
                        current_os.upper(), os_name.upper())
            
            print(f"{os_name.upper()} installer: {status}")
            print(f"  Path: {installer_path}")
            print(f"  Size: {file_size / 1024:.1f} KB\n")
        else:
            print(f"{os_name.upper()} installer: ❌  NOT FOUND")
            print(f"  To build, run: python build_{os_name}.py\n")
    
    print("Remember: For proper functionality, each installer must be built on its target platform.")
    print("Use 'python build_all.py' to build for your current platform.")

if __name__ == "__main__":
    check_installers() 