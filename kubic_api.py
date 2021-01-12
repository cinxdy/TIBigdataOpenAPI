from flask import request
from datetime import datetime
from dateutil.relativedelta import relativedelta
from kubic_user import *
from elasticsearch import Elasticsearch
import esAccount as esAcc

def makeRequest():
    kubic_request = {
        'serviceKey': request.args.get('serviceKey') ,
        'numOfCnt': request.args.get('numOfCnt', 100),
        'rank': request.args.get('rank', 1),
        'keyInTitle': request.args.get('keyInTitle',""),
        'keyInBody': request.args.get('keyInBody',""),
        'writer': request.args.get('writer',""),
        'startDate': request.args.get('startDate',(datetime.today()-relativedelta(years=1)).strftime("%Y%m%d")),
        'endDate': request.args.get('endDate',datetime.today().strftime("%Y%m%d")),
        'institution': request.args.get('institution',""),
        'category': request.args.get('category',""),
    }

    if kubic_request['serviceKey']=="":
        resultCode = 400
        resultMSG = 'Bad Request: No serviceKey'

    elif kubic_request['keyInTitle']=="":
        resultCode = 400
        resultMSG = 'Bad Request: No KeyInTitle'
    
    else:
        resultCode = 200
        resultMSG = 'OK'
    
    print("request:",kubic_request,'resultCode:',resultCode)
    return kubic_request, resultCode, resultMSG

def esSearch(request, host ='203.252.103.104', index='nkdb200803'):
    #Connect to DB
    #host = '203.252.112.14'
    #ES = Elasticsearch([{'host': host, 'port': '9200'}], http_auth=(esAcc.id, esAcc.password))
    
    ES = Elasticsearch(host = host, port=9200)

    print(ES.cat.indices())

    #search the document
    response = ES.search(index=index, body={
        "query": {
            "bool": {
                "must": [
                    { "match": { "post_title": request['keyInTitle'] } },
                    { "bool":{
                        "should": [
                            {"match": {"post_body": request['keyInBody']}},
                            {"match": {"post_writer": request['writer'] }},
                        ]
                    }
                    }

                    ],
                "filter": [{"range": { "indexed_datetime": { "gte": request['startDate'], "lte": request['endDate'] }}}]
            }
        }
    })
    print("response:",str(response)[:30])
    return response

def makeResponse(request, resultCode, resultMSG):
    response = {
            "header":{
                "resultCode": resultCode,
                "resultMSG": resultMSG,
            },
            "body": {}
        }
    if resultCode > 300:
        return response

    if not verification(request['serviceKey']):
        return raiseError(response, 401,'Unauthorized')

    try: data = esSearch(request)
    except Exception as e:
        print(e)
        return raiseError(response, 502,'Bad Gateway')
    print('origin data from ES:',data)

    if data['hits']['total']['value']==0:
        return raiseError(response, 204,'No Content')

    response['body'] = {
                "numOfCnt": request['numOfCnt'],
                "totalCnt": data['hits']['total']['value'],
                "rank" : request['rank'],
                "contents":[{
                    "title": content['_source']['post_title'],
                    "body": content['_source']['post_body'],
                    #' '.join(content['_source']['post_body'].split())[:400],
                    "writer": content['_source']['post_writer'],
                    "date" : content['_source']['post_date'],
                    "institution": content['_source']['published_institution'],
                    "institutionURL": content['_source']['published_institution_url'],
                    "category": content['_source']['top_category'],
                    "fileURL": content['_source']['file_download_url'] if 'file_download_url' in content['_source'].keys() else None,
                    "fileName": content['_source']['file_name'] if 'file_name' in content['_source'].keys() else None,
                    #content['_source']['file_download_url'],
                }for content in data['hits']['hits']]
                }
    print(str(response)[:30])
    return response

def raiseError(response, resultCode, resultMSG):
    response['header']['resultCode'] = resultCode
    response['header']['resultMSG'] = resultMSG
    return response

#    
##class kubic_request:
#    def __init__(self):
#        #request
#        #self.serviceKey = ''
#        self.numOfCnt = 100
#        self.rank = 1
#        #self.keyInTitle = ''
#        #self.keyInBody = ''
#        #self.writer = ''
#        self.startDate = datetime.today()-relativedelta(years=1)
#        self.endDate = datetime.today()
#        #self.institution = ''
#        #self.category = ''
#        print("startdate:"+self.startDate+", enddate:" + self.endDate)
#
#    def getRequest(self):
#        self.serviceKey = request.args.get('serviceKey') 
#        self.numOfCnt = request.args.get('numOfCnt')
#        self.rank = request.args.get('rank')
#        self.keyInTitle = request.args.get('keyInTitle')
#        self.keyInBody = request.args.get('keyInBody')
#        self.writers = request.args.get('writers')
#        self.startDate = request.args.get('startDate')
#        self.endDate = request.args.get('endDate')
#        self.institution = request.args.get('institution')
#        self.category = request.args.get('category')
#
#        if self.serviceKey=='':
#            return 400,'Bad Request: No KeyInTitle'
#        if self.keyInTitle=='':
#            return 400,'Bad Request: No KeyInTitle'
#        return 200,'OK'
##
#
#class kubic_response:
#    def __init__():
#        #self.response = {
#            #"response":{
#            #    "header":{
#            #        "resultCode": self.resultCode,
#            #        "resultMSG": self.resultMSG,
#            #    },
#            #    "body": self.body
#            #    }
#            #}
#
#        self.resultCode = '000'
#        self.resultMSG = 'No Result Code'
#        self.body = {
#                "numOfCnt": ,
#                "totalCnt": ,
#                "rank" : ,
#                "contents":
#                }
#
#    
##    def raiseError(self, resultCode, resultMSG,):
##        self.resultCode = resultCode
##        self.resultMSG = resultMSG
##        self.makeResponse()
##
##        #self.response['response']['header']['resultCode'] = resultCode
##        #self.response['response']['header']['resultMSG'] = resultMSG
#
#    
#    def makeResponse(self, resultCode, resultMSG):
#            #print("input serviceKey:"+self.serviceKey)
#            if not verification(self.serviceKey):
#                self.raiseError('401','Unauthorized')
#                return -1
#
#            try: data = esSearch(self)
#            except:
#                self.raiseError('502','Bad Gateway')
#                return -1
#
#
#        self.response['response']['body'] = {
#                "numOfCnt": self.numOfCnt,
#                "totalCnt": data['hits']['total']['value'],
#                "rank" : self.rank,
#                "contents":[{
#                    "title": content['_source']['post_title'],
#                    "body": content['_source']['post_body'],
#                    #' '.join(content['_source']['post_body'].split())[:400],
#                    "writer": content['_source']['post_writer'],
#                    "date" : content['_source']['post_date'],
#                    "institution": content['_source']['published_institution'],
#                    "institutionURL": content['_source']['published_institution_url'],
#                    "category": content['_source']['top_category'],
#                    "fileURL": content['_source']['file_download_url'] if 'file_download_url' in content['_source'].keys() else None,
#                    "fileName": content['_source']['file_name'] if 'file_name' in content['_source'].keys() else None,
#                    #content['_source']['file_download_url'],
#                }for content in data['hits']['hits']]
#                }
#
#        if data['hits']['total']['value']==0:
#            self.raiseError('204','No Content')
#        else: self.raiseError('200', 'OK')
#            
#    
#    def do(self):
#        if(not self.getRequest()):
#            self.makeResponse()
#        return self.response
#