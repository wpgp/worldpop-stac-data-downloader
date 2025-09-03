"""
WorldPop Desktop Application - Main Entry Point
"""
import tkinter as tk

from src.core.app import WorldPopApp


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    WorldPopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
