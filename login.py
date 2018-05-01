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

def findTransactionById(transaction_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    transaction = []
    curr.execute("SELECT * FROM TRANSACTIONS WHERE transaction_id = '{}'".format(transaction_id))
    transaction = curr.fetchone()
    conn.commit()
    conn.close()
    return transaction

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

def addToMembershipAmount(user_id,group_id,amount):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT amount FROM MEMEBERSHIP WHERE user_id=='{0}' AND group_id=='{1}'".format(user_id,group_id))
    old_amount = curr.fetchone()[0]
    amount = old_amount + int(amount)
    curr.execute("UPDATE MEMEBERSHIP SET amount='{0}' WHERE user_id=='{1}' AND group_id=='{2}'".format(amount,user_id,group_id))
    conn.commit()
    conn.close()

def deleteTransaction(transaction_id):
    transaction = findTransactionById(transaction_id)
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("DELETE FROM TRANSACTIONS WHERE transaction_id = '{}'".format(transaction_id))
    conn.commit()
    conn.close()
    addToUserTotal(transaction[5],transaction[2]*1)
    addToUserTotal(transaction[6],transaction[2]*-1)

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
    curr.execute("INSERT INTO GROUPS (name) VALUES(?)",[name])
    curr.execute("SELECT last_insert_rowid()")
    group_id = curr.fetchone()[0]
    conn.commit()
    conn.close()
    return group_id

def changeCommentToTransaction(comment,transaction_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("UPDATE TRANSACTIONS set comment = '{0}' WHERE transaction_id = '{1}'".format(comment,transaction_id))
    conn.commit()
    conn.close()

def makeMember(group_id,user_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("PRAGMA foreign_keys=ON;")
    curr.execute("INSERT INTO MEMEBERSHIP (group_id,user_id) VALUES(?,?)",
                (group_id,user_id))
    conn.commit()
    conn.close()

def findAllMemberIdsForGroup(group_id):
    member_ids = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT user_id FROM MEMEBERSHIP WHERE(group_id) IS '{0}'".format(group_id))
    member_ids = curr.fetchall()
    conn.commit()
    conn.close()
    return member_ids

def findAllMembersForGroupHomeRendering(group_id):
    member_ids = []
    members = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT user_id,amount FROM MEMEBERSHIP WHERE(group_id) IS '{0}'".format(group_id))
    member_ids = curr.fetchall()
    conn.commit()
    conn.close()
    for i in member_ids:
        user = findUserByUser_Id(i[0])
        members.append([[user[1],user[2],i[1]],i[0]])
    return members

def findAllTransactionsForGroup(group_id):
    transactions = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT title,amount FROM GROUPTRANSACTIONS WHERE(group_id) IS '{0}'".format(group_id))
    transactions = curr.fetchall()
    conn.commit()
    conn.close()
    return transactions

def addToGroupTransactionAmount(groupTransaction_id,amount):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT amount FROM GROUPTRANSACTIONS WHERE(groupTransaction_id) IS '{0}'".format(groupTransaction_id))
    old_amount = curr.fetchone()[0]
    new_amount = int(old_amount) + int(amount)
    curr.execute("UPDATE GROUPTRANSACTIONS SET amount ='{0}' WHERE(groupTransaction_id) IS '{1}'".format(new_amount,groupTransaction_id))
    conn.commit()
    conn.close()

def findGroupTransactionById(groupTransaction_id):
    transaction = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM GROUPTRANSACTIONS WHERE(groupTransaction_id) IS '{0}'".format(groupTransaction_id))
    transaction = curr.fetchone()
    conn.commit()
    conn.close()
    return transaction

def makeGroupTransaction(title,group_id):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("PRAGMA foreign_keys=ON")
    curr.execute("INSERT INTO GROUPTRANSACTIONS (title,group_id) VALUES(?,?)",
                 (title,group_id))
    curr.execute("SELECT last_insert_rowid()")
    newGroupTransaction = curr.fetchone()
    newGroupTransaction_id = newGroupTransaction[0]
    conn.commit()
    conn.close()
    return newGroupTransaction_id

def addPayerToGroupTransaction(groupTransaction_id,payer_id,amount):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("INSERT INTO GROUPTRANSACTIONS_PAYERS (groupTransaction_id,payer_id,amount) VALUES(?,?,?)",
                 (groupTransaction_id,payer_id,amount))
    conn.commit()
    conn.close()

def findAllPayerForGroupTransaction(groupTransaction_id):
    payers = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT payer_id,amount FROM GROUPTRANSACTIONS_PAYERS WHERE (groupTransaction_id) IS '{0}'".format(groupTransaction_id))
    payers = curr.fetchall()
    conn.commit()
    conn.close()
    return payers

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
    flag = 0
    curr.execute("PRAGMA foreign_keys=ON")
    try:
        curr.execute("INSERT INTO SHARES (share,groupTransaction_id,user_id) VALUES(?,?,?)",
                 (share,groupTransaction_id,user_id))
    except:
        flag = 1
    conn.commit()
    conn.close()
    return flag

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

def retrieveGroups():
    groups = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM GROUPS")
    groups = curr.fetchall()
    conn.close()
    return groups

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
    groups = retrieveGroups()
    print ('transaction_id    title  amount  sender_id   receiver_id')
    for i in groups:
        print (i)
    print ("Hello")
