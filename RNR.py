from flask import request
from estest import esSearch
from mongotest import verification

class RNR:
    def __init__(self):
        self.serviceKey = ''
        self.numOfCnt = 0
        self.rank = 0
        self.keyInTitle = ''
        self.keyInBody = ''
        self.writer = ''
        self.startDate = ''
        self.endDate = ''
        self.institution = ''
        self.category = ''

        # response
        self.resultCode = '000'
        self.resultMSG = 'No Result Code'

        self.response = {
            "response":{
                "header":{
                    "resultCode": self.resultCode,
                    "resultMSG": self.resultMSG,
                },
                "body": {}
                }
            }

    def raiseError(self, resultCode, resultMSG):
        self.response['response']['header']['resultCode'] = resultCode
        self.response['response']['header']['resultMSG'] = resultMSG

    def getRequest(self):
        self.serviceKey = request.args.get('serviceKey', "") 
        self.numOfCnt = request.args.get('numOfCnt', 100)
        self.rank = request.args.get('rank', 1)
        self.keyInTitle = request.args.get('keyInTitle',"")
        self.keyInBody = request.args.get('keyInBody',"")
        self.writers = request.args.get('writers')
        self.startDate = request.args.get('startDate')
        self.endDate = request.args.get('endDate')
        self.institution = request.args.get('institution')
        self.category = request.args.get('category')

        print(locals())
        if self.serviceKey=='':
            self.raiseError('400','Bad Request: No ServiceKey')
            return -1
        if self.keyInTitle=='':
            self.raiseError('400','Bad Request: No KeyInTitle')
            return -1

    def makeResponse(self):
        try: data = esSearch(self)
        except:
            self.raiseError('502','Bad Gateway')
            return -1

        if not verification(self.serviceKey):
            self.raiseError('401','Unauthorized')
            return -1
    
        self.response['response']['body'] = {
                "numOfCnt": self.numOfCnt,
                "totalCnt": data['hits']['total']['value'],
                "rank" : self.rank,
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

        if data['hits']['total']['value']==0:
            self.raiseError('204','No Content')
        else: self.raiseError('200', 'OK')
            
        
        #resultCode = '000'
        #resultMSG = 'Cannot Login, Check again your serviceKey'
        
    
    def do(self):
        if(not self.getRequest()):
            self.makeResponse()
        return self.response
