from flask import request
from datetime import datetime
from dateutil.relativedelta import relativedelta
from kubic_user import *
from kubic_function import *

ES, index = ESConnection()

def makeRequest():

    keyList = ['serviceKey','numOfCnt','rank','keyword','keyInTitle','keyInBody','writer','startDate','endDate','institution','category' ]
    
    for k in request.args.keys():
        if not k in keyList:
            resultCode = 400
            resultMSG = 'Bad Request: ' + k
            return {}, resultCode, resultMSG
    
    if not 'serviceKey' in request.args:
        resultCode = 400
        resultMSG = 'Bad Request: No serviceKey'
        return {}, resultCode, resultMSG

    elif not 'keyword' in request.args and not 'keyInTitle' in request.args:
        resultCode = 400
        resultMSG = 'Bad Request: No keyInTitle'
        return {}, resultCode, resultMSG

    kubic_request = {
        'serviceKey': request.args.get('serviceKey') ,
        'numOfCnt': request.args.get('numOfCnt', 100),
        'rank': request.args.get('rank', 1),
        'keyword': request.args.get('keyword',""),
        'keyInTitle': request.args.get('keyInTitle',""),
        'keyInBody': request.args.get('keyInBody',""),
        'writer': request.args.get('writer',""),
        'startDate': request.args.get('startDate',(datetime.today()-relativedelta(years=1)).strftime("%Y-%m-%d")),
        'endDate': request.args.get('endDate',datetime.today().strftime("%Y-%m-%d")),
        'institution': request.args.get('institution',""),
        'category': request.args.get('category',""),
    }

    resultCode = 200
    resultMSG = 'OK'
    
    return kubic_request, resultCode, resultMSG

def simple_search(request):
    # search the keyword in the document
    response = ES.search(index=index, body={    
    "size": request['numOfCnt'],
    "query": {
      "multi_match": {
        "query": request['keyword'],
        "fields": ["post_title", "post_body", "fileName", "fileContent", "file_extracted_content"]
      }
    }
  })
    return response

def detailed_search(request):
    query = {
    "size": request['numOfCnt'],
    "query": {
        "bool": {
            "must":[
                {"wildcard": {"post_title": "*"+request['keyInTitle']+"*" }},
            ],
            # "sort": [{"post_date": {"order" : "desc" #오름차순: asc, 내림차순: desc 
            # }}]    
            "filter": {"range": { "post_date": { "gte": request['startDate'], "lte": request['endDate'] }}}
        },
    }
    }

    if not request['keyInBody'] == "":
        query['query']['bool']['must'].append({"wildcard": {"post_body": "*"+request['keyInBody']+"*" }})
    if not request['writer'] == "":
        query['query']['bool']['must'].append({"wildcard": {"post_writer": "*"+request['writer']+"*" }})
    if not request['institution'] == "":
        query['query']['bool']['must'].append({"wildcard": {"published_institution": "*"+request['institution']+"*" }})
    
    print("query: ",query)
    response = ES.search(index=esAcc.index, body=query)

    # print("response:",str(response)[:30])
    return response

def esSearch(searchType, request):
    return {'simple_search': simple_search(request), 'detailed_search': detailed_search(request) }[searchType]
    
def raiseError(response, resultCode, resultMSG, searchType='all'):
    response['header']['resultCode'] = resultCode
    response['header']['resultMSG'] = resultMSG
    return response

def makeResponse(request, resultCode, resultMSG, searchType):
    response = {
        "header":{
            "resultCode": resultCode,
            "resultMSG": resultMSG,
        },
        "body": {},
    }

    if resultCode != 200:
        return response

    _id = verification(request['serviceKey'])
    if not _id:
        return raiseError(response, 401,'Unauthorized')
        
    if not limitDate(_id):
        return raiseError(response, 401,'Expired')
    
    if not limitTraffic(_id):
        return raiseError(response, 401,'Overused')

    try: data = esSearch(searchType, request)

    except Exception as e:
        print(e)
        return raiseError(response, 502,'Bad Gateway')
    # print('origin data from ES:',data)

    if data['hits']['total']['value']==0:
        return raiseError(response, 204,'No Content')

    def slicingBody(content):
        try:
            post_body = ' '.join(content['_source']['post_body'].split())
            if len(post_body) > 200:
                post_body = post_body[:200]
            return post_body
        except:
            return content['_source']['post_body']
    response['body'] = {
                "numOfCnt": request['numOfCnt'],
                "totalCnt": data['hits']['total']['value'],
                "rank" : request['rank'],
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
    
    raiseTraffic(_id, request['numOfCnt'] if request['numOfCnt'] < data['hits']['total']['value'] else data['hits']['total']['value'])
    return response