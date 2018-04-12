from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__)
from signature import *

'''@app.route('/signIn')
def index():
    return render_template('signIn.html')
'''
@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name
'''
@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['enm']
        password = request.form['password']
        user = findUserByEmail(email)
        if user:
            if str(password) == str(user[3]):
                return (redirect(url_for('success',name=user[2])))
            else:
                return (redirect(url_for('success',name="sahi password de "+str(user[3])+str(password))))
        else:
            return (redirect(url_for('success',name = "Error no such user")))


@app.route('/signUp')
def new_student():
   return render_template('signUp.html')

@app.route('/addUser',methods = ['POST','GET'])
def addUser():
    if request.method == 'POST':
        try:
            name = request.form['nm']
            email = request.form['enm']
            password = request.form['password']
            insertUser(name,email,password)
            msg = "Added successfully"
        except:
            msg = "Unsuccessful"
        finally:
            return (redirect(url_for('success',name = msg)))
'''

if __name__ == '__main__':
    app.run(debug = True)
