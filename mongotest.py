
from pymongo import MongoClient

client = MongoClient('203.252.112.15',27017)
print("success to connect")
print(client)
userdb = client["user"]
print(userdb)
collection = userdb["users"]

for r in collection.find({}):
    print(r)
