import collections
from elasticsearch import Elasticsearch
from hazm import Normalizer, word_tokenize, sent_tokenize
from nltk.util import ngrams

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
    # print(tokens)
    ngram_list = ngrams(tokens, 4)
    all_ngram.extend(list(ngram_list))
all_ngram_phrase = set(
    [" ".join(r) for r in all_ngram]
)  # *******************************************set?

count_ngrams = len(all_ngram_phrase)
print(all_ngram_phrase)

es = Elasticsearch(
    hosts="http://localhost:9200",
    basic_auth=("ya-hossein", "yazahra"),
    verify_certs=False,
)

size_match = int(len(doc_search["keyword"]) / 2)
# resp=es.search(index="docs", query={"terms_set": {"keyword": {"terms": doc_search['keyword'],"minimum_should_match_script": {"source": "Math.min(%s, doc['required_matches'].value)"%size_match}}}})#params.num_terms replace with %s
# search_data=resp['hits']['hits']
# count_search_data=len(search_data)
# print("count_search_data",count_search_data)

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
                                    "source": "Math.min(%s, doc['required_matches'].value)"
                                    % size_match
                                },
                            }
                        }
                    },
                ],
                "filter": [
                    {"match_phrase": {"text": {"query": term}}},
                ],
            }
        },
    )
    # resp=es.search(index="docs", query={"bool": {"must":[
    #     {"terms_set": {"keyword": {"terms": doc_search['keyword'],"minimum_should_match_script": {"source": "Math.min(%s, doc['required_matches'].value)"%size_match}}}},
    #     {"match_phrase": {"text": {"query": term}}}
    # ]}})
    data = resp["hits"]["hits"]
    result.extend(set([r["_id"] for r in data]))
# print(result)

id_count = collections.Counter(result).most_common()  # most_common(len(set(result)))
print("id_count", id_count)
# count_plagiarism_phrase=0

if (id_count[0][1] / count_ngrams) > 0.5:
    print("This paper contains plagiarism ")
