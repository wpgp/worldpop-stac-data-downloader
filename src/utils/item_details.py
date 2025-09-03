"""
Item Details Dialog - Shows detailed information about STAC items
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json


class ItemDetailsDialog:
    def __init__(self, parent, item, info=None):
        self.item = item
        self.info = info or {}
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Item Details - {item.get('id', 'Unknown')}")
        self.dialog.geometry("800x600")
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
        
        # Tab 2: Assets Information
        self.setup_assets_tab(notebook)
        
        # Tab 3: Properties (Raw)
        self.setup_properties_tab(notebook)
        
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
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Basic Information", padding=10)
        basic_frame.pack(fill=tk.X, pady=5)
        
        properties = self.item.get('properties', {})
        
        # Create info fields
        info_fields = [
            ("Item ID", self.item.get('id', 'Unknown')),
            ("Collection", self.item.get('collection', 'Unknown')),
            ("Year", properties.get('year', 'Unknown')),
            ("Resolution", properties.get('resolution', 'Unknown')),
            ("Data Type", properties.get('type', 'Unknown').title()),
            ("Project", properties.get('project', 'Unknown').replace('Global2_', '')),
            ("File Size", self.info.get('size', 'Unknown')),
            ("Download Type", self.info.get('download_type', 'Unknown')),
            ("Last Updated", self.format_date(self.info.get('last_updated', 'Unknown')))
        ]
        
        for i, (label, value) in enumerate(info_fields):
            ttk.Label(basic_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Label(basic_frame, text=str(value)).grid(
                row=i, column=1, sticky=tk.W, padx=15, pady=2)
        
        # Geometric information
        if 'geometry' in self.item and self.item['geometry']:
            geo_frame = ttk.LabelFrame(scrollable_frame, text="Geographic Information", padding=10)
            geo_frame.pack(fill=tk.X, pady=5)
            
            geometry = self.item['geometry']
            bbox = self.item.get('bbox', [])
            
            geo_fields = [
                ("Geometry Type", geometry.get('type', 'Unknown')),
                ("Coordinates Count", len(geometry.get('coordinates', [[]])[0]) if geometry.get('coordinates') else 0),
            ]
            
            if bbox:
                geo_fields.extend([
                    ("Bounding Box", f"[{', '.join(f'{x:.4f}' for x in bbox)}]"),
                    ("West", f"{bbox[0]:.4f}°"),
                    ("South", f"{bbox[1]:.4f}°"),
                    ("East", f"{bbox[2]:.4f}°"),
                    ("North", f"{bbox[3]:.4f}°"),
                ])
            
            for i, (label, value) in enumerate(geo_fields):
                ttk.Label(geo_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                    row=i, column=0, sticky=tk.W, padx=5, pady=2)
                ttk.Label(geo_frame, text=str(value)).grid(
                    row=i, column=1, sticky=tk.W, padx=15, pady=2)
        
        # Age-sex specific information
        if 'agesex' in self.item.get('id', '').lower():
            agesex_frame = ttk.LabelFrame(scrollable_frame, text="Age-Sex Information", padding=10)
            agesex_frame.pack(fill=tk.X, pady=5)
            
            age_groups = properties.get('agesex:age_groups', [])
            sexes = properties.get('agesex:sexes', [])
            
            agesex_fields = [
                ("Age Groups", f"{len(age_groups)} groups"),
                ("Available Sexes", ', '.join(sexes) if sexes else 'Unknown'),
                ("Total Files", len(self.item.get('assets', {})) - 2),  # Exclude thumbnail and archive
            ]
            
            if age_groups:
                agesex_fields.append(("Age Range", f"{age_groups[0]} to {age_groups[-1]}"))
            
            for i, (label, value) in enumerate(agesex_fields):
                ttk.Label(agesex_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                    row=i, column=0, sticky=tk.W, padx=5, pady=2)
                ttk.Label(agesex_frame, text=str(value)).grid(
                    row=i, column=1, sticky=tk.W, padx=15, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_assets_tab(self, notebook):
        """Setup assets information tab"""
        assets_frame = ttk.Frame(notebook)
        notebook.add(assets_frame, text="📁 Assets")
        
        # Assets tree
        columns = ("Asset Key", "Type", "Size", "Role", "Title")
        assets_tree = ttk.Treeview(assets_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            assets_tree.heading(col, text=col)
            if col == "Asset Key":
                assets_tree.column(col, width=150)
            elif col == "Type":
                assets_tree.column(col, width=100)
            elif col == "Size":
                assets_tree.column(col, width=80)
            elif col == "Role":
                assets_tree.column(col, width=100)
            else:
                assets_tree.column(col, width=200)
        
        # Add scrollbar
        assets_scrollbar = ttk.Scrollbar(assets_frame, orient=tk.VERTICAL, command=assets_tree.yview)
        assets_tree.configure(yscrollcommand=assets_scrollbar.set)
        
        # Populate assets
        assets = self.item.get('assets', {})
        for asset_key, asset in assets.items():
            media_type = asset.get('type', asset.get('media_type', 'Unknown'))
            size = asset.get('extra_fields', {}).get('file:size', 'Unknown')
            roles = ', '.join(asset.get('roles', []))
            title = asset.get('title', asset_key)
            
            assets_tree.insert('', tk.END, values=(asset_key, media_type, size, roles, title))
        
        assets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        assets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_properties_tab(self, notebook):
        """Setup raw properties tab"""
        props_frame = ttk.Frame(notebook)
        notebook.add(props_frame, text="🔍 Raw Properties")
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(props_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10))
        text_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        # Format and display raw JSON
        try:
            formatted_json = json.dumps(self.item, indent=2, ensure_ascii=False)
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
        ttk.Button(button_frame, text="Copy Item ID", command=self.copy_item_id).pack(side=tk.RIGHT, padx=5)
    
    def copy_item_id(self):
        """Copy item ID to clipboard"""
        try:
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(self.item.get('id', ''))
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


def show_item_details(parent, item, info=None):
    """Show item details dialog"""
    dialog = ItemDetailsDialog(parent, item, info)
    return dialog