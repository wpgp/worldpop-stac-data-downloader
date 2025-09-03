"""
Download Tab UI Components
"""
import tkinter as tk
from tkinter import ttk


def setup_enhanced_download_tab(app):
    """Setup enhanced download tab with better progress tracking"""
    download_frame = ttk.Frame(app.notebook)
    app.notebook.add(download_frame, text="📥 Downloads")
    
    # Apply consistent styling
    download_frame.configure(padding=15, style="Clean.TFrame")
    
    # Download settings
    settings_frame = ttk.LabelFrame(download_frame, text="📁 Download Settings", 
                                  style='Clean.TLabelframe', padding=10)
    settings_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Directory selection
    dir_frame = ttk.Frame(settings_frame, style="Clean.TFrame")
    dir_frame.pack(fill=tk.X, pady=2)
    
    ttk.Label(dir_frame, text="Directory:", style="Clean.TLabel").pack(side=tk.LEFT)
    dir_entry = ttk.Entry(dir_frame, textvariable=app.download_dir, state="readonly", style="Clean.TEntry")
    dir_entry.pack(side=tk.LEFT)
    dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    ttk.Button(dir_frame, text="Browse", style='Clean.TButton',
              command=app.select_download_dir).pack(side=tk.RIGHT)
    
    # Download options
    options_frame = ttk.Frame(settings_frame, style="Clean.TFrame")
    options_frame.pack(fill=tk.X, pady=5)
    
    app.create_subfolders = tk.BooleanVar(value=True)
    ttk.Checkbutton(options_frame, text="Create subfolders by country/year", 
                   variable=app.create_subfolders, style='Clean.TCheckbutton').pack(side=tk.LEFT)
    
    # Selected items preview
    preview_frame = ttk.LabelFrame(download_frame, text="📋 Selected Items", 
                                 style='Clean.TLabelframe', padding=10)
    preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    # Create tree container frame for better layout control
    tree_container = ttk.Frame(preview_frame, style='Clean.TFrame')
    tree_container.pack(fill=tk.BOTH, expand=True)
    
    # Selected items tree
    selected_columns = ("Title", "Collection", "Item", "File Type", "Size", "Status")
    app.selected_tree = ttk.Treeview(tree_container, columns=selected_columns, 
                                   show="headings", height=10, style='Clean.Treeview')
    
    for col in selected_columns:
        if col == "Title":
            app.selected_tree.column(col, width=350)
        elif col == "Item":
            app.selected_tree.column(col, width=250)
        else:
            app.selected_tree.column(col, width=40)
        # app.selected_tree.column(col, width=300 if col in ["Item", "Title"] else 40)
        app.selected_tree.heading(col, text=col)
    
    selected_scroll = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=app.selected_tree.yview)
    app.selected_tree.configure(yscrollcommand=selected_scroll.set)
    
    app.selected_tree.grid(row=0, column=0, sticky='nsew')
    selected_scroll.grid(row=0, column=1, sticky='ns')
    
    # Add placeholder for empty downloads
    app.selected_placeholder = ttk.Frame(tree_container, style='Clean.TFrame')
    app.selected_placeholder.grid(row=0, column=0, sticky='nsew')
    
    placeholder_content = ttk.Frame(app.selected_placeholder, style='Clean.TFrame')
    placeholder_content.place(relx=0.5, rely=0.5, anchor='center')
    
    # Placeholder icon and text
    ttk.Label(placeholder_content, text="📥", font=('Segoe UI', 48), 
             style='Clean.TLabel').pack(pady=(0, 20))
    ttk.Label(placeholder_content, text="No items selected", 
             font=('Segoe UI', 16, 'bold'), style='Clean.TLabel').pack(pady=(0, 10))
    ttk.Label(placeholder_content, text="Select data from 'Search Results' tab to download", 
             font=('Segoe UI', 11), style='Clean.TLabel').pack()
    
    # Initially show placeholder
    app.selected_placeholder.tkraise()
    
    tree_container.columnconfigure(0, weight=1)
    tree_container.rowconfigure(0, weight=1)
    
    # Download controls section
    controls_section = ttk.Frame(download_frame, style='Clean.TFrame')
    controls_section.pack(fill=tk.X)
    
    # Main download controls
    download_controls = ttk.Frame(controls_section, style='Clean.TFrame')
    download_controls.pack(fill=tk.X)

    # Download buttons
    app.download_button = ttk.Button(download_controls, text="📥 Start Download",
                                    command=app.start_download, style='CleanPrimary.TButton')
    app.download_button.pack(side=tk.LEFT, padx=(0, 15))

    
    # Progress section
    progress_container = ttk.Frame(download_controls, style='Clean.TFrame')
    progress_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Main progress bar
    app.progress_var = tk.DoubleVar()
    app.progress_bar = ttk.Progressbar(progress_container, variable=app.progress_var, 
                                     mode='determinate', maximum=100)
    app.progress_bar.pack(fill=tk.X, pady=(5, 3))
    
    # Progress info
    app.progress_label = ttk.Label(progress_container, text="Ready to download",
                                 style='Clean.TLabel', font=('Segoe UI', 9))
    app.progress_label.pack(side=tk.LEFT)
    
    app.speed_label = ttk.Label(progress_container, text="",
                              style='Clean.TLabel', font=('Segoe UI', 9))
    app.speed_label.pack(side=tk.RIGHT)
    
    # Download stats
    stats_info_frame = ttk.Frame(progress_container, style='Clean.TFrame')
    stats_info_frame.pack(fill=tk.X, pady=(3, 0))
    
    app.download_stats = ttk.Label(stats_info_frame, text="", 
                                 style='Clean.TLabel', font=('Segoe UI', 8))
    app.download_stats.pack(side=tk.RIGHT)

    # Control buttons with variables to track download state
    app.download_active = tk.BooleanVar(value=False)

    app.stop_button = ttk.Button(download_controls, text="⏹ Stop Download",
                                 command=lambda: stop_download(app),
                                 style='Clean.TButton', state='disabled')
    app.stop_button.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 15))

    
    # Download control functions
    def stop_download(app):
        """Stop current download"""
        app.download_active.set(False)
        app.download_button.config(state='normal')
        app.stop_button.config(state='disabled')
        app.progress_var.set(0)
        app.progress_label.config(text="Download stopped")
        app.speed_label.config(text="")
        app.download_stats.config(text="")
    
    # Store function in app for access from operations
    app.stop_download = lambda: stop_download(app)