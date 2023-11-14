from decouple import config
import requests

BASE_URL = config('BASE_URL')

response = requests.get(BASE_URL + "logs/_count", timeout=30)
print(response.text)
