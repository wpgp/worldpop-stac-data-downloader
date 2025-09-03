"""
Modern Filter Tab UI Components - Clean Professional Design
"""
import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config.config import AVAILABLE_YEARS, AVAILABLE_RESOLUTIONS, AVAILABLE_PROJECTS
from .thumbnail_preview import show_thumbnail_preview
from .collection_details import show_collection_details


def setup_professional_styles(app):
    """Setup clean professional styles"""
    style = ttk.Style()
    
    # Clean color scheme - minimal and professional
    colors = {
        'bg': '#ffffff',           # Pure white
        'bg_secondary': '#f8f9fa', # Very light gray
        'border': '#dee2e6',       # Light border
        'text': '#212529',         # Dark text
        'text_secondary': '#6c757d', # Muted text
        'accent': '#495057',       # Professional dark gray
        'hover': '#e9ecef'         # Subtle hover
    }
    
    # Configure clean frame styles
    style.configure('WriteTLabelframe',
                   background=colors['bg'],
                   borderwidth=1)

    style.configure('Clean.TLabelframe', 
                   background=colors['bg'],
                   borderwidth=1,
                   relief='solid')
    
    # Clean frame style for search sections
    style.configure('Clean.TFrame',
                   background=colors['bg'])

    style.configure('Clean.TEntry',
                   background=colors['bg'])


    # Clean label style
    style.configure('Clean.TLabel',
                   background=colors['bg'],
                   foreground=colors['text'])
    
    style.configure('Clean.TLabelframe.Label',
                   background=colors['bg'],
                   foreground=colors['text'],
                   font=('Segoe UI', 10, 'bold'))
    
    # Professional button style
    style.configure('Clean.TButton',
                   background=colors['bg_secondary'],
                   foreground=colors['text'],
                   borderwidth=1,
                   relief='solid',
                   font=('Segoe UI', 10),
                   padding=(6, 3))
    
    # Clean checkbutton style
    style.configure('Clean.TCheckbutton',
                   background=colors['bg'],
                   foreground=colors['text'],
                   font=('Segoe UI', 10))

    # Treeview style
    style.configure('Clean.Treeview',
                    font=('Segoe UI', 10),
                    rowheight=25)

    style.configure('Clean.Treeview.Heading',
                    font=('Segoe UI', 10, 'bold'))

    # Filter frame style
    style.configure('Filter.TLabelframe',
                   background=colors['bg'],
                   borderwidth=1,
                   relief='solid',
                   padding=15)
    
    style.configure('Filter.TLabelframe.Label',
                   background=colors['bg'],
                   foreground=colors['text'],
                   font=('Segoe UI', 10, 'bold'))
    
    # Primary action button
    style.configure('CleanPrimary.TButton',
                   background=colors['bg_secondary'],
                   foreground="#1976d2",
                   borderwidth=1,
                   relief='solid',
                   font=('Segoe UI', 10, 'bold'),
                   padding=(20, 8))
    
    # Map hover state
    style.map('CleanPrimary.TButton',
             background=[('active', colors['text']),
                        ('pressed', colors['text'])])
    
    return colors


