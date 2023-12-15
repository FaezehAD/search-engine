import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


print("="*100)
model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

print("-"*100)

# df = pd.read_json("../../data/data_text/report/info.json")
# df2 = df.to_dict("records")


# ids = None
# with open("./../../upload_data/database/empty_abstract_and_body.txt", "r") as f:
#     ids = f.readlines()


# def is_in_ids(id):
#     for item in ids:
#         if id == item.strip():
#             return True
#     return False


# i = 0
# length = len(df2)

# while i < length:
#     if is_in_ids(str(df2[i]["ID"])):
#         df2.pop(i)
#         i = i - 1
#         length = length - 1
#     i = i + 1

# with open(f"../embeddings/report_title_indices.txt", "w") as f:
#     f.write("")


# def write_id(id):
#     with open(f"../embeddings/report_title_indices.txt", "a") as f:
#         f.write(str(id) + "\n")


# write_id(df2[0]["ID"])
# concat_embedding = model.encode([df2[0]["Title"]]).astype(np.float32)
# print(concat_embedding.shape)

# for i in range(1, len(df2)):
#     write_id(df2[i]["ID"])
#     concat_embedding = np.vstack(
#         (concat_embedding, model.encode([df2[i]["Title"]]).astype(np.float32))
#     )
#     print(i)

# np.savetxt(f"../embeddings/report_title_embeddings.txt", concat_embedding, fmt="%g")
