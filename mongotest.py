
from pymongo import MongoClient
from bson.objectid import ObjectId

from secrets import token_urlsafe 
from passlib.hash import pbkdf2_sha512
import datetime

client = MongoClient('localhost',27017)
userdb = client["user"]

def makeCode():    
    key = token_urlsafe(16)
    hashKey = pbkdf2_sha512.hash(key)
    return hashKey

def addApiUser(email):
    now = datetime.datetime.now().date()

    post = {
        "app_name" : input("app_name>"),
        "app_purpose" : input("app_purpose>"),
        "user_email" : email,
        "veri_code" : makeCode(),
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
    userdb.apiUser.insert_one(post)
