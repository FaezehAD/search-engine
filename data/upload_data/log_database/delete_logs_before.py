from elasticsearch import Elasticsearch
import pickle

# from khayyam import JalaliDatetime, TehranTimezone
# import time

# def get_timestamp():
#     current_time = JalaliDatetime.now(TehranTimezone())
#     formatted_date_time = current_time.strftime("%y-%m-%d %H:%M:%S")
#     return formatted_date_time

# t1 = get_timestamp()

# time.sleep(2)
# t2 = get_timestamp()

# print(t1)
# print(t2)
# print(t2 > t1)

with open("./data/config_variables/ELK_USER.pkl", "rb") as f:
    ELK_USER = pickle.load(f)

with open("./data/config_variables/ELK_PASSWORD.pkl", "rb") as f:
    ELK_PASSWORD = pickle.load(f)

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(ELK_USER, ELK_PASSWORD),
    timeout=30,
)
query = {
    "query": {
        "range": {
            "timestamp": {
                "lt": "02-10-04 16:01:25",
                "script": {
                    "source": "doc['timestamp'].value < params.value",
                    "params": {"value": "abc"},
                },
            }
        }
        # "script": {
        #   "source": "return doc['timestamp'] < '02-10-04 15:56:00';",
        #   "lang": "python"
        # }
    }
}


# query = {"query": {"range": {"timestamp": {"lt": "02-10-04 15:56:00"}}}}

res = es.delete_by_query(index="logs", body=query)

print(res)
