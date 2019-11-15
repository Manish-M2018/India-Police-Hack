from flask import Flask,render_template,request,session,redirect,jsonify,url_for,flash
import pymysql.cursors
import hashlib
from werkzeug.utils import secure_filename
app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='policehack',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    password=request.form['sgn_psw']
    station_name=request.form['station_name']
    email=request.form['sgn_email']
    phash=hashlib.md5(password.encode())
    phash=phash.hexdigest()
    with connection.cursor() as cursor:
        try:
            cursor.execute("insert into users (station_name,email,password) values(%s,%s,%s)",(station_name,email,phash))
            return redirect(url_for("login"))
        except:
            flash("Sign Up Unsuccessful!")
            return redirect(url_for("signup"))

@app.route("/login",methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return("hey")
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form['log_email']
    password = request.form['log_psw']
    phash=hashlib.md5(password.encode())
    phash=phash.hexdigest()

    with connection.cursor() as cursor:
        cursor.execute("select * from users where email=%s",email)
        myresult = cursor.fetchone()
        if(myresult):
            if(phash==myresult['password']):
                #init the session variables
                session['u_id']=myresult['u_id']
                session['station_name']=myresult['station_name']
                session['loggedin']=True
                return("heyyyy!!!!")


if __name__=="__main__":
    app.run(debug=True,threaded=False)