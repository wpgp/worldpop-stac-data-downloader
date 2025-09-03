"""
About Tab UI Components
"""
import tkinter as tk
from tkinter import ttk
import webbrowser
import sys
import platform
from datetime import datetime


def setup_about_tab(app):
    """Setup About tab with software information"""
    about_frame = ttk.Frame(app.notebook)
    app.notebook.add(about_frame, text="About")
    
    # Create scrollable frame
    canvas = tk.Canvas(about_frame, bg='white')
    scrollbar = ttk.Scrollbar(about_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas, style='Clean.TFrame')
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Main content container - centered with max width
    outer_container = ttk.Frame(scrollable_frame, style='Clean.TFrame')
    outer_container.pack(fill=tk.BOTH, expand=True)
    
    # Create a frame to center content horizontally
    center_frame = ttk.Frame(outer_container, style='Clean.TFrame')
    center_frame.pack(expand=True, fill=tk.Y)
    
    # Centered content with fixed maximum width
    content = ttk.Frame(center_frame, style='Clean.TFrame', padding=30)
    content.pack(padx=100)  # This creates margins on both sides for centering
    
    # Header section with logo/title
    header_frame = ttk.Frame(content, style='Clean.TFrame')
    header_frame.pack(fill=tk.X, pady=(0, 30))
    
    # App title and version
    title_label = ttk.Label(header_frame, text="WorldPop STAC Data Downloader", 
                          font=('Segoe UI', 24, 'bold'), style='Clean.TLabel')
    title_label.pack(anchor='w')
    
    version_label = ttk.Label(header_frame, text="Version 1.0.0", 
                            font=('Segoe UI', 12), style='Clean.TLabel')
    version_label.pack(anchor='w', pady=(5, 0))
    
    # Description section
    desc_frame = ttk.LabelFrame(content, text="📝 Description", 
                              style='Clean.TLabelframe', padding=20)
    desc_frame.pack(fill=tk.X, pady=(0, 20))
    
    description_text = '''A desktop application for browsing, searching, and downloading WorldPop population and demographic datasets through the STAC (SpatioTemporal Asset Catalog) API. 

This application provides an intuitive interface to:
• Browse WorldPop collections by country and region
• Filter data by year, resolution, and project type  
• Search and preview datasets with detailed metadata
• Download files with organized folder structures
• Access comprehensive dataset information and thumbnails

Built specifically for researchers, analysts, and organizations working with population and demographic data.

DOI:
10.5258/SOTON/WP00839
10.5258/SOTON/WP00840
10.5258/SOTON/WP00842
10.5258/SOTON/WP00842
'''
    
    desc_label = ttk.Label(desc_frame, text=description_text, 
                         font=('Segoe UI', 10), wraplength=600, justify=tk.LEFT,
                         style='Clean.TLabel')
    desc_label.pack(anchor='w')

    def open_email():
        webbrowser.open("B.Nosatiuk@soton.ac.uk")


    # Developer section
    dev_frame = ttk.LabelFrame(content, text="👥 Development Team", 
                             style='Clean.TLabelframe', padding=20)
    dev_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Lead developer
    ttk.Label(dev_frame, text="Lead Developer:", font=('Segoe UI', 10, 'bold'),
             style='Clean.TLabel').pack(anchor='w')
    ttk.Label(dev_frame, text="Borys Nosatiuk", font=('Segoe UI', 10),
             style='Clean.TLabel').pack(anchor='w', padx=(20, 0))
    ttk.Label(dev_frame, text="Team:", font=('Segoe UI', 10, 'bold'),
             style='Clean.TLabel').pack(anchor='w')
    ttk.Label(dev_frame, text="Maksym Bondarenko", font=('Segoe UI', 10),
             style='Clean.TLabel').pack(anchor='w', padx=(20, 0))
    ttk.Label(dev_frame, text="Rhorom Priyatikanto", font=('Segoe UI', 10),
             style='Clean.TLabel').pack(anchor='w', padx=(20, 0))
    ttk.Label(dev_frame, text="Wenbin Zhang", font=('Segoe UI', 10),
             style='Clean.TLabel').pack(anchor='w', padx=(20, 0))
    ttk.Label(dev_frame, text="Tom McKeen", font=('Segoe UI', 10),
             style='Clean.TLabel').pack(anchor='w', padx=(20, 0))

    # Organization
    ttk.Label(dev_frame, text="Organization:", font=('Segoe UI', 10, 'bold'),
             style='Clean.TLabel').pack(anchor='w', pady=(10, 0))
    ttk.Label(dev_frame, text="WorldPop, Geography and Env. Science, University of Southampton", font=('Segoe UI', 10),
             style='Clean.TLabel').pack(anchor='w', padx=(20, 0))
    
    # Contact
    ttk.Label(dev_frame, text="Contact:", font=('Segoe UI', 10, 'bold'),
             style='Clean.TLabel').pack(anchor='w', pady=(10, 0))

    email_label = ttk.Label(dev_frame, text="B.Nosatiuk@soton.ac.uk", font=('Segoe UI', 10, 'underline'),
                           foreground='blue', cursor='hand2', style='Clean.TLabel')
    email_label.pack(anchor='w', padx=(20, 0))
    email_label.bind("<Button-1>", lambda e: open_email())
    
    # Links section
    links_frame = ttk.LabelFrame(content, text="🔗 Useful Links", 
                               style='Clean.TLabelframe', padding=20)
    links_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Create clickable links
    links = [
        ("WorldPop Website", "https://www.worldpop.org"),
        ("STAC API Documentation", "https://api.stac.worldpop.org/documentation"),
        ("STAC API Swagger", "https://api.stac.worldpop.org/api.html"),
        ("GitHub Repository", "https://github.com/worldpop/worldpop-stac-downloader"),
        ("Report Issues", "https://github.com/worldpop/worldpop-stac-downloader/issues"),
        ("Support portal", "https://sdi.worldpop.org"),
        ("WorldPop Global 2 Release Statement R2025A v1", "https://data.worldpop.org/repo/prj/Global_2015_2030/R2025A/doc/Global2_Release_Statement_R2025A_v1.pdf")
    ]
    
    for link_text, url in links:
        link_frame = ttk.Frame(links_frame, style='Clean.TFrame')
        link_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(link_frame, text="• ", font=('Segoe UI', 10),
                 style='Clean.TLabel').pack(side=tk.LEFT)
        
        link_label = ttk.Label(link_frame, text=link_text, font=('Segoe UI', 10, 'underline'),
                              foreground='blue', cursor='hand2', style='Clean.TLabel')
        link_label.pack(side=tk.LEFT)
        link_label.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
    
    # License section
    license_frame = ttk.LabelFrame(content, text="📄 License", 
                                 style='Clean.TLabelframe', padding=20)
    license_frame.pack(fill=tk.X, pady=(0, 20))
    
    license_text = '''MIT License

Copyright (c) 2024 WorldPop Research Group

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.'''
    
    license_label = ttk.Label(license_frame, text=license_text, 
                            font=('Consolas', 8), wraplength=600, justify=tk.LEFT,
                            style='Clean.TLabel')
    license_label.pack(anchor='w')
    
    # System Info section
    sysinfo_frame = ttk.LabelFrame(content, text="💻 System Information", 
                                 style='Clean.TLabelframe', padding=20)
    sysinfo_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Collect system information
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    sys_info = [
        ("Application Version", "1.0.0"),
        ("Python Version", python_version),
        ("Platform", platform.system()),
        ("Architecture", platform.machine()),
        ("OS Version", platform.release()),
        ("Build Date", datetime.now().strftime("%B %Y"))
    ]
    
    # Create two columns for system info
    sys_left = ttk.Frame(sysinfo_frame, style='Clean.TFrame')
    sys_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    sys_right = ttk.Frame(sysinfo_frame, style='Clean.TFrame') 
    sys_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    for i, (label, value) in enumerate(sys_info):
        target_frame = sys_left if i < 3 else sys_right
        
        info_frame = ttk.Frame(target_frame, style='Clean.TFrame')
        info_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(info_frame, text=f"{label}:", font=('Segoe UI', 9, 'bold'),
                 style='Clean.TLabel').pack(side=tk.LEFT)
        ttk.Label(info_frame, text=value, font=('Segoe UI', 9),
                 style='Clean.TLabel').pack(side=tk.LEFT, padx=(10, 0))
    
    # Acknowledgments section
    ack_frame = ttk.LabelFrame(content, text="🙏 Acknowledgments", 
                             style='Clean.TLabelframe', padding=20)
    ack_frame.pack(fill=tk.X, pady=(0, 20))
    
    ack_text = '''This application was developed using:

• Python and Tkinter for the user interface
• STAC (SpatioTemporal Asset Catalog) specification for data discovery
• FastAPI for the backend STAC API implementation
• PostgreSQL with pgSTAC extension for spatial data storage
• Various open-source libraries and frameworks

Special thanks to the STAC community and all contributors to the open-source geospatial ecosystem.'''
    
    ack_label = ttk.Label(ack_frame, text=ack_text, 
                        font=('Segoe UI', 9), wraplength=600, justify=tk.LEFT,
                        style='Clean.TLabel')
    ack_label.pack(anchor='w')
    
    # Footer with copyright
    footer_frame = ttk.Frame(content, style='Clean.TFrame')
    footer_frame.pack(fill=tk.X, pady=(20, 0))
    
    footer_text = f"© {datetime.now().year} WorldPop Research Group. All rights reserved."
    footer_label = ttk.Label(footer_frame, text=footer_text, 
                           font=('Segoe UI', 8, 'italic'), style='Clean.TLabel')
    footer_label.pack(anchor='center')
    
    # Pack scrollable components
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind("<MouseWheel>", on_mousewheel)
    
    return about_frame