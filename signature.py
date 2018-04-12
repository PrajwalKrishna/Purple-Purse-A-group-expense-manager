from signature_dbms import *
from flask import Flask,render_template,redirect,request,url_for

app = Flask(__name__)

@app.route('/signIn')
def index():
    return render_template('signIn.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['enm']
        password = request.form['password']
        user = findUserByEmail(email)
        if user:
            if str(password) == str(user[3]):
                return (redirect(url_for('success',name=user[1])))
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
