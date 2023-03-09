from datetime import datetime
import sqlite3


def updateAlimentare(termID, dataOraReplenishment):
    ymd = ""
    finalizedAt = ""
    finalizedAt = datetime.strptime(dataOraReplenishment, '%y%m%d %H%M%S').strftime('%y-%m-%d %H%M%S')
    ymd = datetime.strptime(dataOraReplenishment, '%y%m%d %H%M%S').strftime('%y%m%d')

    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\BrinksPrintec.db")
    cur = con.cursor()
    resultSet1 = cur.execute(
        "SELECT RequestedTime FROM Alimentari WHERE TerminalID = '" + termID + "' AND YMD = " + ymd)
    planificat = resultSet1.fetchone()
    sqlStr = "UPDATE Alimentari SET FinalizedAt = '" + finalizedAt + "', DiferenceMinutes =  (cast(strftime('%s','" + finalizedAt + "') AS INTEGER) - CAST(strftime('%s','" + planificat + "') as INTEGER))/60 WHERE TerminalID = '" + termID + "' and YMD = " + ymd
    cur.execute(sqlStr)
    con.commit()
    sqlR = "SELECT TerminalID, TerminalName, RequestedTime, CentruProcesare FROM Alimentari WHERE DiferenceMinutes = 99999 AND YMD = " + ymd
    resultSet2 = cur.execute(sqlR)
    remainingReplenishments = resultSet2.fetchall()
    con.close()
    if remainingReplenishments:
        return remainingReplenishments
    return None


def getInterventiiATM(terminalID, dataLastLich):
    result = []
    # print(dataLastLich)
    # print(type(dataLastLich))

    lastLich = str(dataLastLich)[0:4] + "-" + str(dataLastLich)[4:6] + "-" + str(dataLastLich)[6:] + " 00:00:00"
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\BrinksPrintec.db")
    cur = con.cursor()
    sql = "SELECT G4S_ID, TerminalNo, issueType, RequestDate, ProcessCenter, Description, CodSac, DetaliiSac FROM G4S WHERE TerminalNo = '" + terminalID + "' AND seconds > strftime(\"%s\", '" + lastLich + "')"
    rs = cur.execute(sql)
    result = rs.fetchall()
    con.close()
    if not result:
        return result
    return None
