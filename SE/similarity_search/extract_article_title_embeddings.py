import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer



model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

df = pd.read_json("../../data/data_text/article/new_set.json")
df2 = df.to_dict("records")


with open(f"../embeddings/article_title_indices.txt", "w") as f:
    f.write("")


def write_id(id):
    with open(f"../embeddings/article_title_indices.txt", "a") as f:
        f.write(str(id) + "\n")


write_id(df2[0]["id"])
concat_embedding = model.encode([df2[0]["title"]]).astype(np.float32)
print(concat_embedding.shape)

for i in range(1, len(df2)):
    write_id(df2[i]["id"])
    concat_embedding = np.vstack(
        (concat_embedding, model.encode([df2[i]["title"]]).astype(np.float32))
    )
    print(i)

np.savetxt(f"../embeddings/article_title_embeddings.txt", concat_embedding, fmt="%g")
