import pickle
import requests

with open("./../data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)

response = requests.get(BASE_URL + "reports/_count", timeout=200)
print(response.text)
