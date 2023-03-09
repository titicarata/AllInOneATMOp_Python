import sqlite3

def getSubtaskClient(clientEroare, codATM, dataLastLichCI):
    conn = sqlite3.connect(r"Y:\Operatiuni\Acquiring\ATM\Databases\CapturedCards.db")
    cr = conn.cursor()
    sql = "SELECT IssueNo, CustomerNo, CustomerName, Explanation FROM Subtasks WHERE DataEroare >= "+dataLastLichCI+" AND ATM = '"+codATM+"' AND CustomerNo = '"+clientEroare+"'"
    rs = cr.execute(sql)
    result = rs.fetchall()
    return result


