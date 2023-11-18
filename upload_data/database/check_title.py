import pandas as pd
from SE.models import *


# df = pd.read_json("./data_text/article/AAoutput_04-08 15-17-26.json")
df = pd.read_json("./data_text/article/new_set.json")
df2 = df.to_dict("records")

with open("./upload_data/database/article_titles.txt", "w") as exceptions:
    exceptions.write("")


for i in range(0, len(df2)):
    with open("./upload_data/database/article_titles.txt", "a") as exceptions:
        exceptions.write(f'{df2[i]["title"]}\n')


