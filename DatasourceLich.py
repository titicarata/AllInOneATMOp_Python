import sqlite3


def getLastLichCICO(codATM, esteATMBNA):
    con = sqlite3.connect(r"Y:\Operatiuni\Acquiring\ATM\Databases\LichidariATM.db")
    cur = con.cursor()
    res1 = cur.execute("SELECT max(Datalich) FROM LICHDB WHERE CodATM = '" + codATM + "' AND LICHCO >0")
    dataLastLichCO = res1.fetchone()
    dataLastLichCI = dataLastLichCO
    if esteATMBNA:
        res2 = cur.execute("SELECT MAX(DATALICH) FROM LICHDB WHERE CODATM = '" + codATM + "' AND VOLCI > 0")
        dataLastLichCI = res2.fetchone()
    else:
        dataLastLichCI = dataLastLichCO
    result = [dataLastLichCO, dataLastLichCI]
    con.close()
    return result


def verificare(deScrisDB):
    codATM = deScrisDB[1]
    dataLich = deScrisDB[2]
    con = sqlite3.connect(r"Y:\Operatiuni\Acquiring\ATM\Databases\LichidariATM.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM LICHDB WHERE CODATM = '" + codATM + "' AND DATALICH = " + dataLich)
    verificat = res.fetchall()
    return verificat


def addLichidareDB(deScrisDBLich):
    qusercde = deScrisDBLich[0]
    qcodatm = deScrisDBLich[1]
    qdatalich = deScrisDBLich[2]
    qlichco = deScrisDBLich[3]
    qnrco = deScrisDBLich[4]
    qvolco = deScrisDBLich[5]
    qreplenish = deScrisDBLich[6]
    qvolci = deScrisDBLich[7]
    qnrci = deScrisDBLich[8]
    qvolrc100 = deScrisDBLich[9]
    qnrrc100 = deScrisDBLich[10]
    sql = "INSERT INTO LICHDB (USERCDE, CODATM, DATALICH, LICHCO, NRCO, VOLCO, REPLENISH, VOLCI, NRCI, VOLRC100, NRRC100) VALUES('" + qusercde + "','" + qcodatm + "'," + qdatalich + "," + qlichco + "," + qnrco + "," + qvolco + "," + qreplenish + "," + qvolci + "," + qnrci + "," + qvolrc100 + "," + qnrrc100 + ")"
    conn = sqlite3.connect(r"Y:\Operatiuni\Acquiring\ATM\Databases\LichidariATM.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        if conn:
            conn.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    return cursor.rowcount


def replLichidareDB(deScrisDBLich):
    usercde = deScrisDBLich[0]
    codatm = deScrisDBLich[1]
    datalich = deScrisDBLich[2]
    lichco = deScrisDBLich[3]
    nrco = deScrisDBLich[4]
    volco = deScrisDBLich[5]
    replenish = deScrisDBLich[6]
    volci = deScrisDBLich[7]
    nrci = deScrisDBLich[8]
    volrc100 = deScrisDBLich[9]
    nrrc100 = deScrisDBLich[10]

    sql = "UPDATE LICHDB SET USERCDE = '" + usercde + "', LICHCO = " + lichco + ", NRCO = " + nrco + ", VOLCO = " + volco + ", REPLENISH = " + replenish + ", VOLCI = " + volci + ", NRCI = " + nrci + ", VOLRC100 = " + volrc100 + ", NRRC100 = " + nrrc100 + " WHERE CODATM ='" + codatm + "' AND DATALICH = " + datalich
    conn = sqlite3.connect(r"Y:\Operatiuni\Acquiring\ATM\Databases\LichidariATM.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to replace data into sqlite table", error)
    finally:
        if conn:
            conn.close()
    return cursor.rowcount
