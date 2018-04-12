import sqlite3 as sql
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
 #   return query


def findUserByUser_Id(id):
    query=None
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM USERS WHERE email is '{}'".format(id))
    query = curr.fetchall()
    conn.close()
    return query

def insertTransaction(title,amount,user_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    try:
        curr.execute("INSERT INTO TRANSACTIONS (title,amount,user_id) VALUES(?,?,?)",title,amount,user_id)
    except:
           return 0
    conn.commit()
    conn.close()
    return 1

def deleteTransaction(transaction_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    try:
        pass
    #    curr.execute("DELETE FROM TRANSACTIONS WHERE transaction_id = '{}'".format{transaction_id})
    except:
        return 0
    conn.commit()
    conn.close()

def findTransactionByUser_Id(id,title,amount):
    conn = create_connection("database.db")
    curr = conn.cursor()
   # curr.execute(("SELECT * FROM TRANSACTIONS WHERE user_id IS '{0}' AND title IS '{1}'
    #              AND amount IS '{2}'".format{user_id,title,amount}))
    query = curr.fetchall()
    conn.close()


if __name__ == '__main__':
    insertUser("Prajwal","krishan.com","alphabeta")
    insertUser("Krishna","prajwal.com","siddhsafh")
    users=retrieveUsers()
    for i  in users:
        print i[1]
    #for i in findUserByEmail("microhard.com"):
    #    print i
    #if not findUserByUser_Id(13):
    #    print "not found"
