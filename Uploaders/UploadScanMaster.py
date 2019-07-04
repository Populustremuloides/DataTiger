import pandas as pd
from CustomErrors import *

class UploadScanMaster:
    def __init__(self, cursor, uploader, scanMasterReader):
        self.cursor = cursor
        self.uploader = uploader
        self.scanMasterReader = scanMasterReader
        self.df = None
        self.semicolon = False
        self.tab = False

        self.currentBatch = None

        # separate the different excel sheets
        xls = pd.ExcelFile(self.scanMasterReader.filePath)
        self.sheets = xls.sheet_names

        self.data = None
        self.errorOccured = False


    def uploadBatch(self):
        # get the data
        self.data = pd.read_excel(self.scanMasterReader.filePath, self.sheets[0])

        # get the info about the batch
        columns = list(self.data.columns.values)
        self.scanMasterReader.readBatch(columns)

        # upload the file
        sqlBatch = "INSERT INTO scan_master_batches (file_name, file_path, upload_datetime) VALUES (?,?,?);"
        batchTuple = (self.scanMasterReader.fileName, self.scanMasterReader.filePath, self.scanMasterReader.datetime)
        self.cursor.execute(sqlBatch, batchTuple)

        # retain the batch_id
        sqlBatch = "SELECT scan_master_batch_id FROM scan_master_batches WHERE file_name = ? AND file_path = ? AND upload_datetime = ?;"
        batchTuple = (self.scanMasterReader.fileName, self.scanMasterReader.filePath, self.scanMasterReader.datetime)
        self.cursor.execute(sqlBatch, batchTuple)

        # get the batch id
        currentBatches = self.cursor.fetchall()
        self.currentBatch = currentBatches[-1][0]


    def uploadRow(self):
        # check for duplicates first

        # check for duplicate datetime values
        sqlBatch = "SELECT datetime_run FROM sort_chems_to_datetime_run WHERE datetime_run = ? AND sort_chem = ?;"
        batchTuple = (str(self.scanMasterReader.timestamp), self.scanMasterReader.sortChem)


        self.cursor.execute(sqlBatch, batchTuple)
        batches = self.cursor.fetchall()

        if (len(batches) > 0) and (not self.uploader.allowDuplicates):
            return self.scanMasterReader.error

        else:
            # upload the row
            sqlRow = "INSERT INTO sort_chems_to_datetime_run (sort_chem, datetime_run, scan_master_batch_id) VALUES (?,?,?);"
            rowTuple = (self.scanMasterReader.sortChem, str(self.scanMasterReader.timestamp), self.currentBatch)
            try:
                self.cursor.execute(sqlRow, rowTuple)
            except:
                return self.scanMasterReader.error

            # add to the sort-chem table **************************8
            # see if the sort chem is already in the sort-chems
            sqlCheck = "SELECT * FROM sort_chems WHERE sort_chem = ?;"
            checkTuple = (self.scanMasterReader.sortChem,)

            self.cursor.execute(sqlCheck, checkTuple)
            sortChems = self.cursor.fetchall()

            # if not, upload it
            if len(sortChems) == 0:
                sqlSort = "INSERT INTO sort_chems (sort_chem) VALUES (?);"
                sortTuple = (self.scanMasterReader.sortChem,)
                self.cursor.execute(sqlSort, sortTuple)

            return self.scanMasterReader.noError

    def uploadReads(self):
        self.errorOccured = False
        problematicRows = []

        # go through every row of the data
        for index, row in self.data.iterrows():

            result = self.scanMasterReader.readDataRow(row)
            # make sure there were no errors when parsing the data
            if result == self.scanMasterReader.error:
                problematicRows.append(index)
                self.errorOccured = True

            elif result == self.scanMasterReader.noError:
                # attempt to upload the data
                uploadResult = self.uploadRow()

                # make sure there were no errors when uploading the data
                if uploadResult == self.scanMasterReader.error:
                    self.errorOccured = True
                    problematicRows.append(index)

        if self.errorOccured:
            raise SomeDataNotAddedError(problematicRows, self.scanMasterReader.fileName)




