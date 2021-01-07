from elasticsearch import Elasticsearch

def esSearch(request, host ='203.252.103.104', index='nkdb200803'):
    #Connect to DB
    #host = '203.252.112.15'
    ES = Elasticsearch(hosts=host)
    
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