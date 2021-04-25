from elasticsearch import Elasticsearch
import esAccount as esAcc
from kubic_user import *

def ESConnection():
    ES = Elasticsearch(
        [esAcc.host],
        http_auth=(esAcc.id, esAcc.password),
        scheme="https",
        port=19200,
        verify_certs=False
    )
    return ES, esAcc.index

ES, index = ESConnection()

def simple_search(request):
    # search the keyword in the document
    print(request)
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

def search_in_my_doc(request):
    idList = getMyDocByEmail()
    query = {
    "size": request['numOfCnt'],
    "query": {
        "bool": {
            "must":[ {"wildcard": {"post_title": "*"+request['keyInTitle']+"*" }},
            ],
            # "sort": [{"post_date": {"order" : "desc" #오름차순: asc, 내림차순: desc 
            # }}]    
            "filter": [
                # {"range": { "post_date": { "gte": request['startDate'], "lte": request['endDate'] }}},
                {"terms": {"_id": idList}}, 
            ],
        }
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

def retrieve_all(request):
    query = {
        "from" : request['page'] * request['numOfCnt'] +1,
        "size": int(request['numOfCnt']),
    }
    response = ES.search(index=esAcc.index, body=query)
    return response

def esSearch(searchType, request):
    if searchType=='simple_search': return simple_search(request)
    elif searchType=='detailed_search': return detailed_search(request)
    elif searchType=='my_doc': return search_in_my_doc(request)
    elif searchType == 'retrieve_all': return retrieve_all(request)
    else: return None