import requests
from decouple import config

document_id = 'fbb989020ca3449d941b35e4a07f3f3e'

response = requests.get(f'{config("BASE_URL")}logs/_doc/{document_id}')

if response.status_code == 200:
    document = response.json()
    print('Retrieved document:', document)
else:
    print('Failed to retrieve document.')
