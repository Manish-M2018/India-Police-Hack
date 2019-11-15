from flask import Flask,render_template,request,session,redirect,jsonify,url_for,flash
import pymysql.cursors
import hashlib
from keras.preprocessing import image
from werkzeug.utils import secure_filename
app =Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='pulmacare',
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