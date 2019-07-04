import csv
from Readers.ReadHanna import *

import pandas as pd

class SenseFileOrigin():
    def isQ(self, filePath, sheetNames):
        exl = pd.ExcelFile(filePath)
        df = pd.read_excel(exl, sheetNames[-1])

        hannaReader = ReadHanna(filePath)

        hannaReader.readDataSheetRow(df,3)
        time1 = hannaReader.time
        second1 = int(time1.split(":")[-1])
        minute1 = int(time1.split(":")[-2])
        hour1 = int(time1.split(":")[-3])

        hannaReader.readDataSheetRow(df,4)
        time2 = hannaReader.time
        second2 = int(time2.split(":")[-1])
        minute2 = int(time2.split(":")[-2])
        hour2 = int(time2.split(":")[-3])

        if hour2 - hour1 != 0:
            minute1 = minute1 + (60 * (hour2 - minute1))

        if minute2 - minute1 != 0:
            second2 = second2 + (60 * (minute2 - minute1))

        interval = second2 - second1

        if interval != 0 and interval < 10:
            return True
        else:
            return False

    def senseFileOrigin(self, filePath):

        # check file handle:

        # if filePath.endswith(".xls"):
        #     df = pd.ExcelFile(filePath)
        #     sheetNames = df.sheet_names
        #     if len(sheetNames) == 2:
        #         return "field_hanna"
        if filePath.endswith(".xlsx") or filePath.endswith(".xls"):
            exl = pd.ExcelFile(filePath, nrows = 30)
            sheetNames = exl.sheet_names
            df = pd.read_excel(exl, sheetNames[0])

            columns = list(df.columns.values)

            if "#" == columns[0]:
                return "sites"

            if "Sample ID" in columns[0]:
                if "Site" in columns[1]:
                    return "water"

            if "Sortchem" in columns[0]:
                return "srp"

            if "Operator" in columns[0]:
                return "aqualog"

            if "Sample Identifier" in columns[0]:
                return "docIsotopes"

            if "Chem #" in columns[0]:
                return "masterScan"

            if len(columns) >= 3:
                if "OVSM" in columns[3]:
                    return "no3"
            i = 0
            while i < 15 and i < len(list(df.iloc[:,0])): # read through the first row
                value = str(df.iloc[i,1]).lower()
                if "no" in value:
                    return "lachat"
                i = i + 1

            i = 0
            while i < 10 and i < len(list(df.iloc[:,0])): # read through the first row

                value = str(df.iloc[i,0]).lower()

                if "instrument name" in value:
                    if len(sheetNames) == 2:
                        if self.isQ(filePath, sheetNames):
                            return "q"
                        else:
                            return "field_hanna"

                if "name" in value:
                    return "icp"
                if "number" in value:
                    return "ic"
                if "inj" in value:
                    return "ic"


                if "project" in value: # if it is a sampleID file that wasn't converted to a .csv
                    return "excel_sampleID"
                i = i + 1
            return "ic" # (by default)

        elif filePath.endswith(".csv"):

            if filePath.endswith("fp.csv"):
                return "scan.fp"
            if filePath.endswith("log.csv"):
                return "ignore"

            # open the file and look at the firs
            with open(filePath) as csvFile:
                reader = csv.reader(csvFile, delimiter=",")

                try:
                    firstRow = next(reader)
                    secondRow = next(reader)

                    if firstRow[0].endswith(".LOG"):
                        return "field_eureka"
                    elif "project" in secondRow[0].lower():
                        if "site" in secondRow[1].lower():
                            if "date" in secondRow[2].lower():
                                return "sampleID"
                    elif "Eureka" in secondRow[0]:
                        return "field_eureka"
                    elif "Plot Title" in firstRow[0]:
                        return "field_hobo.csv"
                    elif "stamp" in firstRow[0]:
                        if filePath.endswith("_log.csv"):
                            return "unrecognized"
                        else:
                            return "scan.par"
                    elif "sep" in firstRow[0]:
                        return "elementar"
                    else:
                        return "unrecognized"
                except:
                    # the file was empty (raised an error trying to access it)
                    return "no_data"

        elif filePath.endswith('.hobo'):
            return "field_hobo.hobo"
        elif filePath.endswith(".sql"):
            return "unrecognized"
        elif filePath.endswith('.fp'):
            return "scan.fp"
        elif filePath.endswith(".par"):
            return "scan.par"
        else:
            return "unrecognized"


