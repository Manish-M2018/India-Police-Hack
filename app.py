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
    print('Logout')
    return render_template('index.html')

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
def index():
    if 'loggedin' in session:
        print("hi")
        return redirect(url_for('index'))
    if request.method == 'GET':
        print("hiiiii")
        return render_template('index.html')
    
@app.route('/login',methods=['POST'])
def login():
    email = request.form['log_email']
    password = request.form['log_psw']
    phash=hashlib.md5(password.encode())
    phash=phash.hexdigest()
    print("Yyyyyyyyyyyyyyyyyyyyyy")

    with connection.cursor() as cursor:
        cursor.execute("select * from users where email=%s",email)
        myresult = cursor.fetchone()
        print(myresult)
        if(myresult):
            if(phash==myresult['password']):
                #init the session variables
                print(myresult)
                session['u_id']=myresult['u_id']
                session['station_name']=myresult['station_name']
                session['loggedin']=True
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect login credentials")
                return redirect(url_for('index'))         


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        found= 0
        path = request.files['path']
        filename = secure_filename(path.filename)
        path_name = filename
        filename='static/missing/'+filename
        path.save(filename)    
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
        Person_Name = request.form['Person_Name']
        Perm_Address1 = request.form['Perm_Address1']
        Sex = request.form['Sex']
        Age	 = request.form['Age']
        Height = request.form['Height']
        Build = request.form['Build']
        Complextion = request.form['Complextion']
        Face = request.form['Face']
        Colour = request.form['Colour']
        Hair = request.form['Hair']
        Language_sp = request.form['Language_sp']
        Dress_Description = request.form['Dress_Description']
        ID_Marks = request.form['ID_Marks']
        Phisical_Pecularities = request.form['Phisical_Pecularities']
        Phone = request.form['Phone']
        Email = request.form['Email']
        crime_no = request.form['crime_no']


        try:
            with connection.cursor() as cursor:
                cursor.execute("insert into missing (arr_id,Unit_id,district_Name,Unit_name,FIRNo,FIR_Date,Complainant_Name,Complainant_Relation,Date_Of_Missing,Person_Name,Perm_Address1,Sex,Age,Height,Build,Complextion,Face,Colour,Hair,Language_sp,Dress_Description,ID_Marks,Phisical_Pecularities,Phone,Email,path,crime_no,found) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(arr_id,Unit_id,district_Name,Unit_name,FIRNo,FIR_Date,Complainant_Name,Complainant_Relation,Date_Of_Missing,Person_Name,Perm_Address1,Sex,Age,Height,Build,Complextion,Face,Colour,Hair,Language_sp,Dress_Description,ID_Marks,Phisical_Pecularities,Phone,Email,path_name,crime_no,found))
        except Exception as e:
            print(e)   
            print("Noooooooooooooooooooooooooooo")
    return redirect(url_for('dashboard'))


@app.route('/found',methods=['GET','POST'])
def found():
    return render_template('found.html')

@app.route('/upload_found',methods=['GET','POST'])
def upload_found():
    if request.method == 'POST': 
        path = request.files['path']
        filename = secure_filename(path.filename)
        path_name = filename
        filename='static/found/'+filename
        path.save(filename)  
    try:
        with connection.cursor() as cursor:
            print("Vinodddddddddddddddddddddddddd")
            sql_req="select u_id from users where u_id="
            print(sql_req)
            print(session['u_id'])
            sql_req=sql_req+str(session['u_id'])
            cursor.execute(sql_req)
            res = cursor.fetchone()
            print("res")
            print(res)
            r_id = res['u_id']
            print("r_id")
            print(r_id)
            cursor.execute("insert into found (f_url,u_id) values(%s)",(path_name,r_id))      
    except Exception as e:
        print(e)  
    return redirect(url_for('found'))    

if __name__ == "__main__":
    app.run(debug=True,threaded=False)

    