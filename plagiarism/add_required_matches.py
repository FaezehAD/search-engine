from elasticsearch import Elasticsearch
from decouple import config

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(config("ELK_USER"), config("ELK_PASSWORD")),
    timeout=100,
)

if es.ping():
    print("Connected!")
else:
    print("Cannot connect!")

from elasticsearch import Elasticsearch

es = Elasticsearch()

script = {
    "script": {
        "source": "ctx._source.required_matches = 0",
        "lang": "painless"
    },
    "query": {
        "match_all": {}
    }
}

es.update_by_query(index="reports", body=script)

# update_query = {
#     "script": {
#         "source": "ctx._source.required_matches = params.english_count + params.persian_count",
#         "params": {
#             "english_count": "doc['english_keywords'].length",
#             "persian_count": "doc['persian_keywords'].length"
#         }
#     },
#     "query": {
#         "match_all": {}
#     }
# }

# es.update_by_query(index="reports", body=update_query)
