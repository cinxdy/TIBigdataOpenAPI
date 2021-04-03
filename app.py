from flask import Flask, render_template, abort, session, redirect, url_for
# from flask_restful import Resource, Api
# from secrets import token_urlsafe
# from passlib.hash import pbkdf2_sha512
import json
from kubic_user import *
from kubic_api import *
# from kubic_all import *
import kubic_ssl
import logging
from kubic_class_test import kubic_api

app = Flask(__name__)
app.secret_key = 'random string'

# logging.basicConfig(filename='./logs/2021-01-27.log')
key_saved =0 
@app.route('/', methods=['GET','POST'])
@app.route('/mainPage', methods=['GET','POST'])
def index():
    global key_saved
    if request.method == 'POST':
        id = request.get_json().get('email')
        ip = request.remote_addr
        key = token_urlsafe(8)

        session['id'] = id
        session['ip'] = ip
        session['key'] = key

        print("ID:", id)
        print("IP:", ip)
        print("key:", key)

        return key, 200

    if request.method == 'GET':
        ip = request.remote_addr
        key = request.args.get("K",'')

        if 'id' in session:
            print("ID:", session['id'])
        print("IP:", ip)
        print("key:", key)        
        
        # if session['key'] == key:   
            # print("Success!")
            # session['veri'] = True
        return render_template('mainPage.html')
    else: abort(403)

@app.route('/document')
def document():
    return render_template('document.html')

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
    if request.method == 'POST' and 'reissue' in request.form :
        _id = request.form['reissue']
        # print("_id",_id)
        authKey = reissue(_id)
        return render_template('management.html', email=email_logined, count =countAPI(), doc=getDocByEmail(), authKey = authKey)
    return render_template('management.html', email=email_logined, count =countAPI(), doc=getDocByEmail())

@app.route('/<search_name>')
def test(search_name):
    kubic = kubic_api(search_name)
    return json.dumps(kubic.response, ensure_ascii = False)

# @app.route('/all')
# def all():
#     #get HTTP request and check validity
#     request, resultCode, resultMSG = makeRequest()
#     print("request:",request,'resultCode:',resultCode)
    
#     response = makeResponse(request, resultCode, resultMSG)
    
#     print("responseCode:",response['header']['resultCode'])
#     # print("response:", response['body'])
#     return json.dumps(response, ensure_ascii = False)

# @app.route('/simple_search')
# def simplesearch():
#     print("simple_search>>>")
#     request, resultCode, resultMSG = makeRequest()
#     print("request:",request,'resultCode:',resultCode)
    
#     response = makeResponse(request, resultCode, resultMSG)

#     print("responseCode:",response['header']['resultCode'])
#     return json.dumps(response, ensure_ascii = False)

# @app.route('/detailed_search')
# def detailed_search():
    
#     #get HTTP request and check validity
#     request, resultCode, resultMSG = makeRequest()
#     print("request:",request,'resultCode:',resultCode)
    
#     response = makeResponse(request, resultCode, resultMSG, 'detailed_search')
    
#     print("responseCode:",response['header']['resultCode'])
#     # print("response:", response['body'])
#     return json.dumps(response, ensure_ascii = False)

# @app.route('/my_doc')
# def mydoc():
#     #get HTTP request and check validity
#     request, resultCode, resultMSG = makeDocRequest()
#     print("request:", request, 'resultCode:', resultCode)
    
#     response = makeDocResponse(request, resultCode, resultMSG)
    
#     print("responseCode:",response['header']['resultCode'])
#     # print("response:", response['body'])
#     return json.dumps(response, ensure_ascii = False)

if __name__== "__main__":
    context=(kubic_ssl.crt,kubic_ssl.key)
    app.run(host='0.0.0.0', debug=True, port=15000, ssl_context=context)