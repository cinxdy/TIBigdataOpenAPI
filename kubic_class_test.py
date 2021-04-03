from kubic_user import *
from kubic_data import *
from flask import request

class kubic_api:
    def __init__(self, searchType):
        self.searchType = searchType
        self.resultCode = 200

        rs = self.setRequest()
        if rs != 200:
            self.response = rs
        else: 
            self.response = self.setResponse()
    
    def raiseError(self, resultCode, resultMSG):
        self.resultCode = resultCode
        self.response = {
            "header":{
                "resultCode": resultCode,
                "resultMSG": resultMSG,
            },
            "body": {},
        }
        return self.response
        
    def setRequest(self):
        if self.searchType == 'simple_search':
            keyList = ['serviceKey', 'numOfCnt', 'rank','keyword']
        elif self.searchType == 'detailed_search' or self.searchType == 'my_doc':
            keyList = ['serviceKey','numOfCnt','rank','keyword','keyInTitle','keyInBody','writer','startDate','endDate','institution','category' ]
        else: return self.raiseError(502,'Bad Gateway')

        for k in request.args.keys():
            if not k in keyList:
                return self.raiseError(400,'Bad Request: ' + k)
        
        if not 'serviceKey' in request.args:
            return self.raiseError(400,'Bad Request: No serviceKey')

        elif not 'keyword' in request.args and not 'keyInTitle' in request.args:
            return self.raiseError(400,'Bad Request: No keyInTitle')
        
        if self.searchType == 'simple_search':
            self.request = {                    
                'serviceKey': request.args.get('serviceKey') ,
                'numOfCnt': request.args.get('numOfCnt', 100),
                'rank': request.args.get('rank', 1),
                'keyword': request.args.get('keyword')
            }
        else:
            self.request = {
                'serviceKey': request.args.get('serviceKey') ,
                'numOfCnt': request.args.get('numOfCnt', 100),
                'rank': request.args.get('rank', 1),
                'keyInTitle': request.args.get('keyInTitle',""),
                'keyInBody': request.args.get('keyInBody',""),
                'writer': request.args.get('writer',""),
                'startDate': request.args.get('startDate',(datetime.today()-relativedelta(years=1)).strftime("%Y-%m-%d")),
                'endDate': request.args.get('endDate',datetime.today().strftime("%Y-%m-%d")),
                'institution': request.args.get('institution',""),
                'category': request.args.get('category',""),
            }
        return 200

    def setResponse(self):
        _id = verification(self.request['serviceKey'])
        if not _id:
            return self.raiseError(401,'Unauthorized')
            
        if not limitDate(_id):
            return self.raiseError(401,'Expired')
        
        if not limitTraffic(_id):
            return self.raiseError(401,'Overused')

        try: data = esSearch(self.searchType, self.request)
        except Exception as e:
            print("esSearch() exception:", e)
            return self.raiseError(502,'Bad Gateway')
        
        # print('origin data from ES:',data)

        if data['hits']['total']['value']==0:
            return self.raiseError(204,'No Content')

        def slicingBody(content):
            try:
                post_body = ' '.join(content['_source']['post_body'].split())
                if len(post_body) > 200:
                    post_body = post_body[:200]
                return post_body
            except:
                return content['_source']['post_body']

        self.response = self.raiseError(200, 'OK')
        self.response['body'] = {
                    "numOfCnt": self.request['numOfCnt'],
                    "totalCnt": data['hits']['total']['value'],
                    "rank" : self.request['rank'],
                    "contents":[{
                        "title": content['_source']['post_title'],
                        "body": 
                        # content['_source']['post_body'],
                        slicingBody(content) if 'post_body' in content['_source'].keys() else None,
                        "writer": content['_source']['post_writer'],
                        "date": content['_source']['post_date'] if 'post_date' in content['_source'] else None,
                        "institution": content['_source']['published_institution'],
                        "institutionURL": content['_source']['published_institution_url'],
                        "category": content['_source']['top_category'],
                        "fileURL": content['_source']['file_download_url'] if 'file_download_url' in content['_source'].keys() else None,
                        "fileName": content['_source']['file_name'] if 'file_name' in content['_source'].keys() else None,
                        #content['_source']['file_download_url'],
                    }for content in data['hits']['hits']]
                    }
        
        raiseTraffic(_id, self.request['numOfCnt'] if self.request['numOfCnt'] < data['hits']['total']['value'] else data['hits']['total']['value'])
        return self.response