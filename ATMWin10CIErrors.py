import sqlite3
import os
import datetime
import glob
from datetime import datetime
import re


def win10_ci_errors():
    """
    Titi said: This module is extracting SS type ATM's from ATMDB.db database and for every ATM
    detects the latest electronic journal file in z:/Ejtemp folder.\n
    Iterates through the entire journal and searches for known errors
    and writes the errors in a txt file
    :return: The result file name (will be written in All In One app)
    """
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    strDataSpec = now.strftime("%d/%m/%Y")

    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\ATMDb.db")
    cur = con.cursor()
    res = cur.execute(
        "SELECT substr(Termid,4,5) FROM inventar WHERE ModelATM like 'SS%' AND Location = 'In functiune' AND VersiuneWindows = 'Win 10'")
    listaATMSS = res.fetchall()
    con.close()

    rezultat = []
    files_path = 'z:/Ejtemp'
    dir_list = os.listdir(files_path)

    for filename in dir_list:
        for index, atm_code in enumerate(listaATMSS):
            if atm_code[0] in filename:
                rezultat.append(filename)
                break
    # in rezultat am jurnalele pentru ATM Win 10

    # trebuie sa identific, pentru fiecare dintre acestea, care este ultimul scris
    fisier_rezultat = 'W:/Operatiuni/Acquiring/ATM/TRANSFER_IN_INT/RapoarteATMOperations/DailyReports/JavaResults/Win10CashInErrorsPy.txt'
    if os.path.exists(fisier_rezultat):
        os.remove(fisier_rezultat)

    file_object = open(fisier_rezultat, 'a')
    file_object.write('Execution start : ' + date_time + "\n\n")

    ziCorecta = False
    device = ""
    device_name = ""

    for termid in listaATMSS:
        prima = True
        list_of_files = glob.glob('z:/ejtemp/EJ' + termid[0] + '*.log')
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getmtime)

            with open(latest_file, 'r') as file_local:
                journal = file_local.readlines()

            CashInRecovery = ""
            # dataOraTrx = ""
            startTranzactie = ""
            # codClient = ""
            # lastCIMOperation = ""
            # jurnalSize = len(journal)
            lastTime = ""

            jrnlSize = len(journal)
            for k in range(0, jrnlSize):
                line_searched = journal[k]
                x = re.search(r"\d{2}:\d{2}:\d{2}", line_searched)
                m = re.search(r"M-\d{2}", line_searched)

                if x:
                    lastTime = x.group(0)
                    # print(lastTime)

                if "CIM-" in line_searched and ziCorecta:
                    lastCIMOperation = line_searched.strip()

                if "CLIENT CODE:" in line_searched or "COD CLIENT  " in line_searched:
                    lista = line_searched.split(':')
                    codClient = lista[1].strip()

                if "CASHIN RECOVERY STARTED" in line_searched:
                    if prima:
                        file_object.write("\nATM" + termid + " " + line_searched)
                        prima = False
                    else:
                        file_object.write("         " + line_searched)

                    for p in range(k + 1, jrnlSize):
                        panaLa = journal[p]
                        if "REJECTS:" in panaLa or "CASHIN RECOVERY FAILED" in panaLa or "CASHIN RECOVERY OK" in panaLa:
                            file_object.write("         " + panaLa + "\n")
                            k = p
                            prima = False
                            break
                        else:
                            if len(panaLa) > 2:
                                file_object.write("         " + panaLa)
                                prima = False

                if "TRANSACTION" in line_searched:
                    dataOraTrx = ""
                    CashInRecovery = ""
                    codClient = ""

                if "TRANSACTION START" in line_searched:
                    startTranzactie = journal[k - 1].strip()[-17:-1].replace('*', ' ')
                    # print(journal[k-1] + "\t\t" + startTranzactie)

                if line_searched.startswith("DATA / ORA  :" + strDataSpec):
                    dataOraTrx = line_searched.replace("DATA / ORA  :", "").strip()
                    ziCorecta = True

                if "CASHIN RECOVERY STARTED" in line_searched and ziCorecta:
                    CashInRecovery = line_searched.strip()

                if "CASHIN RECOVERY" in line_searched and ziCorecta and not CashInRecovery and "STARTED" not in line_searched:
                    if prima:
                        file_object.write("ATM" + termid + " " + CashInRecovery)
                        file_object.write("ATM" + termid + " " + line_searched)
                        prima = False
                    else:
                        file_object.write("        " + CashInRecovery)
                        file_object.write("        " + line_searched)

                    CashInRecovery = ""
                    prima = False

                if m:
                    mStatus = m.group()
                    if mStatus != "M-00":
                        if mStatus != "M-81":
                            if "w" in line_searched:
                                device = "NACC-01-GBRU"
                                device_name = "GBRU "
                            elif "E" in line_searched:
                                device = "CASH-01-UsbMediaDispenser"
                                device_name = "Dispenser SS "
                            elif "D" in line_searched:
                                device = "MCRW-01-USBMotorised"
                                device_name = "Card reader "
                            elif "G" in line_searched:
                                device = "RPNT-01-UsbThermal"
                                device_name = "Printer "
                            else:
                                if "y" in line_searched:
                                    device = "MCRW-01-USBContactlessReader"
                                    device_name = "Contactless CardReader "

                            con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\BrinksPrintec.db")
                            cur = con.cursor()
                            res = cur.execute(
                                "SELECT DESCRIPTION FROM MSTATUS WHERE DEVICENAME ='" + device + "' AND MSTATUSCODE = '" + mStatus[2:] + "'")
                            response = res.fetchone()
                            con.close()

                            if response:
                                if prima:
                                    deScris = "ATM" + termid[0] + " ***** " + device_name + " - " + response[
                                        0] + " (" + mStatus + ")" + " - " + lastTime + "\n"
                                    file_object.write(deScris)
                                    prima = False
                                else:
                                    deScris = "         ***** " + device_name + " - " + response[0] + " (" + mStatus + ")" + " - " + lastTime + "\n"
                                    file_object.write(deScris)
                        else:
                            if "CARD INITIALISE ATTEMPT = 3" in journal[k + 1]:
                                deScris = "ATM" + termid[0] + " ***** " + "Eroare chip reader " + startTranzactie.replace('*', ' ') + " (M-81)\n"
                                file_object.write(deScris)

                ziCorecta = False

        else:
            file_object.write("Nu exista nici macar un journal pt ATM" + termid[0] + " astazi\n")

    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    file_object.write("\nExecution end :" + date_time)
    file_object.close()
    os.startfile(fisier_rezultat)

    return fisier_rezultat


if __name__ == "__main__":
    win10_ci_errors()
