import sqlite3
import os


def getFullname():
    userDef = ()
    con = sqlite3.connect("Y:\\Operatiuni\\Acquiring\\ATM\\Databases\\UsersDB.db")
    cur = con.cursor()
    res = cur.execute("SELECT FullName, Prenume FROM users WHERE WindowsUser = '"+os.getlogin().lower()+"'")
    userDef = res.fetchone()
    con.close()
    return userDef



