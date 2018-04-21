import sqlite3 as sql
from signature_dbms import *

def insertTransaction(title,amount,sender_id,receiver_id):
        flag = 1
        if not findUserByUser_Id(sender_id):
            flag = 0
        if not findUserByUser_Id(receiver_id):
            flag = -1
        if sender_id==receiver_id:
            return flag
        if (flag == 1):
            conn = create_connection("database.db")
            curr = conn.cursor()
            curr.execute("PRAGMA foreign_keys=ON;")
            curr.execute("INSERT INTO TRANSACTIONS (title,amount,sender_id,receiver_id) VALUES(?,?,?,?)",
                        (title,amount,sender_id,receiver_id))
            conn.commit()
            conn.close()
            addToUserTotal(sender_id,amount*-1)
            addToUserTotal(receiver_id,amount)
        return flag

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

def addNewGroup(name):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("INSERT INTO GROUPS (name) VALUES(?)",(name))
    conn.commit()
    curr.execute("SELECT SCOPE_INDENTITY()")
    group = curr.fetchone()
    conn.close()
    return group

def addMember(group_id,user_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("PRAGMA foreign_keys=ON;")
    curr.execute("INSERT INTO MEMEBERSHIP (group_id,user_id) VALUES(?,?)",
                (group_id,user_id))
    conn.commit()
    conn.close()

def findAllMembersForGroup(group_id):
    members = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM MEMEBERSHIP WHERE(group_id) IS '{0}'".format(group_id))
    members = curr.fetchall()
    conn.commit()
    conn.close()
    return members

def findAllGroupsForUser(user_id):
    groups = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM MEMEBERSHIP WHERE(user_id) IS '{0}'".format(user_id))
    groups = curr.fetchall()
    conn.commit()
    conn.close()
    return groups

def findAllTransactionsForGroup(group_id):
    transactions = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM GROUPTRANSACTIONS WHERE(group_id) IS '{0}'".format(group_id))
    transactions = curr.fetchall()
    conn.commit()
    conn.close()
    return transactions

def findGroupTransactionById(groupTransaction_id):
    transaction = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM GROUPTRANSACTIONS WHERE(groupTransaction_id) IS '{0}'".format(groupTransaction_id))
    transaction = curr.fetchone()
    conn.commit()
    conn.close()
    return transaction

def makeGroupTransaction(title,amount,group_id,payer_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("PRAGMA foreign_keys=ON")
    curr.execute("INSERT INTO GROUPTRANSACTIONS (title,group_id,payer_id,amount) VALUES(?,?,?,?)",
                 (title,group_id,payer_id,amount))
    curr.execute("SELECT SCOPE_INDENTITY()")
    newGroupTransaction = curr.fetchone()
    newGroupTransaction_id = newGroupTransaction[0]
    conn.commit()
    conn.close()
    return newGroupTransaction_id

def payEqualGroupTransaction(GroupTransaction_id):
    groupTransaction = findGroupTransactionById(groupTransaction_id)
    title = groupTransaction[1]
    amount = groupTransaction[2]
    group_id = groupTransaction[3]
    payer_id = groupTransaction[4]
    members = findAllMembersForGroup(group_id)
    divisions = len(members)
    dividends = amount/divisions
    for i in members:
        insertTransaction(title,dividends,i[1],payer_id)

def makeShare(share,groupTransaction_id,user_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("PRAGMA foreign_keys=ON")
    curr.execute("INSERT INTO SHARES (share,groupTransaction_id,user_id) VALUES(?,?,?)",
                 (share,groupTransaction_id,user_id))
    conn.commit()
    conn.close()

def findShare(groupTransaction_id,user_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    share = []
    curr.execute("SELECT * FROM SHARES WHERE (groupTransaction_id) IS '{0}' AND (user_id) IS '{1}'".format(groupTransaction_id,user_id))
    share = curr.fetchone()
    conn.close()
    if share:
        return share[0]
    else:
        return 0

def payUnequalGroupTransaction(groupTransaction_id):
    groupTransaction = findGroupTransactionById(groupTransaction_id)
    title = groupTransaction[1]
    amount = groupTransaction[2]
    group_id = groupTransaction[3]
    payer_id = groupTransaction[4]
    members = findAllMembersForGroup(group_id)
    divisions = 0
    for i in members:
        divisions += findShare(groupTransaction_id,i[1])
    dividends = amount/divisions
    for i in members:
        amount = dividends*findShare(groupTransaction_id,i[1])
        insertTransaction(title,amount,i[1],payer_id)

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
    #for i in transactions:
    #    for j in i:
    #        print '.',
    #        print j,
    #   print ""
