from flask import Flask,render_template,request,session,redirect,jsonify,url_for,flash
import pymysql.cursors
import hashlib
from werkzeug.utils import secure_filename
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
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
            return redirect(url_for("index"))
        except:
            flash("Sign Up Unsuccessful!")
            return redirect(url_for("signup"))

@app.route("/",methods=['GET', 'POST'])
def login():

    if 'loggedin' in session:
        return("hey")
    if request.method == 'GET':
        return render_template('index.html')
    
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
                return redirect(url_for('dashboard'))

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        filename='static/missing/'+filename
        file.save(filename)    
        # Taking the data from the form
        arr_id = request.form['arr_id']
        Unit_id = request.form['Unit_id']
        district_Name = request.form['district_Name']
        Unit_name = request.form['Unit_name']
        FIRNo = request.form['FIRNo']
        FIR_Date = request.form['FIR_Date']
        Complainant_Name = request.form['Complainant_Name']
        Complainant_Relation = request.form['Complainant_Relation']
        Date_Of_Missing = request.form['Date_Of_Missing']


        try:
            with connection.cursor() as cursor:
                cursor.execute("insert into missing (pic_url) values(%s)",(filename))
        except:

            print("YAyyyyy")   
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True,threaded=False)

    