import requests
import pickle

document_id = 'fbb989020ca3449d941b35e4a07f3f3e'

with open("./../data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)

response = requests.get(f'{BASE_URL}logs/_doc/{document_id}')

if response.status_code == 200:
    document = response.json()
    print('Retrieved document:', document)
else:
    print('Failed to retrieve document.')
