import sqlite3 as sql
from signature_dbms import *
def create_connection(database):
    try:
        conn = sql.connect(database)
        return conn;
    except:
        print "Cannot access database"

#def insertUser(name,email,password):
#    conn = create_connection("database.db")
#   curr = conn.cursor()
 #   try:
  #      curr.execute("INSERT INTO USERS (name,email,password) VALUES(?,?,?)",(name,email,password))
  #  except sql.IntegrityError as e:
  #      print("Account already exists")
  #      return 0
  #  conn.commit()
  #  conn.close()
  #  return 1

def retrieveUsers():
	conn = create_connection("database.db")
	curr = conn.cursor()
	curr.execute("SELECT name, email,password FROM USERS")
	users = curr.fetchall()
	conn.close()
	return users

#def findUserByEmail(email):
#    query=None
#    conn = create_connection("database.db")
#    curr = conn.cursor()
#    curr.execute("SELECT * FROM USERS WHERE email is '{}'".format(email))
#    query = curr.fetchone()
#    conn.close()
#    return query


def findUserByUser_Id(id):
    query = None
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM USERS WHERE email is '{}'".format(id))
    query = curr.fetchall()
    conn.close()
    return query

def insertTransaction(title,amount,sender_id,receiver_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    #try:
    print title ,amount ,sender_id ,    receiver_id
    curr.execute("INSERT INTO TRANSACTIONS (title,amount,sender_id,receiver_id) VALUES(?,?,?,?)",
                    (title,amount,sender_id,receiver_id))
    #except:
    #    return -1
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

def findTransactionByUser_Id(id,title,amount):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute(("SELECT * FROM TRANSACTIONS WHERE user_id IS '{0}' AND title IS '{1}' AND amount IS '{2}'".format(user_id,title,amount)))
    query = curr.fetchall()
    conn.close()

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
    #insertUser("Prajwal","krishan.com","alphabeta")
    insertUser("Bhatt","alia.com","bhatt")
    users=retrieveUsers()
    for i in users:
        print i[0],
        print ':'+i[1]
    print findUserByEmail("krishan.com")
    print "Users ahve finished now comes transactions "
    #insertTransaction("first",28000,20,11)
    transactions = retrieveTransactions()
    print 'transaction_id    title  amount  sender_id   receiver_id'
    for i in transactions:
        print i[0],
        print '     '+i[1]+'    ',
        print i[2],
        print i[5],
        print i[6]
        deleteTransaction(i[0])
