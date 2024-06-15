import tkinter as tk
from datetime import date
import pandas as pd
import os
import datetime
from tkinter import messagebox
from PIL import Image, ImageTk

try: 
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class InquiryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quick Inquiry Recorder")
        

        # Load the logo image
        self.logo_path = os.path.join(os.path.dirname(__file__), 'NE Inquiry.png')
        # self.logo_path= r'C:\Users\john.jayme\Documents\Personal projects\NE Inquiry\NE Inquiry.png'

        logo_image = Image.open(self.logo_path)
        logo_icon = ImageTk.PhotoImage(logo_image)

        # Set the window icon
        self.root.iconphoto(False, logo_icon)

        # Initialize UI components
        self.initialize_ui()

    # def initialize_ui(self):
    #     # UI components like labels, entry fields, buttons
    #     self.entry = tk.Text(self.root, width=50, height=5)
    #     self.entry.grid(row=0, column=0)
        
    #     # Buttons
    #     tk.Button(self.root, text="Save Inquiry", command=self.save_inquiry).grid(row=1, column=0)
    #     tk.Button(self.root, text="Clear Field", command=self.clear).grid(row=2, column=0, pady=(2,5))

    #     # Label for displaying success message
    #     self.success_label = tk.Label(self.root, text="")
    #     self.success_label.grid(row=3, column=0)

    #      # Configure the row and column of the entry widget to expand with the window
    #     self.root.rowconfigure(0, weight=1)  # Make row 0 expandable
    #     self.root.columnconfigure(0, weight=1)  # Make column 0 expandable

    #     self.root.bind("<Return>", self.save_inquiry_wrapper)
    #     self.root.bind("<Escape>", self.clear)
    def initialize_ui(self):
        # UI components like labels, entry fields, buttons
        self.entry = tk.Text(self.root, width=50, height=5,wrap=tk.WORD)
        self.entry.grid(row=0, column=0, columnspan=3, sticky="nsew")  # Span across three columns

        # Configure rows and columns for expanding and centering
        self.root.rowconfigure(0, weight=1)  # Make row 0 expandable
        self.root.columnconfigure(0, weight=1)  # Left padding
        self.root.columnconfigure(1, weight=0)  # Center column
        self.root.columnconfigure(2, weight=1)  # Right padding

        # Buttons centered in the middle column
        tk.Button(self.root, text="Save Inquiry", command=self.save_inquiry).grid(row=1, column=1, pady=10)
        tk.Button(self.root, text="Clear Field", command=self.clear).grid(row=2, column=1, pady=(0, 10))

        # Label for displaying success message
        self.success_label = tk.Label(self.root, text="")
        self.success_label.grid(row=3, column=0, columnspan=3, sticky="ew")  # Span across three columns

        # Bindings
        # self.root.bind("<Return>", self.save_inquiry_wrapper)
        self.root.bind("<Escape>", self.clear)
        self.root.bind("<Return>", self.on_return_pressed)



   #methods
    def on_return_pressed(self, event):
        # Check if Ctrl key is pressed
        if not (event.state & 0x0004):  # 0x0004 is the mask for the Ctrl key
            self.save_inquiry_wrapper()
        
        
    def save_inquiry_wrapper(self, event=None):
        # Wrapper function for save_inquiry to handle event
        self.save_inquiry() 

    def clear_wrapper(self):
        # Wrapper function for clear to handle event
        self.clear()

    def clear(self, event=None):
        # Clear the entry widget or perform other clearing actions
        self.entry.delete("1.0", "end")  
        self.success_label.config(text="")    


    def save_inquiry(self):
        # Check if the entry widget is blank
        if not self.entry.get("1.0", "end").strip():
            # Show a message box
            messagebox.showwarning("Warning", "Do not enter blank")
            return  

    
        
        current_datetimetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        inquiry_details = self.entry.get("1.0", "end-1c")  # Retrieve all text in the Text widget

        home_directory = os.path.expanduser("~")
        new_path = os.path.join(home_directory, "Desktop")
        file_path = os.path.join(new_path, 'inquiries.xlsx')
        if os.path.exists(file_path):
            df_existing = pd.read_excel(file_path)
            df_new = pd.DataFrame([[current_datetimetime, inquiry_details]], columns=['Date', 'Inquiry'])
            df = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df = pd.DataFrame([[current_datetimetime, inquiry_details]], columns=['Date', 'Inquiry'])

        df.to_excel(file_path, index=False)

        # Display success message
        self.success_label.config(text="Inquiry saved successfully!")

    def run(self):
        self.root.mainloop()

# Running the application
if __name__ == "__main__":
    app = InquiryApp()
    app.run()
