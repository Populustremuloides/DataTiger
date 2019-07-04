from SenseFileOrigin import *
from Uploader import *
from EasterEggs import *
from CustomErrors import *
from QueryAnalyses import *
import datetime
import os

class Database:
    def __init__(self):
        # connect to the database
        # "C:\\Users\\BCBrown\\Box\\AbbottLab\\Data\\test1.db"

        try:
            # open the db file
            filename = os.path.join(os.getcwd(), "DatabaseName.txt")
            with open(filename, "r") as dbNameFile:
                dbName = dbNameFile.read()
                self.defaultDBFile = dbName
        except:
            self.defaultDBFile = "C:\\Users\\BCBrown\\Box\\AbbottLab\\Data\\test1.db"

        self.conn = sqlite3.connect(self.defaultDBFile)
        self.cursor = self.conn.cursor()
        self.projectId = "Megafire"
        self.uploader = Uploader(self)
        self.sensor = SenseFileOrigin()
        self.querier = QueryAnalyses(self.cursor, self.uploader)
        self.easterEggs = EasterEggs()
        self.allowDuplicates = False
        self.success = 0
        self.failure = -1
        self.sassCoefficient = 0


    def changeProjectId(self, newId):
        self.projectId = newId
        self.uploader = Uploader(self)


    def analyzeTests(self):
        print("ZZ")
        self.querier.getSortChems()
        print("YY")
        self.sortChemsWithBatches = self.querier.checkSortChemTests()
        print("XX")

        return self.sortChemsWithBatches



    def getProjects(self):
        sqlProjects = "SELECT project_id FROM projects"
        self.cursor.execute(sqlProjects)

        return self.cursor.fetchall()

    def changeSassCoefficient(self, coefficient):
        self.sassCoefficient = coefficient

    def getProjectId(self):
        return self.projectId

    def senseFileOrigin(self, path):
        return self.sensor.senseFileOrigin(path)


    def changeDBFile(self, dbFile):
        if dbFile == "My name is Harry Potter." or "Harry" in dbFile:
            message = "Hello Harry Potter, my name is Tom Riddle"
            return message
        if dbFile == "Do you know anything about the Chamber of Secrets?" or "Chamber" in dbFile:
            message = "yes."
            return message
        if dbFile == "Can you tell me?" or "tell me" in dbFile:
            message = "no.\n\n\nBut I can show you."
            return message

        try:
            filename = os.path.join(os.getcwd(), "DatabaseName.txt")
            with open(filename, "w+") as dbNameFile:
                # clean up the file path
                dbFile = dbFile.replace("file:///","")
                dbFile = dbFile.replace("/","\\")

                # reset the connection
                self.conn = sqlite3.connect(dbFile)
                self.cursor = self.conn.cursor()

                # reset the querier
                self.defaultDBFile = dbFile
                self.querier = QueryAnalyses(self.cursor, self.uploader)

                dbNameFile.write(dbFile)

                # return a success message
                message = "Database File succesfully converted to " + str(dbFile) + "\n\nThis file will be the new default database for this computer.\n\n You clever cat."
                return message
        except:
            # reset to the original connection
            self.conn = sqlite3.connect(self.defaultDBFile)
            self.cursor = self.conn.cursor()

            # return an error
            message = "ERROR: unable to change database file to " + str(dbFile) + "\n\n"
            return message

    def writeTests(self, outputFile):
        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing Aqualog SortChems\n")
        if len(self.querier.missingAqualogs) > 0:
            for sortChem in self.querier.missingAqualogs:
                outputFile.write(sortChem)

                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing DOC-Isotopes SortChems\n")
        if len(self.querier.missingDocs) > 0:
            for sortChem in self.querier.missingDocs:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing Elementar SortChems\n")
        if len(self.querier.missingElementars) > 0:
            for sortChem in self.querier.missingElementars:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing MasterScan SortChems\n")
        if len(self.querier.missingScanDatetimes) > 0:
            for sortChem in self.querier.missingScanDatetimes:
                outputFile.write(sortChem)
                outputFile.write("\n")


        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing Scan-FP SortChems\n")
        if len(self.querier.missingScanFps) > 0:
            for sortChem in self.querier.missingScanFps:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing Scan-Par SortChems\n")
        if len(self.querier.missingScanPars) > 0:
            for sortChem in self.querier.missingScanPars:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing IC-Cation SortChems\n")
        if len(self.querier.missingIcCations) > 0:
            for sortChem in self.querier.missingIcCations:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing IC-Anion SortChems\n")
        if len(self.querier.missingIcAnions) > 0:
            for sortChem in self.querier.missingIcAnions:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing ICP SortChems\n")
        if len(self.querier.missingIcps) > 0:
            for sortChem in self.querier.missingIcps:
                outputFile.write(sortChem)
                outputFile.write("\n")


        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing Lachat SortChems\n")
        if len(self.querier.missingLachats) > 0:
            for sortChem in self.querier.missingLachats:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing NO3-Isotopes SortChems\n")
        if len(self.querier.missingNo3s) > 0:
            for sortChem in self.querier.missingNo3s:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing SRP SortChems\n")
        if len(self.querier.missingSrps) > 0:
            for sortChem in self.querier.missingSrps:
                outputFile.write(sortChem)
                outputFile.write("\n")

        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Missing Water-Isotope SortChems\n")
        if len(self.querier.missingWaters) > 0:
            for sortChem in self.querier.missingWaters:
                outputFile.write(sortChem)
                outputFile.write("\n")


        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Sort Chems that have been found in various "
                         "data files but for which no SampleID entry has been made, "
                         "files the sort Chem has been mentioned in\n")
        if len(self.querier.sortChemsMissingInstructions) > 0:
            for sortChem in self.querier.sortChemsMissingInstructions:
                outputFile.write(sortChem)
                outputFile.write(self.querier.getSortChemOrigins(sortChem, ","))
                outputFile.write("\n")


        outputFile.write("\n")
        outputFile.write("\n")
        outputFile.write("Sort Chems that are set as \'ignored\':\n")
        if len(self.querier.ignoredSortChems) > 0:
            for sortChem in self.querier.ignoredSortChems:
                outputFile.write(sortChem)
                outputFile.write("\n")

    def toString(self, list):
        newList = []
        for item in list:
            newList.append(str(item))
        return newList


    def writeTestsReport(self, path):
        try:
            self.analyzeTests()
            with open(path, "w+") as outputFile:
                for sortChemRow in self.sortChemsWithBatches:
                    sortChemRow = self.toString(sortChemRow)
                    outputFile.write(",".join(sortChemRow))
                    outputFile.write("\n")


                # write the different tests
                self.writeTests(outputFile)
            outputFile.close()
            message = "Successfully downloaded report to " + path + "\n\n"
            return message
        except:
            message = "ERROR: unable to download report.\n\n"
            return message


    def uploadFile(self, path):
        fileOrigin = self.senseFileOrigin(path)
        print(path)
        print(fileOrigin)
        try:
            if fileOrigin == "ignore":
                raise IgnoreFile
            elif fileOrigin == "no_data":
                raise NoDataToParse(path)
            elif fileOrigin == "unrecognized":
                return "ERROR: file format not recognized. " + path + " not uploaded to database.\n\n" + self.easterEggs.pickRandomCondolence(self.sassCoefficient)
            elif fileOrigin == "excel_sampleID":
                return "ERROR: " + path + " must first be converted to a .csv file before uploading to DataTiger.\n\n"
            else:
                self.uploader.uploadFile(self.cursor, path, fileOrigin, self.allowDuplicates)

            self.conn.commit()
            return("Successfully uploaded " + path + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except Warnings as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except ErrorInAqualogRows as e:
            self.conn.commit()
            return(e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except SortChemProblemRows as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except HoboRowsError as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except ICDataError as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except ScanPARReadsError as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except DuplicateScanTimes as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except ProblemRowsDetected as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except ElementarDuplicatesAndProblemsOccured as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except ElementarDuplicateRowsOccured as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except ElementarProblemRowsOccured as e:
            self.conn.commit()
            return (e.message + self.easterEggs.pickRandomCongrats(self.sassCoefficient))
        except IgnoreFile as e:
            self.conn.rollback()
            message = "ERROR: file type for " + path + " recognized as irrelevant. File ignored.\n" + self.easterEggs.pickRandomCondolence(self.sassCoefficient)
            return message
        except Error as e:
            self.conn.rollback()
            message = "ERROR: " + path + " not uploaded because of the following errors:" + "\n" + e.message + self.easterEggs.pickRandomCondolence(self.sassCoefficient)
            return(message)

        # except self.conn.connector.Error as e:
        #     print("SQL command not executed.")
        #     print(e)

    def getMaxSortChem(self, sortChems):
        currentYear = str(datetime.date.today().year)
        try:
            numericSorts = []
            for sortChemTuple in sortChems:
                sortChem = sortChemTuple[0]
                containsLetter = False
                containsDash = False
                startsWithCurrentYear = False

                for letter in sortChem:
                    if letter.isalpha():
                        containsLetter = True
                    if letter == "-":
                        containsDash = True

                currentYear = str(datetime.date.today().year)
                if sortChem.startswith(currentYear):
                    startsWithCurrentYear = True

                if containsDash and startsWithCurrentYear and not containsLetter:
                    year, number = sortChem.split("-")
                    numericSort = int(year + number)
                    numericSorts.append(numericSort)

            maxSortChem = max(numericSorts)
            if str(maxSortChem).startswith(str(currentYear)):
                return maxSortChem
            else:
                return str(currentYear) + "0000"
        except:
            currentYear = str(datetime.date.today().year)
            return str(currentYear) + "0000"

    def newSortChems(self, fileName, howMany):
        # open the output file
        try:
            fileName = fileName + ".csv"
            output = open(fileName, "w+")

            # get the highest sort-chem on record

            sqlSort = "SELECT highest_sort_chems FROM generated_sort_chems;"
            self.cursor.execute(sqlSort)

            sortChems = self.cursor.fetchall()

            maxSortChem = self.getMaxSortChem(sortChems)

            # generate as many sort-chems as we need
            newSortChem = str(int(maxSortChem) + 1)
            for i in range(int(howMany)):
                outputChem = str(newSortChem)[0:4] + "-" + str(newSortChem)[4:]
                output.write(outputChem + "\n")
                newSortChem = int(newSortChem) + 1
            newSortChem = int(newSortChem) - 1
            newSortChem = str(newSortChem)[0:4] + "-" + str(newSortChem)[4:]

            output.close()
            #
            sqlMax = "INSERT INTO generated_sort_chems (highest_sort_chems) VALUES (?);"
            maxTuple = (newSortChem,)

            self.cursor.execute(sqlMax, maxTuple)
            self.conn.commit()
            return "Success! " + str(howMany) + " new sort-chems generated and downloaded to " + fileName + ".csv.\n\n"
        except:
            return "ERROR: sort-chems were not succesfully generated or downloaded. The file you are trying to write to " \
                   "may be open in another program. Please close all instances of excel or another editor that have open the file" \
                   " name you designated. You may also be connected to a database that does not have a \'generated sort-chems\' table." \
                   " If this problem persists, please contact " \
                   "Brian Brown at bcbrown365@gmial.com.\n\n"






