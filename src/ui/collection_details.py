"""
Collection Details Dialog - Shows detailed information about STAC collections
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class CollectionDetailsDialog:
    def __init__(self, parent, collection):
        self.collection = collection
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Collection Details - {collection.get('title', collection.get('id', 'Unknown'))}")
        self.dialog.geometry("600x450")
        self.dialog.resizable(True, True)
        
        # Center the dialog
        self.center_dialog(parent)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
    def center_dialog(self, parent):
        """Center dialog relative to parent window"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the dialog UI"""
        # Create notebook for organized display
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: General Information
        self.setup_general_tab(notebook)
        
        # Tab 2: Spatial and Temporal Extents
        self.setup_extents_tab(notebook)
        
        # Tab 3: Links and Providers
        self.setup_links_tab(notebook)
        
        # Tab 4: Raw Metadata
        self.setup_metadata_tab(notebook)
        
        # Bottom buttons
        self.setup_buttons()
    
    def setup_general_tab(self, notebook):
        """Setup general information tab"""
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="📄 General")
        
        # Create scrollable frame
        canvas = tk.Canvas(general_frame)
        scrollbar = ttk.Scrollbar(general_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Basic information section
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Collection Information", padding=10)
        basic_frame.pack(fill=tk.X, pady=5)
        
        # Create info fields
        info_fields = [
            ("Collection ID", self.collection.get('id', 'Unknown')),
            ("Title", self.collection.get('title', 'Unknown')),
            ("Description", self.collection.get('description', 'Unknown')),
            ("License", self.collection.get('license', 'Unknown')),
            # ("Version", self.collection.get('stac_version', 'Unknown')),
            # ("Created", self.format_date(self.collection.get('created', 'Unknown'))),
            # ("Updated", self.format_date(self.collection.get('updated', 'Unknown'))),
            ("STAC Version", self.collection.get('stac_version', 'Unknown')),
            ("Type", self.collection.get('type', 'Unknown')),
        ]
        
        for i, (label, value) in enumerate(info_fields):
            ttk.Label(basic_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W+tk.N, padx=5, pady=2)
            
            # For long text like description, use a text widget
            if label == "Description" and len(str(value)) > 250:
                text_widget = tk.Text(basic_frame, height=3, width=50, wrap=tk.WORD, font=('Arial', 9))
                text_widget.insert(tk.END, str(value))
                text_widget.config(state=tk.DISABLED)
                text_widget.grid(row=i, column=1, sticky=tk.W, padx=15, pady=2)
            else:
                ttk.Label(basic_frame, text=str(value), wraplength=400).grid(
                    row=i, column=1, sticky=tk.W, padx=15, pady=2)
        
        # Keywords section
        keywords = self.collection.get('keywords', [])
        if keywords:
            keywords_frame = ttk.LabelFrame(scrollable_frame, text="Keywords", padding=10)
            keywords_frame.pack(fill=tk.X, pady=5)
            
            keywords_text = ', '.join(keywords)
            ttk.Label(keywords_frame, text=keywords_text, wraplength=600).pack(anchor=tk.W)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_extents_tab(self, notebook):
        """Setup extents information tab"""
        extents_frame = ttk.Frame(notebook)
        notebook.add(extents_frame, text="🌍 Extents")
        
        # Create scrollable frame
        canvas = tk.Canvas(extents_frame)
        scrollbar = ttk.Scrollbar(extents_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        extent = self.collection.get('extent', {})
        
        # Spatial extent
        spatial = extent.get('spatial', {})
        if spatial:
            spatial_frame = ttk.LabelFrame(scrollable_frame, text="Spatial Extent", padding=10)
            spatial_frame.pack(fill=tk.X, pady=5)
            
            bbox = spatial.get('bbox', [[]])[0] if spatial.get('bbox') else []
            
            if bbox and len(bbox) >= 4:
                spatial_fields = [
                    ("Bounding Box", f"[{', '.join(f'{x:.6f}' for x in bbox)}]"),
                    ("West Longitude", f"{bbox[0]:.6f}°"),
                    ("South Latitude", f"{bbox[1]:.6f}°"),
                    ("East Longitude", f"{bbox[2]:.6f}°"),
                    ("North Latitude", f"{bbox[3]:.6f}°"),
                    ("Width", f"{abs(bbox[2] - bbox[0]):.6f}°"),
                    ("Height", f"{abs(bbox[3] - bbox[1]):.6f}°"),
                ]
                
                for i, (label, value) in enumerate(spatial_fields):
                    ttk.Label(spatial_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                        row=i, column=0, sticky=tk.W, padx=5, pady=2)
                    ttk.Label(spatial_frame, text=str(value)).grid(
                        row=i, column=1, sticky=tk.W, padx=15, pady=2)
        
        # Temporal extent
        temporal = extent.get('temporal', {})
        if temporal:
            temporal_frame = ttk.LabelFrame(scrollable_frame, text="Temporal Extent", padding=10)
            temporal_frame.pack(fill=tk.X, pady=5)
            
            interval = temporal.get('interval', [[]])[0] if temporal.get('interval') else []
            
            if interval and len(interval) >= 2:
                start_date = self.format_date(interval[0]) if interval[0] else 'Open'
                end_date = self.format_date(interval[1]) if interval[1] else 'Open'
                
                temporal_fields = [
                    ("Start Date", start_date),
                    ("End Date", end_date),
                    ("Duration", f"{start_date} to {end_date}"),
                ]
                
                for i, (label, value) in enumerate(temporal_fields):
                    ttk.Label(temporal_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                        row=i, column=0, sticky=tk.W, padx=5, pady=2)
                    ttk.Label(temporal_frame, text=str(value)).grid(
                        row=i, column=1, sticky=tk.W, padx=15, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_links_tab(self, notebook):
        """Setup links and providers tab"""
        links_frame = ttk.Frame(notebook)
        notebook.add(links_frame, text="🔗 Links & Providers")
        
        # Create notebook for links and providers
        sub_notebook = ttk.Notebook(links_frame)
        sub_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Links subtab
        links_subtab = ttk.Frame(sub_notebook)
        sub_notebook.add(links_subtab, text="Links")
        
        links = self.collection.get('links', [])
        if links:
            # Links tree
            links_columns = ("Relation", "URL", "Type")
            links_tree = ttk.Treeview(links_subtab, columns=links_columns, show="headings", height=10)
            
            for col in links_columns:
                links_tree.heading(col, text=col)
                if col == "URL":
                    links_tree.column(col, width=300)
                else:
                    links_tree.column(col, width=100)
            
            # Add scrollbar
            links_scrollbar = ttk.Scrollbar(links_subtab, orient=tk.VERTICAL, command=links_tree.yview)
            links_tree.configure(yscrollcommand=links_scrollbar.set)
            
            # Populate links
            for link in links:
                rel = link.get('rel', 'Unknown')
                href = link.get('href', 'Unknown')
                link_type = link.get('type', 'Unknown')
                
                links_tree.insert('', tk.END, values=(rel, href, link_type))
            
            links_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            links_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Providers subtab
        providers_subtab = ttk.Frame(sub_notebook)
        sub_notebook.add(providers_subtab, text="Providers")
        
        providers = self.collection.get('providers', [])
        if providers:
            # Providers tree
            providers_columns = ("Name", "Description", "Roles", "URL")
            providers_tree = ttk.Treeview(providers_subtab, columns=providers_columns, show="headings", height=10)
            
            for col in providers_columns:
                providers_tree.heading(col, text=col)
                if col in ["Description", "URL"]:
                    providers_tree.column(col, width=200)
                else:
                    providers_tree.column(col, width=150)
            
            # Add scrollbar
            providers_scrollbar = ttk.Scrollbar(providers_subtab, orient=tk.VERTICAL, command=providers_tree.yview)
            providers_tree.configure(yscrollcommand=providers_scrollbar.set)
            
            # Populate providers
            for provider in providers:
                name = provider.get('name', 'Unknown')
                description = provider.get('description', 'Unknown')
                roles = ', '.join(provider.get('roles', []))
                url = provider.get('url', 'Unknown')
                
                providers_tree.insert('', tk.END, values=(name, description, roles, url))
            
            providers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            providers_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_metadata_tab(self, notebook):
        """Setup raw metadata tab"""
        metadata_frame = ttk.Frame(notebook)
        notebook.add(metadata_frame, text="🔍 Raw Metadata")
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(metadata_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 9))
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        # Format and display raw JSON
        try:
            formatted_json = json.dumps(self.collection, indent=2, ensure_ascii=False)
            text_widget.insert(tk.END, formatted_json)
        except Exception as e:
            text_widget.insert(tk.END, f"Error formatting JSON: {e}")
        
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_buttons(self):
        """Setup bottom buttons"""
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Copy Collection ID", command=self.copy_collection_id).pack(side=tk.RIGHT, padx=5)
    
    def copy_collection_id(self):
        """Copy collection ID to clipboard"""
        try:
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(self.collection.get('id', ''))
        except:
            pass
    
    def format_date(self, date_str):
        """Format date string for display"""
        if date_str == 'Unknown' or not date_str:
            return 'Unknown'
        
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except:
            return str(date_str)


def show_collection_details(parent, collection):
    """Show collection details dialog"""
    dialog = CollectionDetailsDialog(parent, collection)
    return dialog