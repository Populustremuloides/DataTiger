from CustomErrors import *
from datetime import datetime

class ReadSampleId:
    def __init__(self, filePath):

        self.missingValues = -1
        self.noZeroOrOne = -2
        self.noError = 0

        self.filePath = filePath

        cleanPath = self.filePath.replace("\\", "/")
        cleanPath = cleanPath.replace("//", "/")
        pathList = cleanPath.split("/")
        self.fileName = pathList[-1]

        self.projectIndex = None
        self.siteIndex = None
        self.dateIndex = None
        self.timeIndex = None
        self.sortChemIndex = None
        self.phIndex = None
        self.orpIndex = None
        self.o2percentIndex = None
        self.o2mgIndex = None
        self.condIndex = None
        self.tempIndex = None
        self.pressIndex = None
        self.calIndex = None
        self.qsaltIndex = None
        self.qtimeIndex = None
        # self.qdateIndex = None
        self.notesIndex = None
        self.samplersIndex = None
        self.conditionsIndex = None
        self.volumeIndex = None
        self.aqualogIndex = None
        self.docIndex = None
        self.elementarIndex = None
        self.scanIndex = None
        self.icIndex = None
        self.icpIndex = None
        self.lachatIndex = None
        self.no3Index = None
        self.srpIndex = None
        self.waterIndex = None
        self.ignoreIndex = None

        self.project = None
        self.site = None
        self.date = None
        self.time = None
        self.sortChem = None
        self.ph = None
        self.orp = None
        self.o2percent = None
        self.o2mg = None
        self.cond = None
        self.temp = None
        self.press = None
        self.cal = None
        self.qsalt = None
        self.qtime = None
        # self.qdate = None
        self.notes = None
        self.samplers = None
        self.conditions = None
        self.volume = None
        self.aqualog = None
        self.doc = None
        self.elementar = None
        self.scan = None
        self.ic = None
        self.icp = None
        self.lachat = None
        self.no3 = None
        self.srp = None
        self.water = None
        self.ignore = None

        self.datetimeUploaded = str(datetime.now())


    def resetValues(self):
        self.project = None
        self.site = None
        self.date = None
        self.time = None
        self.sortChem = None
        self.ph = None
        self.orp = None
        self.o2percent = None
        self.o2mg = None
        self.cond = None
        self.temp = None
        self.press = None
        self.cal = None
        self.qsalt = None
        self.qtime = None
        # self.qdate = None
        self.notes = None
        self.samplers = None
        self.conditions = None
        self.volume = None
        self.aqualog = None
        self.doc = None
        self.elementar = None
        self.scan = None
        self.ic = None
        self.icp = None
        self.lachat = None
        self.no3 = None
        self.srp = None
        self.water = None
        self.ignore = None

    def nullIndexPresent(self):
        if self.projectIndex == None:
            return True
        if self.siteIndex == None:
            return True
        if self.dateIndex == None:
            return True
        if self.timeIndex == None:
            return True
        if self.sortChemIndex == None:
            return True
        if self.phIndex == None:
             return True
        if self.orpIndex == None:
            return True
        if self.o2percentIndex == None:
            return True
        if self.o2mgIndex == None:
            return True
        if self.condIndex == None:
             return True
        if self.tempIndex == None:
            return True
        if self.pressIndex == None:
             return True
        if self.calIndex == None:
             return True
        if self.qsaltIndex == None:
            return True
        if self.qtimeIndex == None:
            return True
        # if self.qdateIndex == None:
        #     return True
        if self.notesIndex == None:
            return True
        if self.aqualogIndex == None:
            return True
        if self.docIndex == None:
            return True
        if self.elementarIndex == None:
             return True
        if self.scanIndex == None:
            return True
        if self.icIndex == None:
            return True
        if self.icpIndex == None:
            return True
        if self.lachatIndex == None:
            return True
        if self.no3Index == None:
            return True
        if self.srpIndex == None:
            return True
        if self.srpIndex == None:
            return True
        if self.waterIndex == None:
            return True
        if self.ignoreIndex == None:
            return True

        return False

    def readBatch(self, headers):

        # get the indices of the headers
        i = 0
        for header in headers:
            header = header.lower()
            if "project" in header:
                self.projectIndex = i
            elif "site" in header:
                self.siteIndex = i
            elif "date" in header and "q" not in header:
                self.dateIndex = i
            elif "time" in header and "q" not in header:
                self.timeIndex = i
            elif "sort" in header:
                self.sortChemIndex = i
            elif "ph" in header:
                self.phIndex = i
            elif "orp" in header:
                self.orpIndex = i
            elif "o2%" in header:
                self.o2percentIndex = i
            elif "o2mg" in header:
                self.o2mgIndex = i
            elif "cond" == header:
                self.condIndex = i
            elif "temp" in header:
                self.tempIndex = i
            elif "press" in header:
                self.pressIndex = i
            elif "cal" in header:
                self.calIndex = i
            elif "salt" in header:
                self.qsaltIndex = i
            elif "q time" in header:
                self.qtimeIndex = i
            # elif "q date" in header:
            #     self.qdateIndex = i
            elif "notes" in header:
                self.notesIndex = i
            elif "sampler" in header:
                self.samplersIndex = i
            elif "condition" in header:
                self.conditionsIndex = i
            elif "volume" in header:
                self.volumeIndex = i
            elif "aqualog" in header:
                self.aqualogIndex = i
            elif "doci" in header:
                self.docIndex = i
            elif "elementar" in header:
                self.elementarIndex = i
            elif "scan" in header:
                self.scanIndex = i
            elif "ic" in header and not "icp" in header:
                self.icIndex = i
            elif "icp" in header:
                self.icpIndex = i
            elif "lachat" in header:
                self.lachatIndex = i
            elif "no3" in header:
                self.no3Index = i
            elif "srp" in header:
                self.srpIndex = i
            elif "water" in header:
                self.waterIndex = i
            elif "ignore" in header:
                self.ignoreIndex = i

            i = i + 1

        if self.nullIndexPresent():
            raise MissingColumn(self.fileName)


    def isnt1or0(self, character):
        if character != "0" and character != "1":
            return True
        else:
            return False


    def fixDate(self, date):
        if not "-" in date:
            if "/" in date:
                try:
                    month, day, year = date.split("/")
                    return year + "-" + str(month) + "-" + str(day)
                except:
                    return "error parsing date"
        else:
            return date

    def blankForNull(self, string):
        string = str(string)
        if string == "" or string.isspace():
            return None
        else:
            return string

    def criticalNullPresent(self):
        if self.site == None:
            return True
        if self.project == None:
            return True
        if self.sortChem == None:
            return True
        return False

    def replaceWhiteSpace(self):

        self.project = self.blankForNull(self.project)
        self.site = self.blankForNull(self.site)
        self.date = self.blankForNull(self.date)
        self.time = self.blankForNull(self.time)
        self.sortChem = self.blankForNull(self.sortChem)
        self.ph = self.blankForNull(self.ph)
        self.orp = self.blankForNull(self.orp)
        self.o2percent = self.blankForNull(self.o2percent)
        self.o2mg = self.blankForNull(self.o2mg)
        self.cond = self.blankForNull(self.cond)
        self.temp = self.blankForNull(self.temp)
        self.press = self.blankForNull(self.press)
        self.cal = self.blankForNull(self.cal)
        self.qsalt = self.blankForNull(self.qsalt)
        self.qtime = self.blankForNull(self.qtime)
        # self.qdate = self.blankForNull(self.qdate)
        self.notes = self.blankForNull(self.notes)
        self.samplers = self.blankForNull(self.samplers)
        self.conditions = self.blankForNull(self.conditions)
        self.volumeFiltered = self.blankForNull(self.volumeFiltered)
        self.aqualog = self.blankForNull(self.aqualog)
        self.doc = self.blankForNull(self.doc)
        self.elementar = self.blankForNull(self.elementar)
        self.scan = self.blankForNull(self.scan)
        self.ic = self.blankForNull(self.ic)
        self.icp = self.blankForNull(self.icp)
        self.lachat = self.blankForNull(self.lachat)
        self.no3 = self.blankForNull(self.no3)
        self.srp = self.blankForNull(self.srp)
        self.water = self.blankForNull(self.water)
        self.ignore = self.blankForNull(self.ignore)

    def readRow(self, row):
        self.resetValues()

        # make sure there are enough
        if len(row) < 27:
            return self.missingValues

        self.project = row[self.projectIndex]
        self.site = row[self.siteIndex]
        self.date = self.fixDate(row[self.dateIndex])
        self.time = row[self.timeIndex]
        self.sortChem = row[self.sortChemIndex]
        self.ph = row[self.phIndex]
        self.orp = row[self.orpIndex]
        self.o2percent = row[self.o2percentIndex]
        self.o2mg = row[self.o2mgIndex]
        self.cond = row[self.condIndex]
        self.temp = row[self.tempIndex]
        self.press = row[self.pressIndex]
        self.cal = row[self.calIndex]
        self.qsalt = row[self.qsaltIndex]
        self.qtime = row[self.qtimeIndex]
        # self.qdate = self.fixDate(row[self.qdateIndex])
        self.notes = row[self.notesIndex]
        if self.samplersIndex != None:
            self.samplers = row[self.samplersIndex]
        if self.conditionsIndex != None:
            self.conditions = row[self.conditionsIndex]
        if self.volumeIndex != None:
            self.volumeFiltered = row[self.volumeIndex]
        self.aqualog = row[self.aqualogIndex]
        self.doc = row[self.docIndex]
        self.elementar = row[self.elementarIndex]
        self.scan = row[self.scanIndex]
        self.ic = row[self.icIndex]
        self.icp = row[self.icpIndex]
        self.lachat = row[self.lachatIndex]
        self.no3 = row[self.no3Index]
        self.srp = row[self.srpIndex]
        self.water = row[self.waterIndex]
        self.ignore = row[self.ignoreIndex]

        # make sure there were 0's and 1's
        if self.isnt1or0(self.aqualog):
            return self.noZeroOrOne
        if self.isnt1or0(self.doc):
            return self.noZeroOrOne
        if self.isnt1or0(self.elementar):
            return self.noZeroOrOne
        if self.isnt1or0(self.scan):
            return self.noZeroOrOne
        if self.isnt1or0(self.ic):
            return self.noZeroOrOne
        if self.isnt1or0(self.icp):
            return self.noZeroOrOne
        if self.isnt1or0(self.lachat):
            return self.noZeroOrOne
        if self.isnt1or0(self.no3):
            return self.noZeroOrOne
        if self.isnt1or0(self.srp):
            return self.noZeroOrOne
        if self.isnt1or0(self.water):
            return self.noZeroOrOne
        if self.isnt1or0(self.ignore):
            return self.noZeroOrOne

        self.replaceWhiteSpace()

        if self.criticalNullPresent():
            return self.missingValues
        else:
            return self.noError


