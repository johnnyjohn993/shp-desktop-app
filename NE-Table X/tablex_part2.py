from tablex_part1 import ApplicationGUI
import tkinter as tk

try: 
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


root = tk.Tk()
app = ApplicationGUI(root)
root.mainloop()