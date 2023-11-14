import numpy as np
from SE.models import *
import numpy as np
from hazm import *
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

all_reports = list(Report.objects.all())


with open(f"./SE/embeddings/report_body_indices.txt", "w") as f:
    f.write("")


def write_id(id):
    with open(f"./SE/embeddings/report_body_indices.txt", "a") as f:
        f.write(str(id) + "\n")


def get_max_pooled(sentences_list):
    return np.max(model.encode(sentences_list, convert_to_numpy=True), axis=0)


def separate_paragraphs(input_str):
    input_str = input_str.replace("\n", "")
    report_sentences = sent_tokenize(input_str)
    return [report_sentences[i : i + 10] for i in range(0, len(report_sentences), 10)]


curr = 0

while True:
    report_body_preprocessed = all_reports[curr].body_preprocessed
    report_id = all_reports[curr].id
    curr += 1
    if report_body_preprocessed is None:
        continue
    report_paragraphs = separate_paragraphs(report_body_preprocessed)
    concat_embedding = get_max_pooled(report_paragraphs[0])
    write_id(report_id)
    for i in range(1, len(report_paragraphs)):
        concat_embedding = np.vstack(
            (concat_embedding, get_max_pooled(report_paragraphs[i]))
        )
        write_id(report_id)
    break


for i in range(curr, len(all_reports)):
    report_body_preprocessed = all_reports[i].body_preprocessed
    if report_body_preprocessed is None:
        continue
    report_id = all_reports[i].id
    report_paragraphs = separate_paragraphs(report_body_preprocessed)
    for j in range(0, len(report_paragraphs)):
        concat_embedding = np.vstack(
            (concat_embedding, get_max_pooled(report_paragraphs[j]))
        )
        write_id(report_id)
    print(f"i: {i}")


np.savetxt(f"./SE/embeddings/report_body_embeddings.txt", concat_embedding, fmt="%g")

