from elasticsearch import Elasticsearch
import esAccount as esAcc

def ESConnection():
    ES = Elasticsearch(
        [esAcc.host],
        http_auth=(esAcc.id, esAcc.password),
        scheme="https",
        port=19200,
        verify_certs=False
    )
    return ES, esAcc.index