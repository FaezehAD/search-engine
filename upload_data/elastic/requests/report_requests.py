from decouple import config
import requests

# https not worked!!!!!!!!!!!!!!!
# BASE_URL = f'http://{config("ELK_USER")}:{config("ELK_PASSWORD")}@localhost:9200/'
BASE_URL = config('BASE_URL')

response = requests.get(BASE_URL + "_cat/indices/", timeout=30)
print(f"response: {response.text}")


# response=requests.delete(BASE_URL+"reports/",timeout=30)
# print(response.text)

# json_obj = {
#     "mappings": {
#         "properties": {
#             "path": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "title": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "year": {
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
#             "report_type": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "english_keywords": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "persian_keywords": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "abstract": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             },
#             "body": {
#                 "type": "text",
#                 "fields": {
#                     "keyword": {
#                         "type": "keyword"
#                     }
#                 }
#             }
#         }
#     }
# }

# response = requests.put(BASE_URL + "reports/",
#                         headers={"Content-Type": "application/json"},
#                         json=json_obj,
#                         timeout=30)

# print(response.text)


# response=requests.get(BASE_URL + "reports/_mapping",
#                       timeout=30)

# print(response.json())

