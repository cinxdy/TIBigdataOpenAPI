
from pymongo import MongoClient
client = MongoClient('kubic.handong.edu',27017)
db = client.user

email_logined = "21600280@handong.edu"
doc = db.mydocs.find_one({"userEmail": email_logined})
print(doc)
print("myDoc:", doc['savedDocIds'])