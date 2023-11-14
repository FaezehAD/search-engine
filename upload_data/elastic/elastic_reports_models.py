from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import os
import re
from decouple import config
from SE.models import *

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(config("ELK_USER"), config("ELK_PASSWORD")),
    timeout=30,
)

if es.ping():
    print("Connected!")
else:
    print("Cannot connect!")

all_reports = list(Report.objects.all())

i = 0
length = len(all_reports)

limit_length = 14000


while i < length:
    report_abstract = all_reports[i].abstract
    if report_abstract is not None:
        if len(report_abstract) > limit_length:
            all_reports.pop(i)
            i = i - 1
            length = length - 1
    i = i + 1


def divide_body(input_body):
    if input_body is None:
        return None
    divided_body = []
    i = 0
    while i < len(input_body) / limit_length:
        divided_body.append(input_body[i * limit_length : (i + 1) * limit_length])
        i += 1
    divided_body.append(input_body[i * limit_length :])
    return divided_body


def replace_dash_with_alphabet(string):
    return string.replace("-", "a")

for k in all_reports[0].english_keywords:
    print(k)


def generator(doc):
    report_serial = doc.serial
    if report_serial is not None:
        report_serial = replace_dash_with_alphabet(report_serial)
    report_english_keywords = list()
    english_keywords = list(doc.english_keywords.all())
    for english_keyword in english_keywords:
        report_english_keywords.append(english_keyword.value)
    
    report_persian_keywords = list()
    persian_keywords = list(doc.persian_keywords.all())
    for persian_keyword in persian_keywords:
        report_persian_keywords.append(persian_keyword.value)
        
    return {
        "_index": "reports",
        "_id": doc.id,
        "_source": {
            "path": doc.path,
            "title": doc.title,
            "year": int(doc.year),
            "serial": report_serial,
            "report_type": doc.report_type,
            "english_keywords": report_english_keywords,
            "persian_keywords": report_persian_keywords,
            "abstract": doc.abstract,
            "body": divide_body(doc.body),
        },
    }


res = helpers.bulk(es, (generator(doc) for doc in all_reports))


print("finished!")


