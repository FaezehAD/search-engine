from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import pickle

with open("./../data/config_variables/ELK_USER.pkl", "rb") as f:
    ELK_USER = pickle.load(f)

with open("./../data/config_variables/ELK_PASSWORD.pkl", "rb") as f:
    ELK_PASSWORD = pickle.load(f)

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(ELK_USER, ELK_PASSWORD),
    timeout=30,
)

if es.ping():
    print("Connected!")
else:
    print("Cannot connect!")


df = pd.read_json("./../data/data_text/article/AAoutput_04-08 15-17-26.json")
# df = pd.read_json("./../../data/data_text/article/new_set.json")
df2 = df.to_dict("records")

i = 0
length = len(df2)

while i < length:
    if len(df2[i]["abstract"]) > 14000:
        print(f'{df2[i]["id"]} has an abstract more than 14000')
        df2.pop(i)
        i = i - 1
        length = length - 1
    i = i + 1


def generator(doc):
    article_abstract = doc["abstract"]
    if (
        article_abstract == "لطفا برای مشاهده چکیده به متن کامل (PDF) مراجعه فرمایید."
        or article_abstract
        == "لطفا برای مشاهده چکیده به متن کامل (pdf) مراجعه فرمایید."
        or article_abstract
        == "متن کامل این مقاله به زبان انگلیسی می باشد, لطفا برای مشاهده متن کامل مقاله به بخش انگلیسی مراجعه فرمایید.لطفا برای مشاهده متن کامل این مقاله اینجا را کلیک کنید"
        or article_abstract == ""
    ):
        article_abstract = None
    year = doc["info"]["year"]
    if year == "":
        article_year = -1
    else:
        try:
            article_year = int(year)
        except ValueError:
            article_year = -1

    # article_keywords = []
    # keywords = doc["keywords"]
    # if keywords == "ثبت نشده است" or keywords == "ثبت نشده است." or keywords == "":
    #     article_keywords = None
    # else:
    #     if " _ " in keywords:
    #         splitted_keywords = keywords.split(" _ ")
    #         end_range = len(splitted_keywords) - 1
    #     else:
    #         splitted_keywords = keywords.split(" ")
    #         end_range = len(splitted_keywords)
    #     for i in range(0, end_range):
    #         article_keywords.append(splitted_keywords[i])
    if doc.get("type") == "همایش":
        article_seminar = doc["info"]["seminar"]
        if article_seminar == "":
            article_seminar = None
        
        return {
            "_index": "articles",
            "_id": doc["id"],
            "_source": {
                "article_type": doc["type"],
                "title": doc["title"],
                "seminar": article_seminar,
                "year": article_year,
                "abstract": article_abstract,
                "persian_keywords": None,
                "english_keywords": None,
                "authors": doc["authors"],
                "body": None,
            },
        }
    # if doc.get("type") == "نشریه":
    #     article_name = doc["info"]["Journal"]
    #     if article_name == "" or article_name == " ":
    #         article_name = None
    #     return {
    #         "_index": "articles",
    #         "_id": doc["id"],
    #         "_source": {
    #             "type": doc["type"],
    #             "title": doc["title"],
    #             "journal_name": article_name,
    #             "year": article_year,
    #             "abstract": article_abstract,
    #             "keywords": article_keywords,
    #             "authors": doc["authors"],
    #         }
    #     }
    # elif doc.get("type") == "مقاله-پژوهشی" or doc.get("type") == "مقاله-نظارتی" or doc.get("type") == "مقاله":
    #     article_executor = doc["info"]["executor"]
    #     if article_executor == "":
    #         article_executor = None
    #     return {
    #         "_index": "articles",
    #         "_id": doc["id"],
    #         "_source": {
    #             "type": doc["type"],
    #             "title": doc["title"],
    #             "executor": article_executor,
    #             "year": article_year,
    #             "abstract": article_abstract,
    #             "keywords": article_keywords,
    #             "authors": doc["authors"],
    #         }
    #     }


res = helpers.bulk(es, (generator(doc) for doc in df2))


