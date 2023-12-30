# import pickle
import requests
import pickle
import uuid
from SE.similarity_search.utils.manage_variables import *


with open("./data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)


response = requests.get(BASE_URL + "_cat/indices/", timeout=30)
print(f"response: {response.text}")


# response=requests.delete(BASE_URL + "logs/",timeout=30)
# print(response.text)


# json_obj = {
#     "mappings": {
#         "properties": {
#             "is_semantic": {
#                 "type": "boolean",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "main_query": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "and_query": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "or_query": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "not_query": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "exact_query": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "start_year": {
#                 "type": "integer",
#                 "null_value": -1
#             },
#             "end_year": {
#                 "type": "integer",
#                 "null_value": -1
#             },
#             "serial": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "report_types": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "report_people": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "search_fields": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "results": {
#                 "type": "nested",
#                 "properties": {
#                     "result_id": {"type": "keyword"},
#                     "title": {"type": "text"},
#                     "click": {"type": "boolean"},
#                     "feedback": {"type": "text"},
#                     }
#             },
#             "timestamp": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#         }
#     }
# }

# response = requests.put(BASE_URL + "logs2/",
#                         headers={"Content-Type": "application/json"},
#                         json=json_obj,
#                         timeout=30)

# print(response.text)


# response=requests.get(BASE_URL + "logs/_mapping",
#                       timeout=30)

# print(response.json())
