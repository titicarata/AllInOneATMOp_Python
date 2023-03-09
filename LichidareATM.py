import datetime
import os
import sqlite3
import csv
import PySimpleGUI as sg
from tkinter import messagebox
import DatasourceATMDaily
import DatasourceBksPrintec
import DatasourceCapturedCards
import DatasourceLich
from datetime import datetime
import DatasourceUsers
import utilsTiti


sg.theme('Default1')


def convertToAcc(destinatie):
    prelucrat = ""
    if "CONTURI  CURENT" in destinatie:
        prelucrat = "Cont curent"
    elif "MASTERCARD DEBI" in destinatie:
        prelucrat = "MCDR"
    elif "MASTERCARD GOLD" in destinatie:
        prelucrat = "MCGR"
    elif "MASTERCARD OPTI" in destinatie:
        prelucrat = "MCOS"
    elif "MASTERCARD STAN" in destinatie:
        prelucrat = "MCSR"
    elif "VISA CLASIC DEB" in destinatie:
        prelucrat = "VCDR"
    elif "VISA CLASSIC" in destinatie:
        prelucrat = "VCCR"
    elif "VISA ELECTRON" in destinatie:
        prelucrat = "VEDR"
    elif "VISA GOLD" in destinatie:
        prelucrat = "VCGR"
    elif destinatie == "":
        prelucrat = "Unknown destination"
    else:
        prelucrat = destinatie[:6] + "******" + destinatie[13:]
    return prelucrat


def calculeazaCI(fisiercsv, startPoz, endPoz):
    erori = []
    depus = 0  # total suma depusa Cash In
    nrCashIn = 0  # numar depuneri
    sysFailureCI = 0  # System failure cashin
    nrSysFailureCI = 0  #
    rc108CI = 0  # Last transaction not completed cashin
    nrrc108CI = 0  #
    rc205 = 0  # Please use cash in
    nrrc205 = 0  #
    bnaTimeout = 0  # BNA Timeout si BNA refund Timeout
    nrbnaTimeout = 0  #
    bnaSendError = 0  # BNA send error cu suma diferita de 0
    nrbnaSendError = 0  #
    provisionReversal = 0  #
    nrProvisionReversal = 0  #
    rc307 = 0  # Please use cash in
    nrrc307 = 0  #
    for i in range(startPoz, endPoz):
        hTrans = fisiercsv[i][7]
        hAmount = fisiercsv[i][8]
        hCompleted = fisiercsv[i][10]
        hCodCl = fisiercsv[i][13]
        hRCode = fisiercsv[i][15]
        hCancCode = '#' if fisiercsv[i][17].strip() == "" else fisiercsv[i][17].strip()
        if "CASH IN" in hTrans or "CASH-IN" in hTrans:
            numarcard = fisiercsv[i][12]
            cardBIN = numarcard[0:6]
            mesaj = ""
            # print(hTrans, hAmount, hCompleted, hCodCl, hRCode, hCancCode)
            if cardBIN == "987654":
                numarcard = "Cardless"

            if hCompleted != "0" and hCodCl != "" and int(hCodCl) > 0 and int(hCompleted) > 0 and hRCode == "0":
                depus += int(hCompleted)
                nrCashIn += 1

            if hCodCl != "" and int(hCodCl) > 0 and hAmount != "0" and hCompleted == "0" and hRCode == "275":
                bnaSendError += int(hAmount)
                nrbnaSendError += 1
                # print("Eroare 275")
                mesaj = "   - BNA SEND ERROR cu suma >0 " + hTrans + ", " + ", " + numarcard + ", " + modiData(
                    fisiercsv[i][1]) + ", " + fisiercsv[i][2].zfill(4) + ", " + hAmount + " RON, Cod Client " + \
                        fisiercsv[i][13]
                erori.append(mesaj)

            if hCodCl != "" and int(hCodCl) > 0 and int(hAmount) > 0 and (
                    hRCode == "278" or hRCode == "280" or hRCode == "999"):
                bnaTimeout += int(hAmount)
                nrbnaTimeout += 1

                if hCodCl != "" and int(hCodCl) > 0 and int(hAmount) > 0 and (
                        hRCode == "278" or hRCode == "280" or hRCode == "999"):
                    bnaTimeout += int(hAmount)
                    nrbnaTimeout += 1
                    mesaj = "   - " + fisiercsv[i][16] + " incercare de depunere pe " + convertToAcc(
                        fisiercsv[i][27]) + ", " + numarcard + ", " + hTrans + ", " + modiData(fisiercsv[i][1]) + ", " + \
                            fisiercsv[i][2].zfill(6) + ", " + hAmount + " RON, Cod Client " + hCodCl
                    erori.append(mesaj)

                if hCodCl != "" and int(hCodCl) > 0 and int(hAmount) > 0 and hRCode == "96":
                    sysFailureCI += int(hAmount)
                    nrSysFailureCI += 1
                    mesaj = "   - System Failure " + hTrans + ", incercare de depunere pe " + \
                            convertToAcc(fisiercsv[i][27]) + ", " + numarcard + ", " + modiData(fisiercsv[i][1]) + \
                            ", " + fisiercsv[i][2].zfill(6) + ", " + hAmount + " RON"
                    erori.append(mesaj)

                if hCodCl != "" and int(hCodCl) > 0 and int(hAmount) > 0 and hCancCode == "108":
                    rc108CI += int(hAmount)
                    nrrc108CI += 1
                    mesaj = "   - Last Transaction not Completed " + hTrans + ", incercare de depunere pe " + \
                            convertToAcc(fisiercsv[i][27]) + ", " + numarcard + ", " + modiData(fisiercsv[i][1]) + \
                            ", " + fisiercsv[i][2].zfill(6) + ", " + hAmount + " RON, Completed amount " + hCompleted + \
                            ", Cod Auth:" + fisiercsv[i][28].replace('-', '').replace(' ', '')
                    erori.append(mesaj)

                if hCodCl != "" and int(hCodCl) > 0 and int(hAmount) > 0 and hCancCode == "400":
                    provisionReversal += int(hAmount)
                    nrProvisionReversal += 1
                    mesaj = "   - Provision Reversal " + hTrans + ", incercare de depunere pe " + \
                            convertToAcc(fisiercsv[i][27]) + ", " + numarcard + ", " + modiData(fisiercsv[i][1]) + \
                            ", " + fisiercsv[i][2].zfill(6) + ", " + hAmount + " RON Cod Auth:" + \
                            fisiercsv[i][28].replace('-', '').replace(' ', '')
                    erori.append(mesaj)

                if hCodCl != "" and int(hCodCl) > 0 and int(hAmount) > 0 and hRCode == "205":
                    rc205 += int(hAmount)
                    nrrc205 += 1
                    mesaj = "   - Please use Cash In (?!?!?!) " + hTrans + ", " + numarcard + ", " + \
                            modiData(fisiercsv[i][1]) + ", " + fisiercsv[i][2].zfill(6) + ", " + hAmount + " RON"
                    erori.append(mesaj)

                if hCodCl != "" and int(hCodCl) > 0 and int(hAmount) > 0 and hRCode == "307":
                    rc307 += int(hAmount)
                    nrrc307 += 1
                    mesaj = "   - Daily Limit Overflow " + hTrans + ", incercare de depunere pe " + \
                            convertToAcc(fisiercsv[i][27]) + ", " + numarcard + ", " + \
                            modiData(fisiercsv[i][1]) + ", " + fisiercsv[i][2].zfill(6) + ", " + hAmount + " RON"
                    erori.append(mesaj)
        if "CASH WITH" in hTrans or "CASH ADV" in hTrans:
            pass

    rezultat = (depus, nrCashIn, bnaSendError, nrbnaSendError, bnaTimeout, nrbnaTimeout, sysFailureCI, nrSysFailureCI,
                rc108CI, nrrc108CI, rc205, nrrc205, provisionReversal, nrProvisionReversal, rc307, nrrc307)
    erori_tup = tuple(erori)
    result = []
    result.append(rezultat)
    result.append(erori_tup)
    return result


