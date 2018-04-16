import sqlite3 as sql
from signature_dbms import *

def insertTransaction(title,amount,sender_id,receiver_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    try:
        curr.execute("INSERT INTO TRANSACTIONS (title,amount,sender_id,receiver_id) VALUES(?,?,?,?)",
                    (title,amount,sender_id,receiver_id))
    except IntegrityError as e:
        return -1
    conn.commit()
    conn.close()
    return 1

def deleteTransaction(transaction_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    try:
        curr.execute("DELETE FROM TRANSACTIONS WHERE transaction_id = '{}'".format(transaction_id))
    except:
        return 0
    conn.commit()
    conn.close()

def findAllTransactionByUser_Id(user_id):
    query = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute(("SELECT * FROM TRANSACTIONS WHERE sender_id is '{0}' OR receiver_id is '{0}'".format(user_id)))
    query = curr.fetchall()
    conn.close()
    return query

def findTransactionByUser_Id(id,title,amount):
    query = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute(("SELECT * FROM TRANSACTIONS WHERE user_id IS '{0}' AND title IS '{1}' AND amount IS '{2}'".format(user_id,title,amount)))
    query = curr.fetchall()
    conn.close()
    return query

def approveTransaction(transaction_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute(("UPDATE TRANSACTIONS SET status=1 WHERE transaction_id ='{0}'").format(transaction_id))
    curr.commit()
    curr.close()

def retrieveTransactions():
	conn = create_connection("database.db")
	curr = conn.cursor()
	curr.execute("SELECT * FROM TRANSACTIONS")
	users = curr.fetchall()
	conn.close()
	return users


if __name__ == '__main__':
    #insertUser("Gujju","yam.com","yam")
    #insertUser("Chaaras","yash.com","yash")
    users=retrieveUsers()
    for i in users:
        print i[0],
        print ':'+i[1]
    print findUserByEmail("krishan.com")
    print "Users ahve finished now comes transactions "
    #insertTransaction("first",170,1,3)
    #insertTransaction("aloo",1200,4,2)
    transactions = findAllTransactionByUser_Id(2)
    print 'transaction_id    title  amount  sender_id   receiver_id'
    for i in transactions:
        print i[0],
        print '     '+i[1]+'    ',
        print i[2],
        print i[5],
        print i[6]
