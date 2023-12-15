import requests
import pickle

with open("./data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)

response = requests.get(BASE_URL + "articles/_count", timeout=30)
print(response.text)
