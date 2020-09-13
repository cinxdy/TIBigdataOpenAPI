from flask import Flask, jsonify, request, Response, render_template
from flask_restful import Resource, Api
from elasticsearch import Elasticsearch
import json

app = Flask(__name__)

#import socket
#def get_ip_address():
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    s.connect(("8.8.8.8", 80))
#    return s.getsockname()[0]

#serverUrl = get_ip_address()  # '192.168.0.110'
#if(serverUrl != "http://203.252.112.15:9200"):
#    serverUrl="http://localhost:9200"
#else:
serverUrl = "203.252.112.14"
print(serverUrl)

# ElasticSearch connection
es = Elasticsearch(hosts=serverUrl, port=9200)
print(es)
print (es.cat.indices())
index_name='nkdb200913'

word = '통일'
res = es.search(index=index_name, body={"query": {"match":{"post_body":word}}})

@app.route('/')
def index():
    return render_template('main.html', response=res)


if __name__== "__main__":
    app.run(host='0.0.0.0',debug=True)