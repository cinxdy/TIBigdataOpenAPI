import urllib.request as r
import urllib.parse as p
import json
import pandas as pd
import ssl

url = "https://kubic.handong.edu:15000/retrieve_all?"
serviceKey = "QyEqZtZ1vC-MNfq_NgsBEQ"
numOfCnt = 200
page = 3

option = "serviceKey="+serviceKey
request = ""
# request = "&numOfCnt="+p.quote(str(numOfCnt))+"&page="+p.quote(str(page))
url_full = url + option + request

print("url>"+url_full+"numOfCnt="+"10")
context = ssl._create_unverified_context()
response = r.urlopen(url_full,context=context).read().decode('utf-8')
print(response)

jsonArray = json.loads(response) 

if jsonArray.get("header").get("resultCode") != 200:
    print("Error!!!")
    print(jsonArray.get("header"))
    quit()

items =jsonArray.get("body").get("contents")
print("items>", items)

df = pd.DataFrame(columns=['title','body','writer','date','category','institution','file'])
for item in items:
    df = df.append(item,ignore_index=True)
print(df)