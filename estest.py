
from elasticsearch import Elasticsearch

def esSearch(title,body):
    serverUrl = "203.252.103.104"
    print(serverUrl)
    es = Elasticsearch(hosts=serverUrl, port=9200)
    print(es)
    print (es.cat.indices())

    index_name="nkdb200803"

    res = es.search(index=index_name, body={
        "query": {
            "bool": {
                "must": [
                    { "match": { "post_title": title } },
                    { "match": { "post_body": body } }
                ]
            }
        }
    })
    return res
#return render_template('main.html', response=res)