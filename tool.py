import sqlite3 as sql
conn = sql.connect("database.db")
curr = conn.cursor()
curr.execute('''
             PRAGMA foreign_key = ON
             ''')
curr.execute('''create table USERS (
                  user_id integer primary key autoincrement,
                  name text not null,
                  email text not null unique,
                  password text not null,
                  total_balance integer default 0,
                  unapproved_balance integer default 0,
                  approved_balance integer default 0,
                  friends text default ",")''')

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

curr.execute('''create table GROUPS(
             group_id integer primary key autoincrement,
             creator_id integer,
             name text not null
             )''')

curr.execute('''create table MEMEBERSHIP(
             group_id integer not null,
             user_id integer not null,
             amount integer default 0,
             FOREIGN KEY(user_id)
                 REFERENCES USERS(user_id)
             FOREIGN KEY(group_id)
                 REFERENCES GROUPS(group_id)
             UNIQUE('group_id', 'user_id')
            )''')

curr.execute('''create table GROUPTRANSACTIONS(
             groupTransaction_id integer primary key autoincrement,
             title text not null,
             group_id integer not null,
             amount integer default 0,
             FOREIGN KEY(group_id)
                 REFERENCES GROUPS(group_id)
            )''')

curr.execute('''create table GROUPTRANSACTIONS_PAYERS(
             groupTransaction_id integer not null,
             payer_id integer not null,
             amount integer default 0,
             FOREIGN KEY(payer_id)
                REFERENCES USERS(user_id)
             FOREIGN KEY(groupTransaction_id)
                REFERENCES GROUPTRANSACTIONS(groupTransaction_id)
             )''')

curr.execute('''create table SHARES(
             share integer not null default 1,
             user_id integer not null,
             groupTransaction_id integer not null,
             FOREIGN KEY(user_id)
                 REFERENCES USERS(user_id)
             FOREIGN KEY(groupTransaction_id)
                 REFERENCES GROUPTRANSACTIONS(groupTransaction)
             UNIQUE ('groupTransaction_id','user_id')
             )''')

curr.close()
