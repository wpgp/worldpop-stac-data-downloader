"""
UI Components and Utilities for Enhanced WorldPop App
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable


class StatusIndicator(ttk.Frame):
    """Modern status indicator with color coding"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.status_colors = {
            'success': '#4caf50',
            'warning': '#ff9800', 
            'error': '#f44336',
            'info': '#2196f3',
            'neutral': '#757575'
        }
        
        self.indicator = tk.Canvas(self, width=12, height=12, highlightthickness=0)
        self.indicator.pack(side=tk.LEFT, padx=(0, 5))
        
        self.label = ttk.Label(self, text="Status")
        self.label.pack(side=tk.LEFT)
        
        self.set_status('neutral', 'Ready')
    
    def set_status(self, status_type: str, text: str):
        """Set status with color indicator"""
        color = self.status_colors.get(status_type, self.status_colors['neutral'])
        
        self.indicator.delete("all")
        self.indicator.create_oval(2, 2, 10, 10, fill=color, outline=color)
        self.label.config(text=text)


class ProgressCard(ttk.Frame):
    """Card-style progress indicator"""
    
    def __init__(self, parent, title: str, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Card styling
        self.configure(relief='solid', borderwidth=1, padding=10)
        
        # Title
        title_label = ttk.Label(self, text=title, font=('Arial', 10, 'bold'))
        title_label.pack(anchor=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(self, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(5, 2))
        
        # Status text
        self.status_text = ttk.Label(self, text="0%", font=('Arial', 8))
        self.status_text.pack(anchor=tk.W)
    
    def update_progress(self, value: float, text: str = None):
        """Update progress value and text"""
        self.progress['value'] = value
        if text:
            self.status_text.config(text=text)
        else:
            self.status_text.config(text=f"{value:.1f}%")


class InfoCard(ttk.Frame):
    """Information card with icon and stats"""
    
    def __init__(self, parent, icon: str, title: str, value: str, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(relief='solid', borderwidth=1, padding=8)
        
        # Icon and title row
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X)
        
        icon_label = ttk.Label(header_frame, text=icon, font=('Arial', 16))
        icon_label.pack(side=tk.LEFT)
        
        title_label = ttk.Label(header_frame, text=title, font=('Arial', 9))
        title_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Value
        self.value_label = ttk.Label(self, text=value, font=('Arial', 14, 'bold'))
        self.value_label.pack(anchor=tk.W, pady=(2, 0))
    
    def update_value(self, value: str):
        """Update the displayed value"""
        self.value_label.config(text=value)


class ModernButton(ttk.Frame):
    """Modern button with icon and enhanced styling"""
    
    def __init__(self, parent, text: str, command: Callable, icon: str = "", 
                 style: str = "primary", **kwargs):
        super().__init__(parent, **kwargs)
        
        # Style colors
        self.styles = {
            'primary': {'bg': '#2e7d32', 'fg': 'white', 'active_bg': '#1b5e20'},
            'secondary': {'bg': '#1976d2', 'fg': 'white', 'active_bg': '#0d47a1'},
            'success': {'bg': '#4caf50', 'fg': 'white', 'active_bg': '#2e7d32'},
            'warning': {'bg': '#ff9800', 'fg': 'white', 'active_bg': '#e65100'},
            'danger': {'bg': '#f44336', 'fg': 'white', 'active_bg': '#c62828'}
        }
        
        button_text = f"{icon} {text}".strip()
        
        self.button = tk.Button(
            self, 
            text=button_text,
            command=command,
            font=('Arial', 9, 'bold'),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8
        )
        self.button.pack()
        
        # Apply style
        if style in self.styles:
            colors = self.styles[style]
            self.button.configure(
                bg=colors['bg'],
                fg=colors['fg'],
                activebackground=colors['active_bg'],
                activeforeground=colors['fg']
            )


class SearchBox(ttk.Frame):
    """Enhanced search box with clear button"""
    
    def __init__(self, parent, placeholder: str = "Search...", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.placeholder = placeholder
        
        # Search entry
        self.entry = ttk.Entry(self, font=('Arial', 10))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Clear button
        clear_btn = ttk.Button(self, text="✕", width=3, command=self.clear)
        clear_btn.pack(side=tk.RIGHT, padx=(2, 0))
        
        # Placeholder functionality
        self.entry.insert(0, self.placeholder)
        self.entry.configure(foreground='grey')
        
        self.entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry.bind('<FocusOut>', self.on_entry_focus_out)
    
    def on_entry_focus_in(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(foreground='black')
    
    def on_entry_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.configure(foreground='grey')
    
    def clear(self):
        self.entry.delete(0, tk.END)
        self.entry.focus()
    
    def get(self):
        value = self.entry.get()
        return value if value != self.placeholder else ""


class DataCard(ttk.Frame):
    """Card for displaying data item information"""
    
    def __init__(self, parent, data_item: Dict[str, Any], **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(relief='solid', borderwidth=1, padding=10)
        
        properties = data_item.get('properties', {})
        
        # Header with title and collection
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X)
        
        title = ttk.Label(header_frame, text=data_item.get('id', 'Unknown'), 
                         font=('Arial', 10, 'bold'))
        title.pack(side=tk.LEFT)
        
        collection = ttk.Label(header_frame, text=f"📍 {data_item.get('collection', 'N/A')}", 
                              font=('Arial', 8), foreground='#666')
        collection.pack(side=tk.RIGHT)
        
        # Details
        details_frame = ttk.Frame(self)
        details_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Year and resolution
        year = ttk.Label(details_frame, text=f"📅 {properties.get('year', 'N/A')}")
        year.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        resolution = ttk.Label(details_frame, text=f"🔍 {properties.get('resolution', 'N/A')}")
        resolution.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # Data type and size
        data_type = ttk.Label(details_frame, text=f"📊 {properties.get('type', 'N/A').title()}")
        data_type.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        size = ttk.Label(details_frame, text=f"💾 {properties.get('general:size', 'N/A')}")
        size.grid(row=1, column=1, sticky=tk.W, padx=(0, 10))


class NotificationToast(tk.Toplevel):
    """Toast notification popup"""
    
    def __init__(self, parent, message: str, notification_type: str = "info", duration: int = 3000):
        super().__init__(parent)
        
        self.notification_type = notification_type
        
        # Configure window
        self.withdraw()  # Hide initially
        self.overrideredirect(True)
        self.configure(bg='white')
        
        # Colors based on type
        colors = {
            'success': {'bg': '#4caf50', 'fg': 'white'},
            'warning': {'bg': '#ff9800', 'fg': 'white'},
            'error': {'bg': '#f44336', 'fg': 'white'},
            'info': {'bg': '#2196f3', 'fg': 'white'}
        }
        
        style_colors = colors.get(notification_type, colors['info'])
        
        # Icon mapping
        icons = {
            'success': '✓',
            'warning': '⚠',
            'error': '✗',
            'info': 'ℹ'
        }
        
        # Create content frame
        content_frame = tk.Frame(self, bg=style_colors['bg'], padx=20, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon
        icon_label = tk.Label(content_frame, text=icons.get(notification_type, 'ℹ'),
                             bg=style_colors['bg'], fg=style_colors['fg'],
                             font=('Arial', 16, 'bold'))
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Message
        message_label = tk.Label(content_frame, text=message,
                                bg=style_colors['bg'], fg=style_colors['fg'],
                                font=('Arial', 10))
        message_label.pack(side=tk.LEFT)
        
        # Position toast
        self.position_toast()
        
        # Show and auto-hide
        self.deiconify()
        self.after(duration, self.destroy)
    
    def position_toast(self):
        """Position toast in top-right corner"""
        self.update_idletasks()
        
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = screen_width - width - 20
        y = 20
        
        self.geometry(f'{width}x{height}+{x}+{y}')


def show_notification(parent, message: str, notification_type: str = "info", duration: int = 3000):
    """Show a toast notification"""
    NotificationToast(parent, message, notification_type, duration)


class ToolTip:
    """Tooltip for widgets"""
    
    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("Arial", 8, "normal"), padx=4, pady=2)
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None