import csv
import os
import sqlite3
from datetime import datetime
import xlsxwriter


def all_last_transactions():
    # start_time = datetime.now()

    output_file = "d:\\JavaResults\\AllLastTranPY.xlsx"

    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\ATMDb.db")
    cur = con.cursor()
    res = cur.execute("select Termid||' - '||Termname FROM CEB WHERE PlafonAprobat > 0")
    cebXls = res.fetchall()
    con.close()

    # initializez structura result_list
    result_list = []
    list_size = len(cebXls)
    b = ['01/01/1999 00:00:00', '01/01/1999 00:00:00', '01/01/1999 00:00:00', '01/01/1999 00:00:00']

    for i in range(0, list_size):
        inner = [cebXls[i][0]]
        inner.extend(b)
        result_list.append(inner)

    # read rest.csv
    csv_records = []
    with open('d:\\Descarcari\\rest.csv', mode='r') as input_file:
        next(input_file, None)          # ignore header
        for row in csv.reader(input_file):
            csv_records.append(row)

    for transaction in csv_records:
        oraTrx = transaction[2].zfill(6)
        dataTrx = transaction[1] + " " + oraTrx
        datetime_trx = datetime.strptime(dataTrx, '%Y%m%d %H%M%S')
        termId = transaction[3]
        transac = transaction[7]

        completed = 0
        if transaction[10] != '':
            completed = int(transaction[10])

        codClient = 0
        if transaction[13] != '':
            codClient = int(transaction[13])
        for record in result_list:
            if termId in record[0]:
                dataOraAny = datetime.strptime(record[1], '%d/%m/%Y %H:%M:%S')
                dataOraCrd = datetime.strptime(record[2], '%d/%m/%Y %H:%M:%S')
                dataCashOut = datetime.strptime(record[3], '%d/%m/%Y %H:%M:%S')
                dataCashIn = datetime.strptime(record[4], '%d/%m/%Y %H:%M:%S')

                if datetime_trx > dataOraAny:
                    record[1] = datetime_trx.strftime("%d/%m/%Y %H:%M:%S")
                if datetime_trx > dataOraCrd:
                    record[2] = datetime_trx.strftime("%d/%m/%Y %H:%M:%S")
                if ('CASH W' in transac or 'CASH ADV' in transac) and completed != 0 \
                        and datetime_trx > dataCashOut:
                    record[3] = datetime_trx.strftime("%d/%m/%Y %H:%M:%S")
                if ('CASH IN' in transac or 'CASH-IN' in transac) and completed != 0 and codClient != 0 \
                        and datetime_trx > dataCashIn:
                    record[4] = datetime_trx.strftime("%d/%m/%Y %H:%M:%S")

    result_list.insert(0, ["Terminal ID & Name", "Last touchscreen trx", "Last card trx", "Last withdrawal", "Last deposit"])
    for record in result_list:
        if record[1] == '01/01/1999 00:00:00':
            record[1] = ''
        if record[2] == '01/01/1999 00:00:00':
            record[2] = ''
        if record[3] == '01/01/1999 00:00:00':
            record[3] = ''
        if record[4] == '01/01/1999 00:00:00':
            record[4] = ''

    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for terminalID, touch, card, retragere, depunere in result_list:
        worksheet.write(row, col, terminalID)
        worksheet.write(row, col + 1, touch)
        worksheet.write(row, col + 2, card)
        worksheet.write(row, col + 3, retragere)
        worksheet.write(row, col + 4, depunere)
        row += 1

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 4, 20)

    workbook.close()
    # end_time = datetime.now()
    # print(end_time-start_time)
    os.startfile(output_file)

    # dataRulare = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    return output_file


if __name__ == "__main__":
    all_last_transactions()
