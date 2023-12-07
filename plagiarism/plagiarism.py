from hazm import Normalizer, word_tokenize, sent_tokenize
from nltk.util import ngrams
from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts="http://localhost:9200",
    basic_auth=("ya-hossein", "yazahra"),
    verify_certs=False,
)

doc_search = {
    "keyword": ["a", "b", "c", "h"],
    "text": "ما هم برای وصل کردن آمدیم ! ولی برای پردازش، جدا بهتر نیست؟",
    "required_matches": 4,
}

all_ngram = []
normalizer = Normalizer()
doc = normalizer.normalize(doc_search["text"])

sentences = sent_tokenize(doc)


for sentence in sentences:
    tokens = word_tokenize(sentence)
    ngram_list = ngrams(tokens, 4)
    all_ngram.extend(list(ngram_list))
all_ngram_phrase = set([" ".join(r) for r in all_ngram])

count_ngrams = len(all_ngram_phrase)
print(all_ngram_phrase)

import collections
import numpy as np

size_match = int(len(doc_search["keyword"]) / 2)

result = []
for term in all_ngram_phrase:
    resp = es.search(
        index="docs",
        query={
            "bool": {
                "must": [
                    {
                        "terms_set": {
                            "keyword": {
                                "terms": doc_search["keyword"],
                                "minimum_should_match_script": {
                                    "source": "Math.min(%s, %s)"
                                    % (size_match, size_match)
                                },
                            }  # doc['required_matches'].value
                        }
                    }
                ],
                "filter": [{"match_phrase": {"text": {"query": term}}}],
            }
        },
    )
    data = resp["hits"]["hits"]
    result.extend(set([r["_id"] for r in data]))

id_count = collections.Counter(result).most_common()
id_percent = [(i[0], np.round(i[1] / count_ngrams, 2)) for i in id_count]
print("id_count", id_percent)

# if (id_count[0][1]/count_ngrams)>0.5:
#     print('This paper contains plagiarism ')
