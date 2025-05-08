import os
import sys
import subprocess
import shutil
from build import build_executable

def create_macos_installer():
    # First build the executable
    build_executable()
    
    # Create the output directory
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Clean up any previous attempts
    dmg_file = "output/FileManager.dmg"
    if os.path.exists(dmg_file):
        os.remove(dmg_file)
    
    # Set app name and paths
    app_name = "FileManager.app"
    app_path = os.path.join("dist", app_name)
    
    # Create app bundle from PyInstaller output
    if not os.path.exists(app_path):
        # Create basic app structure
        os.makedirs(os.path.join(app_path, "Contents", "MacOS"), exist_ok=True)
        os.makedirs(os.path.join(app_path, "Contents", "Resources"), exist_ok=True)
        
        # Move executable and resources
        shutil.move(os.path.join("dist", "FileManager"), os.path.join(app_path, "Contents", "MacOS", "FileManager"))
        
        # Create Info.plist
        with open(os.path.join(app_path, "Contents", "Info.plist"), "w") as f:
            f.write("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>FileManager</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>com.filemanager.app</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>File Manager</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
""")
    
    # Try to create DMG using create-dmg if available
    try:
        # Check if create-dmg is installed
        subprocess.run(["which", "create-dmg"], check=True, stdout=subprocess.PIPE)
        
        # Create DMG
        create_dmg_cmd = [
            "create-dmg",
            "--volname", "File Manager",
            "--volicon", "screenshot.png",
            "--window-pos", "200", "120",
            "--window-size", "600", "400",
            "--icon-size", "100",
            "--icon", app_name, "175", "120",
            "--hide-extension", app_name,
            "--app-drop-link", "425", "120",
            dmg_file,
            app_path
        ]
        
        subprocess.run(create_dmg_cmd, check=True)
        print(f"macOS DMG created: {dmg_file}")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("create-dmg not found. Creating a simple disk image...")
        
        # Create a simple disk image using hdiutil (built into macOS)
        try:
            subprocess.run([
                "hdiutil", "create", 
                "-volname", "File Manager",
                "-srcfolder", app_path,
                "-ov", dmg_file
            ], check=True)
            print(f"macOS DMG created: {dmg_file}")
        except subprocess.CalledProcessError:
            print("Failed to create DMG. Creating a zip archive instead.")
            
            # If hdiutil fails, create a zip archive as fallback
            zip_file = "output/FileManager.zip"
            if os.path.exists(zip_file):
                os.remove(zip_file)
                
            shutil.make_archive(
                os.path.join("output", "FileManager"),
                'zip',
                os.path.dirname(app_path),
                os.path.basename(app_path)
            )
            print(f"macOS app archive created: {zip_file}")

if __name__ == "__main__":
    create_macos_installer() 