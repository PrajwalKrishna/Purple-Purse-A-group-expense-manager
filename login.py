import sqlite3 as sql
from signature_dbms import *

def insertTransaction(title,amount,sender_id,receiver_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    #try:
    curr.execute("INSERT INTO TRANSACTIONS (title,amount,sender_id,receiver_id) VALUES(?,?,?,?)",
                (title,amount,sender_id,receiver_id))
    conn.commit()
    conn.close()
    addToUserTotal(sender_id,amount*-1)
    addToUserTotal(receiver_id,amount)
    #except IntegrityError as e:
    #    return -1
    return 1


def insertFriend(user_id,friend_id):
    friends = findFriends(user_id)
    flag = 1
    for i in friends:
        if str(i) == str(friend_id):
            flag = 0
    if user_id == friend_id:
        flag = 0
    if flag:
        friends.append(friend_id)
        posx=[]
        for i in friends:
            posx.append(str(i))
        print("VHGJVJHHBJ\n")
        print(friends)
        friendList = ','.join(posx)
        print(friendList)
        conn = create_connection("database.db")
        curr = conn.cursor()
        curr.execute(("UPDATE USERS SET friends='{0}' WHERE user_id ='{1}'").format(friendList,user_id))
        conn.commit()
        conn.close()

def deleteTransaction(transaction_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    try:
        curr.execute("DELETE FROM TRANSACTIONS WHERE transaction_id = '{}'".format(transaction_id))
    except:
        return 0
    conn.commit()
    conn.close()

def addToUserTotal(user_id,amount):
    user = findUserByUser_Id(user_id)
    if user:
        conn = create_connection("database.db")
        curr = conn.cursor()
        total = user[4]+amount
        curr.execute(("UPDATE USERS SET total_balance='{0}' WHERE user_id='{1}'").format(total,user_id))
        conn.commit()
        conn.close()
    else:
        print ('Unsuccessful')

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
    "Adder approved transaction will be 0,two way approved be 1,delete approved will be -1"
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute(("UPDATE TRANSACTIONS SET status=1 WHERE transaction_id ='{0}'").format(tansaction_id))
    conn.commit()
    conn.close()

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
    #insertUser("Prajwal","Prajwal.com","Prajwal")
    #insertUser("qwerty","qwerty.com","qwerty")
    #insertUser("Harry","Harry.com","Harry")
    #insertFriend(3,2)
    users=retrieveUsers()
    for i in users:
        print (i[0],':'+i[1])
    print (findUserByEmail("krishan.com"))
    print ("Users ahve finished now comes transactions ")
    #insertTransaction("first",170,1,3)
    #insertTransaction("aloo",1200,4,2)
    #insertTransaction("pak",561,5,2)
    transactions = retrieveTransactions()
    print ('transaction_id    title  amount  sender_id   receiver_id')
    for i in transactions:
        for j in i:
            print '.',
            print j,
        print ""
