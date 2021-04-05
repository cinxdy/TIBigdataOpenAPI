import esAccount as esAcc
from elasticsearch import Elasticsearch
from ssl import create_default_context

ES = Elasticsearch(
    [esAcc.host],
    http_auth=(esAcc.id, esAcc.password),
    scheme="https",
    port=19200,
    verify_certs=False
)

print(ES.info())
print(ES.cat.indices())

index = 'monstache_index'
# ES = Elasticsearch(host = host, port=9200)
# print(ES.info())
# print(ES.cat.indices())

# response = ES.search(index=index, body={})

# response = ES.search(index=index, body={
#     "query": {
#         "bool": {
#             "must": [
#                 { "match": { "post_title": "북핵"} },
#                 { "bool":{
#                     "should": [
#                         # {"match": {"post_body": request['keyInBody']}},
#                         # {"match": {"post_writer": request['writer'] }},
#                         # {"match": {"published_institution": request['institution'] }},
#                         # {"match": {"top_category": request['category'] }},
#                     ]
#                 }
#                 }

#                 ],
#             # "filter": [{"range": { "post_date": { "gte": request['startDate'], "lte": request['endDate'] }}}]
#         }
#     }
# })

# print(response)