import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def run_command(command):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def build_executable():
    # Clean build and dist directories
    for directory in ["build", "dist"]:
        if os.path.exists(directory):
            shutil.rmtree(directory)

    # Determine the OS
    os_system = platform.system().lower()
    print(f"Detected OS: {os_system}")

    # Set platform-specific path separator for PyInstaller
    path_sep = ":" if os_system != "windows" else ";"

    # Common PyInstaller arguments
    pyinstaller_args = [
        "--name=FileManager",
        "--onedir",
        "--windowed",
        "--clean",
        "--noconfirm",
        f"--add-data=screenshot.png{path_sep}.",
        f"--add-data=README.md{path_sep}.",
        f"--add-data=LICENSE.md{path_sep}.",
    ]
    
    # Add platform-specific options
    if os_system == "darwin":
        pyinstaller_args.append("--osx-bundle-identifier=com.filemanager.app")
    elif os_system == "windows":
        pyinstaller_args.append("--icon=screenshot.png")  # Use screenshot as a temporary icon

    # Install dependencies
    print("Installing dependencies...")
    run_command("pip install -r requirements.txt")

    # Create .spec file
    spec_cmd = f"pyinstaller {''.join([' ' + arg for arg in pyinstaller_args])} file_manager.py"
    run_command(spec_cmd)

    # Build the executable
    run_command("pyinstaller FileManager.spec")

    print(f"Build completed. Executable is in the dist/FileManager directory.")
    
    return os_system

if __name__ == "__main__":
    build_executable() 