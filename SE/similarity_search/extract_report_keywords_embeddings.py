import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd


model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

df = pd.read_json("../../data_text/info.json")
df2 = df.to_dict("records")


ids = None
with open("./../../upload_data/empty_abstract_and_body.txt", "r") as f:
    ids = f.readlines()


def is_in_ids(id):
    for item in ids:
        if id == item.strip():
            return True
    return False


i = 0
length = len(df2)

while i < length:
    if is_in_ids(str(df2[i]["ID"])):
        df2.pop(i)
        i = i - 1
        length = length - 1
    i = i + 1

with open(f"../embeddings/report_keywords_indices.txt", "w") as f:
    f.write("")


def get_keywords(keywords_list):
    keywords = list()
    persian_key_list = None
    english_key_list = None
    if len(keywords_list) > 0:
        try:
            persian_key_list = keywords_list["فارسی"]
        except Exception:
            pass
        try:
            english_key_list = keywords_list["انگلیسی"]
        except Exception:
            pass
    if persian_key_list is not None:
        for keyword in persian_key_list:
            if keyword != "" and keyword != "/":
                keywords.append(keyword)
    if english_key_list is not None:
        for keyword in english_key_list:
            if keyword != "" and keyword != "/":
                keywords.append(keyword)
    return keywords


def write_id(id):
    with open(f"../embeddings/report_keywords_indices.txt", "a") as f:
        f.write(str(id)+"\n")


def get_max_pooled(keywords):
    report_embedding = model.encode(keywords, convert_to_numpy=True)
    return np.max(report_embedding, axis=0)


curr = 0

while True:
    keywords = get_keywords(df2[curr]["Keywords"])
    if len(keywords) == 0:
        curr += 1
        continue
    write_id(df2[curr]["ID"])
    concat_embedding = get_max_pooled(keywords)
    curr += 1
    break

for i in range(curr, len(df2)):
    keywords = get_keywords(df2[i]["Keywords"])
    if len(keywords) == 0:
        continue
    write_id(df2[i]["ID"])
    concat_embedding = np.vstack(
        (concat_embedding, get_max_pooled(keywords))
    )
    print(i)


np.savetxt(f"../embeddings/report_keywords_embeddings.txt",
           concat_embedding, fmt="%g")
