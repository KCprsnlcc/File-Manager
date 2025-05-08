# File Manager Release Notes

## Version 1.0.0

### Important Notice About This Release
**Current Release Status:**
- ✅ **macOS (.dmg)**: Ready for use - built on macOS
- ⚠️ **Windows (.exe)**: Placeholder only - must be built on Windows
- ⚠️ **Linux (.deb)**: Placeholder only - must be built on Linux

Since this release was built on macOS, only the macOS installer is fully functional. The Windows and Linux installers included in this release are placeholders and will not work properly. To get functional Windows and Linux installers, please follow the build instructions below on the respective platforms.

### Overview
This is the initial release of the File Manager application, a cross-platform file management tool built with PySide6.

### Build Instructions

#### Important Note on Cross-Platform Building
The File Manager application must be built separately on each target platform to create proper installers:

- **Windows**: Build on a Windows system to create a proper .exe installer
- **macOS**: Build on a macOS system to create a proper .dmg installer
- **Linux**: Build on a Linux system to create a proper .deb package

#### Building on Your Current Platform

1. Clone the repository:
   ```
   git clone https://github.com/KCprsnlcc/File-Manager.git
   cd File-Manager
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the build script for your platform:

   **On Windows:**
   ```
   python build_windows.py
   ```

   **On macOS:**
   ```
   python build_macos.py
   ```

   **On Linux:**
   ```
   python build_linux.py
   ```

4. Find your installer in the `output` directory:
   - Windows: `FileManager-Setup.exe`
   - macOS: `FileManager.dmg`
   - Linux: `filemanager_1.0.0_amd64.deb`

#### Alternative: Using the Unified Build Script

You can also use the unified build script which will automatically detect your platform:
```
python build_all.py
```

To build for a specific platform (creates placeholder installers if not on that platform):
```
python build_all.py --platform windows|macos|linux
```

### Installation Instructions

#### Windows
1. Download `FileManager-Setup.exe` (Note: If downloaded from this release, you'll need to build it on Windows first)
2. Double-click the installer and follow the prompts
3. Launch from the Start Menu or desktop shortcut

#### macOS
1. Download `FileManager.dmg`
2. Open the disk image
3. Drag the File Manager app to your Applications folder
4. Launch from Applications or the Dock

#### Linux
1. Download `filemanager_1.0.0_amd64.deb` (Note: If downloaded from this release, you'll need to build it on Linux first)
2. Install using:
   ```
   sudo dpkg -i filemanager_1.0.0_amd64.deb
   ```
   or double-click the package in your file manager
3. Launch from your applications menu

### Known Issues
- Building installers on a different platform than the target will create placeholder files
- Windows builds must be created on Windows for proper functionality
- Linux builds must be created on Linux for proper functionality
- macOS builds must be created on macOS for proper functionality

### GitHub Releases
All three platform installers are available on the GitHub releases page, but remember that only the installer for the platform it was built on will work properly:
https://github.com/KCprsnlcc/File-Manager/releases

### Features

- Browse and manage files and directories
- Copy, move, delete, and rename files
- Create new directories
- View file properties
- Simple and intuitive user interface

### System Requirements

- Windows 10 or later
- macOS 10.14 or later
- Ubuntu 20.04 or later (or other compatible Linux distributions)

### SHA-256 Checksums

```
6b615691269187efb7cd3b950de6272cc7041e8e821b9d1dc7b4a8a2d96c52a2  FileManager-Setup.exe
b24bf723ef9fe556d9571192be8887be92e1749b0a0cacfdbc2d75eb3844e748  FileManager.dmg
f3b85a5baf3895dcdb81ac82c32705f8ba92ecdb3122bafcd0e9e3fe8bbd61ca  filemanager_1.0.0_amd64.deb
```

### Changelog

- Initial release

### License

This software is released under the License. See LICENSE.md for details.