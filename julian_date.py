from datetime import datetime
from tkinter import simpledialog

def datestdtojd (stddate):
    fmt='%Y-%m-%d'
    sdtdate = datetime.strptime(stddate, fmt)
    sdtdate = sdtdate.timetuple()
    jdate = str(sdtdate.tm_yday).zfill(3)
    return(jdate)

def julian():
    # strftime se traduce "string formatted time"; now va fi reprezentarea string a datei curente
    now = datetime.now().strftime('%Y-%m-%d')
    new_date = simpledialog.askstring(title = "Julian day", prompt = "Enter Date in YYYY-MM-DD format:", initialvalue=now)

    message = f"Julian date for {new_date} is {datestdtojd(new_date)}"
    return message


if __name__ == "__main__":
    julian()

