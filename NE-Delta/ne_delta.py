import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
import subprocess
from PIL import Image, ImageTk


try: 
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class CSVLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NE DELTA Difference Calculator")
        self.file_path1 = None
        self.file_path2 = None
        self.create_widgets()


        # Load the logo image
        self.logo_path = os.path.join(os.path.dirname(__file__), 'NE DELTA.png')
        # self.logo_path= r'C:\Users\john.jayme\Documents\Personal projects\NE Inquiry\NE Inquiry.png'

        logo_image = Image.open(self.logo_path)
        logo_icon = ImageTk.PhotoImage(logo_image)

        # Set the window icon
        self.root.iconphoto(False, logo_icon)

    def create_widgets(self):
        # File 1 selection
        select_button1 = tk.Button(self.root, text="Select CSV File 1", command=self.select_file1)
        select_button1.pack()

        self.file1_label = tk.Label(self.root, text="No File 1 Selected")
        self.file1_label.pack()

        # File 2 selection
        select_button2 = tk.Button(self.root, text="Select CSV File 2", command=self.select_file2)
        select_button2.pack()

        self.file2_label = tk.Label(self.root, text="No File 2 Selected")
        self.file2_label.pack()

        # # Load button
        # load_button = tk.Button(self.root, text="Load Files", command=self.load_files)
        # load_button.pack()

        calculate_button = tk.Button(self.root, text="Calculate and Check Differences", command=self.combined_command,
        width=30, height=1 )
        calculate_button.pack(pady=5,padx=10)
        # Inside the create_widgets method of CSVLoaderApp class

        # Export and Open Excel Button
        # export_excel_button = tk.Button(self.root, text="Export and Open in Excel", command=self.export_and_open)
        # export_excel_button.pack()

        clear_button = tk.Button(self.root, text="Clear All", command=self.clear_all,
        width=30, height=1 )                       
        
        clear_button.pack(pady=5,padx=10)


    def select_file1(self):
        self.file_path1 = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path1:
            self.file1_label.config(text="File 1 Selected: " + self.file_path1)

    def select_file2(self):
        self.file_path2 = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path2:
            self.file2_label.config(text="File 2 Selected: " + self.file_path2)

    def clear_all(self):
        self.file_path1 = None
        self.file_path2 = None
        self.file1_label.config(text="No File 1 Selected")
        self.file2_label.config(text="No File 2 Selected")
        #clear the file csv
        self.result_df = None
        # self.root.geometry('800x600') 

    def calculate_differences(self):
        if self.file_path1 and self.file_path2:
            try:
                df_orig = pd.read_csv(self.file_path1)
                df_secondary = pd.read_csv(self.file_path2)
         ## may need to have validation check for the column name and number of columns for both files FIXME:
                       

                # Fill missing values with 0
                df_orig = df_orig.fillna(0)
                df_secondary = df_secondary.fillna(0)
                
                # Get the initial column name
                initial_column = str(df_orig.columns[0])

                # Sort dataframes
                df_orig_sorted = df_orig.sort_values(by=list(df_orig.columns))
                df_secondary_sorted = df_secondary.sort_values(by=list(df_secondary.columns))

                # Reset index
                df_orig_sorted.reset_index(drop=True, inplace=True)
                df_secondary_sorted.reset_index(drop=True, inplace=True)

                # Merge dataframes
                df_aligned = df_orig_sorted.merge(df_secondary_sorted, on=initial_column, suffixes=('_df1', '_df2'))

                # Calculate differences for each column, except the first one
                for col in df_orig_sorted.columns[1:]:  # Skip the first column
                    df_aligned[col + '_diff'] = df_aligned[col + '_df1'] - df_aligned[col + '_df2']

                # Select columns for the final output: initial_column and differences
                output_columns = [initial_column] + [col + '_diff' for col in df_orig_sorted.columns[1:]]
                self.result_df = df_aligned[output_columns]
              

                # Save the result to a CSV file
                self.result_df.to_csv("result.csv", index=False)
                print("Differences:\n", self.result_df)


            except (KeyError, TypeError) :
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                messagebox.showerror("Error", "1. Check if file1 and file2 have the exact column name. \
                                      \n2. Check if file1 and file2 have the same number of columns. \
                                     \n3. Check if the metrics have str or non int or non float values")
                root.destroy()


        else:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Error", "Both file_path1 and file_path2 must be provided")
            root.destroy()  # Destroy the main window


    def export_and_open(self):
            result_path = "result.csv"
            self.result_df.to_csv(result_path, index=False)
         # Open the Excel file
            if os.name == 'nt':  # for Windows
                os.startfile(result_path)
            # else:  # for macOS and Linux
            #     opener = "open" if sys.platform == "darwin" else "xdg-open"
            #     subprocess.call([opener, excel_path])   

    def combined_command(self):
        self.calculate_differences()
        self.export_and_open()

   

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVLoaderApp(root)
    root.mainloop()