def calculeazaCO(fisiercsv, startPoz, endPoz):
    rezultat = ()
    eroriCO = []
    retras = 0
    ATMCapture = 0
    nrCashOut = 0
    nrCapt = 0
    sysFailureCO = 0
    nrSysFailureCO = 0
    amountCompleted = 0
    nramountCompleted = 0
    for i in range(startPoz, endPoz):
        hTrans = fisiercsv[i][7]
        hAmount = fisiercsv[i][8]
        hCompleted = fisiercsv[i][10]
        hRCode = fisiercsv[i][15].strip()
        hCancCode = fisiercsv[i][17].strip()

        if "CASH ADV" in hTrans or "CASH W" in hTrans:
            if int(hCompleted) > 0 and int(hAmount) > 0:
                retras += int(hCompleted)
                nrCashOut += 1
                if "100" in hCancCode:
                    ATMCapture += int(hCompleted)
                    nrCapt += 1
                    mesaj = "   - ATM Captured Money : " + modiData(fisiercsv[i][1]) + ", " \
                            + fisiercsv[i][2].zfill(6) + ", " + fisiercsv[i][12] + ", " \
                            + fisiercsv[i][8] + " RON, Cod Auth:" + fisiercsv[i][28].replace('-', '').replace(' ', '')
                    eroriCO.append(mesaj)

            # pentru tranzactii la care amount e diferit de completed
            if 0 < int(hCompleted) != int(hAmount) > 0:
                amountCompleted += int(hCompleted)
                nramountCompleted += 1
                numarcard = fisiercsv[i][12]
                # cardBIN = numarcard[:6]
                mesaj = "   - Completed diferit de Amount " + fisiercsv[i][7] + ", " + numarcard + ", " + \
                        modiData(fisiercsv[i][1]) + ", " + fisiercsv[i][2].zfill(6) + ", " + fisiercsv[i][8] + \
                        " RON Cod Auth:" + fisiercsv[i][28].replace('-', '').replace(' ', '')
                eroriCO.append(mesaj)

            if int(hAmount) > 0 and "96" in hRCode:
                sysFailureCO += int(hAmount)
                nrSysFailureCO += 1
                mesaj = "   - System Failure " + fisiercsv[i][7] + ", " + modiData(fisiercsv[i][1]) + ", " + \
                        fisiercsv[i][2].zfill(6) + ", " + fisiercsv[i][12] + ", " + fisiercsv[i][8] + " RON"
                eroriCO.append(mesaj)

    rezultat = (retras, nrCashOut, ATMCapture, nrCapt, amountCompleted, nramountCompleted, sysFailureCO, nrSysFailureCO)
    erori_tup = tuple(eroriCO)
    resultCO = []
    resultCO.append(rezultat)
    resultCO.append(erori_tup)
    return resultCO


