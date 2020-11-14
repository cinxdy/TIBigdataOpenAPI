from flask import Flask, jsonify, request, Response, render_template
from flask_restful import Resource, Api
from secrets import token_urlsafe
from passlib.hash import pbkdf2_sha512
import json
from mongotest import *
from estest import *
import RNR

app = Flask(__name__)

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
    elif request.method == 'GET':
        app_name = request.args.get('app_name')
        app_purpose = request.args.get('app_purpose')
    
    if app_name == None or app_purpose == None :
        return render_template('register.html')

    authKey = registerAPI(app_name,app_purpose)
    return render_template('register.html',app_name=app_name,app_purpose=app_purpose, authKey = authKey)

@app.route('/management')
def management():
    return render_template('management.html',doc=getInform())

@app.route('/api')
def api():
    request = requestAPI()
    data = esSearch(request)
    res = responseForm(data)

    return render_template('api.html', response=res)
    
    if pbkdf2_sha512.verify(secretKey, hashKey):
        return render_template('api.html', response=res)
    return "cannot login"

if __name__== "__main__":
    app.run(host='0.0.0.0',debug=True)
