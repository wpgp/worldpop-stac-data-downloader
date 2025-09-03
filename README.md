# WorldPop Desktop Application

A modern desktop application for browsing and downloading WorldPop population data through the STAC (SpatioTemporal Asset Catalog) API. This application provides an intuitive interface for accessing global population datasets, age/sex demographic data, and related geospatial information.

## About

This application connects to the WorldPop STAC API to provide easy access to:
- **Population Data**: Global population estimates and projections (2015-2030)
- **Age/Sex Demographics**: Detailed demographic breakdowns by age and gender
- **Multiple Resolutions**: Data available at 100m and 1km resolution
- **Global Coverage**: Data for all countries and territories

## Features

- **Browse Collections**: View all available country collections with metadata
- **Advanced Filtering**: Filter by year, resolution, data type, and project
- **Interactive Search**: Real-time search and filtering of datasets
- **Bulk Selection**: Select multiple datasets for batch downloading
- **Progress Tracking**: Monitor download progress with detailed statistics
- **Smart Organization**: Automatic folder creation by country and year
- **Preview & Details**: View thumbnails and detailed metadata for datasets

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: Minimum 4GB, recommended 8GB+
- **Disk Space**: 1GB+ for application, additional space for downloaded data
- **Internet**: Stable connection required for API access and downloads

## Installation & Setup

### Method 1: Run from Source (Development)

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API settings** in `config.py`:
   - Set `API_BASE_URL` to your WorldPop STAC API endpoint
   - Set `API_KEY` if authentication is required
4. **Run the application**:
   ```bash
   python main.py
   ```

### Method 2: Executable (Coming Soon)

A standalone executable version will be available for easy installation without Python dependencies.

To build the executable yourself:
```bash
python build_exe.py
```

## How to Use

### 1. Search & Filter Tab
- **Browse Countries**: View all available collections with search functionality
- **Select Countries**: Click to select/deselect countries of interest
- **Set Filters**: Choose years (2015-2030), resolution (100m/1km), and project types
- **Search Data**: Click "Search Data" to find matching datasets

### 2. Search Results Tab
- **Review Results**: View all datasets matching your criteria
- **Sort & Filter**: Click column headers to sort results
- **Select Items**: Check items you want to download
- **View Details**: Click "Details" button to see full metadata

### 3. Downloads Tab
- **Set Directory**: Choose where to save downloaded files
- **Review Selection**: See all selected items before downloading
- **Configure Options**: Enable subfolder organization by country/year
- **Start Download**: Monitor progress and manage downloads

## Available Data

### Filter Options
- **Years**: 2015-2030 (complete coverage)
- **Resolution**: 100m and 1km spatial resolution
- **Data Types**: Constrained and unconstrained population estimates
- **Projects**: Population totals and Age/Sex demographic breakdowns

### Data Formats
- **Population Data**: GeoTIFF raster files
- **Age/Sex Data**: ZIP archives containing multiple demographic layers
- **Metadata**: STAC-compliant JSON with full dataset information

## File Structure

```
worldpop-desktop-app/
├── src/
│   ├── core/
│   │   ├── app.py           # Main application class
│   │   └── operations.py    # Core business logic
│   └── ui/
│       ├── filter_tab.py    # Search & filter interface
│       ├── results_tab.py   # Search results display
│       ├── download_tab.py  # Download management
│       └── about_tab.py     # Application information
├── main.py                  # Application entry point
├── api_client.py           # STAC API client
├── config.py              # Configuration settings
├── build_exe.py           # Executable builder script
├── requirements.txt       # Python dependencies
└── README.md             # This documentation
```

## Development Status

⚠️ **Beta Testing Phase**: This application is currently in beta testing and under active development. 

- Core functionality is stable and working
- User interface and features are being refined based on feedback
- A digitally signed version for general distribution will be released soon
- Please report any issues or suggestions for improvement

## Building Executable

To create a standalone executable for Windows:

1. **Install PyInstaller** (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script**:
   ```bash
   python build_exe.py
   ```

3. **Find your executable** in the `dist/` folder

The executable will include all dependencies and can be run on Windows systems without Python installed.

## Troubleshooting

### Connection Issues
- Verify `API_BASE_URL` is correct in `config.py`
- Check that the STAC API server is running and accessible
- Ensure API key is valid if authentication is required
- Test network connectivity and firewall settings

### Download Issues
- Confirm write permissions to the selected download directory
- Check available disk space (datasets can be large)
- Verify download URLs are accessible from your network
- Try selecting a different download location

### Performance Issues
- Close other applications to free up system memory
- Choose fewer datasets for simultaneous download
- Select a local drive (not network drive) for downloads
- Check internet connection speed and stability

## Contributing

This application is part of the WorldPop project infrastructure. For feature requests, bug reports, or contributions:

1. Test thoroughly before reporting issues
2. Provide detailed information about your system and the problem
3. Include steps to reproduce any bugs
4. Suggest improvements based on actual usage experience

## License & Attribution

This application is designed to work with WorldPop STAC API for accessing global population data. 

- **WorldPop Data**: Please cite WorldPop datasets according to their licensing terms
- **Application**: Developed for the WorldPop project at the University of Southampton
- **STAC Standard**: Follows OGC SpatioTemporal Asset Catalog specifications