


import zipfile
import csv
import os

import constants as C

def zip_count():
    all_files = 0

    for fname in C.FILE_LIST:
        with zipfile.ZipFile(fname, mode='r') as _zipfile:
            year = fname[5:-4]
            master_count = 0
            master_path = C.PARM_PATH + "{}_MASTER.csv".format(year)
            if os.path.exists(master_path):
                with open(master_path, 'r') as f_out:
                    wr = csv.reader(f_out, lineterminator='\n', delimiter=';')
                    next(wr, None)  # skip the headers
                    for line in wr:
                        master_count += 1

            file_count = len(set(_zipfile.namelist()))
            print("{} contains {}/{} files.".format(fname, file_count, master_count))
            all_files += file_count

    print("Total filecount: {}".format(all_files))


def describe(CONN):
    cursor = CONN.cursor()
    tablesToIgnore = ["sqlite_sequence"]
    totalTables = 0
    totalColumns = 0
    totalRows = 0
    totalCells = 0
    
    # Get List of Tables:      
    tableListQuery = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY Name"
    cursor.execute(tableListQuery)
    tables = map(lambda t: t[0], cursor.fetchall())
    
    for table in tables:
    
        if (table in tablesToIgnore):
            continue            
            
        columnsQuery = "PRAGMA table_info(%s)" % table
        cursor.execute(columnsQuery)
        numberOfColumns = len(cursor.fetchall())
        
        rowsQuery = "SELECT Count() FROM '%s'" % table
        cursor.execute(rowsQuery)
        numberOfRows = cursor.fetchone()[0]
        
        numberOfCells = numberOfColumns*numberOfRows
        
        print("%s\t%d\t%d\t%d" % (table, numberOfColumns, numberOfRows, numberOfCells))
        
        totalTables += 1
        totalColumns += numberOfColumns
        totalRows += numberOfRows
        totalCells += numberOfCells

    print( "" )
    print( "Number of Tables:\t%d" % totalTables )
    print( "Total Number of Columns:\t%d" % totalColumns )
    print( "Total Number of Rows:\t%d" % totalRows )
    print( "Total Number of Cells:\t%d" % totalCells )
