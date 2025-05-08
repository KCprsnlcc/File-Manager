# Building File Manager Executables

This document explains how to build executable packages for Windows, macOS, and Linux.

## Prerequisites

- Python 3.7 or higher
- PySide6
- Platform-specific tools (details below)

## Common Build Process

For all platforms, make sure you have Python and the required dependencies installed:

```bash
pip install -r requirements.txt
```

## Quick Build (Recommended)

Use the `build_all.py` script to build for the current platform or specify a target platform:

```bash
# Build for the current platform
python build_all.py

# Build for a specific platform
python build_all.py --platform windows
python build_all.py --platform macos
python build_all.py --platform linux

# Build for all platforms (creates placeholders for non-current platforms)
python build_all.py --platform all
```

## Platform-Specific Build Instructions

### Windows (.exe)

1. Install requirements:
   - [Chocolatey](https://chocolatey.org/install)
   - NSIS (will be installed automatically by the script if needed)

2. Run the build script:
   ```bash
   python build_windows.py
   ```

3. The installer will be created in the `output` directory as `FileManager-Setup.exe`

### macOS (.dmg)

1. Install requirements:
   - [Homebrew](https://brew.sh/)
   - create-dmg (will be installed automatically by the script if needed)

2. Run the build script:
   ```bash
   python build_macos.py
   ```

3. The DMG file will be created in the `output` directory as `FileManager.dmg`

### Linux (.deb)

1. Install requirements:
   - dpkg-dev (will be installed automatically by the script if needed)

2. Run the build script:
   ```bash
   python build_linux.py
   ```

3. The Debian package will be created in the `output` directory as `filemanager_1.0.0_amd64.deb`

## Manual Building

If you prefer to build manually without using the provided scripts:

1. Build with PyInstaller:
   ```bash
   pyinstaller --name=FileManager --onedir --windowed --clean --noconfirm file_manager.py
   ```

2. The executable will be in the `dist/FileManager` directory.

## Cross-Platform Building

Note that building installers on a platform different from the target platform will create placeholder files. For proper installers, you should build on each target platform:

- Build Windows installers on Windows
- Build macOS installers on macOS
- Build Linux installers on Linux

## Uploading to GitHub

After building the packages, you can upload them to GitHub releases:

1. Create a new release on GitHub
2. Upload the generated packages from the `output` directory
3. Add release notes explaining the changes

## Troubleshooting

- If you encounter any issues with dependencies, make sure you have installed all required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

- For platform-specific issues, check the console output for error messages that can help identify the problem. 