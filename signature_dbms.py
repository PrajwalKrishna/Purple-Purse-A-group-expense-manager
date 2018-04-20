import sqlite3 as sql
import hashlib

def create_connection(database):
    try:
        conn = sql.connect(database)
        return conn;
    except:
        print ("Cannot access database")

def hasher(password):
    password_en = password.encode()
    hashed = hashlib.sha384(password_en)
    hash_paso = hashed.hexdigest()
    return hash_paso

def insertUser(name,email,password):
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("PRAGMA foreign_keys=ON;")
    try:
        curr.execute("INSERT INTO USERS (name,email,password) VALUES(?,?,?)",(name,email,hasher(password)))
    except sql.IntegrityError as e:
        print("Account already exists")
        return None
    conn.commit()
    conn.close()
    return email

def findUserByUser_Id(id):
    query = None
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM USERS WHERE user_id is '{}'".format(id))
    query = curr.fetchone()
    conn.close()
    return query

def findUserByEmail(email):
    query=None
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute("SELECT * FROM USERS WHERE email = '{}'".format(email))
    query = curr.fetchone()
    conn.close()
    return query

def findAllTransactionBetween(user_id,friend_id):
    query = []
    conn = create_connection("database.db")
    curr = conn.cursor()
    curr.execute(("SELECT * FROM TRANSACTIONS WHERE sender_id is '{0}' AND receiver_id is '{1}'".format(user_id,friend_id)))
    query = curr.fetchall()
    curr.execute(("SELECT * FROM TRANSACTIONS WHERE sender_id is '{0}' AND receiver_id is '{1}'".format(friend_id,user_id)))
    query2 = curr.fetchall()
    for i in query2:
        query.append(i)
    conn.close()
    return query

def findBalanceBetween(user_id,friend_id):
    transactions = findAllTransactionBetween(user_id,friend_id)
    balance = 0
    for i in transactions:
        if str(i[5]) == str(user_id):
            balance -= i[2]
        else:
            balance += i[2]
    return balance

def findFriends(user_id):
    user = findUserByUser_Id(user_id)
    friends = user[7].split(",")
    friendList = []
    for i in friends:
        if not i:
            continue
        friend = findUserByUser_Id(i)
        toAdd = [friend[1],friend[2],findBalanceBetween(user_id,i)]
        friendList.append(toAdd)
    return friendList

def retrieveUsers():
	conn = create_connection("database.db")
	curr = conn.cursor()
	curr.execute("SELECT name, email,password FROM USERS")
	users = curr.fetchall()
	conn.close()
	return users

'''
friends = db.Table('friends',
db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(50), index=True, unique= True)
   email = db.Column(db.String(50),index=True, unique= True)


   is_friend = db.relationship('User', #defining the relationship, User is left side entity
        secondary = friends,
        primaryjoin = (friends.c.user_id == id),
        secondaryjoin = (friends.c.friend_id == id),
        backref = db.backref('friends', lazy = 'dynamic'),
        lazy = 'dynamic'
    )
'''
