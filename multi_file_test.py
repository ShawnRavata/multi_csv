from tkinter import *
from tkinter.filedialog import askopenfilenames
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import Plot
from colorcet import glasbey

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
        self.master_impedance_dataframe = pd.DataFrame
        #tracker variables for the CSV files moved in
        #allows you to have a list of the name of all the columns in a CSV
        self.impedance_list = []
        self.phase_list = []
        self.system_phase_list = []
        self.imaginary_list = []
        self.real_list = []
        self.master_list = []
        self.filename_list = []

    def create_individual_dataframe_list(self):
        for iterator in self.csv_tuple:
            print("csv iterator =", iterator)
            temp_obj = single_dataframe()
            temp_obj.filterdata(file_arg=iterator)
            self.dataframes_list.append(temp_obj)

    def initialize_name_list(self):
        spreadsheet = self.dataframes_list[0].spreadsheet
        self.impedance_list = list(filter(lambda name: 'IMPEDANCE' in name, list(spreadsheet)))
        self.phase_list = list(filter(lambda name: name.startswith("PHASE"), list(spreadsheet)))
        self.system_phase_list = list(filter(lambda name: name.startswith("SYSTEM PHASE"), list(spreadsheet)))
        self.imaginary_list = list(filter(lambda name: 'IMAGINARY' in name, list(spreadsheet)))
        self.real_list = list(filter(lambda name: 'REAL' in name, list(spreadsheet)))
        for i in range(len(self.impedance_list)-2):
            if(len(self.impedance_list) == len(self.phase_list)):
                self.master_list.append([self.impedance_list[i], self.phase_list[i], self.real_list[i],
                                        self.imaginary_list[i], self.system_phase_list[i]])
    def create_one_master_dataframe(self):
        temp_frame_list = []
        for i in range(len(self.dataframes_list)):
            temp_frame_list.append(self.dataframes_list[i].spreadsheet)
        self.master_dataframe = pd.concat(objs=temp_frame_list)
        self.master_dataframe = self.master_dataframe.dropna()
        # self.master_dataframe.to_csv(r"C:\Users\matts\PycharmProjects\multi_csv_graph\master_data_frame.csv",
        #                    index=None, header=True)

    def clean_up_impedance_data(self):
        # self.master_impedance_dataframe
        spreadsheet = self.master_dataframe[self.impedance_list]
        spreadsheet = spreadsheet.mask(cond=spreadsheet[self.impedance_list] > 10_000)
        spreadsheet = spreadsheet.dropna(axis=1,how="all")
        spreadsheet.insert(loc=0, column="DATA SOURCE", value=self.master_dataframe["DATA SOURCE"].values,
                                allow_duplicates=True)
        spreadsheet.to_csv(r"C:\Users\matts\PycharmProjects\multi_csv_graph\master_data_frame.csv",
                           index=None, header=True)
        self.master_impedance_dataframe = spreadsheet

    def slice_data(self):
        data_slice = pd.DataFrame()
        # for i in range(len(self.csv_tuple)):
        self.create_filename_list()
        temp_data_slice = pd.DataFrame()
        print(self.filename_list)
        temp_data_slice = self.master_impedance_dataframe[["DATA SOURCE", "IMPEDANCE 1"]].pivot(
            columns="DATA SOURCE", values="IMPEDANCE 1")
        print(temp_data_slice["D1_B3_6.5.19_T1"].first_valid_index())
        #cuts off the first value of a data read in run
        for i in range(3):
            temp_data_slice[self.filename_list[i]]= temp_data_slice[
                self.filename_list[i]].shift(-(temp_data_slice[self.filename_list[i]].first_valid_index() + 1))
        temp_data_slice.to_csv(r"C:\Users\matts\PycharmProjects\multi_csv_graph\data_slice.csv",
                           index=None, header=True)

    def create_filename_list(self):
        for iterator in range(len(self.dataframes_list)):
            self.filename_list.append(self.dataframes_list[iterator].filename)


    # def bokeh_plot(self):
    #     grid = []
    #     # data_source = ColumnDataSource(self.spreadsheet)
    #     for i in range(len(self.impedance_list)):
    #         line = Plot(output_backend="webgl")  # for the glyph API
    #         line = figure(plot_width= 400, plot_height= 400, title="Impedance Data Overlay",
    #                       x_axis_label="Time(s)", y_axis_label="Impedance(ohms)", output_backend="webgl")
    #         temp_list = []
    #         max_index_length = 0;
    #         for j in range(len(self.csv_tuple)):
    #             if max_index_length < self.dataframes_list:
    #
    #         for j in range(len(self.csv_tuple)):
    #
    #             data_source = column
    #             temp_list.append(line.step(x="TIME", y=self.impedance_list[i], line_color=glasbey[i], source=data_source,
    #                                    line_width=2))
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # temp_list.append(line)
            # grid.append(temp_list)
            # grid = bl.layout(children=grid)
            # div = Div(text="""
            #     <h1>Ravata Impedance Data</h1>
            #     <p>This is Impedance Data generated by the Ravata Rize system
            #     </p>
            #     """)
            # doc = Document()
            # doc.add_root(column(div, grid, sizing_mode="scale_width"))
            # if __name__ == "__main__":
            #     doc.validate()
            # filename = "graph_all_" + str(self.filename) + ".html"
            # with open(filename, "w") as f:
            #     f.write(file_html(doc, INLINE, "RAVATA"))
            # print("Wrote %s" % filename)
            # view(filename)


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
        spreadsheet = pd.read_csv(file,sep = ",")
        for i in range(len(spreadsheet)):
            list_check = list(spreadsheet.iloc[i])
            if (list_check[0] == "TIME"):
                spreadsheet = pd.read_csv(file, skiprows=(i + 1))
                self.skipped_rows = i + 1
                break
        # masks the values above 10_000 ohms which correspond to air
        # masks them with blank NaN values to be excluded from graphing
        #drop all na values from dataframe
        #spreadsheet = spreadsheet.dropna()
        #drop the last row of our spreadsheet due to errors with the arduino not reading full complete rows
        spreadsheet.drop(spreadsheet.tail(1).index, inplace=True)
        file_name = self.filter_file_name(file_arg=file_arg)
        spreadsheet.insert(loc=0, column="DATA SOURCE", value = file_name)
        self.spreadsheet = spreadsheet
    

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
data_frame.clean_up_impedance_data()
data_frame.slice_data()





