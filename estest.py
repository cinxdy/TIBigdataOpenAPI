from elasticsearch import Elasticsearch
import esAccount as esAcc

def esSearch(request, host ='203.252.103.104', index='nkdb200803'):
    #Connect to DB
    host = '203.252.112.14'
    ES = Elasticsearch([{'host': host, 'port': '9200'}], http_auth=(esAcc.id, esAcc.password)
    
    #search the document
    #res = ES.search(index=index)
    res = ES.search(index=index, body={
        "query": {
            "bool": {
                "must": [
                    { "match": { "post_title": request.keyInTitle } },
                    { "match": { "post_body": request.keyInBody } }
                ]
            }
        }
    })
    print(res)
    return res
host = '203.252.112.14'
print(Elasticsearch([{'host': host, 'port': '9200'}], http_auth=('elastic', 'epp2020')).cat.indices())