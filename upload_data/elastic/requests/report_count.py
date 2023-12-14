from decouple import config
import requests

# BASE_URL = f'http://{config("ELK_USER")}:{config("ELK_PASSWORD")}@localhost:9200/'
BASE_URL = config('BASE_URL')

response = requests.get(BASE_URL + "reports/_count", timeout=200)
print(response.text)
