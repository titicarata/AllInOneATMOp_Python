import sqlite3


def getLastErrorsATM(codATM, newDataLichCI):
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\ATMDaily.db")
    cur = con.cursor()
    sql = "SELECT datetime(Seconds, 'unixepoch'), CodClient FROM CashIn WHERE seconds>=strftime(\"%s\",'"+newDataLichCI+"') AND TerminalID = '"+codATM+"' ORDER BY Seconds"
    rs = cur.execute(sql)
    result = rs.fetchall()
    return result

