#!/usr/bin/env python3
import os
import sys
import platform
import argparse
from build import build_executable

def main():
    parser = argparse.ArgumentParser(description='Build File Manager executable packages')
    parser.add_argument('--platform', choices=['windows', 'macos', 'linux', 'all', 'current'],
                        default='current', help='Target platform (default: current)')
    args = parser.parse_args()
    
    # Determine the current OS
    current_os = platform.system().lower()
    if current_os == 'darwin':
        current_os = 'macos'
    
    # Determine which platforms to build for
    platforms_to_build = []
    if args.platform == 'all':
        platforms_to_build = ['windows', 'macos', 'linux']
    elif args.platform == 'current':
        platforms_to_build = [current_os]
    else:
        platforms_to_build = [args.platform]
    
    print(f"Building for platforms: {', '.join(platforms_to_build)}")
    
    # Build for each platform
    for platform_name in platforms_to_build:
        print(f"\n=== Building for {platform_name} ===\n")
        
        if platform_name == 'windows':
            if current_os == 'windows':
                from build_windows import create_windows_installer
                create_windows_installer()
            else:
                print(f"Warning: Building Windows installer on {current_os} will create a placeholder.")
                from build_windows import create_windows_installer
                create_windows_installer()
        
        elif platform_name == 'macos':
            if current_os == 'macos':
                from build_macos import create_macos_installer
                create_macos_installer()
            else:
                print(f"Warning: Cannot build macOS installer on {current_os}.")
        
        elif platform_name == 'linux':
            if current_os == 'linux':
                from build_linux import create_linux_installer
                create_linux_installer()
            else:
                print(f"Warning: Building Linux package on {current_os} will create a placeholder.")
                from build_linux import create_linux_installer
                create_linux_installer()
    
    print("\nBuild process completed!")
    print("Check the 'output' directory for the generated packages.")

if __name__ == "__main__":
    main() 