from flask import Flask, render_template, abort, session, redirect, url_for, request
from flask_cors import CORS
# from flask_restful import Resource, Api
# from secrets import token_urlsafe
# from passlib.hash import pbkdf2_sha512
import json
from kubic_user import *
from kubic_api import *
from kubic_email import *
# from kubic_all import *
import kubic_ssl
import logging
from kubic_class import kubic_api

from time import time

app = Flask(__name__)
app.secret_key = 'random string'
CORS(app)

# logging.basicConfig(filename='./logs/2021-01-27.log')
key_saved =0 

# @app.before_request
# def before_request(request):
    # id = request.form['email']
    # ip = request.remote_addr
    # key = token_urlsafe(8)

    # session['id'] = id
    # session['ip'] = ip
    # session['key'] = key

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route('/', methods=['GET','POST'])
@app.route('/mainPage', methods=['GET','POST'])
def home():
    return "Server is running normally"
# def index():
#     global key_saved
#     if request.method == 'POST':
#         id = request.get_json().get('email')
#         ip = request.remote_addr
#         key = token_urlsafe(8)

#         session['id'] = id
#         session['ip'] = ip
#         session['key'] = key

#         print("ID:", id)
#         print("IP:", ip)
#         print("key:", key)

#         return key, 200

#     if request.method == 'GET':
#         ip = request.remote_addr
#         key = request.args.get("K",'')

#         if 'id' in session:
#             print("ID:", session['id'])
#         print("IP:", ip)
#         print("key:", key)        
        
#         # if session['key'] == key:   
#             # print("Success!")
#             # session['veri'] = True
#         return render_template('mainPage.html')
#     else: abort(403)

# @app.route('/document')
# def document():
#     return render_template('document.html')

# @app.route('/register', methods=['GET','POST'])
@app.route('/register', methods=['POST'])
def register():
    # if request.remote_addr != '127.0.0.1':
    #     abort(403)
    if request.method == 'POST':
        email = request.form['email']
        session['id']=email
        app_type = request.form['app_type']
        app_name = request.form['app_name']
        app_purpose = request.form['app_purpose']

        if app_type=='public':
            authKey = registerAPI('public',app_name,app_purpose)
            return {'authKey':authKey}
        elif app_type=='private':
            key = preRegisterAPI(email, app_name, app_purpose)
            send_veri_email(email, app_name, app_purpose, key)
            return {'authKey': 'success'}
        return {'authKey': 'fail'}
        # return render_template('register.html',app_name=app_name,app_purpose=app_purpose, authKey = authKey)
    return redirect(home)

# @app.route('/registerManual', methods=['GET','POST'])
# def registerManual():
#     email = request.args.get('email')
#     # app_type = request.form['app_type']
#     app_name = request.args.get('app_name')
#     app_purpose = request.args.get('app_purpose')

#     return {'succeed':True}

    # accept = request.args.get('accept')
    # if(accept):
        # authKey = registerAPI('private', app_name,app_purpose)
        # send_info_email(session['id'], app_name, app_purpose, authKey)
        # return '정상 승인 처리되었습니다.'
    # else: 
        # return render_template('refuse.html',app_name=app_name,app_purpose=app_purpose, authKey = authKey)
        # reason = request.args.get('reason')
        # send_refuse_email(session['id'], app_name, app_purpose, reason)
        # return '정상 반려 처리되었습니다.'

@app.route('/acceptPreUser', methods=['GET','POST'])
def registerManual():
    if request.method == 'GET':
        key = request.args.get('key')
        email, app_name, app_purpose = getPreuserInfoByKey(key)
        docList = getDocListPreUser()
        return render_template('accept.html', email = email, app_name=app_name,app_purpose=app_purpose, key=key, docList=docList)

    elif request.method == 'POST': # post
        key = request.form['key']
        accept = int(request.form['accept'])
        reason = request.form['reason']
        if reason == None: return '사유를 입력해주세요. 처리되지 않았습니다.'

        email, app_name, app_purpose = getPreuserInfoByKey(key)
        session['id'] = email
        updatePreuserInfoByKey(key, accept, reason)

        if accept:
            authKey = registerAPI('private',app_name,app_purpose)
            send_info_email(email, app_name, app_purpose, authKey)
        else:
            send_refuse_email(email, app_name, app_purpose, reason)
        return '정상처리되었습니다'


@app.route('/reissue', methods=['POST'])
def reissue():
    session['id'] = request.form['email']
    _id = request.form['_id']
    authKey = reissueAPI(_id)
    return {'authKey':authKey}

@app.route('/delete', methods=['POST'])
def deleteAPIs():
    _id = request.form['_id']
    succeed = deleteAPI(_id)    
    return {'succeed':succeed}


@app.route('/<search_name>')
def api(search_name):
    start = time()

    kubic = kubic_api(search_name)
    print("Ip:", request.remote_addr)
    # print("Date:", request.date) # None으로 뜸
    # print("Request:", request.args)
    print("Execution Time:", time() - start)
    return json.dumps(kubic.response, ensure_ascii = False)


# @app.route('/management', methods=['GET','POST'])
# def management():
#     # if request.remote_addr != '127.0.0.1':
#     #     abort(403)
#     if request.method == 'POST' and 'reissue' in request.form :
#         _id = request.form['reissue']
#         # print("_id",_id)
#         authKey = reissue(_id)
        
#         # return {authKey:authKey}
#         return render_template('management.html', email=email_logined, count =countAPI(), doc=getDocByEmail(), authKey = authKey)
#     return render_template('management.html', email=email_logined, count =countAPI(), doc=getDocByEmail())


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