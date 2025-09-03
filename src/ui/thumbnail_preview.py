"""
Thumbnail Preview Window
"""
import tkinter as tk
import requests
import io
import threading
import sys
import os

from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.config.config import API_BASE_URL, API_KEY


def show_thumbnail_preview(parent, collection_id, collection_title):
    """Show thumbnail preview in a new window"""
    
    # Create preview window
    preview_window = tk.Toplevel(parent)
    preview_window.title(f"Preview - {collection_title}")
    preview_window.resizable(True, True)
    
    # Set desired window size
    window_width = 800
    window_height = 650
    
    # Get screen dimensions
    screen_width = preview_window.winfo_screenwidth()
    screen_height = preview_window.winfo_screenheight()
    
    # Calculate center position
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    
    # Set size and position in one go
    preview_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    
    # Make it modal
    preview_window.transient(parent)
    preview_window.grab_set()
    
    # Header with collection info
    header_frame = tk.Frame(preview_window, bg='white', pady=10)
    header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
    
    title_label = tk.Label(header_frame, 
                          text=collection_title,
                          font=('Segoe UI', 14, 'bold'),
                          bg='white',
                          fg='#212529')
    title_label.pack()
    
    id_label = tk.Label(header_frame,
                       text=f"Collection ID: {collection_id}",
                       font=('Segoe UI', 10),
                       bg='white',
                       fg='#6c757d')
    id_label.pack(pady=(2, 0))
    
    # Separator
    separator = tk.Frame(preview_window, height=1, bg='#dee2e6')
    separator.pack(fill=tk.X, padx=10, pady=5)
    
    # Main content area
    content_frame = tk.Frame(preview_window, bg='white')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Loading indicator
    loading_frame = tk.Frame(content_frame, bg='white')
    loading_frame.pack(expand=True)
    
    loading_label = tk.Label(loading_frame,
                            text="🔄 Loading thumbnail...",
                            font=('Segoe UI', 12),
                            bg='white',
                            fg='#6c757d')
    loading_label.pack(pady=50)
    
    # Image container (hidden initially)
    image_frame = tk.Frame(content_frame, bg='white')
    
    # Error container (hidden initially)  
    error_frame = tk.Frame(content_frame, bg='white')
    
    def load_thumbnail():
        """Load thumbnail in background thread"""
        try:
            # Try to get thumbnail from API
            headers = {}
            if API_KEY:
                headers['Authorization'] = f'Bearer {API_KEY}'
            
            thumbnail_url = f"{API_BASE_URL}/thumbnails/collections/{collection_id}"
            print(f"Requesting thumbnail from: {thumbnail_url}")
            print(f"Headers: {headers}")
            
            response = requests.get(thumbnail_url, headers=headers, timeout=10)
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    # Load image with PIL
                    image_data = io.BytesIO(response.content)
                    pil_image = Image.open(image_data)
                    
                    # Resize image to fit window (max 500x400)
                    pil_image.thumbnail((500, 400), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Update UI in main thread
                    preview_window.after(0, lambda: show_image(photo, pil_image.size))
                except Exception as e:
                    # Fallback without PIL - show basic info
                    content_type = response.headers.get('content-type', 'unknown')
                    content_length = len(response.content)
                    preview_window.after(0, lambda: show_basic_info(content_type, content_length))
                
            else:
                error_message = f"No thumbnail available (HTTP {response.status_code})"
                try:
                    response_text = response.text[:200]  # First 200 chars
                    print(f"Error response body: {response_text}")
                    if response_text:
                        error_message += f"\nDetails: {response_text}"
                except:
                    pass
                preview_window.after(0, lambda: show_error(error_message))
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            preview_window.after(0, lambda: show_error(f"Network error: {str(e)}"))
        except Exception as e:
            print(f"General error: {e}")
            preview_window.after(0, lambda: show_error(f"Error loading image: {str(e)}"))
    
    def show_image(photo, size):
        """Show loaded image"""
        loading_frame.pack_forget()
        error_frame.pack_forget()
        
        # Image display
        image_label = tk.Label(image_frame, image=photo, bg='white')
        image_label.image = photo  # Keep reference
        image_label.pack(pady=10)
        
        # Image info
        info_label = tk.Label(image_frame,
                            text=f"Size: {size[0]} x {size[1]} pixels",
                            font=('Segoe UI', 9),
                            bg='white',
                            fg='#6c757d')
        info_label.pack()
        
        image_frame.pack(expand=True)
    
    def show_basic_info(content_type, content_length):
        """Show basic thumbnail info without PIL"""
        loading_frame.pack_forget()
        error_frame.pack_forget()
        
        # Thumbnail icon
        icon_label = tk.Label(image_frame,
                            text="🖼️",
                            font=('Segoe UI', 48),
                            bg='white',
                            fg='#495057')
        icon_label.pack(pady=20)
        
        # Basic info
        info_text = f"Thumbnail Available\n\nType: {content_type}\nSize: {content_length:,} bytes"
        
        info_label = tk.Label(image_frame,
                            text=info_text,
                            font=('Segoe UI', 11),
                            bg='white',
                            fg='#495057',
                            justify='center')
        info_label.pack()
        
        image_frame.pack(expand=True)
    
    def show_error(error_message):
        """Show error message"""
        loading_frame.pack_forget()
        image_frame.pack_forget()
        
        error_icon = tk.Label(error_frame,
                            text="❌",
                            font=('Segoe UI', 24),
                            bg='white',
                            fg='#dc3545')
        error_icon.pack(pady=(30, 10))
        
        error_label = tk.Label(error_frame,
                             text=error_message,
                             font=('Segoe UI', 11),
                             bg='white',
                             fg='#dc3545',
                             wraplength=400)
        error_label.pack()
        
        error_frame.pack(expand=True)
    
    # Footer with close button
    footer_frame = tk.Frame(preview_window, bg='#f8f9fa', pady=10)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    close_button = tk.Button(footer_frame,
                           text="Close",
                           command=preview_window.destroy,
                           font=('Segoe UI', 10),
                           bg='#6c757d',
                           fg='white',
                           border=0,
                           padx=20,
                           pady=8,
                           cursor='hand2')
    close_button.pack(side=tk.RIGHT, padx=10)
    
    # Start loading thumbnail in background
    threading.Thread(target=load_thumbnail, daemon=True).start()
    
    # Handle window close
    def on_close():
        preview_window.grab_release()
        preview_window.destroy()
    
    preview_window.protocol("WM_DELETE_WINDOW", on_close)