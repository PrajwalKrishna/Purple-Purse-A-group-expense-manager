# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)
from signature import *
from login import *

@app.route('/success/<name>')
def success(name):
    return ' %s' % name

@app.route('/users/<user_id>/userAddTransaction')
def addTransaction(user_id):
    return render_template('addTransaction.html')

@app.route('/addTransactionToData',methods = ['POST','GET'])
def addTransactionToData():
    if request.method == 'POST':
        name = request.form['nm']
        sender_id = int(request.form['sender'])
        receiver_id = int(request.form['receiver'])
        amount = int(request.form['amt'])
        return_value = insertTransaction(name,amount,sender_id,receiver_id)
        if return_value is 1:
            msg = 'success'
        elif return_value is -1:
            msg = 'sender_id does not exist'
        else:
            msg = 'receiver_id does not exist'
        return (redirect(url_for('success',name = msg)))

@app.route('/<user_id>/addFriends',methods = ['POST','GET'])
def addFriends(user_id):
    if request.method == 'POST':
        name = request.form['friend']
        user = findUserByEmail(name)
        if user:
            friend_id = user[0]
            insertFriend(user_id,friend_id)
            return redirect(url_for('renderHome',user_id = user_id))
        else:
            return redirect(url_for('success',name = "Not valid email"))

@app.route('/users/<user_id>/passbook')
def renderPassbook(user_id):
    user_name = findUserByUser_Id(user_id)[1]
    transactions = findAllTransactionByUser_Id(user_id)
    return render_template('passbook_maker.html',transactions = transactions,user_name = user_name)

@app.route('/<user_id>/makeGroupForm')
def renderMakeGroupForm(user_id):
    return render_template('makeGroupForm.html',user = user_id)

@app.route('/establishMembership',methods = ['POST','GET'])
def establishMembership():
    if request.method == 'POST':
        email = request.form['email']
        group_id = request.form['group_id']
        user = findUserByEmail(email)
        if user:
            user_id = user[0]
            makeMember(group_id,user_id)
        return (redirect("/group/{}".format(group_id)))

@app.route('/makeGroup',methods = ['POST','GET'])
def makeGroup():
    if request.method == 'POST':
        name = request.form['name']
        creator = request.form['creator']
        group_id = addNewGroup(name)
        makeMember(group_id,creator)
        return (redirect("/group/{}".format(group_id)))

@app.route('/group/<group_id>')
def renderGroup(group_id):
    group = findGroupById(group_id)
    members = findAllMembersForGroup(group_id)
    return render_template("group_home.html",name = group[2],memberList = members,group_id = group[0])

if __name__ == '__main__':
    app.run(debug = True)
