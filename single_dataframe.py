class single_dataframe(combined_csv_dataframe):
    def __init__(self):
        self.filename = ""
        self.spreadsheet = pd.DataFrame()
        self.skipped_rows = 0

    def filter_file_name(self, file_arg):
        # opens up file browser for data file
        #filter filename into useable variable
        self.filename = file_arg
        self.filename = self.filename.split(sep="/")
        self.filename = str(self.filename[-1])
        self.filename = self.filename.split(".")
        self.filename = self.filename[0:-1]
        self.filename = '.'.join(self.filename)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        return str(root.filename)

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
        spreadsheet = spreadsheet.dropna()
        self.spreadsheet = spreadsheet
        return spreadsheet
