import esAccount as esAcc
from elasticsearch import Elasticsearch


host = '203.252.112.14'
ES = Elasticsearch([{'host': host, 'port': '19200'}], http_auth=(esAcc.id, esAcc.password))
index = 'monstache_index'
# ES = Elasticsearch(host = host, port=9200)
print(ES.cat.indices())

# response = ES.search(index=index, body={})

response = ES.search(index=index, body={
    "query": {
        "bool": {
            "must": [
                { "match": { "post_title": "북핵"} },
                { "bool":{
                    "should": [
                        # {"match": {"post_body": request['keyInBody']}},
                        # {"match": {"post_writer": request['writer'] }},
                        # {"match": {"published_institution": request['institution'] }},
                        # {"match": {"top_category": request['category'] }},
                    ]
                }
                }

                ],
            # "filter": [{"range": { "post_date": { "gte": request['startDate'], "lte": request['endDate'] }}}]
        }
    }
})

print(response)