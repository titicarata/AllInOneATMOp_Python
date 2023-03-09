from os import getlogin
import sys
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import *
from tkinter import ttk
from datetime import datetime

import LichidareATM
from ATMWin10CIErrors import win10_ci_errors
from AllLastTran import all_last_transactions
from utilsTiti import AddLogInfoAndDB
from arhivare_ejtemp import arhivare_ejtemp
from julian_date import julian
from detect_last_replenishment import detect_last_replenishment


def callback():
    user_option = app_selection.get()
    # dataRulare = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    match user_option:
        case 2:
            mesaj = win10_ci_errors()
            AddLogInfoAndDB("Generare Raport erori Cash In Win 10", "ATM Win10 Cash In errors")
            addText(f"File created : {mesaj}")
        case 4:
            detect_last_replenishment()
        case 9:
            mesaj = LichidareATM.Lichidare_ATM()
            addText(mesaj)
        case 14:
            mesaj = all_last_transactions()  # Last transaction extins
            AddLogInfoAndDB("Detectare ultima tranzactie (cu/fara succes, Cash In/CashOut)",
                            "Last Transaction Extins")
            addText(f"File created : {mesaj}")
        case 22:
            mesaj = arhivare_ejtemp()
            addText(mesaj)
        case 37:
            mesaj = julian()
            addText(mesaj)
        case _:
            addText("Optiune neimplementata inca")


def terminator():
    sys.exit()


def addText(string):
    output_text_area.insert(tk.END, '\n' + string + '\n')
    output_text_area.see("end")


def clearLog():
    output_text_area.delete('1.0', END)


root = Tk()
s = ttk.Style()
s.configure('my.TButton', font='Calibri 9')

buttonOK = ttk.Button(root, text='OK')
buttonCancel = ttk.Button(root, text='Close')
buttonClearLog = ttk.Button(root, text='Clear log', style='my.TButton', command=lambda: output_text_area.delete(1.0, END))

lblBlank0 = ttk.Label(text="", font='Arial 8 italic')
lblBlank0.grid(row=1, column=1, sticky=W, columnspan=2, padx=15)

lblBlank = ttk.Label(text="", font='Arial 8 italic')
lblBlank.grid(row=16, column=1, sticky=W, columnspan=2, padx=15)

lblOwner = ttk.Label(text="2023-2027, " + '\u00A9' + " Titi Carat" + '\u0103' + "  Vers. 341.22.001", font=('Arial 8 italic'))
lblOwner.grid(row=17, column=1, sticky=W, columnspan=2, padx=15)

buttonOK.grid(row=26, column=4, sticky=E + W, padx=5)
buttonCancel.grid(row=26, column=3, sticky=E + W, padx=5)
buttonClearLog.grid(row=26, column=1, sticky=E + W, padx=15)

buttonOK.config(command=callback)
buttonCancel.config(command=terminator)

app_selection = IntVar()

