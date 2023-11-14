import pandas as pd

df = pd.read_json("./../data_text/AAoutput_04-08 15-17-26.json")
df2 = df.to_dict("records")

non_abs = 0
nash = 0
ham = 0
magh = 0
dup = 0
ids_list = list()

for i in range(0, len(df2)):
    id = df2[i]["id"]
    if id in ids_list:
        dup += 1
        continue
    ids_list.append(id)
    article_abstract = df2[i]["abstract"]
    if (article_abstract == "لطفا برای مشاهده چکیده به متن کامل (PDF) مراجعه فرمایید." or
        article_abstract == "لطفا برای مشاهده چکیده به متن کامل (pdf) مراجعه فرمایید." or
        article_abstract == "متن کامل این مقاله به زبان انگلیسی می باشد, لطفا برای مشاهده متن کامل مقاله به بخش انگلیسی مراجعه فرمایید.لطفا برای مشاهده متن کامل این مقاله اینجا را کلیک کنید" or
            article_abstract == ""):
        article_abstract = None
        non_abs += 1
        continue
    if df2[i]["type"] == "نشریه":
        nash += 1
    elif df2[i]["type"] == "همایش":
        ham += 1
    elif df2[i]["type"] == "مقاله-پژوهشی" or df2[i]["type"] == "مقاله-نظارتی" or df2[i]["type"] == "مقاله":
        magh += 1

print(f"non abs: {non_abs}")
print(f"nashrieh: {nash}")
print(f"ham: {ham}")
print(f"maghaleh: {magh}")
print(f"dup: {dup}")
print(f"total: {len(df2)}")