def setup_enhanced_filter_tab(app):
    """Setup clean professional filter tab"""
    # Main container with clean background
    main_container = ttk.Frame(app.notebook)
    app.notebook.add(main_container, text="🔍  Search & Filter")
    
    colors = setup_professional_styles(app)
    
    # Create main layout with proper spacing
    main_container.configure(padding=15, style="Clean.TLabelframe")
    
    # Top section - Country Search and Selection (full width)
    countries_section = ttk.LabelFrame(main_container, text="Countries & Regions", 
                                     style='Clean.TLabelframe', padding=10)
    countries_section.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    # Search input
    search_frame = ttk.Frame(countries_section, padding=10)
    search_frame.pack(fill=tk.X, pady=(0, 8))
    
    ttk.Label(search_frame, text="Search:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
    app.collection_search = ttk.Entry(search_frame, font=('Segoe UI', 12), width=25, foreground=colors['text'])
    app.collection_search.pack(side=tk.LEFT)
    app.collection_search.pack(side=tk.LEFT, padx=(0, 5))
    app.collection_search.bind('<KeyRelease>', app.filter_collections)
    
    def clear_search():
        app.collection_search.delete(0, tk.END)
        app.filter_collections(None)  # Trigger filtering to show all results
    
    clear_btn = ttk.Button(search_frame, text="Clear", style='Clean.TButton',
                          command=clear_search)
    clear_btn.pack(side=tk.LEFT, padx=(0, 15))
    
    # Quick actions
    ttk.Button(search_frame, text="Select All", style='Clean.TButton',
              command=app.select_all_collections).pack(side=tk.LEFT, padx=(0, 5))
    def clear_all_selections():
        for item in app.collections_tree.get_children():
            app.collections_tree.item(item, text='☐')
        app.update_stats()
    
    ttk.Button(search_frame, text="Clear All", style='Clean.TButton',
              command=clear_all_selections).pack(side=tk.LEFT, padx=(0, 5))
    
    # Statistics on the right
    ttk.Label(search_frame, text="Collections:", font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(15, 5))
    app.stats_collections = ttk.Label(search_frame, text="0", font=('Segoe UI', 9, 'bold'))
    app.stats_collections.pack(side=tk.LEFT, padx=(0, 15))
    
    ttk.Label(search_frame, text="Selected:", font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(15, 5))
    app.stats_selected = ttk.Label(search_frame, text="0", font=('Segoe UI', 9, 'bold'))
    app.stats_selected.pack(side=tk.LEFT, padx=(0, 15))

    ttk.Label(search_frame, text="Search Results:", font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(15, 5))

    app.stats_results = ttk.Label(search_frame, text="0", font=('Segoe UI', 9, 'bold'))
    app.stats_results.pack(side=tk.LEFT, padx=(0, 15))
    
    # Collections list
    list_frame = ttk.Frame(countries_section)
    list_frame.pack(fill=tk.BOTH, expand=True)

    columns = ("Country", "Updated", "Preview", "Details")
    app.collections_tree = ttk.Treeview(list_frame, columns=columns,
                                        show="tree headings", height=10, style='Clean.Treeview')

    # Configure columns
    app.collections_tree.column("#0", width=20, anchor='center')
    app.collections_tree.heading("#0", text="Select")
    
    app.collections_tree.column("Country", width=200, anchor='w')
    app.collections_tree.heading("Country", text="Country / Region")
    
    app.collections_tree.column("Updated", width=90, anchor='center')
    app.collections_tree.heading("Updated", text="Updated")
    
    app.collections_tree.column("Preview", width=80, anchor='center')
    app.collections_tree.heading("Preview", text="Preview")
    
    app.collections_tree.column("Details", width=80, anchor='center')
    app.collections_tree.heading("Details", text="Details")
    
    # Scrollbar
    tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=app.collections_tree.yview)
    app.collections_tree.configure(yscrollcommand=tree_scroll.set)
    
    app.collections_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Configure row styling for button appearance
    app.collections_tree.tag_configure('button_cell', background='#f8f9fa', foreground='#495057')
    app.collections_tree.tag_configure('button_hover', background='#e9ecef', foreground='#0d6efd')
    
    # Bind events - separate handling for selection vs preview
    def handle_tree_click(event):
        region = app.collections_tree.identify_region(event.x, event.y)
        column = app.collections_tree.identify_column(event.x)
        item = app.collections_tree.identify('item', event.x, event.y)
        
        # print(f"Click: region={region}, column={column}, item={item}")  # Debug
        
        if region == "cell" and item:
            if column == "#3":  # Preview column (3rd column: Country=1, Updated=2, Preview=3)
                print("Preview button clicked!")  # Debug
                # Visual feedback - briefly highlight the button
                app.collections_tree.selection_set(item)
                app.root.after(100, lambda: app.collections_tree.selection_remove(item))
                show_collection_preview(app, item)
            elif column == "#4":  # Details column (4th column: Country=1, Updated=2, Preview=3, Details=4)
                print("Details button clicked!")  # Debug
                # Visual feedback - briefly highlight the button
                app.collections_tree.selection_set(item)
                app.root.after(100, lambda: app.collections_tree.selection_remove(item))
                show_collection_details_dialog(app, item)
            elif column == "#0":  # Selection column
                app.toggle_collection_selection(event)
        elif region == "tree" and item and column == "#0":
            # Handle clicks on tree area for selection
            app.toggle_collection_selection(event)
    
    # Track the currently hovered item and column to properly reset
    app.hovered_item = None
    app.hovered_column = None
    
    # Add hover effect for better UX
    def on_motion(event):
        region = app.collections_tree.identify_region(event.x, event.y)
        column = app.collections_tree.identify_column(event.x)
        item = app.collections_tree.identify('item', event.x, event.y)
        
        # Reset previous hover if we moved to a different item/column
        if app.hovered_item and (app.hovered_item != item or app.hovered_column != column):
            current_values = list(app.collections_tree.item(app.hovered_item, 'values'))
            if len(current_values) >= 4:
                current_values[2] = "🔍 Thumbnail"  # Reset preview button
                current_values[3] = "📋 Metadata"  # Reset details button
                app.collections_tree.item(app.hovered_item, values=current_values)
            app.hovered_item = None
            app.hovered_column = None
        
        if region == "cell" and item and (column == "#3" or column == "#4"):  # Preview or Details column
            app.collections_tree.configure(cursor="hand2")
            # Visual hover effect - make text bold/colored
            current_values = list(app.collections_tree.item(item, 'values'))
            if column == "#3":  # Preview column
                current_values[2] = "🔍 PREVIEW"  # Make uppercase and add emoji
            elif column == "#4":  # Details column  
                current_values[3] = "📋 DETAILS"  # Make uppercase and add emoji
            app.collections_tree.item(item, values=current_values)
            app.hovered_item = item
            app.hovered_column = column
        else:
            app.collections_tree.configure(cursor="")
    
    def show_collection_preview(app, tree_item):
        """Show preview for selected collection"""
        try:
            # Get collection ID from tags instead of using index
            tags = app.collections_tree.item(tree_item, 'tags')
            if tags and len(tags) > 0:
                collection_id = tags[0]  # First tag is the collection ID
                
                # Get collection title from the tree values
                values = app.collections_tree.item(tree_item, 'values')
                collection_title = values[0] if values else collection_id  # First value is the title
                
                print(f"Opening preview for collection: {collection_id} ({collection_title})")
                
                # Show preview window
                show_thumbnail_preview(app.root, collection_id, collection_title)
            else:
                print("No collection ID found in item tags")
        except Exception as e:
            print(f"Error showing preview: {e}")
    
    def show_collection_details_dialog(app, tree_item):
        """Show details for selected collection"""
        try:
            # Get collection ID from tags
            tags = app.collections_tree.item(tree_item, 'tags')
            if tags and len(tags) > 0:
                collection_id = tags[0]  # First tag is the collection ID
                
                # Find the collection object from the collections list
                collection = None
                for coll in app.collections:
                    if coll.get('id') == collection_id:
                        collection = coll
                        break
                
                if collection:
                    print(f"Opening details for collection: {collection_id}")
                    show_collection_details(app.root, collection)
                else:
                    print(f"Collection not found: {collection_id}")
            else:
                print("No collection ID found in item tags")
        except Exception as e:
            print(f"Error showing collection details: {e}")
    
    app.collections_tree.bind('<Button-1>', handle_tree_click)
    app.collections_tree.bind('<Motion>', on_motion)
    
    # Bottom section - Filters (horizontal layout)
    filters_section = ttk.LabelFrame(main_container, text="Data Filters",
                                   style='Filter.TLabelframe')
    filters_section.pack(fill=tk.X, pady=(5, 15))
    
    # Years filter (left)
    years_frame = ttk.LabelFrame(filters_section, text="Years",
                                style='Filter.TLabelframe')
    years_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

    years_frame.pack(fill=tk.BOTH, expand=True, pady=3)
    
    # Configure grid columns to distribute evenly
    for col in range(8):
        years_frame.columnconfigure(col, weight=1, uniform="year_col")
    
    app.year_vars = {}
    for i, year in enumerate(AVAILABLE_YEARS):
        var = tk.BooleanVar()
        app.year_vars[year] = var
        cb = ttk.Checkbutton(years_frame, text=str(year), variable=var, style='Clean.TCheckbutton')
        cb.grid(row=i//8, column=i%8, sticky=tk.W+tk.E, padx=3, pady=4)
    
    # Resolution filter (center)
    resolution_frame = ttk.LabelFrame(filters_section, text="Resolution",
                                    style='Filter.TLabelframe')
    resolution_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
    
    app.resolution_vars = {}
    for res in AVAILABLE_RESOLUTIONS:
        var = tk.BooleanVar(value=True)
        app.resolution_vars[res] = var
        cb = ttk.Checkbutton(resolution_frame, text=res, variable=var, style='Clean.TCheckbutton')
        cb.pack(anchor=tk.W, pady=3, padx=3)
    
    # Project filter (right)
    project_frame = ttk.LabelFrame(filters_section, text="Project Type",
                                 style='Filter.TLabelframe')
    project_frame.pack(side=tk.RIGHT, fill=tk.Y)
    
    app.project_vars = {}
    for proj in AVAILABLE_PROJECTS:
        var = tk.BooleanVar(value=True)
        app.project_vars[proj] = var
        display_name = proj.replace("Global2_", "").replace("_", " & ")
        cb = ttk.Checkbutton(project_frame, text=display_name, variable=var, style='Clean.TCheckbutton')
        cb.pack(anchor=tk.W, pady=3, padx=3)
    
    # Search controls - bottom section
    search_section = ttk.Frame(main_container, style='Clean.TFrame')
    search_section.pack(fill=tk.X)
    
    # Main search button
    search_controls = ttk.Frame(search_section, style='Clean.TFrame')
    search_controls.pack(fill=tk.X)
    
    app.search_button = ttk.Button(search_controls, text="🔍 Search Data", 
                                  style='CleanPrimary.TButton',
                                  command=app.search_items)
    app.search_button.pack(side=tk.LEFT, padx=(0, 15))
    
    # Progress bar and status
    progress_container = ttk.Frame(search_controls, style='Clean.TFrame')
    progress_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    app.search_progress = ttk.Progressbar(progress_container, mode='indeterminate')
    # Center the progress bar considering the status label below
    app.search_progress.pack(fill=tk.X, pady=(5, 3))
    
    app.search_status = ttk.Label(progress_container, text="Ready to search", style="Clean.TLabel",
                                 font=('Segoe UI', 9))
    app.search_status.pack(anchor='w')