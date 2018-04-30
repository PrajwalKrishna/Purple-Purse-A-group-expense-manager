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

@app.route('/transaction/<transaction_id>')
def renderTransaction(transaction_id):
    previous_transaction = findTransactionById(transaction_id)
    name = previous_transaction[1]
    amount = previous_transaction[2]
    reciver = findUserByUser_Id(previous_transaction[6])
    reciver_name = reciver[1]
    reciver_email = reciver[2]
    sender = findUserByUser_Id(previous_transaction[5])
    sender_name = sender[1]
    sender_email = sender[2]
    comments = previous_transaction[3]
    return render_template("renderTransaction.html",name = name,amount = amount,
                           reciver = reciver_name,sender = sender_name,comments = comments,
                           reciver_email = reciver_email,sender_email = sender_email,transaction_id =transaction_id)

@app.route('/addCommentToTransaction',methods = ['POST'])
def addCommentToTransaction():
    comment = request.form['comment']
    transaction_id = request.form['transaction_id']
    changeCommentToTransaction(comment,transaction_id)
    return redirect('/transaction/'+str(transaction_id))

@app.route('/<transaction_id>/deleteTransaction')
def deleteTransactionByUser(transaction_id):
    deleteTransaction(transaction_id)
    return (url_for('success',name = 'Successfully Deleted'))

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
    result = []
    for i in transactions:
        user = findUserByUser_Id(i[5])[1]
        result.append([[i[2],i[1],user,i[3]],i[0]])
    return render_template('passbook_maker.html',transactions = result,user_name = user_name)

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
    members = findAllMembersForGroupHomeRendering(group_id)
    transactions = findAllTransactionsForGroup(group_id)
    return render_template("group_home.html",name = group[2],memberList = members,transactionList = transactions,group_id = group[0])

@app.route('/groups/addGroupTransaction',methods = ['POST'])
def addGroupTransaction():
    name = request.form['groupTransactionName']
    group_id = request.form['group_id']
    groupTransaction_id = makeGroupTransaction(name,group_id)
    member_ids = findAllMemberIdsForGroup(group_id)
    payer_ids = findAllPayerForGroupTransaction(group_id)
    members = []
    payers = []
    for i in member_ids:
        user = findUserByUser_Id(i[0])
        members.append([user[1],user[2]])
    for i in payer_ids:
        payer = findUserByUser_Id(i[0])
        payers.append([user[1],user[2],i[1]])
    return render_template("addGroupTransaction.html",memberList = members,name = name ,payerList = payers,groupTransaction_id = groupTransaction_id)

@app.route('/execGroupTransaction',methods = ['POST'])
def execGroupTransaction():
    groupTransaction_id = request.form['groupTransaction_id']
    groupTransaction = findGroupTransactionById(groupTransaction_id)
    group_id = groupTransaction[2]
    group = findGroupById(group_id)
    title = groupTransaction[1]+"("+group[2]+")"
    temp = findAllMemberIdsForGroup(group_id)
    member_ids = []
    members = []
    for i in temp:
        member_ids.append(i[0])
        members.append([i[0],0,0,'true'])
    total_amount = 0
    payer_email = request.form['email']
    payer_id = findUserByEmail(payer_email)[0]
    amount = request.form['amount']
    addPayerToGroupTransaction(groupTransaction_id,payer_id,amount)
    for i in members:
        if i[0]==payer_id:
            i[2] -= int(amount)
            break

    total_amount+=int(amount)
    k=1
    total_shares=0
    for i in members:
        include = []
        shares = request.form['share'+str(k)]
        include = request.form.getlist('member'+str(k))
        i[3] = include
        if include:
            i[1]=int(shares)
            total_shares+=int(shares)
            makeShare(int(shares),groupTransaction_id,i[0])
        k = k + 1

    dividends = total_amount/total_shares
    for i in members:
        if i[3]:
            i[2] += dividends * i[1]
        if i[2]:
            insertTransaction(title,i[2],payer_id,i[0])
    return redirect(url_for('success',name = "Happy"))

@app.route('/addPayer',methods = ['POST'])
def addASinglePayer():
    email = request.form['email']
    user = findUserByEmail(email)
    if user:
        user_id = user[0]
    addPayerToGroupTransaction(group_id,user_id,amount)
    return render_template("addGroupTransaction.html",memberList = members)

if __name__ == '__main__':
    app.run(debug = True)
