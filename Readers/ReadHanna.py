from CustomErrors import *
import pandas as pd
import re
from math import isnan


class ReadHanna():
    def __init__(self, path):

        # for the info sheet
        self.instrumentName = None
        self.instrumentId = None
        self.serialNum = None
        self.pcSoftwareVersion = None
        self.meterSoftwareVersion = None
        self.meterSoftwareDate = None
        self.referenceTemp = None
        self.temperatureCoefficient = None
        self.tdsFactor = None
        self.lotName = None
        self.remarks = None
        self.startDate = None
        self.startTime = None
        self.samplesNo = None
        self.loggingInterval = None
        self.numParameters = None

        # for the data sheet
        self.date = None
        self.time = None
        self.temp = None
        self.pH = None
        self.orp = None
        self.ec = None
        self.pressure = None
        self.dissolvedOxygenPercent = None
        self.dissolvedOxygen = None
        self.remarks = None

        # Grab the first three letters of the file name
        self.filePath = path
        cleanPath = path.replace("\\", "/")
        cleanPath = cleanPath.replace("//", "/")
        pathList = cleanPath.split("/")
        self.fileName = pathList[-1]
        self.sitePrefix = self.fileName[0:3].upper()

        self.dateIndex = None
        self.timeIndex = None
        self.tempIndex = None
        self.pHIndex = None
        self.orpIndex = None
        self.ecIndex = None
        self.pressureIndex = None
        self.dissolvedOxygenPercentIndex = None
        self.dissolvedOxygenIndex = None
        self.remarksIndex = None

        self.dataSheetHeadersCalled = False

    def getFilePath(self):
        return self.filePath

    def getFileName(self):
        return self.fileName

    def readInfoSheet(self, df):
        try:
            for index, row in df.iterrows():
                if index == 0:
                    if row[0] == "Instrument Name":
                        self.instrumentName = row[1]
                    else:
                        raise hannaInfoSheetChanged(0)
                        # TODO: change the errors to be specific
                if index == 1:
                    if row[0] == "Instrument ID":
                        if pd.isnull(row[1]):
                            self.instrumentId = "NULL"
                            print("null value detected")
                        else:
                            self.instrumentId = row[1]
                    else:
                        raise hannaInfoSheetChanged(0)
                if index == 2:
                    if row[0] == "Instrument Serial No.":
                        self.serialNum = row[1]
                    else:
                        raise hannaInfoSheetChanged(2)
                if index == 3:
                    if row[0] == "PC Software Version":
                        self.pcSoftwareVersion = row[1]
                    else:
                        raise hannaInfoSheetChanged(3)
                if index == 4:
                    if row[0] == "Meter Software Version":
                        self.meterSoftwareVersion = row[1]
                    else:
                        raise hannaInfoSheetChanged(4)
                if index == 5:
                    if row[0] == "Meter Software Date":
                        self.meterSoftwareDate = row[1]
                    else:
                        raise hannaInfoSheetChanged(5)
                if index == 9:
                    if row[0] == "Reference Temperature":
                        if row[1].endswith("C"): # make sure it's celcius
                            # save just the number
                            nums = [int(s) for s in row[1].split() if s.isdigit()]
                            self.referenceTemp = nums[0]
                        else:
                            raise hannaInfoSheetChanged(9)
                    else:
                        raise hannaInfoSheetChanged(9)
                if index == 10:
                    if row[0] == "Temperature Coefficient":
                        if row[1].endswith("C"): # make sure it's celcius
                            num = (row[1].split(" "))[0]
                            self.temperatureCoefficient = num
                        else:
                            raise hannaInfoSheetChanged(10)
                    else:
                        raise hannaInfoSheetChanged(10)
                if index == 11:
                    if row[0] == "TDS Factor":
                        self.tdsFactor = row[1]
                    else:
                        raise hannaInfoSheetChanged(11)
                if index == 15:
                    if row[0] == "Lot Name":
                        if len(row[1]) >= 3:
                            self.lotName = row[1][0:3] # just save the 3 letters representing the site
                        else:
                            self.lotName = str(row[1])
                    else:
                        raise hannaInfoSheetChanged(15)

                if index == 16:
                    if row[0] == "Remarks":
                        self.remarks = row[1]
                    else:
                        raise hannaInfoSheetChanged(16)
                if index == 17:
                    if row[0] == "Started Date and Time":
                        text = row[1].split(" - ")

                        # remove extra space
                        self.startDate = text[0]
                        self.startTime = text[1]

                        # format the strings for sqlite
                        self.startDate = re.sub("\W+", "-", self.startDate)
                        self.startTime = re.sub("\W+", ":", self.startTime)

                    else:
                        raise hannaInfoSheetChanged(17)

                if index == 18:
                    if row[0] == "Samples No":
                        self.samplesNo = row[1]
                    else:
                        raise hannaInfoSheetChanged(18)
                if index == 19:
                    if row[0] == "Logging Interval":
                        if row[1] == "---":
                            self.loggingInterval = None
                        else:
                            self.loggingInterval = row[1]
                    else:
                        raise hannaInfoSheetChanged(19)
                if index == 20:
                    if row[0] == "Parameters No.":
                        self.numParameters = row[1]
                    else:
                        raise hannaInfoSheetChanged(20)

            if self.instrumentId == "Nan":
                print("got an nan")

            # print(self.instrumentName)
            # print(self.serialNum)
            # print(self.pcSoftwareVersion)
            # print(self.meterSoftwareVersion)
            # print(self.meterSoftwareDate)
            # print(self.referenceTemp)
            # print(self.temperatureCoefficient)
            # print(self.tdsFactor)
            # print(self.lotName)
            # print(self.remarks)
            # print(self.startDate)
            # print(self.startTime)
            # print(self.samplesNo)
            # print(self.loggingInterval)
            # print(self.numParameters)

            return [0]

        except hannaInfoSheetChanged:
            return [1, hannaInfoSheetChanged] # fixme: this might cause problems

    def readDataSheetHeaders(self, headers):
        i = 0
        for header in headers:
            header = header.lower()
            if "date" in header:
                self.dateIndex = i
            elif "time" in header:
                self.timeIndex = i
            elif "temp" in header:
                self.tempIndex = i
            elif "ph" in header:
                self.pHIndex = i
            elif "orp" in header:
                self.orpIndex = i
            elif "ec" in header:
                self.ecIndex = i
            elif "press" in header:
                self.pressureIndex = i
            elif "d.o." in header and "%" in header:
                self.dissolvedOxygenPercentIndex = i
            elif "d.o." in header and "mg" in header:
                self.dissolvedOxygenIndex = i
            elif "remarks" in header:
                self.remarksIndex = i
            i = i + 1
        self.dataSheetHeadersCalled = True

    def resetValues(self):
        self.date = None
        self.time = None
        self.temp = None
        self.pH = None
        self.orp = None
        self.ec = None
        self.pressure = None
        self.dissolvedOxygenPercent = None
        self.dissolvedOxygen = None
        self.remarks = None

    def readDataSheetRow(self, df, rowIndex):
        if not self.dataSheetHeadersCalled:
            self.readDataSheetHeaders(list(df.columns.values))
        try:

            self.resetValues()
            row = list(df.loc[rowIndex]) #convert from series object to list

            if not isnan(row[5]): # check to see if this is the bottom of the table
                if self.dateIndex != None:
                    self.date = (row[self.dateIndex]).strftime("%Y-%m-%d")
                if self.timeIndex != None:
                    self.time = (row[self.timeIndex]).strftime("%H:%M:%S")
                if self.tempIndex != None:
                    self.temp = row[self.tempIndex]
                if self.pHIndex != None:
                    self.pH = row[self.pHIndex]
                if self.orpIndex != None:
                    self.orp = row[self.orpIndex]
                if self.ecIndex != None:
                    self.ec = float(row[self.ecIndex])
                if self.pressureIndex != None:
                    self.pressure = row[self.pressureIndex]
                if self.dissolvedOxygenPercentIndex != None:
                    self.dissolvedOxygenPercent = row[self.dissolvedOxygenPercentIndex]
                if self.dissolvedOxygenIndex != None:
                    self.dissolvedOxygen = row[self.dissolvedOxygenIndex]
                if self.remarksIndex != None:
                    self.remarks = row[self.remarksIndex]

            return [0]

        except errorProcessingHannaData:
            print("error in ReadHanna")
            return [1, errorProcessingHannaData]