def modiData(dataBS):
    return dataBS[6:] + "/" + dataBS[4:6] + "/" + dataBS[:4]


def mascareCard(nrCard):
    noSpaces = nrCard.replace(' ', '')
    return noSpaces[0:6] + '******' + noSpaces[-4:]

def Lichidare_ATM():
    # preia ciNou
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\ATMDaily.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM CINou WHERE date(Data) > date('now', '-75 day')")
    ciNou = res.fetchall()
    con.close()

    startDate = datetime.now()
    dataLansare = startDate.strftime("%d/%m/%Y %H:%M:%S")

    # citesc atmlich.csv
    fisiercsv = []
    ATMuri = []
    zileReplenishment = []
    with open('d:/JavaUtils/atmlich.csv', mode='r') as inputfile:
        next(inputfile, None)  # ignora header
        for row in csv.reader(inputfile):
            fisiercsv.append(row)
            if not row[3] in ATMuri:
                ATMuri.append(row[3])

    myText = ""
    if len(ATMuri) != 1:
        myText = "Continutul D:\\JavaUtils\\atmlich.csv este incorect!\nPutina atentie, da?"
        messagebox.showinfo(myText, "Eroare")

    else:
        codATM = ATMuri[0]
        gasitZiua = False
        #####################################
        ###   aici incepe marea prelucrare
        #####################################
        # creeaza lista zileReplenishment
        for index, inregistrare in enumerate(fisiercsv):
            inregistrare[2] = inregistrare[2].zfill(6)
            if inregistrare[7] == "REPLENISHMENT":
                if len(zileReplenishment) > 0:
                    for j in range(0, len(zileReplenishment)):
                        if zileReplenishment[j][1] == inregistrare[1]:
                            gasitZiua = True

                if not gasitZiua:
                    innerZiua = []
                    innerZiua.append(index)
                    innerZiua.append(int(inregistrare[1]))
                    zileReplenishment.append(innerZiua)

        # print(zileReplenishment)
        # citeste informatiile despre ATM din BD
        con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\ATMDB.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM CEB WHERE TERMID = '" + codATM + "'")
        nomATM = res.fetchall()
        con.close()

        isBrinks = True if "G4S" in nomATM[0][9] else False
        esteBranch = True if "true" in nomATM[0][2] else False
        esteATMBNA = True if "true" in nomATM[0][8] else False
        denumireATM = nomATM[0][1]
        plafonMaximCO = int(nomATM[0][20])
        termName = nomATM[0][1]

        dataSfarsit = fisiercsv[0][1]
        oraSfarsit = fisiercsv[0][2]
        dataInceput = fisiercsv[len(fisiercsv) - 1][1]
        oraInceput = fisiercsv[len(fisiercsv) - 1][2]

        # daca este ATM Brinks
        # caut prima tranzactie cu REPLENISHMENT pt a gasi ora la care s-a facut lichidarea -> dataOraReplenishment
        #
        if isBrinks:
            dataOraReplenishment = ""
            remainingReplenishments = []
            for inregistrare in fisiercsv:
                if inregistrare[7] == "REPLENISHMENT":
                    # actualizeaza BD cu dataOra efectuarii lichidarii (legat de Plan alimentari)
                    dataOraReplenishment = inregistrare[1] + " " + inregistrare[2]
                    remainingReplenishments = DatasourceBksPrintec.updateAlimentare(codATM, dataOraReplenishment)
                    break
            # daca mai sunt alimentari Brinks in asteptare, le afiseaza
            if remainingReplenishments is not None:
                myText = "Alimentari in asteptare : \n"
                for restant in remainingReplenishments:
                    informatie = restant[0] + ' - ' + restant[1] + ', ' + restant[3] + ', planificata la ' + restant[
                        2] + '\n'
                    myText += informatie
                    messagebox.showinfo(myText, "Ca sa stii ...")

        lastAlim = 0  # suma alimentata
        alimentat = 0  # alimentarea "de data trecuta"
        retras = 0  # total suma retrasa Cash Out
        depus = 0  # total suma depusa Cash In
        ATMCapture = 0  # total suma ATMCapture
        nrCashOut = 0  # numar retrageri
        nrCashIn = 0  # numar depuneri
        nrCapt = 0  # numar ATM Capture money
        sysFailureCO = 0  # System failure Cash Out
        nrSysFailureCO = 0
        sysFailureCI = 0  # System failure cashin
        nrSysFailureCI = 0
        rc108CI = 0  # Last transaction not completed cashin
        nrrc108CI = 0
        rc205 = 0  # Please use cash in
        nrrc205 = 0
        rc307 = 0  # Daily limit overflow Cash In
        nrrc307 = 0
        bnaTimeout = 0  # BNA Timeout si BNA refund Timeout
        nrbnaTimeout = 0
        bnaSendError = 0  # BNA send error cu suma diferita de 0
        nrbnaSendError = 0
        provisionReversal = 0  # RC 400
        nrProvisionReversal = 0
        amountCompleted = 0  # tranzactii cu amount si completed pozitive dar diferite
        nramountCompleted = 0

        doarCashIn = False
        faraRealimentare = False
        dataLichidareDB = fisiercsv[0][1]
        if "REPLENISHMENT" in fisiercsv[0][7] and "CASSETTE STATUS REPORT" in fisiercsv[1][7] \
                and "CASSETTE STATUS REPORT" in fisiercsv[2][7]:
            faraRealimentare = True

        startCalculCupiura = 0
        endCalculCupiura = 0
        result = True  # True daca esteATMBNA si se face doar Cash In; False daca se face cu totul; None pt Abort

        calculCI = ()
        calculCO = ()

        if esteATMBNA:
            result = messagebox.askyesnocancel("Verificare lichidare " + codATM + " " + termName, "Doar lichidare Cash In?")
            if result is True:
                doarCashIn = True
            elif result is False:
                doarCashIn = False
            else:  # None
                return "Abort check liquidation"

        dataLichidareTxt = datetime.strptime(fisiercsv[0][1], '%Y%m%d').strftime('%d/%m/%Y')

        if len(zileReplenishment) == 1:  # cel mai probabil e dezinstalare
            # print("Cel mai probabil este dezinstalare ATM")
            endCalculCupiura = int(zileReplenishment[0][0])
            calculCO = calculeazaCO(fisiercsv, 0, endCalculCupiura)
            if esteATMBNA:
                calculCI = calculeazaCI(fisiercsv, 0, endCalculCupiura)
        elif len(zileReplenishment) == 2 and faraRealimentare:
            # print("Cel mai probabil este golire temporara ATM")
            endCalculCupiura = int(zileReplenishment[1][0])
            calculCO = calculeazaCO(fisiercsv, 2, endCalculCupiura)
            if esteATMBNA:
                calculCI = calculeazaCI(fisiercsv, 2, endCalculCupiura)
        elif len(zileReplenishment) == 2:
            # print("Cel mai probabil este realimentare normala ATM")
            calculCO = calculeazaCO(fisiercsv, int(zileReplenishment[0][0]), int(zileReplenishment[1][0]))
            startCalculCupiura = int(zileReplenishment[0][0])
            endCalculCupiura = int(zileReplenishment[1][0])
            if esteATMBNA:
                calculCI = calculeazaCI(fisiercsv, startCalculCupiura, endCalculCupiura)
        else:
            # print("Cel mai probabil este realimentare normala la un ATM cu una sau mai multe goliri Cash in intermediare")
            cateLichSunt = len(zileReplenishment)
            startCalculCupiura = int(zileReplenishment[0][0])
            endCalculCupiura = int(zileReplenishment[cateLichSunt - 1][0])
            calculCO = calculeazaCO(fisiercsv, startCalculCupiura, endCalculCupiura)
            if esteATMBNA:
                calculCI = calculeazaCI(fisiercsv, startCalculCupiura, int(zileReplenishment[1][0]))

        numeATM = fisiercsv[1][4]
        doarBNA = False
        if result:
            doarBNA = True

        rezultatCO = calculCO[0]
        retras = rezultatCO[0]
        nrCashOut = rezultatCO[1]
        ATMCapture = rezultatCO[2]
        nrCapt = rezultatCO[3]
        amountCompleted = rezultatCO[4]
        nramountCompleted = rezultatCO[5]
        sysFailureCO = rezultatCO[6]
        nrSysFailureCO = rezultatCO[7]
        if esteATMBNA and doarCashIn:
            retras = 0
            nrCashOut = 0
            ATMCapture = 0
            nrCapt = 0
            amountCompleted = 0
            nramountCompleted = 0
            sysFailureCO = 0
            nrSysFailureCO = 0

        if esteATMBNA:
            rezultatCI = calculCI[0]
            depus = rezultatCI[0]
            nrCashIn = rezultatCI[1]
            bnaSendError = rezultatCI[2]
            nrbnaSendError = rezultatCI[3]
            bnaTimeout = rezultatCI[4]
            nrbnaTimeout = rezultatCI[5]
            sysFailureCI = rezultatCI[6]
            nrSysFailureCI = rezultatCI[7]
            rc108CI = rezultatCI[8]
            nrrc108CI = rezultatCI[9]
            rc205 = rezultatCI[10]
            nrrc205 = rezultatCI[11]
            provisionReversal = rezultatCI[12]
            nrProvisionReversal = rezultatCI[13]
            rc307 = rezultatCI[14]
            nrrc307 = rezultatCI[15]
            depus += rc108CI
            nrCashIn += nrrc108CI

            # - @inregATMPRO :de sus in jos caut ADD MONEY TO CASSETTE 1 (alimentare
            # valabila si daca nu a dat raport la final)

        valRaportCI = 0
        primaInreg = 0
        if len(zileReplenishment) > 1:
            for i in range(0, len(fisiercsv)):
                tranzactie = fisiercsv[i][7].strip()
                amountQ = fisiercsv[i][8]
                if "CASHIN CASSETTE STATUS REPORT" in tranzactie:
                    valRaportCI = int(fisiercsv[i][8])
                if valRaportCI == 0 and "CASHOUT CASSETTE STATUS REPORT" in tranzactie and int(
                        amountQ) > 0 and "ADD MONEY" in fisiercsv[i + 1][7].strip():
                    primaInreg = i
                    lastAlim = int(amountQ)
                    break
        if len(zileReplenishment) == 1 or faraRealimentare:
            primaInreg = 0
            lastAlim = 0

            # - @inregATMPRO :gasesc prima inreg la care nr card nu incepe cu 999111
            # (devine primaInreg)
        for j in range(primaInreg, len(fisiercsv)):
            if "999111" not in fisiercsv[j][12]:
                primaInreg = j
                break

                #        @inregATMPRO :de jos in sus caut REPLENISHMENT, apoi in sus, cat timp cardul incepe cu 999111,
                #    	caut CASHOUT CASSETTE STATUS REPORT si preiau valoarea daca este > 0 sau ADD MONEY cu valori pozitive

        # add a flag variable
        break_out_flag = False
        for i in range(len(fisiercsv) - 1, 0, -1):
            if "REPLENISHMENT" in fisiercsv[i][7]:
                ultimaInreg = i  # deocamdata e ultima inregistrare care conteaza
                # print("ultimainreg " + str(ultimaInreg))
                # daca, in sus, urmeaza ADD MONEY, adun ca sa aflu alimentarea anterioara
                for jj in range(ultimaInreg, 0, -1):
                    if "999111" not in fisiercsv[jj][12]:
                        ultimaInreg = jj
                        # print("ultimainreg " + str(ultimaInreg))
                        break_out_flag = True
                    else:
                        if "ADD MONEY" in fisiercsv[jj][7]:
                            alimentat = int(fisiercsv[jj][8]) + int(fisiercsv[jj - 1][8]) + int(
                                fisiercsv[jj - 2][8]) + int(fisiercsv[jj - 3][8])
                            # print("Calcul alimentat = " + str(alimentat))
                            break_out_flag = True

                    if break_out_flag:
                        break
            if break_out_flag:
                break

        kData = ""
        kOra = ""
        incepeCashIn = 0
        if len(zileReplenishment) == 1:
            incepeCashIn = int(zileReplenishment[0][0])
        else:
            incepeCashIn = int(zileReplenishment[1][0])

        ciATM = []
        dataEndCIN = str(zileReplenishment[0][1])
        dataEndCashIn = datetime.strptime(dataEndCIN, "%Y%m%d")
        dataStartCIN = str(fisiercsv[incepeCashIn][1])
        dataStartCashIn = datetime.strptime(dataStartCIN, "%Y%m%d")
        for z in range(len(ciNou), 0):
            innerCINOU = ciNou[z]
            kData = innerCINOU[2]
            kOra = innerCINOU[3]
            qATM = innerCINOU[0].strip()
            dataCINOU = datetime.strptime(kData, "%Y-%m-%d")
            if qATM == codATM:
                if dataStartCashIn <= dataCINOU <= dataEndCashIn:
                    ciATM.append(innerCINOU)

        # print("alimentat : {}, retras : {}".format(alimentat, retras))

        deLichidat = alimentat - retras

        con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\LichidariATM.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM LICHDB WHERE CODATM ='" + codATM + "' AND DATALICH =" + dataLichidareDB)
        fisierPreluat = res.fetchall()
        # print(fisierPreluat)
        cur.close()
        con.close()

        wDetalii = ''
        numeMartor = "d:\\JavaResults\\Backup\\Lichidare " + codATM + " " + dataLichidareTxt.replace("/", ".") + ".txt"
        if doarCashIn:
            numeMartor = f"d:/JavaResults/Backup/Lichidare Cash In {codATM} " + dataLichidareTxt.replace("/",".") + ".txt"
            wDetalii = f"Lichidare Cash In {codATM}"
        if not esteATMBNA or (esteATMBNA and not doarCashIn):
            numeMartor = "d:\\JavaResults\\Backup\\Lichidare " + codATM + " " + dataLichidareTxt.replace("/", ".") + ".txt"
            wDetalii = f"Lichidare {codATM}"


        fisMartor = open(numeMartor, 'w')

        deScrisDB = []
        identic = False
        deAfisat = ""
        for y in range(0, len(fisierPreluat)):
            inner = fisierPreluat[y]

            wUser1 = inner[0]
            wCodATM = inner[1].strip()
            wDataLichidare = inner[2]

            wLichCO = 0 if inner[3] == 0 else inner[3]
            wNrCO = 0 if inner[4] == 0 else inner[4]
            wVolCO = 0 if inner[5] == "" else inner[5]
            wAlim = 0 if inner[6] == "" else inner[6]
            wSumaCI = 0 if inner[7] == "" else inner[7]
            wNrCI = 0 if inner[8] == "" else inner[8]
            if wCodATM == codATM and dataLichidareTxt == wDataLichidare:
                if deAfisat == "":
                    deAfisat = "Mai exista cel putin o lichidare pentru " + wCodATM + " " + wDataLichidare + " : \n"
                else:
                    deAfisat = "\n" + "#######################" + "\n"
                with open(numeMartor, 'a') as f:
                    fisMartor.write(deAfisat)
                    fisMartor.write("  User          " + wUser1 + "\n")
                    fisMartor.write("  Lichidare CO  " + '{:>8,}'.format(wLichCO) + "\n")
                    fisMartor.write("  Nr retrageri  " + '{:>8,}'.format(wNrCO) + "\n")
                    fisMartor.write("  Vol retrageri " + '{:>8,}'.format(wVolCO) + "\n")
                    fisMartor.write("  Alimentare    " + '{:>8,}'.format(wAlim) + "\n")
                    fisMartor.write("  Vol depuneri  " + '{:>8,}'.format(wSumaCI) + "\n")
                    fisMartor.write("  Nr depuneri   " + '{:>8,}'.format(wNrCI) + "\n")

            if result:  # daca e ATM cash in dar nu se face decat golire cash in
                lastAlim = 0
                deLichidat = 0

            if wLichCO == str(deLichidat) and wNrCO == str(nrCashOut) and wVolCO == str(retras) and \
                    wAlim == str(lastAlim) and wSumaCI == str(depus) and wNrCI == str(nrCashIn):
                identic = True
                break

        # de aici incepe scrierea in fisierul martor

        fisMartor.write("Buna ziua,\n")
        fisMartor.write("\n")
        fisMartor.write("Data lichidare : " + dataLichidareTxt + "\n")

        if not doarBNA or not esteATMBNA:
            fisMartor.write("Suma corecta pentru lichidare Cash Out " + codATM + " " + numeATM + " : " + '{:,}'.format(
                deLichidat) + " RON\n")
            fisMartor.write(
                "Retrageri cu succes : " + '{:,}'.format(nrCashOut) + " tranzactii - " + '{:,}'.format(retras) + " RON\n")
            if lastAlim > 0:
                fisMartor.write("Alimentare conform Banksoft  : " + '{:,}'.format(lastAlim) + " RON\n")
            else:
                fisMartor.write("Alimentare conform Banksoft  : 0 RON (fara realimentare)\n")

        if lastAlim > plafonMaximCO:
            fisMartor.write("    ###############################################################")
            fisMartor.write("    #  ATENTIE !!! Plafonul maxim aprobat este de " + str(plafonMaximCO) + " RON\n")
            fisMartor.write("    ###############################################################")

        eroriCOstr = calculCO[1]
        # print(eroriCOstr)
        if (nrCapt > 0):
            fisMartor.write(
                "Ar trebui regasit un plus in valoare de maxim " + '{:,}'.format(ATMCapture) + " RON, datorat :\n")
            eroriCOstr = calculCO[1]
            for eroare in eroriCOstr:
                if "ATM Captured Money" in eroare:
                    fisMartor.write(eroare + "\n")

        if esteATMBNA:
            fisMartor.write(
                "Suma corecta pentru lichidare Cash In " + codATM + " " + numeATM + " : " + str(depus) + " RON\n")
            fisMartor.write("Depuneri cu succes : " + str(nrCashIn) + " tranzactii\n")

        # print(esteBranch)
        if esteBranch:
            fisMartor.write(
                "\nIn cazul in care constatati alte diferente de numerar, va rugam sa solicitati instructiuni de solutionare la REG_OP.\n")
            fisMartor.write("Va rugam sa inregistrati CORECT in Ab-solut cat mai curind operatiunile de "
                            "alimentare/lichidare si sa completati in issue CORE referintele acestor operatiuni.\n")

        # aici trebuie inserata partea cu FLM/SLM, saci, etc
        ultimaLichidare = DatasourceLich.getLastLichCICO(codATM, esteATMBNA)

        interventii = DatasourceBksPrintec.getInterventiiATM(codATM, ultimaLichidare[0][0])
        deAdaugat = ""
        userDetails = []
        if interventii is not None:
            for interv in interventii:
                deAdaugat = "    " + interv[0] + ", " + interv[2] + ", " + interv[3] + ", \n        " + interv[5] + ","
                if interv[6] == "0" or interv[6] is None:
                    deAdaugat += "\n        fara sac"
                else:
                    deAdaugat += "\n        " + interv[6] + ", " + interv[7]
            fisMartor.write("\n" + deAdaugat)

            # DatasourceEroriCashIn act11 = new DatasourceEroriCashIn();
            # act11.open();
        newDataLichCI = datetime.strptime(str(ultimaLichidare[1][0]), "%Y%m%d").strftime("%Y-%m-%d") + " 00:00:00"
        EroriCI = DatasourceATMDaily.getLastErrorsATM(codATM, newDataLichCI)

        if EroriCI:
            for erori in EroriCI:
                dataEroare = erori[0]
                clientEroare = erori[1]
                eroriATM = DatasourceCapturedCards.getSubtaskClient(clientEroare, codATM, ultimaLichidare[1])
                if eroriATM:
                    fisMartor.write("Erori Cash In :\n")
                    for item in eroriATM:
                        fisMartor.write(
                            "Issue CORE : " + item[0] + ", Cod client " + item[1] + ", " + item[2] + "\n" + item[
                                3] + "\n")

        fisMartor.write("\nO zi buna,\n")
        userDetails = list(DatasourceUsers.getFullname())
        fisMartor.write(userDetails[0] + "\n")
        fisMartor.write("Echipa ATM Operations\n\n")

        eroriCIBS = calculCI[1]
        eroriCOBS = calculCO[1]
        if esteATMBNA:
            if eroriCIBS or eroriCOBS:
                fisMartor.write(userDetails[1] + ", ar trebui facute verificari pentru : \n")
                for eroareCI in eroriCIBS:
                    fisMartor.write(eroareCI + "\n")
                for eroareCO in eroriCOBS:
                    fisMartor.write(eroareCO + "\n")
        else:
            if eroriCOBS:
                for eroareCO in eroriCOBS:
                    fisMartor.write(eroareCO + "\n")

        if ciATM:
            fisMartor.write(" In CINou.xlsx apar :\n")
            for innerCINOU in ciATM:
                fisMartor.write(
                    "     O incercare de depunere cu ENCASH  " + innerCINOU[2] + " " + innerCINOU[2] + ", " + innerCINOU[
                        4] + " RON, Cod client " + innerCINOU[6] + " , Nume client " + innerCINOU[7])

        # adaugam si cupiura
        # daca este cazul, scriem in martor
        retrageri = 0
        ron5 = 0
        ron10 = 0
        ron50 = 0
        ron100 = 0
        totalRetrageri = 0

        for i in range(startCalculCupiura, endCalculCupiura):
            inner = fisiercsv[i]
            if len(inner) == 33 and int(inner[10]) > 0:
                dispensate = inner[32].replace(' ', '').lstrip()
                suta = 0
                if dispensate != '':
                    suta = int(dispensate[0:2])
                    ron100 += suta
                    cincizeci = int(dispensate[2:4])
                    ron50 += cincizeci
                    zece = int(dispensate[8:10])
                    ron10 += zece
                    cinci = int(dispensate[14:])
                    ron5 += cinci
                    retrageri += 1

        totalRetrageri = ron100 * 100 + ron50 * 50 + ron10 * 10 + ron5 * 5
        if totalRetrageri != retras:
            if not esteATMBNA or (esteATMBNA and not doarBNA):
                fisMartor.write("Conform raport Banksoft, la " + codATM + " - " + denumireATM + " au fost :\n" + str(
                    retrageri) + " retrageri in valoare totala de " + str(totalRetrageri) + " RON")
                fisMartor.write("Cupiura : \n" + str(ron100) + " x 100 RON\n" + str(ron50) + " x  50 RON\n" + str(
                    ron10) + " x  10 RON\n" + str(ron5) + " x   5 RON\n")

        fisMartor.close()
        # copiere mesaj in clipboard; se citeste fisierul numeMartor
        utilsTiti.copyFileToClipboard(numeMartor)

        # adaugare in baza de date
        deScrisDBLich = []
        deScrisDBLich.append(userDetails[1])
        deScrisDBLich.append(codATM)
        deScrisDBLich.append(datetime.strptime(dataLichidareTxt, "%d/%m/%Y").strftime("%Y%m%d"))

        if esteATMBNA:
            if not doarBNA:
                deScrisDBLich.append(str(deLichidat))
                deScrisDBLich.append(str(nrCashOut))
                deScrisDBLich.append(str(retras))
                deScrisDBLich.append(str(lastAlim))
                deScrisDBLich.append(str(depus))
                deScrisDBLich.append(str(nrCashIn))
            else:
                deScrisDBLich.append("0")
                deScrisDBLich.append("0")
                deScrisDBLich.append("0")
                deScrisDBLich.append("0")
                deScrisDBLich.append(str(depus))
                deScrisDBLich.append(str(nrCashIn))
        else:
            deScrisDBLich.append(str(deLichidat))
            deScrisDBLich.append(str(nrCashOut))
            deScrisDBLich.append(str(retras))
            deScrisDBLich.append(str(lastAlim))
            deScrisDBLich.append("0")
            deScrisDBLich.append("0")

        deScrisDBLich.append(str(ATMCapture))
        deScrisDBLich.append(str(nrCapt))

        utilsTiti.AddLogInfoAndDB(wDetalii, "Lichidare ATM")

        rezultatParent = ""
        existaLichidarea = DatasourceLich.verificare(deScrisDBLich)
        # for lich in existaLichidarea:
        #     print(lich)
        if len(existaLichidarea) == 0:      # nu exista o astfel de lichidare
            succes = DatasourceLich.addLichidareDB(deScrisDBLich)
            if succes == 1:
                return "A fost adaugata lichidarea in BD LICHDB\n"
        elif len(existaLichidarea) == 1:    # exista o lichidare
            mesaj = f"Exista o lichidare : \n" \
                    f"User, Data, LichCO, NrCO, VolCO, Alimentare, VolCI, NrCI, Vol Captured, Nr Captured\n " \
                    f"{existaLichidarea[0]} \nCe facem ?"
            label = sg.Text(mesaj, size=(80, 4))
            add_button = sg.Button("Add record", size=25, key='Add', pad=10)
            rep_button = sg.Button("Replace record", size=25, key='Replace', pad=10)
            ign_button = sg.Button("I just want the result", size=25, key='Ign', pad=10)
            # exit_button = sg.Button("Exit", size=25)

            window = sg.Window("There are more records",
                               layout=[[label],
                                       [add_button, rep_button, ign_button],
                                       []],
                               font=('Tahoma', 10))

            event, values = window.read()
            match event:
                case "Add":
                    print("Adaugare inregistrare")
                    succesAdd = DatasourceLich.addLichidareDB(deScrisDBLich)
                    if succesAdd > 0:
                        messagebox.showinfo("Lichidare ATM", "A fost adaugata lichidarea in BD LICHDB")

                case 'Replace':
                    print("Inlocuire inregistrare")
                    succesUpd = DatasourceLich.replLichidareDB(deScrisDBLich)
                    if succesUpd > 0:
                        messagebox.showinfo("Lichidare ATM", "A fost inlocuita lichidarea in BD LICHDB")

                case "Ign":
                    print("Ignor, vreau doar raspunsul")
                    os.startfile(numeMartor, operation='open')

                case sg.WIN_CLOSED:
                    pass

            window.close()

        else:       # exista mai mult de o inregistrare in BD
            msg = "Mai exista cel putin doua lichidari pt acest ATM\n"
            for item in existaLichidarea:
                msg = msg + item[0]+"\n"



            messagebox.showinfo("Lichidare ATM", rezultatParent)

            label = sg.Text(msg, size=(80, 4))
            adaug_button = sg.Button("Add record", size=25, key='Add', pad=10)
            ign_button = sg.Button("Ignore", size=25, key='Ign', pad=10)

            rep_button0 = sg.Button("Replace record ", size=25, key='Replace', pad=10)

            window = sg.Window("There are more records",
                               layout=[[label],
                                       [adaug_button, rep_button, ign_button],
                                       []],
                               font=('Tahoma', 10))

            event, values = window.read()
            match event:
                case "Add":
                    print("Adaugare inregistrare")
                    succesAdd = DatasourceLich.addLichidareDB(deScrisDBLich)
                    if succesAdd > 0:
                        messagebox.showinfo("Lichidare ATM", "A fost adaugata lichidarea in BD LICHDB")

                case 'Replace':
                    print("Inlocuire inregistrare")
                    succesUpd = DatasourceLich.replLichidareDB(deScrisDBLich)
                    if succesUpd > 0:
                        messagebox.showinfo("Lichidare ATM", "A fost inlocuita lichidarea in BD LICHDB")

                case "Ign":
                    print("Ignor, vreau doar raspunsul")
                    os.startfile(numeMartor, operation='open')

                case sg.WIN_CLOSED:
                    pass

            window.close()





            # TODO exit(2)

        os.startfile(numeMartor, operation='open')
        return f"File created : {numeMartor}"