tk.Radiobutton(root, text='ATM Html', value=1, variable=app_selection, foreground='red').grid(row=2, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='ATM Win 10 CI Errors', value=2, variable=app_selection).grid(row=3, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Cbk card', value=3, variable=app_selection, foreground='red').grid(row=4, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Detect last replenishment', value=4, variable=app_selection).grid(row=5, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Detect today errors', value=5, variable=app_selection, foreground='red').grid(row=6, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Error log NCR', value=6, variable=app_selection, foreground='red').grid(row=7, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Import sold ATM', value=7, variable=app_selection, foreground='red').grid(row=8, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Info ATM', value=8, variable=app_selection, foreground='red').grid(row=9, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Lichidare ATM', value=9, variable=app_selection, state='normal').grid(row=10, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Non financial', value=10, variable=app_selection, foreground='red').grid(row=11, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Recuperare EJ + Rapoarte Daily', value=11, variable=app_selection, foreground='red').grid(row=12, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Refuz la plata', value=12, variable=app_selection, foreground='red').grid(row=13, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Dezinstalari in perioada', value=13, variable=app_selection, foreground='red').grid(row=14, column=1, sticky=W, padx=30)
tk.Radiobutton(root, text='Last transaction extins', value=14, variable=app_selection).grid(row=15, column=1, sticky=W, padx=30)

tk.Radiobutton(root, text='Statistici cash', value=15, variable=app_selection, foreground='red').grid(row=2, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Raport activitate', value=16, variable=app_selection, foreground='red').grid(row=3, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Raport erori cash in', value=17, variable=app_selection, foreground='red').grid(row=4, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Last cash in trx', value=18, variable=app_selection, foreground='red').grid(row=5, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Dispenser errors', value=19, variable=app_selection, foreground='red').grid(row=6, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Retrieve card number', value=20, variable=app_selection, foreground='red').grid(row=7, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Sold ATM', value=21, variable=app_selection, foreground='red').grid(row=8, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Arhivare z:\\EjTemp', value=22, variable=app_selection).grid(row=9, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Raport cupiura', value=23, variable=app_selection, foreground='red').grid(row=10, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Modificare plafoane', value=24, variable=app_selection, foreground='red').grid(row=11, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Numar lichidari', value=25, variable=app_selection, foreground='red').grid(row=12, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Jurnalizare ATM', value=26, variable=app_selection, foreground='red').grid(row=13, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Issue CORE card', value=27, variable=app_selection, foreground='red').grid(row=14, column=2, sticky=W, padx=30)
tk.Radiobutton(root, text='Subtask CORE', value=28, variable=app_selection, foreground='red').grid(row=15, column=2, sticky=W, padx=30)

tk.Radiobutton(root, text='Lichidari CORE', value=29, variable=app_selection, foreground='red').grid(row=2, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Brinks', value=30, variable=app_selection, foreground='red').grid(row=3, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='EJ Brinks', value=31, variable=app_selection, foreground='red').grid(row=4, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Verificari FLM Brinks', value=32, variable=app_selection, foreground='red').grid(row=5, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Inventar ATM', value=33, variable=app_selection, foreground='red').grid(row=6, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Bigdata collection', value=34, variable=app_selection, foreground='red').grid(row=7, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Easy ATM', value=35, variable=app_selection, foreground='red').grid(row=8, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Long ATM Reconciliation', value=36, variable=app_selection, foreground='red').grid(row=9, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Julian Date', value=37, variable=app_selection).grid(row=10, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Operatii DB SQL', value=38, variable=app_selection, foreground='red').grid(row=11, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Import ePO', value=39, variable=app_selection, foreground='red').grid(row=12, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Verificare update', value=40, variable=app_selection, foreground='red').grid(row=13, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Ultimul jurnal', value=41, variable=app_selection, foreground='red').grid(row=14, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Verificare MCode', value=42, variable=app_selection, foreground='red').grid(row=15, column=3, sticky=W, padx=30)
tk.Radiobutton(root, text='Facturi ATM&POS', value=43, variable=app_selection, foreground='red').grid(row=2, column=4, sticky=W, padx=30)
tk.Radiobutton(root, text='ATM Profitability', value=44, variable=app_selection, foreground='red').grid(row=3, column=4, sticky=W, padx=30)
tk.Radiobutton(root, text='SLM Printec', value=45, variable=app_selection, foreground='red').grid(row=4, column=4, sticky=W, padx=30)
tk.Radiobutton(root, text='RO_IM Printec', value=46, variable=app_selection, foreground='red').grid(row=5, column=4, sticky=W, padx=30)

output_text_area = scrolledtext.ScrolledText(root, undo=True, height=10, wrap="word", font='Calibri 9')
output_text_area.grid(row=18, column=1, columnspan=8, sticky=W + E + N + S, padx=10, pady=20)

if getlogin().casefold() == 'titi':
    tk.Radiobutton(root, text='Add quote', value=47, variable=app_selection, foreground='red').grid(row=13, column=4, sticky=W, padx=30)
    tk.Radiobutton(root, text='Only Titi', value=48, variable=app_selection, foreground='red').grid(row=14, column=4, sticky=W, padx=30)
    tk.Radiobutton(root, text='User Admin', value=49, variable=app_selection, foreground='red').grid(row=15, column=4, sticky=W, padx=30)

root.geometry("900x620")
root.title("All In One ATM Operations information system")
root.mainloop()
