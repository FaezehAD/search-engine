import faiss


def read_k():
    with open("./SE/embeddings/variables.txt", "r") as f:
        lines = f.readlines()

    k = int(lines[1])

    return k


def load_report_index(index_type):
    index = faiss.read_index(
        f"./SE/embeddings/faiss_report_{index_type}_index.index")
    return index

def load_article_index(index_type):
    index = faiss.read_index(
        f"./SE/embeddings/faiss_article_{index_type}_index.index")
    return index
