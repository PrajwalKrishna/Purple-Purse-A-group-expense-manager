# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)
from signature import *
from login import *

def verifyGroupLogin(group_id):
    member_ids = findAllMemberIdsForGroup(group_id)
    flag  = False
    for i in member_ids:
        if session['user_id'] == int(i[0]):
            flag = True
    return flag

@app.route('/success/<name>')
def success(name):
    return ' %s' % name

@app.route('/users/<user_id>/userAddTransaction')
def addTransaction(user_id):
    if session['user_id']== int(user_id):
        return render_template('addTransaction.html')
    else:
        return redirect('/signIn')

@app.route('/transaction/<transaction_id>')
def renderTransaction(transaction_id):
    previous_transaction = findTransactionById(transaction_id)
    if session['user_id'] == int(previous_transaction[5]) or session['user_id'] == int(previous_transaction[6]):
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
    else:
        return redirect('/signIn')

@app.route('/addCommentToTransaction',methods = ['POST'])
def addCommentToTransaction():
    comment = request.form['comment']
    transaction_id = request.form['transaction_id']
    transactions = findTransactionById(transaction_id)
    if session['user_id'] == int(transactions[5]) or session['user_id'] == int(transactions[6]):
        changeCommentToTransaction(comment,transaction_id)
        return redirect('/transaction/'+str(transaction_id))
    else:
        return redirect('/signIn')

@app.route('/<transaction_id>/deleteTransaction')
def deleteTransactionByUser(transaction_id):
    transactions = findTransactionById(transaction_id)
    if session['user_id'] == transactions[5] or session['user_id'] == transaction_id:
        deleteTransaction(transaction_id)
        return (url_for('success',name = 'Successfully Deleted'))
    else:
        return redirect('/signIn')

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
    if session['user_id'] == int(user_id):
        if request.method == 'POST':
            name = request.form['friend']
            user = findUserByEmail(name)
            if user:
                friend_id = user[0]
                insertFriend(user_id,friend_id)
                return redirect(url_for('renderHome',user_id = user_id))
            else:
                return redirect(url_for('success',name = "Not valid email"))
    else:
        return redirect('/signIn')

@app.route('/users/<user_id>/passbook')
def renderPassbook(user_id):
    if session['user_id'] == int(user_id):
        user_name = findUserByUser_Id(user_id)[1]
        transactions = findAllTransactionByUser_Id(user_id)
        result = []
        for i in transactions:
            if int(user_id) == i[6]:
                user = findUserByUser_Id(i[5])
                result.append([[i[2],i[1],user[1],i[3]],i[0]])
            else:
                user = findUserByUser_Id(i[6])
                result.append([[i[2]*-1,i[1],user[1],i[3]],i[0]])
        return render_template('passbook_maker.html',transactions = result,user_name = user_name)
    else:
        return redirect('/signIn')

@app.route('/<user_id>/makeGroupForm')
def renderMakeGroupForm(user_id):
    if session['user_id'] == int(user_id):
        return render_template('makeGroupForm.html',user = user_id)
    else:
        return redirect('/signIn')

@app.route('/establishMembership',methods = ['POST','GET'])
def establishMembership():
    if request.method == 'POST':
        email = request.form['email']
        group_id = request.form['group_id']
        user = findUserByEmail(email)
        if verifyGroupLogin(group_id):
            if user:
                user_id = user[0]
                makeMember(group_id,user_id)
            return (redirect("/group/{}".format(group_id)))
        else:
            return redirect('/signIn')

@app.route('/makeGroup',methods = ['POST','GET'])
def makeGroup():
    if request.method == 'POST':
        name = request.form['name']
        creator = request.form['creator']
        if session['user_id'] == int(creator):
            group_id = addNewGroup(name)
            makeMember(group_id,creator)
            return (redirect("/group/{}".format(group_id)))
        else:
            return redirect('/signIn')

@app.route('/<group_id>/members/<user_id>')
def renderMember(group_id,user_id):
    return redirect(url_for('success',name = group_id+user_id))

@app.route('/group/<group_id>')
def renderGroup(group_id):
    if verifyGroupLogin(group_id):
        group = findGroupById(group_id)
        members = findAllMembersForGroupHomeRendering(group_id)
        transactions = findAllTransactionsForGroup(group_id)
        return render_template("group_home.html",name = group[2],memberList = members,transactionList = transactions,group_id = group[0])
    else:
        return redirect('/signIn')

@app.route('/groups/addGroupTransaction',methods = ['POST'])
def addGroupTransaction():
    name = request.form['groupTransactionName']
    group_id = request.form['group_id']
    if verifyGroupLogin(group_id):
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
    else:
        return redirect('/signIn')

@app.route('/execGroupTransaction',methods = ['POST'])
def execGroupTransaction():
    groupTransaction_id = request.form['groupTransaction_id']
    groupTransaction = findGroupTransactionById(groupTransaction_id)
    group_id = groupTransaction[2]
    if verifyGroupLogin(group_id):
        group = findGroupById(group_id)
        title = groupTransaction[1]+"("+group[2]+")"
        temp = findAllMemberIdsForGroup(group_id)
        member_ids = []
        members = []
        for i in temp:
            member_ids.append(i[0])
            members.append([i[0],0,0,'true'])
        total_amount = 0
        email_passer = request.form['email_passer']
        total_amount_recieved = request.form['amount_passer']
        new_email = []
        flag = []
        payer = []
        new_amount = []
        payer_details = []
        for i in email_passer:
            if i == '(':
                new_email = []
                flag = 0
                new_amount = []
            elif i == '#':
                flag = 1
            elif i ==')':
                flag = 3
                new_email = ''.join(new_email)
                new_amount = ''.join(new_amount)
                payer = findUserByEmail(new_email)
                payer_details.append([payer,new_amount])
            elif flag == 0:
                new_email.append(i)
            elif flag == 1:
                new_amount.append(i)


        for i in payer_details:
            payer_id = int(i[0][0])
            amount = int(i[1])
            total_amount += amount
            addPayerToGroupTransaction(groupTransaction_id,payer_id,amount)
            for j in members:
                if j[0]==payer_id:
                    j[2] -= int(amount)
                    break

        print ("Shape of Love")
        k = 1
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

        print ("Shape of You")
        payer_iterator  = 0
        addToGroupTransactionAmount(groupTransaction_id,total_amount)
        dividends = total_amount/total_shares
        print (payer_details[0][1])
        print ("Shape of Water")
        for i in members:
            if i[3]:
                i[2] += dividends * i[1]
            if i[2]>0:
                while True:
                    print ("ENter")
                    print (i)
                    print (payer_iterator)
                    if i[2] <= int(payer_details[payer_iterator][1]):
                        insertTransaction(title,i[2],int(payer_details[payer_iterator][0][0]),i[0])
                        payer_details[payer_iterator][1] = int(payer_details[payer_iterator][1]) - i[2]
                        break
                    else:
                        insertTransaction(title,int(payer_details[payer_iterator][1]),int(payer_details[payer_iterator][0][0]),i[0])
                        i[2] -= int(payer_details[payer_iterator][1])
                        payer_iterator += 1
                addToMembershipAmount(i[0],group_id,i[2])
        return redirect(url_for('success',name = "Happy"))
    else:
        return redirect('/signIn')

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
