import requests
import pickle


query = {"query": {"match_all": {}}}

with open("./data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)

response = requests.post(BASE_URL + "logs/_delete_by_query", json=query)

if response.status_code == 200:
    result = response.json()
    deleted_count = result["deleted"]
    print(f"{deleted_count} documents deleted.")
else:
    print("Failed to delete documents.")
