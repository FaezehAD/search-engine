from decouple import config
import requests
import uuid

# BASE_URL = f'http://{config("ELK_USER")}:{config("ELK_PASSWORD")}@localhost:9200/'

BASE_URL = config('BASE_URL')

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

# response = requests.put(BASE_URL + "logs/",
#                         headers={"Content-Type": "application/json"},
#                         json=json_obj,
#                         timeout=30)

# print(response.text)


# response=requests.get(BASE_URL + "logs/_mapping",
#                       timeout=30)

# print(response.json())


