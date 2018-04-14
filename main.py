from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)
from signature import *

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/addTransaction/')
def new_Transaction():
    if request.method == 'POST':
        try:
            name = request.form['nm']
            sender_id = int(request.form['sender'])
            receiver_id = int(request.form['receiver'])
            amount = int(request.form['amt'])
            insertUser(name,sender,receiver,amt)
            msg = "Added successfully"
        except:
            msg = "Unsuccessful"
        finally:
            return (redirect(url_for('success',name = msg)))

@app.route('/user/<name>')
def renderForUser():
    pass

if __name__ == '__main__':
    app.run(debug = True)
