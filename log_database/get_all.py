import requests
from decouple import config


query = {
    'query': {
        'match_all': {}
    }
}

response = requests.get(f'{config("BASE_URL")}logs/_search', json=query)

results = response.json()["hits"]["hits"]
print(len(results))
# for r in results:
#     print(r["_source"]["is_semantic"])
    # results2 = r["_source"]["results"]
    # for result in results2:
    #     print(result["result_id"])
