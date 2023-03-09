import glob
import os
import zipfile
import datetime
import PySimpleGUI as sg
from utilsTiti import AddLogInfoAndDB

sg.theme('Default1')

def get_data_minima():
    """
    Titi said: This function detects the oldest file date
    creation among electronic journals stored in z:/Ejtemp
    folder (CDE) and return the date when it was extracted from ATM
    considering that the electronic journal follows the
    pattern 'EJ17xxx_YYYYmmdd_HHMM.log'

    :return: Integer reflecting date extraction
    """
    pattern = "EJ17???_????????_????.log"
    data_maxima = get_today_int()-1
    os.chdir("z:/ejtemp")
    files_to_archive = glob.glob(pattern, recursive=False)
    # detectez data minima din numele fisierelor
    if len(files_to_archive) == 0:
        return 0
    for file in files_to_archive:
        if int(file.split('_')[1]) <= data_maxima:
            data_maxima = int(file.split('_')[1])
    return data_maxima


def get_today_int():
    """
    Titi said: This function convert current date into an integer using pattern 'yyyymmdd'

    :return: Integer like 20230124 (if current date is January 24, 2023)
    """
    now = datetime.datetime.now()
    date_time = int(now.strftime("%Y%m%d"))
    return date_time


def arhivare_ejtemp():
    """
    Titi said: This module is detecting the oldest file date creation among electronic journals
     stored in z:\\Ejtemp folder and propose to archive all electronic journals generated in that day.
     The archive will be stored in z:\\Ejtemp\\new_folder and its name will be like yyyymmdd.zip

    :return: A message will be displayed in Output area

    """
    rezultat = ""
    astazi = get_today_int()
    label = sg.Text("Date to archive :")
    input_box1 = sg.InputText(tooltip="Enter date (yyyymmdd)",
                              key="data",
                              default_text=str(get_data_minima()),
                              size=(30, 10))
    run_button = sg.Button("Run", size=(10, 1))
    exit_button = sg.Button("Exit", size=(10, 1))

    window = sg.Window("Enter date",
                       layout=[[label],
                               [input_box1],
                               [run_button, exit_button]],
                       font=('Calibri', 12))

    # while True:
    event, values = window.read()

    match event:
        case "Run":
            data_min = values['data']
            # reutilizez variabila files_to_archive
            files_to_archive = []
            file_pattern = f"z:\\ejtemp\\EJ*{data_min}*.log"
            for file in glob.glob(file_pattern, recursive=False):
                files_to_archive.append(file)

            archive_name = f"z:\\ejtemp\\new_folder\\{data_min}_.zip"
            if os.path.exists(archive_name):
                os.remove(archive_name)

            alternate_path = []

            with zipfile.ZipFile(archive_name, 'w') as zipObj2:
                for file in files_to_archive:
                    alternate_path.append("W:\\Operatiuni\\Acquiring\\ATM\\Transfer_IN_INT\\ejtemp\\"+file[10:])
                    zipObj2.write(file[10:], compress_type=zipfile.ZIP_DEFLATED)

            rezultat += f"{archive_name} archive created (contains {len(files_to_archive)} files)\n"

            for filePath in files_to_archive:
                os.remove(filePath)
            for alternate_filePath in alternate_path:
                if os.path.exists(alternate_filePath):
                    os.remove(alternate_filePath)
            data_min = get_data_minima()
            if data_min != 0:
                dataRulare = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                data_arhivare = datetime.datetime.strptime(str(data_min),"%Y%m%d").strftime("%d/%m/%Y")
                AddLogInfoAndDB(dataRulare, "Arhivare z:\ejtemp pentru "+data_arhivare, "Arhivare jurnale EJTEMP")
        case "Exit":
            window.close()
        case sg.WIN_CLOSED:
            window.close()

    window.close()
    sg.popup_ok("Gata !")
    return rezultat


if __name__ == "__main__":
    arhivare_ejtemp()