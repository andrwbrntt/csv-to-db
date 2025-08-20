# used for the root window
import tkinter as tk
# used to allow user to choose files and save locations
from tkinter import filedialog as fd
# used to prompt user input
from tkinter import messagebox as mb
#used for table name input
from tkinter import simpledialog as sd
# used to create the dataframe and perform minimal cleaning
import pandas as pd
# used to connect and convert files to databases
import sqlite3 as sql

# creates and hides the root window
root = tk.Tk()
root.withdraw()

# handle user file selection
while True:
    # file dialog to select csv
    file_path = fd.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        # create dataframe from the csv
        df = pd.read_csv(file_path)
        # preview types and structure
        print(df.dtypes)
        print(df.head())
        # confirm data preview
        preview = mb.askyesno("Data preview", "Does the data preview appear as intended?")
        if preview:
            break
        else:
            # prompt to choose another file
            choose_another = mb.askyesno("Choose another file", "Would you like to choose another file?")
            if choose_another:
                continue
            else:
                exit()
    else:
        exit()    

# strip whitespace and standardize case for headers
df.columns = df.columns.str.strip().str.lower()

# handle user input for database and table name
while True:
    # select save location, set default and restrict to database files
    db_path = fd.asksaveasfilename(defaultextension=".db", filetypes=[("Database files", "*.db")])
    if db_path:
        while True:
            # prompt user to enter the table name
            table_name = sd.askstring("Table name", "Enter the table name:")
            if table_name:
                # create connection to sqlite
                connection = sql.connect(db_path)
                # convert dataframe to database
                df.to_sql(table_name, connection, if_exists="replace", index=False)
                connection.close()
                mb.showinfo("Success", "Database successfully created")
                exit()
            else:
                # handle table name cancellation
                retry = mb.askyesno("Table name", "No table name provided. Retry?")
                if retry:
                    continue
                else:
                    exit()
    else:
        # handle save file cancellation
        save_file = mb.askyesno("Save file", "No save location selected. Select location to save?")
        if save_file:
            continue
        else:
            exit()