
from pymongo import MongoClient
from bson.objectid import ObjectId
from secrets import token_urlsafe 
from passlib.hash import pbkdf2_sha512
from datetime import datetime
from dateutil.relativedelta import relativedelta
#import logging

client = MongoClient('localhost',27017)
db = client.user
trafficLimit = 3000

def getEmail():
    email_logined = "21800409@handong.edu"
    return email_logined

email_logined = getEmail()

def countAPI():
    count = db.apiUser.count({"user_email": email_logined})
    return count

def generateCode():
    key = token_urlsafe(16)
    hashKey = pbkdf2_sha512.hash(key)
    return key, hashKey

def registerAPI(app_name, app_purpose):
    today = datetime.today()
    key, hashKey = generateCode()

    post = {
        "app_name" : app_name,
        "app_purpose" : app_purpose,
        "user_email" : email_logined,
        "veri_code" : hashKey,
        "reporting_date" : today,
        "expiration_date" : (today+relativedelta(years=1)),
        "traffic":0
    }

    db.apiUser.insert_one(post)
    return key

def reissue(_id):
    today = datetime.today()
    key, hashKey = generateCode()

    post = {
        "app_name" : "testtesttest",
        "veri_code" : hashKey,
        "reporting_date" : today,
        "expiration_date" : (today+relativedelta(years=1)),
        }

    db.apiUser.update({"_id": ObjectId(_id)}, {'$set': post})
    print("reissue> app_name", post['app_name'],"key", key)
    return key

def getDocByEmail():
    docList = db.apiUser.find({"user_email": email_logined})
    return docList

def getDocById(_id):
    doc = db.apiUser.find_one({"_id": ObjectId(_id)})
    return doc

def findHash():
    doc = getDocByEmail()
    hashKeyList = [item['veri_code'] for item in doc]
    return hashKeyList

def verification(serviceKey):
    hashKeyList = findHash()
    for hashKey in hashKeyList:
        if(pbkdf2_sha512.verify(serviceKey, hashKey)):
            doc = db.apiUser.find_one({"veri_code": hashKey})
            return doc['_id']
    return False

def limitTraffic(_id):
    doc = getDocById(_id)
    if doc['traffic'] > trafficLimit:
        return False
    return True

def limitDate(_id):
    doc = getDocById(_id)
    if doc['expiration_date'] < datetime.today():
        return False
    return True

def raiseTraffic(_id, numOfCnt):
    doc = getDocById(_id)
    post = {"traffic" : doc['traffic']+numOfCnt}
    db.apiUser.update({"_id": ObjectId(_id)}, {'$set':post})
    doc = getDocById(_id)
    print(doc)

def getMyDocByEmail():
    doc = db.mydocs.find_one({"userEmail": email_logined})
    print(doc) 
    print("myDoc:", doc['savedDocIds'])
    return doc['savedDocIds']