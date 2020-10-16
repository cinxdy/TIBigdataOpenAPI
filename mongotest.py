
from pymongo import MongoClient
from secrets import token_urlsafe 
from passlib.hash import pbkdf2_sha512
import datetime

client = MongoClient('localhost',27017)
db = client.user

email_logined = "cindy@handong.edu"

def makeCode():
    key = token_urlsafe(16)
    hashKey = pbkdf2_sha512.hash(key)
    return hashKey

def login(email,password):
    doc = db.users.find_one({"email": email})
    #print(doc)
    if doc != None and password == doc['password']:
        email_logined = email
        return "Login Succeeded"
    return "Login Failed"

def register():
    now = datetime.datetime.now().date()

    post = {
        "app_name" : input("app_name>"),
        "app_purpose" : input("app_purpose>"),
        "user_email" : email_logined,
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
    db.apiUser.insert_one(post)

def getInform():
    doc = db.apiUser.find({"email": email_logined})
    return doc

if __name__ == "__main__":
    email_try = input()
    password_try = input()
    
    print(login(email_try,password_try))
    print(getInform())
