import requests
from decouple import config


response = requests.get(config('BASE_URL')+'reports/_doc/1775669')

print(response.json())