if __name__ == "__main__":
    Lichidare_ATM()



    """
    
                DatasourceLich adaug = new DatasourceLich();
                adaug.open();
                List<List<String>> existaLichidarea = adaug.verificare(deScrisDBLich);
                switch (existaLichidarea.size()) {
                case 0:
                    int succes = adaug.addLichidareDB(deScrisDBLich);
                    if (succes > 0) {
                        allInOne.addText("\n" + "A fost adaugata lichidarea in BD LICHDB");
                    }
                    break;
                case 1:
                    Object[] optiuni = { "Adaugare inregistrare", "Inlocuire inregistrare", "Ignor, vreau doar raspunsul" };
                    String mesaj = "Exista o lichidare :\n"
                            + "User, Data, LichCO, NrCO, VolCO, Alimentare, VolCI, NrCI, Vol Captured, Nr Captured\n"
                            + existaLichidarea.get(0).toString() + "\n\n" + "Ce facem ?";
                    int nDB = JOptionPane.showOptionDialog(null, mesaj, "Lichidare " + codATM + " " + denumireATM,
                            JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE, null, optiuni, optiuni[1]);
                    if (nDB == 0) {
                        int succesAdd = adaug.addLichidareDB(deScrisDBLich);
    
                        if (succesAdd > 0) {
                            allInOne.addText("\n" + "A fost adaugata lichidarea in BD LICHDB");
                        }
    
                    } else if (nDB == 1) {
                        int succesUpd = adaug.replaceLichidareDB(deScrisDBLich);
                        if (succesUpd > 0) {
                            allInOne.addText("\n" + "A fost updatata lichidarea in BD LICHDB");
                        }
                    }
                    break;
                case 2:
                    String mesaj2 = "Exista inregistrarile :\n\n";
                    for (int i = 0; i < existaLichidarea.size(); i++) {
                        mesaj2 = mesaj2 + String.valueOf(i) + ". " + existaLichidarea.get(i).toString() + "\n";
                    }
    
                    List<String> optiuniLich = new ArrayList<>();
                    optiuniLich.add("Adaugare");
                    optiuniLich.add("Ignorare");
                    for (int i = 0; i < existaLichidarea.size(); i++) {
                        optiuniLich.add("Inlocuire " + String.valueOf(i));
                    }
    
                    Object[] pentruOptiuni = optiuniLich.toArray();
                    int nDBLich = JOptionPane.showOptionDialog(null, mesaj2, "Lichidare " + codATM + " " + denumireATM,
                            JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE, null, pentruOptiuni, pentruOptiuni[1]);
                    // Adaugare lichidare
                    if (nDBLich == 0) {
                        int succesAdd = adaug.addLichidareDB(deScrisDBLich);
    
                        if (succesAdd > 0) {
                            allInOne.addText("\n" + "A fost adaugata lichidarea in BD LICHDB");
                        }
    
                    }
                    // Ignorare
                    if (nDBLich == 1) {
                        allInOne.addText("\n" + "Ai ales sa ignori, treaba ta, sa nu zici ca nu ti-am spus!");
                    }
    
                    if (nDBLich > 1) {
                        int succesUpdLich = adaug.replaceLichidareDB(deScrisDBLich, existaLichidarea.get(nDBLich - 2));
                    }
    
                    break;
                default:
                    break;
                }
    """

