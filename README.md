# WorldPop STAC Data Downloader (Beta)

A desktop application for downloading WorldPop population data through the STAC API.

## Important Beta Version Notice

**This is beta software:**
- The executable is NOT digitally signed
- Antivirus software may show false positive warnings
- **Recommended**: Build the executable yourself using the instructions below

## Quick Start

### Method 1: Simple Build Using .bat File (Recommended)

**For users without terminal experience:**

1. **Download** or clone this repository
2. **Double-click** the `build.bat` file in the project folder
3. **Wait** for the build to complete (may take several minutes)
4. **Find** the ready executable in the `dist/` folder

The `build.bat` file automatically:
- Checks for Python installation
- Installs required dependencies
- Builds the executable
- Notifies when complete

### Method 2: Run from Source Code

**If you have Python installed:**

1. **Double-click** the `run.bat` file - the program will start immediately
2. Or run in terminal:
   ```bash
   python main.py
   ```

### Method 3: Manual Build via Terminal

**For experienced users:**

```bash
# 1. Clone repository
git clone <repository-url>
cd stac-data-downloader

# 2. Install dependencies
pip install -r requirements.txt

# 3. Build executable
python build_exe.py

# Ready file will be in dist/ folder
```

## Security Warnings

### Why might antivirus block the program?

**This is normal for beta version!** Reasons:

- The executable file has no digital signature
- The program is new and unknown to antivirus databases
- PyInstaller applications often trigger false positives

### What to do if antivirus blocks?

**Option 1 (Recommended):** Build it yourself
- Use `build.bat` for automatic building
- This way you can be sure of the code safety

**Option 2:** Add exception
- Add project folder to antivirus exceptions
- Temporarily disable protection during installation

**Option 3:** Use source code
- Run via `run.bat` or `python main.py`
- Does not require building executable

## Troubleshooting

### Build Problems

**"Python not found":**
- Install Python 3.8+ from [python.org](https://python.org)
- During installation, select "Add Python to PATH"

**"Dependency errors":**
- Run: `pip install -r requirements.txt`
- Ensure stable internet connection

**"PyInstaller errors":**
- The `build.bat` file will automatically install PyInstaller
- Or manually: `pip install pyinstaller`

### Runtime Problems

**"File won't start":**
- Check if file is blocked by antivirus
- Run as administrator
- Try rebuilding

**"API errors":**
- Check internet connection
- Ensure STAC API is accessible

## How to Use the Program

### 1. Search and Filter
- **Select Countries**: Browse and select countries of interest
- **Set Filters**: Year (2015-2030), resolution (100m/1km), project type
- **Search Data**: Click "Search Data" to find matching datasets

### 2. Search Results
- **View Results**: All datasets matching your criteria
- **Sort**: Click column headers to sort results
- **Select**: Check items you want to download
- **Details**: "Details" button for full metadata

### 3. Downloads
- **Select Folder**: Where to save files
- **Review Selection**: List of selected items
- **Configure Options**: Automatic folder organization by country/year
- **Start Download**: Monitor progress

## Available Data

- **Population Data**: Estimates and projections (2015-2030)
- **Demographics**: Age and sex breakdowns
- **Resolution**: 100m and 1km
- **Coverage**: All countries and territories

## Feedback

This is a beta version! Your feedback helps improve the product:

- **Found bugs**: Describe the problem in detail
- **Suggestions**: Ideas for functionality improvements
- **Testing**: Results on different systems
