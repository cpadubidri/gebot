import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

def getFolder():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')  # You can change the theme to 'clam', 'alt', 'default', or 'classic'
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory()
    root.destroy()  # Destroy the root window after selection
    return folder_path

if __name__ == "__main__":
    folder_path = select_folder()
    print(f"Selected folder: {folder_path}")
    # You can now use the folder_path variable for further processing
