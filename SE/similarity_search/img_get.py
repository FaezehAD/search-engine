
import requests
from bs4 import BeautifulSoup

report_url = "https://rc.majlis.ir" + "/fa/report/show/1776813"
response = requests.get(report_url)
print(response.text)
# soup = BeautifulSoup(response.text, "html.parser")
# images = soup.find_all(
#     "img", src=lambda src: src.startswith("https://rc.majlis.ir/")
# )
# response = requests.get([image["src"] for image in images][0])
# image_content = response.content

# print(image_content)