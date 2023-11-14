import numpy as np
import faiss


def make_index(index_type):
    sentence_embeddings = np.loadtxt(
        f"./../embeddings/report_{index_type}_embeddings.txt", dtype=np.float32)
    d = sentence_embeddings.shape[1]
    print(f"d: {d}")
    print(sentence_embeddings.shape)
    index = faiss.IndexFlatL2(d)
    # print(index.is_trained)

    index.add(sentence_embeddings)

    print(f"total num: {index.ntotal}")

    # k = 30

    faiss.write_index(
        index, f"./../embeddings/faiss_report_{index_type}_index.index")

    # with open("./../embeddings/variables.txt", "w") as f:
    #     f.write(f"{d}\n{k}")

    # variables:
    # first line: d
    # second line: k


# make_index("keywords")
# make_index("title_xlm")
# make_index("abstract")
make_index("body")
