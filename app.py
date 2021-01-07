from flask import Flask, jsonify, request, Response, render_template
from flask_restful import Resource, Api
from secrets import token_urlsafe
from passlib.hash import pbkdf2_sha512
import json
from mongotest import *
from RNR import *

app = Flask(__name__)
app.secret_key = 'random string'

@app.route('/')
@app.route('/mainPage')
def index():
    return render_template('mainPage.html')

@app.route('/myInform')
def myInform():
    count = db.apiUser.count({"user_email": email_logined})
    return render_template('myInform.html',email=email_logined,count=count)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        app_name = request.form['app_name']
        app_purpose = request.form['app_purpose']
        authKey = registerAPI(app_name,app_purpose)
        return render_template('register.html',app_name=app_name,app_purpose=app_purpose, authKey = authKey)

    return render_template('register.html')

@app.route('/management', methods=['GET','POST'])
def management():
    if request.method == 'POST':
        _id = request.form['reissue']
        authKey = reissue(_id)
        return render_template('management.html', doc=getInform(), authKey = authKey)
    return render_template('management.html',doc=getInform())

@app.route('/api')
def api():
    rnr = RNR()
    response = rnr.do()
    print(response)
    return json.dumps(response,ensure_ascii = False)

if __name__== "__main__":
    app.run(host='0.0.0.0', debug=True)