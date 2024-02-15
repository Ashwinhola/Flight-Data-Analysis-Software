from math import exp
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
import re
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import RectangleSelector
matplotlib.use("TkAgg")

# chhosing the excel sheets
class MetaData:
    def __init__(self,parent=None,root=None):
        self.parent=parent
        self.root=root
        self.current_browsing_file_index = None  # To keep track of which Excel file is currently being browsed
        self.selected_excel_file_path_1 = ""
        self.selected_excel_file_path_2 = ""
        self.selected_sheet_1 = ""
        self.selected_sheet_2 = ""
        self.selected_log_file_path = ""
        self.Init_UI()
        
    def Init_UI(self):
        self.info_label = tk.Label(self.root, text="", bg="#E3E3E3")
        self.info_label.place(x=80,y=100)
        self.info_label.config(font=('Helvetica bold',15))

        # Create buttons to browse Excel files
        self.browse_excel_button_1 = tk.Button(self.root, text="Select Analog parameters file", bg="#E3E3E3", command=lambda: self.browse_and_select_excel(0))
        self.browse_excel_button_1.config(font=('Helvetica bold',15))
        self.browse_excel_button_1.place(x=100,y=270)

        self.sheet_label_1 = tk.Label(self.root, text="Select Sheet for analog parameters",bg="#E3E3E3")
        self.sheet_label_1.config(font=('Helvetica bold',15))
        self.sheet_label_1.place(x=100,y=350)

        self.sheet_dropdown_1 = ttk.Combobox(self.root, textvariable="")
        self.sheet_dropdown_1.config(font=('Helvetica bold',15))
        self.sheet_dropdown_1.place(x=100,y=450)
        self.sheet_dropdown_1.config(state="disabled")
        self.sheet_dropdown_1.bind("<<ComboboxSelected>>", lambda event: self.on_sheet_selected(event))

        self.browse_excel_button_2 = tk.Button(self.root, text="Select Discrete Parameters",bg="#E3E3E3", command=lambda: self.browse_and_select_excel(1))
        self.browse_excel_button_2.config(font=('Helvetica bold',15))
        self.browse_excel_button_2.place(x=550,y=270)
        self.browse_excel_button_2.config(state="disabled")

        self.sheet_label_2 = tk.Label(self.root, text="Select Sheet for discrete parameters",bg="#E3E3E3")
        self.sheet_label_2.config(font=('Helvetica bold',15))
        self.sheet_label_2.place(x=550,y=350)

        self.sheet_dropdown_2 = ttk.Combobox(self.root, textvariable="")
        self.sheet_dropdown_2.config(font=('Helvetica bold',15))
        self.sheet_dropdown_2.place(x=550,y=450)
        self.sheet_dropdown_2.config(state="disabled")
        self.sheet_dropdown_2.bind("<<ComboboxSelected>>", lambda event: self.on_sheet_selected(event))

        # Create a button to browse and select log file
        self.browse_log_button = tk.Button(self.root, text="Select Log File",bg="#E3E3E3", command=self.browse_and_select_log)
        self.browse_log_button.config(font=('Helvetica bold',15))
        self.browse_log_button.place(x=325,y=550)
        self.browse_log_button.config(state="disabled")

        # Create a button to confirm and close the window
        self.confirm_button = tk.Button(self.root, text="Close",bg="#E3E3E3", command=self.close_window)
        self.confirm_button.config(font=('Helvetica bold',15))
        self.confirm_button.place(x=325,y=650)

    def browse_and_select_excel(self,file_index):
        self.current_browsing_file_index = file_index
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            if file_index == 0:
                self.selected_excel_file_path_1 = file_path
                self.sheet_dropdown_1.config(state="normal")
            else:
                self.selected_excel_file_path_2 = file_path
                self.sheet_dropdown_2.config(state="normal")

            self.update_sheet_dropdown()

    def update_sheet_dropdown(self,parent=None,root=None):
        excel_file_path = self.selected_excel_file_path_1 if self.current_browsing_file_index == 0 else self.selected_excel_file_path_2

        if excel_file_path:
            excel_sheets = pd.ExcelFile(excel_file_path).sheet_names

            if self.current_browsing_file_index == 0:
                self.sheet_dropdown_1["values"] = excel_sheets
                self.sheet_dropdown_1.set("")  # Reset the sheet selection
            else:
                self.sheet_dropdown_2["values"] = excel_sheets
                self.sheet_dropdown_2.set("")  # Reset the sheet selection

    def on_sheet_selected(self,event):
        if self.current_browsing_file_index == 0:
            self.selected_sheet_1 = self.sheet_dropdown_1.get()
            self.current_browsing_file_index = 1
            self.browse_excel_button_2.config(state="normal")
            self.update_sheet_dropdown()
        else:
            self.selected_sheet_2 = self.sheet_dropdown_2.get()
            self.browse_log_button.config(state="normal")

    def browse_and_select_log(self):
        file_path = filedialog.askopenfilename(filetypes=[("Log files", "*.log")])
        if file_path:
            self.selected_log_file_path = file_path
            self.update_info_label()
            self.operate()

    def close_window(self):
        self.root.destroy()

    def update_info_label(self):
        self.info_label.config(text=f"Selected Excel File 1: {self.selected_excel_file_path_1} \n Sheet: {self.selected_sheet_1}\nSelected Excel File 2: {self.selected_excel_file_path_2} \n Sheet: {self.selected_sheet_2}\nSelected Log File: {self.selected_log_file_path}")
        #if MetaData.selected_excel_file_path_1!="" and MetaData.selected_excel_file_path_2!="" and MetaData.selected_log_file_path!="" and MetaData.selected_sheet_1!="" and MetaData.selected_sheet_2!="":
        self.parent.selected_excel_file_path_1=self.selected_excel_file_path_1
        self.parent.selected_excel_file_path_2=self.selected_excel_file_path_2
        self.parent.selected_log_file_path=self.selected_log_file_path
        self.parent.selected_sheet_1=self.selected_sheet_1
        self.parent.selected_sheet_2=self.selected_sheet_2
        
    def operate(self,):
        df = pd.read_excel(self.selected_excel_file_path_1,sheet_name=self.selected_sheet_1, skiprows=10)
        #print(df)
        data = {
            'BYTE': [],
            'PARAMETER': [],
            'RANGE': [],
            'NO_OF_BYTES': [],
            'PACKET': [],
            'BIT': []
        }

        new_df = pd.DataFrame(data)

        num_columns = df.shape[1]
        byte_values = []
        parameter_values = []
        range_values = []
        no_of_bytes_values = []
        # Loop through the columns of the original DataFrame
        no_of_cols_per_packet=7
        for i in range(num_columns):
            j = i % no_of_cols_per_packet
            
            # Get values to insert from the original DataFrame
            values_to_insert = df.iloc[:, i].tolist()
            
            # Update the appropriate list based on condition
            if j == 0:
                byte_values.extend(values_to_insert)
            elif j == 1:
                parameter_values.extend(values_to_insert)
            elif j == 2:
                range_values.extend(values_to_insert)
            elif j == 3:
                no_of_bytes_values.extend(values_to_insert)
        # Update the new_df DataFrame with the lists
        new_df['BYTE'] = byte_values
        new_df['PARAMETER'] = parameter_values
        new_df['RANGE'] = range_values
        new_df['NO_OF_BYTES'] = no_of_bytes_values
        # Print the updated new DataFrame
        packet=0
        packet_values = []

        # Iterate through the rows of the DataFrame
        for index, row in new_df.iterrows():
            byte_value = row['BYTE']
            
            # Check if byte_value is 1
            if byte_value == 1:
                packet += 1
            
            # Append the current packet value to the list
            packet_values.append(packet)

        # Update the 'Packet' column with the packet_values list
        new_df['PACKET'] = packet_values
        new_df = new_df.dropna(subset=['BYTE'])
        new_df = new_df[~new_df['BYTE'].apply(lambda x: isinstance(x, (int, float)) and 8 <= x <= 21)]


        #print(new_df.head(30))
        # Print the updated DataFrame

        #print(new_df.head(100))

        #reading for discrete parameters

        df1 = pd.read_excel(self.selected_excel_file_path_2,sheet_name=self.selected_sheet_2, skiprows=7)
        #print(df)
        data1 = {
            'BYTE': [],
            'PARAMETER': [],
            'RANGE': [],
            'NO_OF_BYTES': [],
            'PACKET': [],
            'BIT': []
        }

        new_df1 = pd.DataFrame(data1)

        num_columns1 = df1.shape[1]
        byte_values1 = []
        parameter_values1 = []
        bit_values1= []
        # Loop through the columns of the original DataFrame
        no_of_cols_per_packet1=6
        for i in range(num_columns1):
            j = i % no_of_cols_per_packet1
            
            # Get values to insert from the original DataFrame
            values_to_insert1 = df1.iloc[:, i].tolist()
            
            # Update the appropriate list based on condition
            if j == 0:
                byte_values1.extend(values_to_insert1)
            elif j == 2:
                parameter_values1.extend(values_to_insert1)
            elif j == 1:
                bit_values1.extend(values_to_insert1)
        # Update the new_df DataFrame with the lists
        new_df1['BYTE'] = byte_values1
        new_df1['PARAMETER'] = parameter_values1
        new_df1['BIT'] = bit_values1
        # Print the updated new DataFrame
        packet=-1
        packet_values = []
        new_df1 = new_df1.dropna(subset=['BYTE'])
        new_df1['BYTE'] = new_df1['BYTE'].astype(int)
        # Iterate through the rows of the DataFrame
        for index, row in new_df1.iterrows():
            byte_value = row['BYTE']
            bit_values1 = row['BIT']
            # Check if byte_value is 1
            if (byte_value == 8 and bit_values1 == 'Bit 1') or (byte_value == 14 and bit_values1 == 'Bit 1') :
                packet += 1
            
            # Append the current packet value to the list
            packet_values.append(packet)

        # Update the 'Packet' column with the packet_values list
        new_df1['PACKET'] = packet_values
        new_df1['PACKET'] = new_df1['PACKET'].replace(0, 'ALL')


        #print(new_df1)

        combined_df = pd.concat([new_df, new_df1], ignore_index=True)
        bit_mapping = {
            'Bit 1': 1,
            'Bit 2': 2,
            'Bit 3': 3,
            'Bit 4': 4,
            'Bit 5': 5,
            'Bit 6': 6,
            'Bit 7': 7,
            'Bit 8': 8
        }

        combined_df['BIT'] = combined_df['BIT'].replace(bit_mapping)
        combined_df['BIT'] = combined_df['BIT'].apply(lambda x: int(x) if pd.notna(x) else x)

        #print(combined_df.tail())
        parameter_values2=combined_df['PARAMETER']
        #combined_df['PARAMETER'] = parameter_values2
        #print(list(parameter_values2))
        #print(parameter_values)
        log_filename =self.selected_log_file_path  # Replace with your log file's name
        desired_line_length = 256
        lines_with_desired_length = []
        header1='aa'
        header2='55'
        footer='99'
        stored_eng_val={}
        with open(log_filename, "r") as log_file:
            for line in log_file:
                cleaned_line = line.replace(" ", "").strip()  # Remove spaces and leading/trailing whitespace
                if len(cleaned_line) == desired_line_length and cleaned_line[0:2] == header1 and cleaned_line[2:4] == header2 and cleaned_line[-2:] ==footer:
                    lines_with_desired_length.append(cleaned_line)
        min_frame_time=lines_with_desired_length[0][6:14]
        min_frame_time=int(min_frame_time,base=16)
        
        self.parent.combined_df=combined_df
        self.parent.parameter_values=parameter_values
        self.parent.lines_with_desired_length=lines_with_desired_length
        self.parent.min_frame_time=min_frame_time
        self.parent.new_df = new_df
        self.parent.meta_button.config(bg="#C1FFC1")

        
