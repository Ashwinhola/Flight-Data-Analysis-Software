from math import exp
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
import re
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path 
import time 

class Plot:   
    def __init__(self,parent=None,root=None): 
        self.parent=parent
        self.root=root
        self.selected_parameters_values = {}  # To store the selected parameters and their corresponding values
        self.MAX_SELECTED_PARAMETERS = 5
        self.img_names={}
        self.plotted_param = {}
        self.offset_param={}
        self.offset={}
        self.offset1=[]
        self.stored_eng_val={}
        self.fig, self.ax = plt.subplots()
        self.Init_UI()
        
    def Init_UI(self): 
        self.label1 = tk.Label(self.root, text="Name of the image file:", bg="#E3E3E3")
        self.label1.place(x=20, y=15)
        self.label1.config(font=('Helvetica bold', 10))

        self.img_name=tk.StringVar()
        self.file_entry = tk.Entry(self.root,textvariable = self.img_name, font=('calibre',10,'normal'))
        self.file_entry.place(x=200, y=15)
        self.file_entry.config(font=('Helvetica bold', 10))
        # Create a label and Combobox
        self.label = tk.Label(self.root, text="Select Parameter:", bg="#E3E3E3")
        self.label.place(x=20, y=60)
        self.label.config(font=('Helvetica bold', 10))
        # Get unique values from 'PARAMETER' column
        self.parameter_values = [str(value) for value in self.parent.combined_df['PARAMETER'].unique()]

        self.combobox = ttk.Combobox(self.root)
        self.combobox.place(x=200, y=60)
        self.combobox.bind("<KeyRelease>", lambda event: self.on_combobox_keyrelease(event))
        self.combobox.config(font=('Helvetica bold', 10))
        self.combobox['values'] = self.parameter_values
        
        self.label1 = tk.Label(self.root, text="Select File Extension:", bg="#E3E3E3")
        self.label1.place(x=20, y=250)
        self.label1.config(font=('Helvetica bold', 10))

        self.combobox1 = ttk.Combobox(self.root)
        self.combobox1.place(x=200, y=250)
        self.combobox1.config(font=('Helvetica bold', 10))
        self.combobox1['values'] = [".jpg",".svg"]

        # Create buttons to add and remove parameters
        self.add_button = tk.Button(self.root, text="Add Parameter", bg="#E3E3E3", command=lambda *args:self.add_parameter(*args))
        self.add_button.place(x=30, y=125)
        self.add_button.config(font=('Helvetica bold', 10))

        self.remove_button = tk.Button(self.root, text="Remove Selected", bg="#E3E3E3", command=lambda *args:self.remove_selected(*args))
        self.remove_button.place(x=200, y=125)
        self.remove_button.config(font=('Helvetica bold', 10))

        # Create a textbox to display the selected point's values
        self.textbox = self.ax.text(0.7, 0.9, '', transform=self.ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.7))

        self.var1 = tk.IntVar()
        self.var1.set(0)

        self.check1 = tk.Radiobutton(self.root, text="", bg="#E3E3E3", variable=self.var1, value=1)
        self.check1.place(x=20, y=200)

        self.plot_button = tk.Button(self.root, text="Plot Separate", bg="#E3E3E3", command=lambda *args:self.plot_separate(*args))
        self.plot_button.place(x=55, y=200)
        self.plot_button.config(font=('Helvetica bold', 10))

        self.check2 = tk.Radiobutton(self.root, text="", bg="#E3E3E3", variable=self.var1, value=2)
        self.check2.place(x=200, y=200)

        self.plot_button1 = tk.Button(self.root, text="Plot Together", bg="#E3E3E3", command=lambda *args:self.plot_selected_parameter(*args))
        self.plot_button1.place(x=235, y=200)
        self.plot_button1.config(font=('Helvetica bold', 10))

        # Create a Treeview widget to display the selected rows as a table
        self.tree = ttk.Treeview(self.root, height=9, columns=self.parent.new_df.columns.tolist(), show='headings')
        self.tree.place(x=400, y=15)

        # Add headings to the Treeview columns
        for col in self.parent.combined_df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")  # Adjust the column width as needed

        self.add_plot = tk.Button(self.root, text="Add Plot", bg="#E3E3E3", command=lambda *args:self.add_graph(*args))
        self.add_plot.place(x=680, y=240)
        self.add_plot.config(font=('Helvetica bold', 10))

        self.plot_all = tk.Button(self.root, text="Plot All", bg="#E3E3E3", command=lambda *args:self.plot_to_img(*args))
        self.plot_all.place(x=400, y=650)
        self.plot_all.config(font=('Helvetica bold', 10))

        self.rem = tk.Button(self.root, text="Delete", bg="#E3E3E3", command=lambda *args:self.remove(*args))
        self.rem.place(x=500, y=650)
        self.rem.config(font=('Helvetica bold', 10))

        self.edit_val = tk.Button(self.root, text="Edit", bg="#E3E3E3", command=lambda *args:self.edit(*args))
        self.edit_val.place(x=600, y=650)
        self.edit_val.config(font=('Helvetica bold', 10))

        self.exp_all = tk.Button(self.root, text="Export All", bg="#E3E3E3", command=lambda *args:self.export_all(*args))
        self.exp_all.place(x=700, y=650)
        self.exp_all.config(font=('Helvetica bold', 10))

        self.imp_all = tk.Button(self.root, text="Import All", bg="#E3E3E3", command=lambda *args:self.import_all(*args))
        self.imp_all.place(x=800, y=650)
        self.imp_all.config(font=('Helvetica bold', 10))
            
        self.tree1 = ttk.Treeview(self.root, height=15, columns=["IMAGE FILE","PARAMETER1","PARAMETER2","PARAMETER3","PARAMETER4","PARAMETER5","DESCRIPTION","EXTENSION"], show='headings')
        self.tree1.place(x=380, y=290)


        # Add headings to the Treeview columns
        for col in ["IMAGE FILE","PARAMETER1","PARAMETER2","PARAMETER3","PARAMETER4","PARAMETER5","DESCRIPTION","EXTENSION"]:
            self.tree1.heading(col, text= col)
            self.tree1.column(col, width=100, anchor="center")
            
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", font=('Helvetica bold', 10), rowheight=100)


        # Create a button to close the window
        self.close_button = tk.Button(self.root, text="Close", bg="#E3E3E3", command=self.root.destroy)
        self.close_button.place(x=400, y=700)
        self.close_button.config(font=('Helvetica bold', 10))
    
    def on_combobox_keyrelease(self,event):
        text = self.combobox.get()
        filtered_values = [value for value in self.parent.parameter_values if text.lower() in value.lower()]
        self.combobox['values'] = filtered_values


    def add_parameter_from_file(self):
        for j in self.selected_parameters_values:
            para=j
            range_no=self.selected_parameters_values[j][0][2]
            packet_no=self.selected_parameters_values[j][0][4]
            no_of_byte=self.selected_parameters_values[j][0][3]
            bit_no=self.selected_parameters_values[j][0][5]
            byte_no=self.selected_parameters_values[j][0][0]
            self.stored_eng_val[para]={'eng_val':[],'time_stamp':[]}
            if isinstance(byte_no, (int, float)) and 8 <= byte_no <= 21:
                start_byte=(byte_no*2)-2
                end_byte=byte_no*2
                if isinstance(byte_no,(int,float)) and 8<= byte_no <= 13:
                    prev_dtime_s = float('-inf')
                    if len(self.offset)!=0:
                        for i in range(len(self.offset)):
                            if para not in self.offset:
                                for k in range(0,10,2):
                                    if k not in self.offset1:
                                        self.offset[para]=k
                                        self.offset1.append(k)
                                        break  
                            else:
                                break
                    else:
                        for k in range(0,10,2):
                            if k not in self.offset1:
                                self.offset[para]=self.offset1.append(k)
                                break
                    for i in range(len(self.parent.lines_with_desired_length)):
                        hexa_val=self.parent.lines_with_desired_length[i][start_byte:end_byte]
                        decimal_integer=int(hexa_val,base=16)
                        binary_val = bin(decimal_integer)[2:]  # Convert decimal to binary
                        if len(binary_val)<8:
                            binary_val=((8-len(binary_val))*'0')+binary_val
                        time_s = self.parent.lines_with_desired_length[i][6:14]
                        dtime_s = int(time_s, base=16)

                        if dtime_s > prev_dtime_s :  # Check if the new timestamp is greater
                            temp=int(binary_val[int(bit_no)-1])
                            temp+=self.offset[para]
                            self.stored_eng_val[para]['eng_val'].append(temp)
                            self.stored_eng_val[para]['time_stamp'].append((dtime_s-self.parent.min_frame_time)/100)
                            prev_dtime_s = dtime_s

                else:
                    prev_dtime_s = float('-inf')
                    if len(self.offset)!=0:
                        for i in range(len(self.offset)):
                            if para not in self.offset:
                                for k in range(0,10,2):
                                    if k not in self.offset1:
                                        self.offset[para]=k
                                        self.offset1.append(k)
                                        break
                            else:
                                break
                    else:
                        for k in range(0,10,2):
                            if k not in self.offset1:
                                self.offset[para]=k
                                self.offset1.append(k)
                                break
                    for i in range(len(self.parent.lines_with_desired_length)):
                        if self.parent.lines_with_desired_length[i][5]==str(packet_no):
                            hexa_val=self.parent.lines_with_desired_length[i][start_byte:end_byte]
                            decimal_integer=int(hexa_val,base=16)
                            binary_val = bin(decimal_integer)[2:]  # Convert decimal to binary
                            if len(binary_val)<8:
                                binary_val=((8-len(binary_val))*'0')+binary_val
                            time_s = self.parent.lines_with_desired_length[i][6:14]
                            dtime_s = int(time_s, base=16)

                            if dtime_s > prev_dtime_s:  # Check if the new timestamp is greater
                                temp=int(binary_val[int(bit_no) - 1])
                                temp+=self.offset[para]
                                self.stored_eng_val[para]['eng_val'].append(temp)
                                self.stored_eng_val[para]['time_stamp'].append((dtime_s-self.parent.min_frame_time)/100)
                                prev_dtime_s = dtime_s
            else:
                def extract_numbers(self,input_str):
                    if '-' in input_str:
                        start, end = map(int, input_str.split('-'))
                        return list(range(start, end + 1))
                    else:
                        return [int(input_str)]

                numbers = extract_numbers(self,str(byte_no))
                start_byte=(numbers[0]-1)*2
                end_byte=((numbers[-1])*2)
                #print(start_byte)
                #print(end_byte)
                #extract the range values and fo data engineering

                def extract_range_values(self,input_str):
                    try:
                        if ' to ' in input_str:
                            start, end = map(int, re.findall(r'-?\d+', input_str))
                            return start, end
                        else:
                            return None, None
                    except ValueError:
                        return None, None
                standard_flag=1
                start, end = extract_range_values(self,(str(range_no)))
                if start is not None and end is not None:
                    #print(f"Range: {start} to {end}")
                    pass
                else:
                    if str(range_no)=='nan':
                        start=0
                        end=2**(8*no_of_byte)
                        #print(f"Range: {start} to {end}")
                    else:
                        start=0
                        end=str(range_no)
                        tk.messagebox.showwarning("Warning","Cannot process:"+str(range_no))
                        standard_flag=0

                bias=0
                prev_dtime_s = float('-inf')
                self.offset[para]=0
                for i in range(len(self.parent.lines_with_desired_length)):
                    if self.parent.lines_with_desired_length[i][5]==str(packet_no):
                        hexa_val=self.parent.lines_with_desired_length[i][start_byte:end_byte]
                        #print("Raw value= ",hexa_val)
                        if standard_flag==1:
                            if start<0:
                                bias=-(start)
                                end=end+bias
                                start=0
                            decimal_integer=int(hexa_val,base=16)
                            decimal_integer*=end
                            decimal_integer=(decimal_integer)/(2**(8*no_of_byte))
                            decimal_integer-=bias
                            time_s=self.parent.lines_with_desired_length[i][6:14]
                            dtime_s=int(time_s,base=16)
                            if dtime_s > prev_dtime_s:  # Check if the new timestamp is greater
                                self.stored_eng_val[para]['eng_val'].append(decimal_integer)
                                self.stored_eng_val[para]['time_stamp'].append((dtime_s-self.parent.min_frame_time)/100)
                                prev_dtime_s = dtime_s
    def add_parameter(self):
        selected_param = self.combobox.get()
        if selected_param=="":
            tk.messagebox.showwarning("Warning","Select a Parameter from Combobox.")
        else:
            if selected_param not in self.selected_parameters_values:
                if len(self.selected_parameters_values) < self.MAX_SELECTED_PARAMETERS:
                    self.selected_parameters_values[selected_param] = self.parent.combined_df[self.parent.combined_df['PARAMETER'] == selected_param].values.tolist()
                    self.update_treeview()
                    self.update_combobox() 
                    self.add_parameter_from_file()
                else:
                    tk.messagebox.showwarning("Warning","Maximum number of selected parameters reached (5).")
            else:
                tk.messagebox.showinfo("Information","Parameter already selected.")

    def remove_selected(self):
        data=self.param_select()
        for selected_param in data:
            if selected_param in self.selected_parameters_values:
                del self.selected_parameters_values[selected_param]
                del self.stored_eng_val[selected_param]        #recent change
                self.update_treeview()
            if selected_param in self.plotted_param:
                self.plotted_param.pop(selected_param)

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for param, rows in self.selected_parameters_values.items():
            for row in rows:
                self.tree.insert('', 'end', values=row)

    def update_combobox(self):
        self.combobox.set("")  # Clear the current selection
        self.combobox['values'] = self.parent.parameter_values  # Update the combobox values
        
    def annot(self,event):
        x_clicked, y_clicked=event.xdata,event.ydata
        annotation=event.inaxes.annotate(f'({x_clicked:.2f},{y_clicked:.2f})',(x_clicked,y_clicked),textcoords="offset points",xytext=(0,10),ha="center")
        annotation.set_visible(True)
        plt.draw()
        self.root.after(5000,lambda:annotation.remove())

    # Connect the function to the figure's button_press_event
    
    def plot_selected_parameter(self,*args):
        data=self.param_select()
        for selected_param in data:
            if selected_param not in self.plotted_param:
                self.plotted_param[selected_param] = self.stored_eng_val[selected_param]
                self.offset_param[selected_param]=self.offset[selected_param]
        if selected_param in self.stored_eng_val:
            plt.close(self.fig)
            self.fig,self.ax=plt.subplots()
            max_eng_value = float('-inf')
            min_eng_value = float('inf')
            max_time_stamp = float('-inf')
            for param, data in self.plotted_param.items():
                eng_values = data['eng_val']
                timestamps = data['time_stamp']
                #print(offset_param[param])
                #offset2 = self.offset_param[param]  # Get the offset value
                eng_values = [float(value) for value in eng_values]  # Convert to float
                
                if eng_values:
                    max_eng_value = (max(eng_values)*0.3)+max(eng_values)
                    min_eng_value = (min(eng_values)*0.3)-min(eng_values)
                
                if timestamps:
                    max_time_stamp = max(max_time_stamp, max(timestamps))
                
                if eng_values and timestamps:
                    label = f"{param}"  # Include offset in the legend label
                    self.ax.plot(timestamps, eng_values, linewidth=1, linestyle='-', label=label)
            
            self.ax.set_xlabel('Timestamp in seconds')
            self.ax.set_ylabel(param)
            self.ax.set_title(self.file_entry.get())
            
            if max_time_stamp > 0:
                self.ax.set_xlim(0, max_time_stamp)
            if max_eng_value > 0:
                self.ax.set_ylim(min_eng_value, max_eng_value)
            elif min_eng_value < 0:
                self.ax.set_ylim(min_eng_value, 0)
            
            self.ax.legend()
            self.ax.grid(True)  # Add grid lines
            
            plt.tight_layout()
            self.fig.canvas.mpl_connect('button_press_event',lambda event: self.annot(event))
            plt.show()
            self.plotted_param={}
        else:
            tk.messagebox.showwarning("Warning","Selected parameter not found.")
            
    def plot_separate(self,*args):
        global i
        data=self.param_select()
        if len(data)>=2:
            for selected_param in data:
                if selected_param not in self.plotted_param:
                    self.plotted_param[selected_param] = self.stored_eng_val[selected_param]
            if selected_param in self.stored_eng_val:
                plt.close(self.fig)
                self.fig,self.ax=plt.subplots(nrows=len(self.plotted_param),ncols=1)
                i=0
                max_eng_value = float('-inf')
                min_eng_value = float('inf')
                max_time_stamp = float('-inf')
                for param, data in self.plotted_param.items():
                    eng_values = data['eng_val']
                    timestamps = data['time_stamp']
                    eng_values = [float(value) for value in eng_values]  # Convert to float
                    
                    if eng_values:
                        max_eng_value = (max(eng_values)*0.3)+max(eng_values)
                        min_eng_value = (min(eng_values)*0.3)-min(eng_values)
                    
                    if timestamps:
                        max_time_stamp = max(max_time_stamp, max(timestamps))
                    
                    if eng_values and timestamps:
                        label = f"{param}"  # Include offset in the legend label
                        self.ax[i].plot(timestamps, eng_values, linewidth=1, linestyle='-', label=label)
                
                        self.ax[i].set_xlabel('Timestamp in seconds')
                        self.ax[i].set_ylabel(param)
                        self.ax[i].set_title(self.file_entry.get())
                
                    if max_time_stamp > 0:
                        self.ax[i].set_xlim(0, max_time_stamp)
                    if max_eng_value > 0:
                        self.ax[i].set_ylim(min_eng_value, max_eng_value)
                    elif min_eng_value < 0:
                        self.ax[i].set_ylim(min_eng_value, 0)
                
                    self.ax[i].legend()
                    self.ax[i].grid(True)  # Add grid lines
                    i+=1
                
                plt.tight_layout()
                self.fig.canvas.mpl_connect('button_press_event', lambda event: self.annot(event))
                plt.show()
                self.plotted_param={}
            else:
                tk.messagebox.showwarning("Warning","Selected parameter not found.")
        else:
            tk.messagebox.showwarning("Warning","Select 2 or more parameters for plot separate.")
        
    def add_graph(self,*args):
        img_name=self.file_entry.get()
        data=self.param_select()
        n=len(data)
        if img_name not in self.img_names:
            if n!=5:
                data.extend(["None"]*(5-n))
            if self.var1.get()==1:
                data.append("Multiple plots")
            elif self.var1.get()==2:
                data.append("Single plot")
            if self.combobox1.get()==None:
                tk.messagebox.showwarning("Warning","Select file extension.")
            else:
                data.append(self.combobox1.get())
            if self.var1.get()==0:
                tk.messagebox.showwarning("Warning","Select either:Plot Separate [OR] Plot Together.")
            elif data[0]=="None":
                tk.messagebox.showwarning("Warning","Add atleast 1 parameter to the treeview.")
            elif data[-2]=="Multiple plots" and n==1:
                tk.messagebox.showwarning("Warning","Select atleast 2 parameters for plot separate.")
            elif data[-1]=="":
                tk.messagebox.showwarning("Warning","Select file extension.")
            else:
                self.img_names[img_name]=data
                self.update_tree() 
                self.file_entry.delete(first=0,last=10)
                self.tree.delete(*self.tree.get_children())
                self.plotted_param={}
                self.selected_parameters_values={}
                self.var1.set(0)
                self.combobox1.set("")
        else:
            tk.messagebox.showwarning("Warning","File name already entered.")

    def plot_to_img(self,*args):
        img_plotted=[]
        for name in self.img_names.keys():
            param={}
            plt.close(self.fig)
            size=(18,10)
            for k in [j for j in self.img_names[name][0:4] if j!="None"]:
                param[k]=self.stored_eng_val[k]
            if self.img_names[name][5]=="Multiple plots":
                n=len([j for j in self.img_names[name][0:4] if j!="None"])
                self.fig,self.ax=plt.subplots(nrows=n,ncols=1,figsize=size)
                self.fig.suptitle(name)
            else:
                self.fig,self.ax=plt.subplots(figsize=size)
            i=0
            max_eng_value = float('-inf')
            min_eng_value = float('inf')
            max_time_stamp = float('-inf')
            for para, data in param.items():
                eng_values = data['eng_val']
                timestamps = data['time_stamp']
                eng_values = [float(value) for value in eng_values]  # Convert to float
                
                if eng_values:
                    if self.img_names[name][5]=="Multiple plots":
                        max_eng_value = (max(eng_values)*0.3)+max(eng_values)
                        min_eng_value = (min(eng_values)*0.3)-min(eng_values)
                    else:
                        max_eng_value = max(max_eng_value,max(eng_values))
                        min_eng_value = min(min_eng_value,min(eng_values))
                
                if timestamps:
                    max_time_stamp = max(max_time_stamp, max(timestamps))
                
                if self.img_names[name][5]=="Multiple plots":
                    if eng_values and timestamps:
                        label = f"{para}"  # Include offset in the legend label
                        self.ax[i].plot(timestamps, eng_values, linewidth=1, linestyle='-', label=label)
            
                        self.ax[i].set_xlabel('Timestamp in seconds')
                        self.ax[i].set_ylabel('Eng Value')
                    
                    if max_time_stamp > 0:
                        self.ax[i].set_xlim(0, max_time_stamp)
                    if max_eng_value > 0:
                        self.ax[i].set_ylim(min_eng_value, max_eng_value)
                    elif min_eng_value < 0:
                        self.ax[i].set_ylim(min_eng_value, 0)
            
                    self.ax[i].legend()
                    self.ax[i].grid(True)  # Add grid lines
                    i+=1
                else:
                    if eng_values and timestamps:
                        label = f"{para}"  # Include offset in the legend label
                        self.ax.plot(timestamps, eng_values,linewidth=1, linestyle='-', label=label)
            
                        self.ax.set_xlabel('Timestamp in seconds')
                        self.ax.set_ylabel('Eng Value')
                        self.ax.set_title(name)
            
                    if max_time_stamp > 0:
                        self.ax.set_xlim(0, max_time_stamp)
                    if max_eng_value > 0:
                        self.ax.set_ylim(min_eng_value, max_eng_value)
                    elif min_eng_value < 0:
                        self.ax.set_ylim(min_eng_value, 0)
            
                    self.ax.legend()
                    self.ax.grid(True)  # Add grid lines
            plt.tight_layout()
            flag=self.check(name)
            if flag==1:
                plt.savefig(name+self.img_names[name][-1])
                img_plotted.append(name)
            else:
                pass
        for n in img_plotted:
            del self.img_names[n]
        self.update_tree()
        
    def check(self,name):
        ext=self.img_names[name][-1]
        directory=Path(r"D:\python internship")
        if directory.exists() and directory.is_dir():
            file_names=[file for file in directory.iterdir() if (str(file)).endswith(name+ext)]
            if len(file_names)==0:
                return 1
            else:
                tk.messagebox.showwarning("Warning","File already exists:"+name)
                return 0
    
    def update_tree(self):
        self.tree1.delete(*self.tree1.get_children())
        for img in self.img_names.keys():
            self.tree1.insert('', 'end', values=[img]+self.img_names[img]) 

    def remove(self):
        selected_items=self.tree1.selection()     
        if selected_items:
            data1=[]
            for item in selected_items:
                item_values=self.tree1.item(item,'values')
                data1.append(item_values[0])

        for name in data1:
            del self.img_names[name]
        self.update_tree()

    def edit(self,parent=None,root=None):
        selected_item=self.tree1.selection()
        if selected_item:
            item_value=self.tree1.item(selected_item,'values')
        self.remove()
        if item_value[-2]=="Multiple plots":
            self.var1.set(1)
        else:
            self.var1.set(2)
        self.file_entry.delete(0,10)
        self.file_entry.insert(0,item_value[0])
        for i in item_value[1:5]:
            if i!="None":
                self.selected_parameters_values[i]=self.parent.combined_df[self.parent.combined_df['PARAMETER']==i].values.tolist()
        self.update_treeview()
        self.update_combobox()
        self.combobox1.set(item_value[-1])
        self.add_parameter_from_file()

    def export_all(self):
        file_path=tk.filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[('CSV files','*.csv')])
        if file_path:
            selected_data=[]
            for item in self.tree1.get_children():
                selected_data.append(self.tree1.item(item)['values'])
            df1 = pd.DataFrame(selected_data, columns=["IMAGE FILE","PARAMETER1","PARAMETER2","PARAMETER3","PARAMETER4","PARAMETER5", "DESCRIPTION","EXTENSION"])
            df1.to_csv(file_path, index=False)
            tk.messagebox.showinfo("Information","Data exported successfully to:"+file_path)

    def import_all(self):
        file_path =tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            imported_df = pd.read_csv(file_path)
            for index, row in imported_df. iterrows():
                name=row.iloc[0]
                l=[i for i in row[1:]]
                self.img_names[name]=l
                for i in l[:-1]:
                    if i!="None":
                        self.selected_parameters_values[i] =self.parent.combined_df[self.parent.combined_df['PARAMETER'] ==i].values.tolist()
            self.update_tree()
            self.add_parameter_from_file()
            tk.messagebox.showinfo("Information","Data imported successfully from:"+file_path)
            self.selected_parameters_values={}
            
    def param_select(self):
        selected_items = self.tree.selection()
        if selected_items:
            data=[]
            for item in selected_items:
                item_values = self.tree.item(item, 'values')
                data.append(item_values[1])
            return(data)
        else:
            tk.messagebox.showwarning("Warning","Select atleast one parameter on the treeview.")


        
