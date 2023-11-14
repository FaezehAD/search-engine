import requests
from decouple import config


query = {
    'query': {
        'match_all': {}
    }
}

response = requests.post(config("BASE_URL")+'logs/_delete_by_query', json=query)

if response.status_code == 200:
    result = response.json()
    deleted_count = result['deleted']
    print(f'{deleted_count} documents deleted.')
else:
    print('Failed to delete documents.')