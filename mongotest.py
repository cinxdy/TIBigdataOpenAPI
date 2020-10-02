
from pymongo import MongoClient

client = MongoClient('localhost',27017)
userdb = client["user"]
collection = userdb["users"]

for r in collection.find():
    print(r)
