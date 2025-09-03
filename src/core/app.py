"""
Main Application Class for WorldPop Desktop Application
"""
import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.config import (
    API_BASE_URL, API_KEY, AVAILABLE_YEARS, AVAILABLE_RESOLUTIONS,
    AVAILABLE_PROJECTS, DEFAULT_DOWNLOAD_DIR
)
from src.core.api_client import WorldPopSTACClient

from src.core.operations import AppOperations
from src.ui.filter_tab import setup_enhanced_filter_tab
from src.ui.results_tab import setup_enhanced_results_tab
from src.ui.download_tab import setup_enhanced_download_tab
from src.ui.about_tab import setup_about_tab


class WorldPopApp(AppOperations):
    def __init__(self, root):
        self.root = root
        self.setup_window()

        # Initialize API client
        self.client = WorldPopSTACClient(API_BASE_URL, API_KEY)

        # State variables
        self.collections = []
        self.search_results = []
        self.selected_items = []
        self.download_dir = tk.StringVar(value=DEFAULT_DOWNLOAD_DIR)

        # UI Theme colors
        self.colors = {
            'bg': '#ADD8E6',
            'primary': '#2e7d32',  # Green
            'secondary': '#1976d2',  # Blue  
            'accent': '#ff6f00',  # Orange
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336',
            'text': '#212121',
            'text_light': '#757575'
        }

        self.setup_styles()
        self.setup_ui()
        self.load_collections()

    def setup_window(self):
        """Setup main window properties"""
        self.root.title("WorldPop STAC API Browser & Downloader")
        self.root.geometry("1300x900")
        self.root.minsize(1000, 850)

        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # Set window icon (if available)
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'components', 'icon.ico')
            self.root.iconbitmap(icon_path)
        except:
            pass  # Icon not available

    def setup_styles(self):
        """Setup custom ttk styles"""
        self.style = ttk.Style()

        # Configure custom styles
        self.style.configure('Title.TLabel', font=('Arial', 20, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        self.style.configure('Info.TLabel', font=('Arial', 10), foreground=self.colors['text_light'])
        self.style.configure('Status.TLabel', font=('Arial', 10, 'bold'))
        self.style.configure('Success.TLabel', foreground=self.colors['success'])
        self.style.configure('Warning.TLabel', foreground=self.colors['warning'])
        self.style.configure('Error.TLabel', foreground=self.colors['error'])

        # Button styles
        self.style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Secondary.TButton', font=('Arial', 9))

        # Modern Notebook tab styles
        self.style.configure('Modern.TNotebook',
                             background='#ffffff',
                             borderwidth=0,
                             tabmargins=[0, 0, 0, 0])

        self.style.configure('Modern.TNotebook.Tab',
                             background='#f8f9fa',
                             foreground='#757575',
                             padding=[10, 10],
                             font=('Segoe UI', 10, 'bold'),
                             borderwidth=1,
                             focuscolor='1976d2')

        # Active tab styling  
        self.style.map('Modern.TNotebook.Tab',
                       background=[('selected', '#ffffff'),
                                   ('active', '#e9ecef')],
                       foreground=[('selected', '#1976d2'),
                                   ('active', '#1976d2')],
                       relief=[('selected', 'flat'),
                               ('active', 'flat')])

    def setup_ui(self):
        """Setup user interface"""
        # Header
        self.setup_header()

        # Main content
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Main content notebook
        self.setup_main_content(main_frame)

        # Footer with status
        self.setup_footer()

    def setup_header(self):
        """Setup application header with title and connection status"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        # Logo section (left side)
        logo_frame = ttk.Frame(header_frame)
        logo_frame.pack(side=tk.LEFT, padx=(0, 20))

        # Load logos
        self.load_logos(logo_frame)

        # Title section
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(title_frame, text="WorldPop STAC API",
                  style='Title.TLabel').pack(anchor=tk.W)

        ttk.Label(title_frame, text="Browse, search, and download population datasets",
                  style='Info.TLabel').pack(anchor=tk.W)

        # Connection status
        status_frame = ttk.Frame(header_frame)
        status_frame.pack(side=tk.RIGHT)

        ttk.Label(status_frame, text="API Status:", style='Subtitle.TLabel').pack(anchor=tk.E)
        self.connection_status = ttk.Label(status_frame, text="Connecting...",
                                           style='Warning.TLabel')
        self.connection_status.pack(anchor=tk.E)

        ttk.Label(status_frame, text=f"URL: {API_BASE_URL}",
                  style='Info.TLabel').pack(anchor=tk.E)

        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, padx=10)

    def setup_main_content(self, parent):
        """Setup main content area with improved notebook"""

        notebook_container = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
        notebook_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.notebook = ttk.Notebook(notebook_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 5))

        setup_enhanced_filter_tab(self)
        setup_enhanced_results_tab(self)
        setup_enhanced_download_tab(self)
        setup_about_tab(self)

        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def setup_footer(self):
        """Setup application footer with status information"""
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Separator(footer_frame, orient='horizontal').pack(fill=tk.X)

        status_frame = ttk.Frame(footer_frame)
        status_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_text = ttk.Label(status_frame, text="Ready")
        self.status_text.pack(side=tk.LEFT)

        ttk.Label(status_frame, text=f"WorldPop STAC Data Downloader v1.0.0 | {datetime.now().year}",
                  style='Info.TLabel').pack(side=tk.RIGHT)

    def load_logos(self, parent_frame):
        """Load and display company logos"""
        # Logo files to look for (you can add more logos)
        logo_files = [
            'worldpop_logo.png',
            'university_logo.png',
            # 'logo1.png',
            # 'logo2.png',
        ]

        logo_width = 250
        logo_height = 60
        logos_loaded = 0
        max_logos = 2

        for logo_file in logo_files:
            if logos_loaded >= max_logos:
                break

            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'components', logo_file)

            if os.path.exists(logo_path):
                try:
                    try:
                        # Use PIL for better image handling with fixed dimensions
                        pil_image = Image.open(logo_path)

                        # Resize to exact dimensions (may distort aspect ratio slightly)
                        # Use LANCZOS for high quality scaling
                        pil_image = pil_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

                        # Convert to PhotoImage
                        tk_image = ImageTk.PhotoImage(pil_image)
                    except Exception as e:
                        # Fallback to basic tkinter (limited format support)
                        # Note: tkinter PhotoImage has limited resizing capabilities
                        tk_image = tk.PhotoImage(file=logo_path)
                        # For tkinter, we'll subsample if the image is too large
                        if hasattr(tk_image, 'width') and hasattr(tk_image, 'height'):
                            if tk_image.width() > logo_width or tk_image.height() > logo_height:
                                # Calculate subsample factors
                                x_factor = max(1, tk_image.width() // logo_width)
                                y_factor = max(1, tk_image.height() // logo_height)
                                factor = max(x_factor, y_factor)
                                tk_image = tk_image.subsample(factor)

                    # Create a frame with fixed size to contain the logo
                    logo_container = ttk.Frame(parent_frame, width=logo_width + 4, height=logo_height)
                    logo_container.pack_propagate(False)  # Don't let children resize the container
                    logo_container.pack(side=tk.RIGHT, padx=(5, 20))

                    # Create label with logo inside the container
                    logo_label = ttk.Label(logo_container, image=tk_image)
                    logo_label.image = tk_image  # Keep a reference to prevent garbage collection
                    logo_label.pack(expand=True)  # Center the image in the container

                    logos_loaded += 1

                except Exception as e:
                    print(f"Failed to load logo {logo_file}: {e}")
                    continue

        # If no logos were loaded, show text placeholder
        if logos_loaded == 0:
            # Create a styled frame to look like a logo placeholder
            logo_placeholder = ttk.Frame(parent_frame, relief='solid', borderwidth=1)
            logo_placeholder.pack(side=tk.LEFT, padx=(0, 10))

            ttk.Label(logo_placeholder, text="🏢", font=('Arial', 24)).pack(padx=10, pady=10)
            ttk.Label(logo_placeholder, text="Company\nLogo",
                      font=('Arial', 8), style='Info.TLabel').pack(padx=10, pady=(0, 10))

    def on_tab_changed(self, event):
        """Handle tab change events"""
        selected_tab = event.widget.tab('current')['text']
        if "Results" in selected_tab:
            self.update_stats()
        elif "Downloads" in selected_tab:
            self.update_selected_tree()

    def update_stats(self):
        """Update statistics in sidebar"""
        # Count visible collections in tree
        visible_collections = len(self.collections_tree.get_children())

        # Count selected collections 
        selected_collections = 0
        for item in self.collections_tree.get_children():
            if self.collections_tree.item(item, 'text') == '☑':
                selected_collections += 1

        # Update labels
        self.stats_collections.config(text=str(visible_collections))
        if hasattr(self, 'stats_results'):
            self.stats_results.config(text=str(len(self.search_results)))
        self.stats_selected.config(text=str(selected_collections))
