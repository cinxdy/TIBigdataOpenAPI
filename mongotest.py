
from pymongo import MongoClient
from secrets import token_urlsafe 
from passlib.hash import pbkdf2_sha512
import datetime

client = MongoClient('localhost',27017)
db = client.user
email_logined = "cindy@handong.edu"

def getEmail():
    pass

def generateCode():
    key = token_urlsafe(16)
    hashKey = pbkdf2_sha512.hash(key)
    return key, hashKey

def registerAPI(app_name, app_purpose):
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
    print(post)
    db.apiUser.insert_one(post)
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

    print(post)
    db.apiUser.update({'_id':_id}, post)
    return key

def getInform():
    doc = db.apiUser.find({"user_email": email_logined})
#    print(doc[0]['app_name'])
    return doc

def findHash():
    doc = db.apiUser.find({"user_email":email_logined})
    hashKeyList = [item['veri_code'] for item in doc]
    print(hashKeyList)
    return hashKeyList

def verification(serviceKey, hashKeyList):
    for hashKey in hashKeyList:
        if(pbkdf2_sha512.verify(serviceKey, hashKey)):
            return True
    return False

