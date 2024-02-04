import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
import re
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from meta import MetaData
from plot import Plot
from Real_time import RealTimePlott

#This is the main class which must be called to run the whole application.
class main:
    def __init__(self,root=None):
        self.root=root
        self.selected_excel_file_path_1 = ""    #Stores the excel file path of analog parameters.
        self.selected_excel_file_path_2 = ""    #Stores the excel file path of discrete parameters.
        self.selected_sheet_1 = ""              #Stores the sheet name in the selected excel sheet, for analog parameters.
        self.selected_sheet_2 = ""              #Stores the sheet name in the selected excel sheet, for discrete parameters.
        self.selected_log_file_path = ""        #Stores the log file path of raw data.
        self.combined_df=pd.DataFrame()         #Dataframe to store engineering data.
        self.parameter_values=[]
        self.lines_with_desired_length=[]       #Stores each data packet of 128 bytes which have required length, header and footer values.
        self.min_frame_time=0
        self.new_df = pd.DataFrame()
        self.Init_UI()

    #Function to display the initial UI of the application.
    def Init_UI(self):
        #The constant menu frame on the left.
        self.frame1=tk.Frame(self.root,width=300,height=850,bg="#BFEFFF", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.frame1.pack(side='left', anchor='nw')

        #Parent frame for the changing frame on the right  .  
        self.mainframe=tk.Frame(root,width=1200,height=850,bg="#E3E3E3", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.mainframe.pack(side='left', anchor='nw')

        #Button for the home page, which contains info about each of the other pages.
        self.home_button=tk.Button(self.frame1,text="Home",bg="#BFEFFF", fg="#000080", bd=0, command=self.home)
        self.home_button.place(x=50,y=120)
        self.home_button.config(font=('Helvetica bold',18))
        
        #Empty label used to indicate that the home page is being displayed at the moment.
        self.home_indicator=tk.Label(self.frame1,text=" ", bg="#BFEFFF")
        self.home_indicator.place(x=5,y=120, width=5, height=40)

        #Button for the meta data page, which must be clicked and data files must be selected before accessing any other buttons below this one.
        self.meta_button=tk.Button(self.frame1,text="Select Meta Data",bg="#BFEFFF", fg="#000080", bd=0, command=self.meta_data)
        self.meta_button.place(x=50,y=200)
        self.meta_button.config(font=('Helvetica bold',18))

        #Empty label used to indicate that the meta data page is being displayed at the moment.
        self.meta_indicator=tk.Label(self.frame1,text=" ", bg="#BFEFFF")
        self.meta_indicator.place(x=5, y=200, width=5, height=40)
        
        #Button for plotting of graphs page, requires meta data to plot graphs.
        self.plot_button=tk.Button(self.frame1,text="Plot Graph",bg="#BFEFFF", fg="#000080", bd=0, command=self.plotting_graph)
        self.plot_button.place(x=50,y=280)
        self.plot_button.config(font=('Helvetica bold',18))

        #Empty label used to indicate that the graph plotting page is being displayed at the moment.
        self.plot_indicator=tk.Label(self.frame1,text=" ", bg="#BFEFFF")
        self.plot_indicator.place(x=5, y=280, width=5, height=40)
        
        #Button for data analysis page, requires meta data.
        self.analysis_button=tk.Button(self.frame1,text="Graph Analysis",bg="#BFEFFF", fg="#000080", bd=0, command=self.print_data)
        self.analysis_button.place(x=50,y=360)
        self.analysis_button.config(font=('Helvetica bold',18))
        
        # Add this to your existing UI code, e.g., in the Init_UI method
        self.real_time_plot_button = tk.Button(self.frame1, text="Real-Time Plot", bg="#BFEFFF", fg="#000080", bd=0, command=self.real_time_plot)
        self.real_time_plot_button.place(x=50, y=440)
        self.real_time_plot_button.config(font=('Helvetica bold', 18))
        
        self.real_indicator=tk.Label(self.frame1,text=" ", bg="#BFEFFF")
        self.real_indicator.place(x=5, y=440, width=5, height=40)

        
        #Empty label used to indicate that the analysis page is being displayed at the moment.
        self.analysis_indicator=tk.Label(self.frame1,text=" ", bg="#BFEFFF")
        self.analysis_indicator.place(x=5, y=360, width=5, height=40)

    #Function to display the home page, funtion called when home_button clicked.    
    def home(self):
        self.del_frame()
        self.indicate(self.home_indicator)
        #Initial frame that must display the home page contents.
        self.frame2=tk.Frame(self.mainframe,width=1200,height=850,bg="#E3E3E3", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.frame2.pack(side='left', anchor='nw')
        self.frame2.tkraise()       #Displays this frame above any other existing frames(on the left of the window only).
        
        #Contents of the home page.
        self.label1=tk.Label(self.frame2,text="Information about each button",bg="#E3E3E3")
        self.label1.config(font=('Helvetica bold',25))
        self.label1.place(x=110,y=360)

    #Function to display the meta data page, funtion called when meta_button clicked.
    def meta_data(self):
        self.del_frame()
        self.indicate(self.meta_indicator)

        #Initial frame that must display the meta data page contents.
        self.frame2=tk.Frame(self.mainframe,width=1200,height=850,bg="#E3E3E3", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.frame2.pack(side='left', anchor='nw')
        self.frame2.tkraise()       #Displays this frame above any other existing frames(on the left of the window only).

        MetaData(self,self.frame2)  #Class belonging to meta.py.
        
    #Function to display the graph plotting page, funtion called when plot_button clicked.
    def plotting_graph(self):
        self.del_frame()
        self.indicate(self.plot_indicator)

        #Initial frame that must display the graph plotting page contents.
        self.frame2=tk.Frame(self.mainframe,width=1200,height=850,bg="#E3E3E3", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.frame2.pack(side='left', anchor='nw')
        self.frame2.tkraise()       #Displays this frame above any other existing frames(on the left of the window only).

        if self.selected_excel_file_path_1!="":     #Checks whether meta data has been selected or not.
            Plot(self,self.frame2)  #Class belonging to plot.py.
        else:
            tk.messagebox.showwarning("Warning","Choose Meta Data.")

    #Example function.    
    def print_data(self):
        self.del_frame()
        self.indicate(self.analysis_indicator)
        self.frame2=tk.Frame(self.mainframe,width=1200,height=850,bg="#E3E3E3", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.frame2.pack(side='left', anchor='nw')

    #Function to delete all previous child frames on the left parent frame.
    def del_frame(self):
        for frame in self.mainframe.winfo_children():
            frame.destroy()

    #Function to display only the label next to the immediate selceted button, thus indicating the page being displayed at the moment.         
    def indicate(self, lb):
        self.hide_indicator()
        lb.config(bg="#000080")
    
    #Function to conceal all the labels (indicators).
    def hide_indicator(self):
        #Changing label bg colour to that of the left frame, thus concealing it as the labels do not have visible borders.
        self.home_indicator.config(bg="#BFEFFF")
        self.meta_indicator.config(bg="#BFEFFF")
        self.plot_indicator.config(bg="#BFEFFF")
        self.analysis_indicator.config(bg="#BFEFFF")
        
    #Function to display the graph plotting in real-time page, funtion called when realtime_button clicked.
    def real_time_plot(self):
        self.del_frame()
        self.indicate(self.real_indicator)
        
                #Initial frame that must display the graph plotting page contents.
        self.frame2=tk.Frame(self.mainframe,width=1200,height=850,bg="#E3E3E3", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.frame2.pack(side='left', anchor='nw')
        self.frame2.tkraise()       #Displays this frame above any other existing frames(on the left of the window only).
        
        if self.selected_excel_file_path_1!="":     #Checks whether meta data has been selected or not.
            RealTimePlott(self,self.frame2)  #Class belonging to plot.py.
        else:
            tk.messagebox.showwarning("Warning","Choose Meta Data.")
            
     #Example function.    
    def print_data(self):
        self.del_frame()
        self.indicate(self.analysis_indicator)
        self.frame2=tk.Frame(self.mainframe,width=1200,height=850,bg="#E3E3E3", highlightbackground="#000080", highlightthickness=1,bd= 0)
        self.frame2.pack(side='left', anchor='nw')

    #Function to delete all previous child frames on the left parent frame.
    def del_frame(self):
        for frame in self.mainframe.winfo_children():
            frame.destroy()

    #Function to display only the label next to the immediate selceted button, thus indicating the page being displayed at the moment.         
    def indicate(self, lb):
        self.hide_indicator()
        lb.config(bg="#000080")
    
    #Function to conceal all the labels (indicators).
    def hide_indicator(self):
        #Changing label bg colour to that of the left frame, thus concealing it as the labels do not have visible borders.
        self.home_indicator.config(bg="#BFEFFF")
        self.meta_indicator.config(bg="#BFEFFF")
        self.plot_indicator.config(bg="#BFEFFF")
        self.analysis_indicator.config(bg="#BFEFFF")
        self.real_indicator.config(bg="#BFEFFF")


#Root window. 
root=tk.Tk()
#Setting the size for the root window.
root.geometry("1500x850")
#Calling the main class.
main(root)
#Starts displaying the UI.
root.mainloop()
        