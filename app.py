from flask import Flask, jsonify, request, Response, render_template
from flask_restful import Resource, Api
from elasticsearch import Elasticsearch
from secrets import token_urlsafe
from passlib.hash import pbkdf2_sha512
import json
from mongotest import *

app = Flask(__name__)

@app.route('/')
@app.route('/mainPage')
def index():
    return render_template('mainPage.html')

@app.route('/myInform')
def myInform():
    return render_template('myInform.html',doc=getInform())

#@app.route('/Register')
#def index():
#    return render_template('Register.html')
#
#    
#@app.route('/Management')
#def index():
#    return render_template('Management.html')



key = token_urlsafe(16)
hashKey = pbkdf2_sha512.hash(key)
@app.route('/Key')
def generateKey():
    return key

@app.route('/api')
def api():
    secretKey = request.args.get('secretKey',"")
    title = request.args.get('title',"")
    body = request.args.get('body',"")
    
    if pbkdf2_sha512.verify(secretKey, hashKey):
        return "search for:"+title +"-"+ body
    return "cannot login"

if __name__== "__main__":
    app.run(host='127.0.0.1',debug=True)