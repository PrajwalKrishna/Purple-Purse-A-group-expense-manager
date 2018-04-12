import sqlite3 as sql
from login import create_connection

def insertUser(name,email,password):
    conn = create_connection("database.db")
    curr = conn.cursor()
    try:
        curr.execute("INSERT INTO USERS (name,email,password) VALUES(?,?,?)",(name,email,password))
    except sql.IntegrityError as e:
        print("Account already exists")
        return 0
    conn.commit()
    conn.close()
    return 1

def findUserByEmail(email):
    query=None
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM USERS WHERE email = '{}'".format(email))
    query = curr.fetchone()
    conn.close()
    return query
