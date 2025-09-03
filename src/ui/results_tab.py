"""
Results Tab UI Components
"""
import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.item_details import show_item_details


def setup_enhanced_results_tab(app):
    """Setup enhanced results tab with better visualization"""
    results_frame = ttk.Frame(app.notebook)
    app.notebook.add(results_frame, text="   📋  Search Results   ")
    
    # Results header with controls
    header_frame = ttk.Frame(results_frame)
    header_frame.pack(fill=tk.X, padx=10, pady=5)
    
    app.results_summary = ttk.Label(header_frame, text="No search results", 
                                   style='Subtitle.TLabel')
    app.results_summary.pack(side=tk.LEFT)
    
    controls_frame = ttk.Frame(header_frame)
    controls_frame.pack(side=tk.RIGHT)
    
    ttk.Button(controls_frame, text="Select All", style='Clean.TButton',
              command=app.select_all_results).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(controls_frame, text="Clear All", style='Clean.TButton',
              command=app.clear_selection).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(controls_frame, text="Show Details", style='Clean.TButton',
              command=app.show_selected_item_details).pack(side=tk.LEFT, padx=(0, 5))
    ttk.Button(controls_frame, text="Go to Downloads", style='CleanPrimary.TButton',
              command=app.go_to_downloads).pack(side=tk.LEFT, padx=(0, 5))
    
    # Enhanced results tree with more columns
    tree_frame = ttk.Frame(results_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    columns = ("Collection", "Item ID", "Year", "Resolution", "Project", "File Type", "Size", "Updated", "Details")
    app.results_tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings", style='Clean.Treeview')
    
    # Configure columns
    app.results_tree.column("#0", width=40)
    app.results_tree.heading("#0", text="✓")
    
    column_widths = {"Collection": 40, "Item ID": 220, "Year": 50, "Resolution": 50,
                    "Project": 100, "File Type": 40, "Size": 50, "Updated": 70, "Details": 70}
    
    # Initialize sorting state for each column
    app.sort_columns = {}
    
    for col in columns:
        width = column_widths.get(col, 100)
        app.results_tree.column(col, width=width)
        app.results_tree.heading(col, text=col)
        # Initialize sort state (True = ascending, False = descending, None = no sort)
        app.sort_columns[col] = None
    
    # Scrollbars
    tree_v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=app.results_tree.yview)
    tree_h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=app.results_tree.xview)
    app.results_tree.configure(yscrollcommand=tree_v_scroll.set, xscrollcommand=tree_h_scroll.set)
    
    app.results_tree.grid(row=0, column=0, sticky='nsew')
    tree_v_scroll.grid(row=0, column=1, sticky='ns')
    tree_h_scroll.grid(row=1, column=0, sticky='ew')
    
    # Add placeholder for empty results
    app.results_placeholder = ttk.Frame(tree_frame, style='Clean.TFrame')
    app.results_placeholder.grid(row=0, column=0, sticky='nsew')
    
    placeholder_content = ttk.Frame(app.results_placeholder, style='Clean.TFrame')
    placeholder_content.place(relx=0.5, rely=0.5, anchor='center')
    
    # Placeholder icon and text
    ttk.Label(placeholder_content, text="🔍", font=('Segoe UI', 48), 
             style='Clean.TLabel').pack(pady=(0, 20))
    ttk.Label(placeholder_content, text="No search results", 
             font=('Segoe UI', 16, 'bold'), style='Clean.TLabel').pack(pady=(0, 10))
    ttk.Label(placeholder_content, text="Go to 'Search & Filter' tab and perform a data search", 
             font=('Segoe UI', 11), style='Clean.TLabel').pack()
    
    # Initially show placeholder
    app.results_placeholder.tkraise()
    
    tree_frame.columnconfigure(0, weight=1)
    tree_frame.rowconfigure(0, weight=1)
    
    # Bind events for item selection and details
    def handle_results_tree_click(event):
        region = app.results_tree.identify_region(event.x, event.y)
        column = app.results_tree.identify_column(event.x)
        item = app.results_tree.identify('item', event.x, event.y)
        
        # print(f"Results click: region={region}, column={column}, item={item}")  # Debug
        
        if region == "cell" and item:
            if column == "#9":  # Details column (9th column)
                # print("Item details button clicked!")  # Debug
                # Visual feedback - briefly highlight the button
                app.results_tree.selection_set(item)
                app.root.after(100, lambda: app.results_tree.selection_remove(item))
                show_item_details_for_result(app, item)
            elif column == "#0":  # Selection column (first column)
                # print("Item selection column clicked!")  # Debug
                app.toggle_item_selection(event)
        elif region == "tree" and item and column == "#0":
            # Handle clicks on tree area for selection
            # print("Tree area selection clicked!")  # Debug
            app.toggle_item_selection(event)
        elif region == "cell" and item and column in ["#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8"]:
            # Allow selection by clicking on any data column (not Details)
            # print(f"Data column {column} clicked for selection!")  # Debug
            app.toggle_item_selection(event)
    
    def show_item_details_for_result(app, tree_item):
        """Show details for selected result item"""
        try:
            item_index = app.results_tree.index(tree_item)
            if item_index < len(app.search_results):
                selected_item = app.search_results[item_index]
                
                # Get item info
                item_id = selected_item.get('id', '').lower()
                if 'agesex' in item_id:
                    info = app.get_agesex_info(selected_item)
                else:
                    info = app.get_population_info(selected_item)
                
                # Show details dialog
                show_item_details(app.root, selected_item, info)
        except Exception as e:
            print(f"Error showing item details: {e}")
    
    def sort_results_by_column(app, column):
        """Sort results by the specified column"""
        if not app.search_results:
            return
        
        # Toggle sort direction for this column
        current_sort = app.sort_columns.get(column)
        if current_sort is None or current_sort == False:
            ascending = True
        else:
            ascending = False
        
        app.sort_columns[column] = ascending
        
        # Reset other columns' sort state
        for col in app.sort_columns:
            if col != column:
                app.sort_columns[col] = None
        
        # Define sorting key functions for different data types
        def get_sort_key(item, col_name):
            if col_name == "Collection":
                return item.get('collection', '').lower()
            elif col_name == "Item ID":
                return item.get('id', '').lower()
            elif col_name == "Year":
                year = item.get('properties', {}).get('year', 0)
                return int(year) if str(year).isdigit() else 0
            elif col_name == "Resolution":
                res = item.get('properties', {}).get('resolution', '')
                # Convert resolution to numeric for proper sorting (100m -> 100, 1km -> 1000)
                if '100m' in str(res):
                    return 100
                elif '1km' in str(res):
                    return 1000
                else:
                    return 0
            elif col_name == "Project":
                proj = item.get('properties', {}).get('project', '').replace('Global2_', '')
                return proj.lower()
            elif col_name == "File Type":
                item_id = item.get('id', '').lower()
                return "ZIP" if 'agesex' in item_id else "TIF"
            elif col_name == "Size":
                # Extract numeric value from size string for sorting
                item_id = item.get('id', '').lower()
                if 'agesex' in item_id:
                    info = app.get_agesex_info(item)
                else:
                    info = app.get_population_info(item)
                size_str = str(info['size'])
                # Extract numeric part (e.g., "4.41 MB" -> 4.41)
                try:
                    import re
                    match = re.search(r'([\d.]+)', size_str)
                    if match:
                        value = float(match.group(1))
                        # Convert to bytes for consistent sorting
                        if 'GB' in size_str.upper():
                            return value * 1024 * 1024 * 1024
                        elif 'MB' in size_str.upper():
                            return value * 1024 * 1024
                        elif 'KB' in size_str.upper():
                            return value * 1024
                        else:
                            return value
                    return 0
                except:
                    return 0
            elif col_name == "Updated":
                item_id = item.get('id', '').lower()
                if 'agesex' in item_id:
                    info = app.get_agesex_info(item)
                else:
                    info = app.get_population_info(item)
                date_str = info['last_updated']
                if date_str and date_str != 'Unknown':
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        return dt
                    except:
                        return datetime.min
                return datetime.min
            else:
                return ''
        
        # Sort the search results
        app.search_results.sort(key=lambda x: get_sort_key(x, column), reverse=not ascending)
        
        # Update the display
        app.update_search_results()
        
        # Update column headers to show sort direction
        for col in columns:
            if col == "Details":  # Skip Details column
                continue
            if col == column:
                if ascending:
                    app.results_tree.heading(col, text=f"{col} ↑")
                else:
                    app.results_tree.heading(col, text=f"{col} ↓")
            else:
                app.results_tree.heading(col, text=col)
    
    # Add sorting functionality to column headers
    def setup_column_sorting():
        """Setup click handlers for column sorting"""
        sortable_columns = ["Collection", "Item ID", "Year", "Resolution", "Project", "File Type", "Size", "Updated"]
        
        for col in sortable_columns:
            app.results_tree.heading(col, text=f"{col} ⇅", 
                                   command=lambda c=col: sort_results_by_column(app, c))
    
    # Initialize column sorting
    setup_column_sorting()
    
    # Track hover for results table too
    app.results_hovered_item = None
    app.results_hovered_column = None
    
    def on_results_motion(event):
        region = app.results_tree.identify_region(event.x, event.y)
        column = app.results_tree.identify_column(event.x)
        item = app.results_tree.identify('item', event.x, event.y)
        
        # Reset previous hover if we moved to a different item/column
        if app.results_hovered_item and (app.results_hovered_item != item or app.results_hovered_column != column):
            current_values = list(app.results_tree.item(app.results_hovered_item, 'values'))
            if len(current_values) >= 9:
                current_values[8] = "📋 Details"  # Reset details button
                app.results_tree.item(app.results_hovered_item, values=current_values)
            app.results_hovered_item = None
            app.results_hovered_column = None
        
        if region == "cell" and item and column == "#9":  # Details column
            app.results_tree.configure(cursor="hand2")
            # Visual hover effect
            current_values = list(app.results_tree.item(item, 'values'))
            if len(current_values) >= 9:
                current_values[8] = "📋 DETAILS"  # Make uppercase
                app.results_tree.item(item, values=current_values)
                app.results_hovered_item = item
                app.results_hovered_column = column
        else:
            app.results_tree.configure(cursor="")
    
    app.results_tree.bind("<Button-1>", handle_results_tree_click)
    app.results_tree.bind("<Motion>", on_results_motion)
    app.results_tree.bind("<Button-3>", app.show_item_context_menu)  # Right click