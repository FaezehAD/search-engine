from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import os
import re
import pickle
from SE.models import *


es = Elasticsearch(
    hosts=["http://localhost:9200"],
    timeout=300,
)


if es.ping():
    print("Connected!")
else:
    print("Cannot connect!")


doc_dict = dict()
directory = "./data/data_text/report/txt/"
doc_list = list()
for filename in os.listdir(directory):
    filename = filename[:-4]
    clean_filename = clean_string(filename)
    if " " in filename or "$" in filename or "م" in filename:
        doc_dict[clean_filename] = filename
    doc_list.append(clean_filename)

df = pd.read_json("./data/data_text/report/info.json")

df2 = df.to_dict("records")

ids = list()
with open("./upload_data/database/empty_abstract_and_body.txt", "r") as f:
    for line in f:
        ids.append(line.strip())


def is_in_ids(id_to_check):
    for item in ids:
        if id_to_check == item.strip():
            return True
    return False


i = 0
length = len(df2)

limit_length = 14000


while i < length:
    report_abstract = df2[i]["Abstract"]
    if is_in_ids(str(df2[i]["ID"])) or len(report_abstract) > limit_length:
        df2.pop(i)
        i = i - 1
        length = length - 1
    i = i + 1


def divide_body(input_body):
    divided_body = []
    if input_body is not None:
        i = 0
        while i < len(input_body) / limit_length:
            divided_body.append(input_body[i * limit_length : (i + 1) * limit_length])
            i += 1
        divided_body.append(input_body[i * limit_length :])
    return divided_body


def replace_dash_with_alphabet(string):
    return string.replace("-", "a")


def generator(doc):
    id = int(doc["ID"])
    try:
        report = Report.objects.get(pk=id)
    except Report.DoesNotExist:
        print(f"id: {id}")
    report_english_keywords = list()
    for english_key in report.english_keywords.all():
        report_english_keywords.append(english_key.value)
    report_persian_keywords = list()
    for persian_key in report.persian_keywords.all():
        report_persian_keywords.append(persian_key.value)
    report_required_matches = len(report_english_keywords) + len(
        report_persian_keywords
    )
    return {
        "_index": "reports",
        "_id": doc["ID"],
        "_source": {
            "path": report.path,
            "title": report.title,
            "year": report.year,
            "serial": replace_dash_with_alphabet(report.serial),
            "report_type": report.report_type,
            "english_keywords": report_english_keywords,
            "persian_keywords": report_persian_keywords,
            "required_matches": report_required_matches,
            "abstract": report.abstract,
            "body": divide_body(report.body),
            "body_preprocessed": divide_body(report.body_preprocessed),
        },
    }


res = helpers.bulk(es, (generator(doc) for doc in df2))




