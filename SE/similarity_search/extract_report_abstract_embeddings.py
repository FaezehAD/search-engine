import numpy as np
from hazm import *
from sentence_transformers import SentenceTransformer
from SE.models import *


model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

all_reports = list(Report.objects.all())


with open(f"./SE/embeddings/report_abstract_indices.txt", "w") as f:
    f.write("")


def write_id(id):
    with open(f"./SE/embeddings/report_abstract_indices.txt", "a") as f:
        f.write(str(id) + "\n")


def get_max_pooled(report_abs_preprocessed):
    report_sentences = sent_tokenize(report_abs_preprocessed)
    report_embedding = model.encode(report_sentences, convert_to_numpy=True)
    return np.max(report_embedding, axis=0)


curr = 0

while True:
    report_abs_preprocessed = all_reports[curr].abstract_preprocessed
    if report_abs_preprocessed is None:
        curr += 1
        continue
    write_id(all_reports[curr].id)
    concat_embedding = get_max_pooled(report_abs_preprocessed)
    curr += 1
    break

for i in range(curr, len(all_reports)):
    report_abs_preprocessed = all_reports[i].abstract_preprocessed
    if report_abs_preprocessed is None:
        continue
    write_id(all_reports[i].id)
    concat_embedding = np.vstack(
        (concat_embedding, get_max_pooled(report_abs_preprocessed))
    )
    print(i)

np.savetxt(
    f"./SE/embeddings/report_abstract_embeddings.txt",
    concat_embedding,
    fmt="%g",
)
