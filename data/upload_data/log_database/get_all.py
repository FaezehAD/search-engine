import requests
import pickle


query = {
    'query': {
        'match_all': {}
    }
}
with open("./../data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)
response = requests.get(f'{BASE_URL}logs/_search', json=query)

results = response.json()["hits"]["hits"]
print(len(results))
# for r in results:
#     print(r["_source"]["is_semantic"])
    # results2 = r["_source"]["results"]
    # for result in results2:
    #     print(result["result_id"])
