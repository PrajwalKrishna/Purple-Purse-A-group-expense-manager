from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)
from signature import *
from login import *

@app.route('/success/<name>')
def success(name):
    return ' %s' % name

@app.route('/users/<user_id>/userAddTransaction')
def addTransaction(user_id):
    print 'hello world'
    print user_id
    return render_template('addTransaction.html')

@app.route('/addTransactionToData',methods = ['POST','GET'])
def addTransactionToData():
    print "hi there is hope left"
    if request.method == 'POST':
        #try:
            name = request.form['nm']
            sender_id = int(request.form['sender'])
            receiver_id = int(request.form['receiver'])
            amount = int(request.form['amt'])
            insertTransaction(name,amount,sender_id,receiver_id)
            msg = "Added successfully"
        #except:
        #    msg = "Unsuccessful"
        #finally:
            return (redirect(url_for('success',name = msg)))

@app.route('/users/<user_id>/passbook')
def renderPassbook(user_id):
    user_name = findUserByUser_Id(user_id)[1]
    transactions = findAllTransactionByUser_Id(user_id)
    return render_template('passbook_maker.html',transactions = transactions,user_name = user_name)

if __name__ == '__main__':
    app.run(debug = True)
