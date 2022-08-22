import requests

response = requests.post(url = "http://localhost:15000/", json = {"email":"21800409@handong.edu"} )
print("response:", response, response.text)
key = response.text
response = requests.get(url= "http://localhost:15000?K="+key)
print("response:", response)


