from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import os
import re
from decouple import config

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(config("ELK_USER"), config("ELK_PASSWORD")),
    timeout=30,
)

if es.ping():
    print("Connected!")
else:
    print("Cannot connect!")


def clean_string(input_str):
    cleaned_str = re.sub(r"[^a-zA-Z0-9-]", "", input_str)
    return cleaned_str


doc_dict = dict()
directory = "../../data_text/report/txt/"
doc_list = list()
for filename in os.listdir(directory):
    filename = filename[:-4]
    clean_filename = clean_string(filename)
    if " " in filename or "$" in filename or "م" in filename:
        doc_dict[clean_filename] = filename
    doc_list.append(clean_filename)

df = pd.read_json("../../data_text/report/info.json")

df2 = df.to_dict("records")

ids = None
with open("../database/empty_abstract_and_body.txt", "r") as f:
    ids = f.readlines()


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
    i = 0
    while i < len(input_body) / limit_length:
        divided_body.append(input_body[i * limit_length : (i + 1) * limit_length])
        i += 1
    divided_body.append(input_body[i * limit_length :])
    return divided_body


def replace_dash_with_alphabet(string):
    return string.replace("-", "a")


def generator(doc):
    print(doc["ID"])
    report_title = doc["Title"]
    if report_title == "":
        report_title = None
    try:
        report_year = int(doc["Info"]["سال"])
    except Exception:
        report_year = -1
    try:
        report_type = doc["Info"]["نوع"]
    except Exception:
        report_type = None
    try:
        report_serial = doc["Info"]["شماره مسلسل"]
    except Exception:
        report_serial = None
    keywords_list = doc["Keywords"]
    persian_key_list = None
    english_key_list = None
    report_persian_keywords = list()
    report_english_keywords = list()
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
                report_persian_keywords.append(keyword)
    if english_key_list is not None:
        for keyword in english_key_list:
            if keyword != "" and keyword != "/":
                report_english_keywords.append(keyword)
    report_required_matches = len(report_persian_keywords) + len(
        report_english_keywords
    )
    report_abstract = doc["Abstract"]
    if report_abstract == "":
        report_abstract = None
    report_body = None
    if report_serial is not None:
        file_title = None
        if report_serial in doc_list:
            file_title = report_serial
        else:
            if "-" in report_serial:
                index = report_serial.index("-")
                report_serial = report_serial[:index]
            if (report_serial + "-1") in doc_list:
                file_title = report_serial + "-1"
            elif (report_serial + "-2") in doc_list:
                file_title = report_serial + "-2"
            elif (report_serial + "-3") in doc_list:
                file_title = report_serial + "-3"
            elif (report_serial + "-4") in doc_list:
                file_title = report_serial + "-4"
            elif (report_serial + "-5") in doc_list:
                file_title = report_serial + "-5"
            elif (report_serial + "-6") in doc_list:
                file_title = report_serial + "-6"
            elif (report_serial + "-7") in doc_list:
                file_title = report_serial + "-7"
            elif (report_serial + "-8") in doc_list:
                file_title = report_serial + "-8"
            elif (report_serial + "-9") in doc_list:
                file_title = report_serial + "-9"
            elif (report_serial + "-10") in doc_list:
                file_title = report_serial + "-10"
        if file_title is not None:
            try:
                with open(
                    (directory + file_title + ".txt"), "r", encoding="utf_8"
                ) as file:
                    buffer = file.read()
                    if len(buffer) > 300:
                        report_body = divide_body(buffer)
            except FileNotFoundError:
                file_title = doc_dict[file_title]
                with open(
                    (directory + file_title + ".txt"), "r", encoding="utf_8"
                ) as file:
                    buffer = file.read()
                    if len(buffer) > 300:
                        report_body = divide_body(buffer)
    if report_serial is not None:
        report_serial = replace_dash_with_alphabet(report_serial)
    return {
        "_index": "reports",
        "_id": doc["ID"],
        "_source": {
            "path": doc["Path"],
            "title": report_title,
            "year": report_year,
            "serial": report_serial,
            "report_type": report_type,
            "english_keywords": report_english_keywords,
            "persian_keywords": report_persian_keywords,
            "required_matches": report_required_matches,
            "abstract": report_abstract,
            "body": report_body,
        },
    }


res = helpers.bulk(es, (generator(doc) for doc in df2))



