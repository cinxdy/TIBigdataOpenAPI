from flask import Flask, jsonify, request, Response, render_template, abort
from flask_restful import Resource, Api
from secrets import token_urlsafe
from passlib.hash import pbkdf2_sha512
import json
from kubic_user import *
from kubic_api import *
import logging

app = Flask(__name__)
app.secret_key = 'random string'
logging.basicConfig(filename='./logs/2021-01-27.log')
key_saved =0 
@app.route('/', methods=['GET','POST'])
@app.route('/mainPage', methods=['GET','POST'])
def index():
    global key_saved
    if request.method == 'POST':
        # id = request.form['email']
        id = request.get_json().get('email')
        print("IP:", request.remote_addr)
        print("ID:", id)
        key = token_urlsafe(8)
        print("key:", key)
        key_saved = key
        return key, 200
    if request.method == 'GET':
        print("IP:", request.remote_addr)
        id = request.args.get("K",'')
        print("ID:", id)

    if key_saved == id:
        print("Success!")
        return render_template('mainPage.html')
    else: abort(403)

@app.route('/myInform')
def myInform():
    count = countAPI()
    return render_template('myInform.html',email=email_logined,count=count)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        app_name = request.form['app_name']
        app_purpose = request.form['app_purpose']
        authKey = registerAPI(app_name,app_purpose)
        #매크로 차단하는 기능 추가 예정
        return render_template('register.html',app_name=app_name,app_purpose=app_purpose, authKey = authKey)
    return render_template('register.html')

@app.route('/management', methods=['GET','POST'])
def management():
    if request.method == 'POST':
        _id = request.form['reissue']
        print("_id",_id)
        authKey = reissue(_id)
        return render_template('management.html', doc=getInform(), authKey = authKey)
    return render_template('management.html', doc=getInform())

@app.route('/api')
def api():
    #get HTTP request and check validity
    request, resultCode, resultMSG = makeRequest()
    response = makeResponse(request, resultCode, resultMSG)

    #print(response)
    return json.dumps(response,ensure_ascii = False)

if __name__== "__main__":
    app.run(host='0.0.0.0', debug=True)