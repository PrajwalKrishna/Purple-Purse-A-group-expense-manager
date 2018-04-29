from signature_dbms import *
from flask import Flask,render_template,redirect,request,url_for,session

app = Flask(__name__)

@app.route('/signIn')
def index():
    return render_template('signIn.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['enm']
        password = request.form['password']
        password = hasher(password)
        print (email)
        user = findUserByEmail(email)
        if user:
            if str(password) == str(user[3]):
                #session['logged_in'] = True
                #session['user_id'] =  user[0]
                return (redirect(("/users/{}").format(user[0])))
            else:
                return (redirect(url_for('success',name="sahi password de "+
                                         str(user[3])+str(password))))
        else:
            return (redirect(url_for('success',name = "Error no such user")))


@app.route('/signUp')
def new_student():
   return render_template('signUp.html')

@app.route('/users/<user_id>')
def renderHome(user_id):
    user = findUserByUser_Id(user_id)
    return render_template("user_home.html",name=user[1],email=user[2],
                           user_id=user[0],total_balance=user[4],
                           approved_balance=user[6],unapproved_balance=user[5],
                           friendList=findFriends(user_id),groupList=findAllGroupsForUser(user_id))


@app.route('/addUser',methods = ['POST','GET'])
def addUser():
    verify = None
    if request.method == 'POST':
        try:
            name = request.form['nm']
            email = request.form['enm']
            password = request.form['password']
            print (name,email,password)
            verify = insertUser(name,email,password)
            msg = "Added successfully"
        except:
            msg = "Unsuccessful try again later"
        finally:
            if verify is not None:
                user = findUserByEmail(email)
                print ("hi")
                return (redirect(("/users/{}").format(user[0])))
            else:
              return (redirect(url_for('success',name =
                                       "Account for Email already exist")))
