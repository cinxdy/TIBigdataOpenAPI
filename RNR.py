from flask import request

class requestAPI:
    serviceKey = ''
    numOfCnt = 0
    rank = 0
    title = ''
    body = ''
    writer = ''
    startDate = ''
    endDate = ''
    institution = ''
    category = ''

    def __init__(self):
        self.serviceKey = request.args.get('serviceKey', "")
        self.numOfCnt = request.args.get('numOfCnt', 100)
        self.rank = request.args.get('rank', 1)
        self.title = request.args.get('title',"")
        self.body = request.args.get('body',"")
        self.writers = request.args.get('writers')
        self.startDate = request.args.get('startDate')
        self.endDate = request.args.get('endDate')
        self.institution = request.args.get('institution')
        self.category = request.args.get('category')

class responseAPI:
    response = {}
    
    resultCode = 0
    resultMSG = ''
    body = {}
    #numOfCnt = 0
    #totalCnt = 0
    #rank = 0
    #title = ''
    #body = ''
    #writer = ''
    #date = ''
    #institution = ''
    #institutionURL = ''
    #category = ''
    #fileURL = ''

    def __init__(self, veri, request, data):
        if veri == True:
            self.resultCode = '200'
            self.resultMSG = 'OK'
            self.body = {
                    "numOfCnt": request.numOfCnt,
                    "totalCnt": data['hits']['total']['value'],
                    "rank" : request.rank,
                    "contents":[{
                        "title": content['_source']['post_title'],
                        "body": content['_source']['post_body'],
                        "writer": content['_source']['post_writer'],
                        "date" : content['_source']['post_date'],
                        "institution": content['_source']['published_institution'],
                        "institutionURL": content['_source']['published_institution_url'],
                        "category": content['_source']['top_category'],
                        #"fileURL": content['_source']['file_download_url'],
                    } 
                    for content in data['hits']['hits']]
                }
        else:
            self.resultCode = '000'
            self.resultMSG = 'Cannot Login, Check again your serviceKey'
        
        self.response = {
            "response":{
                "header":{
                    "resultCode": self.resultCode,
                    "resultMSG": self.resultMSG,
                },
                "body": self.body
            }
        }
    
