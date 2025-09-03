"""
Configuration settings for WorldPop Desktop App
"""
import os

# API Configuration
API_BASE_URL = "https://api.stac.worldpop.org"
API_KEY = os.getenv("WORLDPOP_API_KEY", "")

# Available filter options
AVAILABLE_YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
AVAILABLE_RESOLUTIONS = ["100m", "1km"]
AVAILABLE_PROJECTS = ["Population", "Age and Sex Structures"]

# Download settings
DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "WorldPop_Data")
CHUNK_SIZE = 8192  # 8KB chunks for downloading