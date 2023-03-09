from datetime import datetime
import sqlite3
import os
import xlsxwriter
from tkinter import messagebox

from utilsTiti import AddLogInfoAndDB, get_active_atms_last, isFileLocked


def get_last_CO(TerminalID):
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\LichidariATM.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT max(Datalich) FROM LICHDB WHERE CODATM ='{TerminalID}' AND LICHCO > 0")
    last_date = res.fetchone()
    con.close()
    return str(last_date[0])


def get_last_CI(TerminalID):
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\LichidariATM.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT max(Datalich) FROM LICHDB WHERE CODATM ='{TerminalID}' AND VOLCI > 0")
    last_date = res.fetchone()
    con.close()
    return str(last_date[0])


def change_to_dmy(lastCO):
    return f"{lastCO[6:]}/{lastCO[4:6]}/{lastCO[:4]}"


def detect_last_replenishment(user_option):
    exportXlsx = []
    match user_option:
        case 'All':
            AddLogInfoAndDB("Rulare Detect last replenishment", "Detect last replenishment")
            cebxls = get_active_atms_last()
            captabel = ["Terminal ID", "Lichidare Cash Out", "Lichidare Cash In"]
            exportXlsx.append(captabel)
            for item in cebxls:
                lastCI = ''
                lastCO = get_last_CO(item[0])

                if lastCO == 'None':
                    lastCO = ''

                if item[1] == 'true':
                    lastCI = get_last_CI(item[0])
                    if lastCI == 'None':
                        lastCI = ''

                if len(lastCO) == 8:
                    lastCO = change_to_dmy(lastCO)
                if len(lastCI) == 8:
                    lastCI = change_to_dmy(lastCI)

                inner = [item[0], lastCO, lastCI]
                exportXlsx.append(inner)

    output_file = "d:/LongATMReconciliation/UltimaAlimentareATM.xlsx"

    if isFileLocked(output_file):
        message = f"Fisierul {output_file} \neste deja deschis. Inchide-l inainte sa apesi OK"
        messagebox.showinfo("Eroare", message)

    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    for terminalID, lastcashout, lastcashin in exportXlsx:
        worksheet.write(row, col, terminalID)
        worksheet.write(row, col + 1, lastcashout)
        worksheet.write(row, col + 2, lastcashin)
        row += 1

    worksheet.set_column(0, 2, 18)
    workbook.close()
    os.startfile(output_file)


if __name__ == "__main__":
    detect_last_replenishment('All')
