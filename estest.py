from elasticsearch import Elasticsearch

#Connect to DB
serverUrl = "203.252.103.104"
print(serverUrl)
es = Elasticsearch(hosts=serverUrl, port=9200)
print (es.cat.indices())
index_name="nkdb200803"

def esSearch(request):
    #search the document
    res = es.search(index=index_name, body={
        "query": {
            "bool": {
                "must": [
                    { "match": { "post_title": request.title } },
                    { "match": { "post_body": request.body } }
                ]
            }
        }
    })
    return res

