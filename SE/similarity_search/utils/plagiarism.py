from hazm import Normalizer, word_tokenize, sent_tokenize
from nltk.util import ngrams
from elasticsearch import Elasticsearch
import pickle
import collections
import numpy as np
from .report_utils import *
from .result import *


def check_plagiarism(input_text, input_keywords_list):
    with open("./data/config_variables/ELK_USER.pkl", "rb") as f:
        ELK_USER = pickle.load(f)

    with open("./data/config_variables/ELK_PASSWORD.pkl", "rb") as f:
        ELK_PASSWORD = pickle.load(f)

    es = Elasticsearch(
        hosts=["http://localhost:9200"],
        basic_auth=(ELK_USER, ELK_PASSWORD),
        timeout=30,
    )
    all_ngram = []
    normalizer = Normalizer()
    doc = normalizer.normalize(input_text)

    sentences = sent_tokenize(doc)

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        ngram_list = ngrams(tokens, 4)
        all_ngram.extend(list(ngram_list))

    all_ngram_phrase = set(
        [" ".join(r) for r in all_ngram]
    )  # set of all 4-grams of input text

    ngrams_count = len(all_ngram_phrase)

    match_size = max(int(len(input_keywords_list) / 2), 1)

    results = []

    for term in all_ngram_phrase:
        response = es.search(
            index="reports",
            query={
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "minimum_should_match": match_size,
                                "should": [
                                    {"match": {"persian_keywords": key}}
                                    for key in input_keywords_list
                                ],
                            }
                        }
                    ],
                    "filter": [{"match_phrase": {"body_preprocessed": f"{term}"}}],
                }
            },
        )
        data = response["hits"]["hits"]
        results.extend(set([r["_id"] for r in data]))

    id_count = collections.Counter(results).most_common()

    id_percent = list()
    for i in id_count:
        result = get_report_by_id(int(i[0]))
        rate = 100.0 * np.round(i[1] / ngrams_count, 3)
        if rate < 10.0:
            break
        persian_keywords, english_keywords, departments = get_report_details(result)
        id_percent.append(
            Result(result, rate, persian_keywords, english_keywords, departments)
        )
    return id_percent


# check_plagiarism(
#     "با نقش‌آفرینی ایران و دیگر متحدان سوریه، امنیت نسبی در این کشور برقرار شده و با شروع دوره بازسازی، این کشور نیازمند آن است تا با احیای توان گذشته و تقویت بخش‌های مهم اقتصادی و تجاری، خسارت‌های ناشی از بحران را جبران کند.",
# با نقش‌آفرینی ایران و دیگر متحدان سوریه، امنیت نسبی در این کشور برقرار شده و با شروع دوره بازسازی، این کشور نیازمند آن است تا با احیای توان گذشته و تقویت بخش‌های مهم اقتصادی و تجاری، خسارت‌های ناشی از بحران را جبران کند.
#     ["دیپلماسی اقتصادی"],
# )
