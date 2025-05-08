import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path
from build import build_executable

def create_linux_installer():
    # First build the executable
    os_system = build_executable()
    
    # Create the output directory
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Package version and architecture
    version = "1.0.0"
    arch = "amd64"  # Assuming 64-bit system
    package_name = f"filemanager_{version}_{arch}"
    
    # Check if we're on Linux
    if os_system != 'linux':
        print("Warning: This script should be run on Linux for proper package creation.")
        print("Creating a placeholder .deb package instead.")
        
        # Create a simulated .deb package
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock control file
            control_content = f"""Package: filemanager
Version: {version}
Architecture: {arch}
Maintainer: Your Name <your.email@example.com>
Description: File Manager Application
 A basic file manager application built with PySide6.
Section: utils
Priority: optional
Homepage: https://github.com/KCprsnlcc/File-Manager
Depends: libc6 (>= 2.17)
"""
            with open(os.path.join(temp_dir, "control"), "w") as f:
                f.write(control_content)
            
            # Create a tarball of the package structure
            shutil.make_archive(
                os.path.join("output", package_name),
                'gztar',
                temp_dir
            )
            
            # Rename the tarball to .deb for demonstration
            tar_path = os.path.join("output", f"{package_name}.tar.gz")
            deb_path = os.path.join("output", f"{package_name}.deb")
            
            if os.path.exists(deb_path):
                os.remove(deb_path)
            
            shutil.move(tar_path, deb_path)
        
        print(f"Linux .deb package placeholder created: output/{package_name}.deb")
        print("Note: This is a simulated .deb package. To create a real .deb package, run this script on a Linux system.")
        return
    
    # Install required tools
    try:
        subprocess.run(["dpkg", "--version"], check=True, stdout=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing dpkg-dev...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "dpkg-dev"], check=True)
    
    # Create a temporary directory for building the package
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the package structure
        package_dir = os.path.join(temp_dir, package_name)
        os.makedirs(package_dir)
        
        # Create the DEBIAN directory
        debian_dir = os.path.join(package_dir, "DEBIAN")
        os.makedirs(debian_dir)
        
        # Create control file
        with open(os.path.join(debian_dir, "control"), "w") as f:
            f.write(f"""Package: filemanager
Version: {version}
Architecture: {arch}
Maintainer: Your Name <your.email@example.com>
Description: File Manager Application
 A basic file manager application built with PySide6.
Section: utils
Priority: optional
Homepage: https://github.com/KCprsnlcc/File-Manager
Depends: libc6 (>= 2.17)
""")
        
        # Create the application directory structure
        app_dir = os.path.join(package_dir, "usr", "share", "applications")
        bin_dir = os.path.join(package_dir, "usr", "bin")
        share_dir = os.path.join(package_dir, "usr", "share", "filemanager")
        
        os.makedirs(app_dir)
        os.makedirs(bin_dir)
        os.makedirs(share_dir)
        
        # Copy the PyInstaller output to the package directory
        dist_dir = os.path.join("dist", "FileManager")
        for item in os.listdir(dist_dir):
            src = os.path.join(dist_dir, item)
            dst = os.path.join(share_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        
        # Create a launcher script
        with open(os.path.join(bin_dir, "filemanager"), "w") as f:
            f.write("""#!/bin/bash
exec /usr/share/filemanager/FileManager "$@"
""")
        
        # Make the launcher script executable
        os.chmod(os.path.join(bin_dir, "filemanager"), 0o755)
        
        # Create desktop file for application menu integration
        with open(os.path.join(app_dir, "filemanager.desktop"), "w") as f:
            f.write("""[Desktop Entry]
Name=File Manager
Comment=Browse and manage files
Exec=/usr/bin/filemanager
Icon=/usr/share/filemanager/screenshot.png
Terminal=false
Type=Application
Categories=Utility;FileManager;
""")
        
        # Build the .deb package
        deb_file = f"output/{package_name}.deb"
        if os.path.exists(deb_file):
            os.remove(deb_file)
            
        subprocess.run(["dpkg-deb", "--build", package_dir, deb_file], check=True)
        
        print(f"Linux .deb package created: {deb_file}")

if __name__ == "__main__":
    create_linux_installer() 