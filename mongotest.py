
from pymongo import MongoClient
from secrets import token_urlsafe 
from passlib.hash import pbkdf2_sha512
import datetime
import logging

client = MongoClient('localhost',27017)
db = client.user

def getEmail():
    email_logined = "21800409@handong.edu"
    #app.logger.debug('getEmail():'+'email_logined:'+email_logined)
    return email_logined

def generateCode():
    key = token_urlsafe(16)
    hashKey = pbkdf2_sha512.hash(key)
    #app.logger.debug('generateCode:'+"key"+key+"hashKey"+hashKey)
    return key, hashKey

def registerAPI(email_logined, app_name, app_purpose):
    now = datetime.datetime.now().date()
    key, hashKey = generateCode()

    post = {
        "app_name" : app_name,
        "app_purpose" : app_purpose,
        "user_email" : email_logined,
        "veri_code" : hashKey,
        "reporting_date" : {
            'year': int(now.strftime('%y')),
            'month': int(now.strftime('%m')),
            'date': int(now.strftime('%d'))
            },
        "expiration_date" : {
            'year': int(now.strftime('%y'))+1,
            'month': int(now.strftime('%m')),
            'date': int(now.strftime('%d'))
            },
        "traffic":0
    }

    db.apiUser.insert_one(post)
    #app.logger.debug('registerAPI():'+'email_logined:'+email_logined+'post:'+str(post)+'key:'+key)
    return key

def reissue(_id):
    now = datetime.datetime.now().date()
    key, hashKey = generateCode()

    post = {
        "veri_code" : hashKey,
        "reporting_date" : {
            'year': int(now.strftime('%y')),
            'month': int(now.strftime('%m')),
            'date': int(now.strftime('%d'))
            },
        "expiration_date" : {
            'year': int(now.strftime('%y'))+1,
            'month': int(now.strftime('%m')),
            'date': int(now.strftime('%d'))
            },
    }

    db.apiUser.update({'_id':_id}, post)
    #app.logger.debug('reissue():'+'_id:'+_id+'post:'+str(post)+'key:'+key)
    return key

def getInform(email_logined):
    doc = db.apiUser.find({"user_email": email_logined})
    #app.logger.debug('getInform():'+'email_logined:'+email_logined+'doc:'+str(doc))
    return doc

def findHash(email_logined):
    doc = getInform(email_logined)
    hashKeyList = [item['veri_code'] for item in doc]
    #app.logger.debug('findHash():'+'email_logined:'+email_logined+'hashKeyList:'+str(hashKeyList))
    return hashKeyList

def verification(serviceKey, hashKeyList):
    for hashKey in hashKeyList:
        if(pbkdf2_sha512.verify(serviceKey, hashKey)):
            return True
    return False

