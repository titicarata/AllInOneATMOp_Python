import csv
import os
import sqlite3
from datetime import datetime
import pyperclip as pc


def AddLogInfoAndDB(detalii, categorie):
    user = " ".join(os.getlogin().replace('.', ' ').title().split(' '))
    datalansare = datetime.now()
    dataRulare = datetime.strftime(datalansare, "%d/%m/%Y %H:%M:%S")

    dataR = datetime.strptime(dataRulare, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\ATMOperations.db")
    cur = con.cursor()
    sql = "REPLACE INTO ATMOP (User, DataRulare, Detalii, Categorie, seconds) " + "VALUES('" + user.strip() + "','" + dataRulare + "','" + detalii + "','" + categorie + "', strftime('%s','" + dataR + "'))"
    cur.executescript(sql)
    con.close()


def citesteFisierCsvFaraHead(pathToCsvFile, openMode):
    result = []
    with open(pathToCsvFile, openMode) as inputfile:
        next(inputfile, None)       # ignora header
        for row in csv.reader(inputfile):
            result.append(row)
    return result


def copyFileToClipboard(path):
    fo = open(path, 'r').read()
    pc.copy(fo)


def copyStringToClipboard(path):
    fo = open(path, 'r').read()
    pc.copy(fo)


def pasteFromClipboard():
    return pc.paste()


def get_active_atms_last():
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\ATMDB.db")
    cur = con.cursor()
    res = cur.execute("SELECT Termid, Bna FROM CEB WHERE PlafonAprobat > 0 ORDER BY Termid")
    cebxls = res.fetchall()
    con.close()
    return cebxls


def isFileLocked(filePath):
    '''
    Checks to see if a file is locked. Performs two checks
        1. Checks if the file even exists
        2. Attempts to open the file for reading. This will determine if the file has a write lock.
            Write locks occur when the file is being edited or copied to, e.g. a file copy destination
    @param filePath:
    '''

    if not (os.path.exists(filePath)):
        return False

    try:
        with open(filePath, 'w') as f:
            pass
    except IOError as e:
        return True

    return False


if __name__ == "__main__":
    print("utilsTiti loaded")