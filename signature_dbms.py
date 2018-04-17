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

def findFriends(user_id):
    user = findUserByUser_Id(user_id)
    friendList = user[7].split(",")
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
