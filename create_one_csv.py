from tkinter import *
from tkinter.filedialog import askopenfilenames
import pandas as pd

class multifilesApp(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.csv_tuple = ()

    def initializeUI(self):
        self.master.title('Select Files Application')
        self.grid(row=0, column=0,sticky=W)

        # Create the button to select files
        self.button1 = Button(self.master, text='Select Files', command=self.selectFiles, width=10)
        self.button1.grid(row=30, column=0)

    def selectFiles(self):
        files = askopenfilenames(filetypes=(('CSV files', '*.csv'),
                                       ('All files', '*.*')),
                                       title='Select Input File'
                                       )
        self.csv_tuple = root.tk.splitlist(files)
        print('Your selected files = ', self.csv_tuple)




class combined_csv_dataframe(multifilesApp):
    def __init__(self ):
        multifilesApp.__init__(self)
        self.filename = ""
        self.dataframes_list = []
        self.master_dataframe = pd.DataFrame()
        #tracker variables for the CSV files moved in
        #allows you to have a list of the name of all the columns in a CSV
        self.impedance_list = []
        self.phase_list = []
        self.system_phase_list = []
        self.imaginary_list = []
        self.real_list = []
        self.master_list = []

    def create_individual_dataframe_list(self):
        for iterator in self.csv_tuple:
            print("csv iterator =", iterator)
            temp_obj = single_dataframe.filterdata(self=single_dataframe(), file_arg=iterator)
            self.dataframes_list.append(temp_obj)

    def initialize_name_list(self):
        spreadsheet = self.dataframes_list[0]
        self.impedance_list = list(filter(lambda name: 'IMPEDANCE' in name, list(spreadsheet)))
        self.phase_list = list(filter(lambda name: name.startswith("PHASE"), list(spreadsheet)))
        self.system_phase_list = list(filter(lambda name: name.startswith("SYSTEM PHASE"), list(spreadsheet)))
        self.imaginary_list = list(filter(lambda name: 'IMAGINARY' in name, list(spreadsheet)))
        self.real_list = list(filter(lambda name: 'REAL' in name, list(spreadsheet)))
        for i in range(len(self.impedance_list)):
            if(len(self.impedance_list) == len(self.phase_list)):
                self.master_list.append([self.impedance_list[i], self.phase_list[i], self.real_list[i],
                                        self.imaginary_list[i], self.system_phase_list[i]])
    def create_one_master_dataframe(self):
        print("first master dataframe",self.master_dataframe)
        self.master_dataframe = pd.concat(self.dataframes_list)
        print("second master dataframe",self.master_dataframe)
        self.master_dataframe.to_csv(r"C:\Users\matts\PycharmProjects\multi_csv_graph\master_data_frame.csv",
                           index=None, header=True)




# Begin Main
class single_dataframe(combined_csv_dataframe):
    def __init__(self):
        self.filename = ""
        self.spreadsheet = pd.DataFrame()
        self.skipped_rows = 0
        self.file_path = ""

    def filter_file_name(self, file_arg):
        # opens up file browser for data file
        #filter filename into useable variable
        self.filename = file_arg
        self.filename = self.filename.split(sep="/")
        self.file_path = self.filename[0:-1]
        self.file_path = "/".join(self.file_path)
        self.filename = str(self.filename[-1])
        self.filename = self.filename.split(".")
        self.filename = self.filename[0:-1]
        self.filename = '.'.join(self.filename)
        return self.filename
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def filterdata(self,file_arg):
        file = file_arg
        # finds the first location of "TIME" in the data file and creates the dataframe from that
        spreadsheet = pd.read_csv(file)
        for i in range(len(spreadsheet)):
            list_check = list(spreadsheet.iloc[i])
            if (list_check[0] == "TIME"):
                spreadsheet = pd.read_csv(file, skiprows=(i + 1))
                self.skipped_rows = i + 1
                break
        # masks the values above 10_000 ohms which correspond to air
        # masks them with blank NaN values to be excluded from graphing
        spreadsheet = spreadsheet.mask(spreadsheet > 10_000)
        #drop all na values from dataframe
        #spreadsheet = spreadsheet.dropna()
        #drop the last row of our spreadsheet due to errors with the arduino not reading full complete rows
        spreadsheet.drop(spreadsheet.tail(1).index, inplace=True)
        file_name = self.filter_file_name(file_arg=file_arg)
        spreadsheet.insert(loc=0, column="DATA SOURCE", value = file_name)
        self.spreadsheet = spreadsheet
        return spreadsheet

#declare app scope not in the if loop here
app = None

#loop file selection until user exits the tkinter window
if __name__ == "__main__":
    root = Tk()
    root.minsize(width=250, height=400)
    #root.geometry("1200x800")
    root.geometry("400x300")

    # Call the parser GUI application
    app = multifilesApp(master=root)
    app.initializeUI()
    app.mainloop()

data_frame = combined_csv_dataframe()
data_frame.csv_tuple = app.csv_tuple
data_frame.create_individual_dataframe_list()
data_frame.initialize_name_list()
data_frame.create_one_master_dataframe()





