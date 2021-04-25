import esAccount as esAcc
from elasticsearch import Elasticsearch
from ssl import create_default_context
# context = create_default_context(Purpose.CLIENT_AUTH)
ES = Elasticsearch(
    [esAcc.host],
    http_auth=(esAcc.id, esAcc.password),
    scheme="https",
    port=19200,
    # use_ssl=False,
    verify_certs=False,
    # ssl_context=context
)

# print(ES.info())
# print(ES.cat.indices())

index = 'monstache_index'
request= {}
request['page'] = 1
request['numOfCnt'] = 100
if request['page'] < 100:
    query = {
        "from" : request['page'] * request['numOfCnt'] +1,
        "size": int(request['numOfCnt']),
        "sort": [
            {"post_date.keyword": {"order":"asc"}},
            {"post_title.keyword": {"order":"asc"}}
        ]
    }
    response = ES.search(index=esAcc.index, body=query)
else:
    request['page']
print(response['hits']['hits'])


# print(response)



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