import re
import csv
from CustomErrors import NoDataToParse, HoboSerialNumUnparsable, HoboIncorrectlyFormated, HoboMissingData, SiteNotInFileName

class ReadHobo():
    def __init__(self, path):
        self.filePath = path
        cleanPath = self.filePath.replace("\\", "/")
        cleanPath = cleanPath.replace("//", "/")
        pathList = cleanPath.split("/")
        self.fileName = pathList[-1]

        self.siteId = None
        self.projectId = None
        self.serialNum = None
        self.downloadDate = None
        self.batchIdentifier = None
        self.dateExtracted = None

    def getFileName(self):
        return self.fileName

    def getFilePath(self):
        return self.filePath

    def getDateAndTime(self, string):
        stringList = string.split(" ")
        date = stringList[0].replace("/", "-")

        time = stringList[1]

        meridian = stringList[2]

        if meridian == "PM":
            timeList = time.split(":")
            hour = int(timeList[0])
            hour = hour + 12
            timeList[0] = str(hour)
            time = ":".join(timeList)

        return[date, time]



    def readHobo(self):
        # open the file
        with open(self.filePath) as csvFile:
            reader = csv.reader(csvFile, delimiter=",")

            try:
                row1 = next(reader)
                row2 = next(reader)
            except:
                raise NoDataToParse(self.filePath)
            try:
                result = re.search("S/N: \d+", row2[2])
                snString = result.group(0)
                snList = snString.split(" ")
                self.serialNum = snList[1]
                csvFile.close()
            except:
                csvFile.close()
                raise HoboSerialNumUnparsable(self.filePath)

    def readBatch(self):
        # get the site id from the file name
        fileList = self.fileName.split(".")
        fileWords = fileList[0]
        result = re.search(r"[a-zA-Z]+", fileWords)
        try:
            self.siteId = result.group(0)
        except:
            raise SiteNotInFileName(self.fileName)

        if self.serialNum == None:
            self.readHobo()

        # extract the date if it is in the title
        rawExtractionDate = fileWords.replace(self.serialNum, "")
        rawExtractionDate = rawExtractionDate.replace(self.siteId, "")
        self.extractionDate = ""
        for c in rawExtractionDate:
            if c.isnumeric():
                self.extractionDate = self.extractionDate + c

        if len(self.extractionDate) == 6: # if it is likely to be a date
            year = self.extractionDate[0:2]
            month = self.extractionDate[2:4]
            day = self.extractionDate[4:6]
            self.extractionDate = "20" + year + "-" + month + "-" + day
        else:
            self.extractionDate = None

        # open the file
        with open(self.filePath) as csvFile:
            reader = csv.reader(csvFile, delimiter=",")
            try:
                firsRow = next(reader)
                secondRow = next(reader)
                thirdRow = next(reader)
            except:
                raise NoDataToParse(self.fileName)

            try:
                self.firstLoggedDate, self.firstLoggedTime = self.getDateAndTime(thirdRow[1])

            except:
                raise HoboIncorrectlyFormated(self.fileName)

        self.siteId = self.siteId.upper() # this must be done here because if it were to be done earlier, the date would be messed up


    def readRow(self, row, i):
        try:
            self.logDate, self.logTime = self.getDateAndTime(row[1])
            self.absolutePressure = row[2]
            self.temperature = row[3]

            if self.logDate == "":
                self.logDate = None
            if self.logTime == "":
                self.logTime = None
            if self.absolutePressure == "":
                self.absolutePressure = None
            if self.temperature == None:
                self.temperature = None

        except:
            raise HoboMissingData(self.fileName, i)

