from sqlite3 import Cursor, Connection
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

from core.Database.basic import createConnectionToDatabase

def checkValidUser(user_id:int) -> bool:
    con = createConnectionToDatabase()
    cur = con.cursor()
    
    #check if there is user with the same id
    cur.execute(f"Select * from User where user_id = {user_id}")
    res = cur.fetchall()

    #check if there are any rows in return of command
    found = False
    for a in res:
        found = True
        break
    
    cur.close()
    con.close()

    return found

def addUser(user_id: int, user_name: str):
    #Handle adding new user
    if checkValidUser(user_id) == False:
        con = createConnectionToDatabase()
        cur = con.cursor()

        today = datetime.today()

        #TODO change user admin 
        cur.execute("INSERT INTO User VALUES (?, ?, ?, ?)", (user_id, user_name, today.strftime("'%Y-%m-%d'"), True)) # The user is not an admin (False) first true
        con.commit()

        print("Added new user : " + str(user_id))

        cur.close()
        con.close()
    else:
        print("User already exists!")

    

def getUser(user_id: int) -> Optional[Tuple[int, str, str, bool]]:
    con = createConnectionToDatabase()
    cur = con.cursor()
    
    #check if there is user with the same id
    cur.execute(f"Select * from User where user_id = {user_id}")
    res = cur.fetchone()

    cur.close()
    con.close()

    return res

def isUserAdmin(user_id: int) -> bool:
    con = createConnectionToDatabase()
    cur = con.cursor()
    
    #check if there is user with the same id
    cur.execute(f"Select * from User where user_id = {user_id} and user_admin = TRUE;")
    res = cur.fetchone()

    cur.close()
    con.close()

    return res