
import pandas as pd
import tkinter.scrolledtext as st
import tkinter as tk
from filehandler import FileHandler
import os
from PIL import Image, ImageTk
import re

class ApplicationGUI:
    def __init__(self, root):
        self.file_handler = FileHandler()
        self.root = root
        self.setup_ui()
        


        # Load the logo image
        self.logo_path = os.path.join(os.path.dirname(__file__), 'NE TABLE-X.png')
        # self.logo_path= r'C:\Users\john.jayme\Documents\Personal projects\NE Inquiry\NE Inquiry.png'

        logo_image = Image.open(self.logo_path)
        logo_icon = ImageTk.PhotoImage(logo_image)

        # Set the window icon
        self.root.iconphoto(False, logo_icon)

    def setup_ui(self):
        self.root.title("SQL Sript Table Extractor")

        # Configure the grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=0) # Adjusted weight for label
        self.root.grid_rowconfigure(1, weight=1) # Main text area
        self.root.grid_rowconfigure(2, weight=0) # Buttons
        self.root.grid_rowconfigure(3, weight=0) # Status label

        
        # window 1
        input_label = tk.Label(self.root, text="Enter your Script:", font=("Arial", 10))
        input_label.grid(row=0, column=0, sticky='nw')

        self.input_script_sql = st.ScrolledText(self.root, wrap='word', height=10, width=30,undo=True)
        self.input_script_sql.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        self.input_script_sql.focus_set()

        save_button = tk.Button(self.root, text="Load Script", command=self.all_buttons, cursor="hand2")
        save_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        clear_button = tk.Button(self.root, text="Clear All", command=self.clear_all, cursor="hand2")
        clear_button.grid(row=2, column=0, padx=(200,10), pady=10 , sticky='w')

        input_label_2 = tk.Label(self.root, text="Extracted Active Tables:",font=("Arial", 10))
        input_label_2.grid(row=0, column=1, sticky='nw')

        # window 2
        self.output_var = tk.StringVar()
        output_label = tk.Label(self.root, textvariable=self.output_var)
        output_label.grid(row=3, column=0, sticky='nw', padx=10, pady=10)

        # extract_button = tk.Button(self.root, text="Extract Active Tables", command=self.extract_active_tables, cursor="hand2")
        # extract_button.grid(row=2, column=1, pady=10, sticky='w')

        # ScrolledText widget for displaying active tables
        self.active_table = st.ScrolledText(self.root, wrap='word', height=10, width=20)
        self.active_table.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        
        #Window 3
        input_label_3 = tk.Label(self.root, text="Inactive Tables:", font=("Arial", 10))
        input_label_3.grid(row=5, column=0, sticky='w')


        # Button for extracting inactive tables
        # extract_inactive_button = tk.Button(self.root, text="Extract Inactive Tables", command=self.extract_inactive_and_display, cursor="hand2")
        # extract_inactive_button.grid(row=7, column=0, pady=10, padx=10, sticky='w')

        # ScrolledText widget for displaying Inactive table
        self.inactive_table = st.ScrolledText(self.root, wrap='word', height=10, width=20)
        self.inactive_table.grid(row=6, column=0, sticky='nsew', padx=10, pady=10)

        self.root.bind_all("<Return>", self.all_buttons_bind)
        self.root.bind_all("<Escape>", self.clear_all_bind)

    def set_focus(self):
        self.focus_set()

    def all_buttons(self):
        self.save_to_file()
        #self.clear_all()
        self.extract_active_tables()
        self.extract_inactive_and_display()

    def all_buttons_bind(self, event):
        self.all_buttons()


    def copy_text(self):
        selected_text = self.input_script_sql.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
    

    def save_to_file_bind(self, event):
        self.save_to_file()

    def clear_all_bind(self, event):
        self.clear_all()


    def clear_all(self):
      
        self.input_script_sql.delete("1.0", tk.END)  # Clearing the script
        # Clearing active_table
        self.active_table.config(state='normal')  # Enable editing
        self.active_table.delete("1.0", tk.END)
        self.active_table.config(state='disabled')  # Make it read-only again

        # Clearing inactive_table
        self.inactive_table.config(state='normal')  
        self.inactive_table.delete("1.0", tk.END)
        self.inactive_table.config(state='disabled')  

        #clear text
        self.output_var.set("")
        

    def save_to_file(self):
        text = self.input_script_sql.get("1.0", tk.END)
        self.file_handler.save_to_file(text.strip())
        self.output_var.set("Script has been Loaded")

    

    def extract_active_tables(self):
        code = self.file_handler.read_from_file()
        extracted_words = self.file_handler.extract_words(code)

        # Convert the list to a set to remove duplicates and then back to a list
        unique_words = list(set(extracted_words))

        # Insert the header
        header = "Active Tables:"
        self.active_table.config(state='normal')  # Enable editing
        self.active_table.delete('1.0', tk.END)  # Clear existing text
        self.active_table.insert('end', header + '\n')  # Display the header on a new line

        # Display the list
        self.display_active_list(unique_words)


    def display_active_list(self, lst):
        for item in lst:
            self.active_table.insert('end', item + '\n')  # Display each item on a new line

        self.active_table.config(state='disabled')



    #Method for Inactive tables

    def extract_inactive_and_display(self):
        code = self.file_handler.read_from_file()
        inactive_words = self.file_handler.extract_inactive_words(code)
        unique_words = list(set(inactive_words))

        # Insert the header
        header = "Inactive Tables:"
        self.inactive_table.config(state='normal')  # view only
        self.inactive_table.delete('1.0', tk.END)
        self.inactive_table.insert('end', header + '\n')

        # Display the list
        self.display_inactive_list(unique_words)
        


    def display_inactive_list(self, lst):
        for item in lst:
            self.inactive_table.insert('end', item + '\n')

        self.inactive_table.config(state='disabled')
































    # def extract_inactive_and_display(self):
    #         code = self.file_handler.read_from_file()
    #         inactive_words = self.file_handler.extract_inactive_words(code)

    #         # Create DataFrame
    #         df = pd.DataFrame(inactive_words, columns=["Active Tables:"])

    #         # Strip whitespace from each entry
    #         df['Active Tables:'] = df['Active Tables:'].str.strip()

    #         # Drop duplicates
    #         df = df.drop_duplicates()

    #         # Display the DataFrame
    #         self.display_dataframe(df)

    # def display_dataframe(self, df):
    #         self.inactive_table.config(state='normal')  # Enable editing
    #         self.inactive_table.delete('1.0', tk.END)  # Clear existing text
    #         self.inactive_table.insert('end', df.to_string(index=False))  # Display the DataFrame
    #         self.inactive_table.config(state='disabled')