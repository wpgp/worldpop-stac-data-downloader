"""
Build script for creating standalone Windows executable
"""
import subprocess
import sys
import os
import shutil
from pathlib import Path

def check_dependencies():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller found (version {PyInstaller.__version__})")
        return True
    except ImportError:
        print("PyInstaller not found!")
        print("Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install PyInstaller")
            return False

def clean_build_directories():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)

def find_icon():
    """Find application icon"""
    # Look for .ico files first (best for Windows)
    icon_files = ['icon.ico', 'app_icon.ico', 'worldpop_icon.ico']

    # Check in src/components directory first
    components_dir = os.path.join('src', 'components')
    if os.path.exists(components_dir):
        for icon in icon_files:
            icon_path = os.path.join(components_dir, icon)
            if os.path.exists(icon_path):
                print(f"✓ Using icon: {icon_path}")
                return icon_path

    # Fallback to root directory
    for icon in icon_files:
        if os.path.exists(icon):
            print(f"✓ Using icon: {icon}")
            return icon
            
    print("No .ico icon found, using default")
    return None

def build_executable():
    """Build standalone executable using PyInstaller"""
    print("Building WorldPop STAC Browser executable for Windows...")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Clean build directories
    clean_build_directories()
    
    # Find icon
    icon_path = find_icon()
    
    try:
        # Build PyInstaller command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--onefile",  # Single file executable
            "--windowed",  # No console window
            "--name", "WorldPop_STAC_Data_Downloader",
            "--distpath", "dist",
            "--workpath", "build",
            "--add-data", "src;src",  # Include src directory
            "--hidden-import", "PIL",
            "--hidden-import", "PIL._tkinter_finder", 
            "--hidden-import", "PIL.Image",
            "--hidden-import", "PIL.ImageTk",
            "--hidden-import", "tkinter",
            "--hidden-import", "requests",
            "--hidden-import", "urllib3",
            "--collect-all", "tkinter",
            "--collect-all", "PIL",
        ]

        # Add icon if found
        if icon_path:
            if icon_path.endswith('.ico'):
                cmd.extend(["--icon", icon_path])
            else:
                print("Icon file is not .ico format, skipping icon")

        # Add components directory with all assets
        components_dir = os.path.join('src', 'components')
        if os.path.exists(components_dir):
            cmd.extend(["--add-data", f"{components_dir};src/components"])
        
        # Add individual data files from root (fallback)
        data_files = ['worldpop_logo.png', 'company_logo.png']
        for file in data_files:
            if os.path.exists(file):
                cmd.extend(["--add-data", f"{file};."])

        cmd.append("main.py")
        
        print("Running PyInstaller...")
        print(f"Command: {' '.join(cmd)}")
        print("-" * 60)

        result = subprocess.run(cmd, check=True, capture_output=False)
        
        # Check if executable was created
        exe_path = os.path.abspath("dist/WorldPop_STAC_Data_Downloader.exe")
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024*1024)  # Size in MB
            
            print("\n" + "=" * 60)
            print("BUILD SUCCESSFUL!")
            print("=" * 60)
            print(f"Executable location: {exe_path}")
            print(f"File size: {file_size:.1f} MB")
            print(f"Target OS: Windows")

            print("\nBeta Version Notice:")
            print("• This is a beta version currently under testing")
            print("• A digitally signed version will be available soon")
            print("• Report any issues for improvement")

            return True
        else:
            print("Executable was not created successfully")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print("\nTroubleshooting:")
        print("• Make sure all dependencies are installed (pip install -r requirements.txt)")
        print("• Check that main.py exists and runs without errors")
        print("• Try running with --debug flag for more details")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main build function"""
    print("WorldPop STAC Browser - Executable Builder")
    print("=" * 60)
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("This build script is optimized for Windows")
        print("Building anyway, but some features may not work correctly...")

    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("main.py not found in current directory")
        print("Please run this script from the application root directory")
        return False

    # Build executable
    success = build_executable()
    
    if success:
        print("\nNext steps:")
        print("1. Test the executable on your system")
        print("2. Test on other Windows machines if possible")
        print("3. Report any issues for fixes before release")
        print("4. The exe is ready for beta testing distribution")
    else:
        print("\nBuild failed. Please check the error messages above.")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)