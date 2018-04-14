import sqlite3 as sql
conn = sql.connect("database.db")
curr = conn.cursor()
curr.execute('''create table USERS (
                  user_id integer primary key autoincrement,
                  name text not null,
                  email text not null unique,
                  password text not null)''')

curr.execute('''create table TRANSACTIONS (
                transaction_id integer primary key autoincrement,
                title text not null,
                amount int not null,
                comment text,
                status int default 0,
                sender_id integer not null,
                receiver_id integer not null,
                FOREIGN KEY(sender_id)
                    REFERENCES USERS(user_id)
                FOREIGN KEY(receiver_id)
                    REFERENCES USERS(user_id)
                )''')

#curr.execute('''create table
 #            ''')
curr.close()
