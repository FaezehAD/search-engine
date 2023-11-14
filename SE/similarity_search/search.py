# import datetime
import numpy as np
from sentence_transformers import SentenceTransformer, util
import requests
import copy
from transformers import XLMRobertaModel, XLMRobertaTokenizer
import torch
from decouple import config
from SE.models import *
from .load_indices import *
from .sort_results import *
from .utils.utils import *
from .utils.report_utils import *
from .filter_departments import *


XLM_REBERTA_MODEL_NAME = "xlm-roberta-large"

# model = XLMRobertaModel.from_pretrained(XLM_REBERTA_MODEL_NAME)
# tokenizer = XLMRobertaTokenizer.from_pretrained(XLM_REBERTA_MODEL_NAME)

# BASE_URL = f'http://{config("ELK_USER")}:{config("ELK_PASSWORD")}@localhost:9200/'
BASE_URL = config('BASE_URL')

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

checkboxes = ["3", "", "", "", "1"]

raw_results = None
search_method = "1"


def get_search_method():
    global search_method
    return search_method


def set_search_method(input_method):
    global search_method
    search_method = input_method


def get_raw_results():
    global raw_results
    if raw_results is None:
        return None
    new_raw = list()
    for r in raw_results:
        new_raw.append(r)
    return new_raw


def set_checkboxes(input_checkboxes):
    global checkboxes
    checkboxes = input_checkboxes


def get_checkboxes():
    global checkboxes
    return checkboxes


def get_min_score():
    return sort_results_cos_sim(get_raw_results(), asc=False)


def get_max_score():
    return sort_results_cos_sim(get_raw_results(), asc=True)


def get_date_ascending():
    raw_results = get_raw_results()
    if raw_results is None:
        return (False, None)
    is_available, results = sort_results_date(raw_results, True, True)
    return (is_available, results)


def get_date_descending():
    raw_results = get_raw_results()
    if raw_results is None:
        return (False, None)
    is_available, results = sort_results_date(raw_results, True, False)
    return (is_available, results)


with open("./SE/embeddings/report_keywords_indices.txt", "r") as f:
    keywords_ids = f.readlines()

# with open("./SE/embeddings/report_title_xlm_indices.txt", "r") as f:
with open("./SE/embeddings/report_title_indices.txt", "r") as f:
    title_ids = f.readlines()

with open("./SE/embeddings/report_abstract_indices.txt", "r") as f:
    abstract_ids = f.readlines()

with open("./SE/embeddings/report_body_indices.txt", "r") as f:
    body_ids = f.readlines()

report_keywords_index = load_report_index("keywords")
report_title_index = load_report_index("title")
# report_title_index = load_report_index("title_xlm")
report_abstract_index = load_report_index("abstract")
report_body_index = load_report_index("body")

k = read_k()


def replace_dash_with_alphabet(string):
    return string.replace("-", "a")


def get_embeddings(embedding_type):
    sentence_embeddings = np.loadtxt(
        f"./SE/embeddings/report_{embedding_type}_embeddings.txt", dtype=np.float32
    )
    return sentence_embeddings


def get_semantic_results(indices, ids, xq, embeddings):
    results = list()
    ids_to_return = list()
    for item in indices:
        id = int(ids[int(item)].strip())
        if id in ids_to_return:
            continue
        ids_to_return.append(id)
        embedding = embeddings[int(item)]
        score = util.cos_sim(xq, embedding)
        report = Report.objects.get(pk=id)
        persian_keywords, english_keywords, departments = get_details(report)
        results.append(
            (
                report,
                round(score.item() * 100, 2),
                persian_keywords,
                english_keywords,
                departments,
            )
        )
    return results


def get_syntactic_results(response_hits):
    results = list()
    for item in response_hits:
        report = Report.objects.get(pk=item["_id"])
        persian_keywords, english_keywords, departments = get_details(report)
        results.append((report, 200, persian_keywords, english_keywords, departments))
    return results


def get_results(
    start_year,
    end_year,
    results,
    serial,
    people_list,
    supervisory,
    legislative,
    strategic,
):
    global raw_results
    results = delete_outdated_results(results, True, start_year, end_year)
    if people_list is not None and len(people_list) != 0:
        results = verify_people(results, people_list)
    raw_results = copy.copy(
        verify_types(
            verify_serials(
                delete_min_rate(results),
                serial,
            ),
            supervisory,
            legislative,
            strategic,
        )
    )
    return get_min_score()


def semantic_search(
    query,
    option,
    start_year,
    end_year,
    input_serial,
    people_list,
    supervisory,
    legislative,
    strategic,
):
    global checkboxes
    results = None
    # input_ids = tokenizer.encode(query, add_special_tokens=True, return_tensors="pt")
    # with torch.no_grad():
    #     output = model(input_ids)
    # xq = output.last_hidden_state.mean(dim=1).squeeze().numpy()
    xq = model.encode([query]).astype(np.float32)
    # st = datetime.datetime.now()
    if checkboxes[0] == "3":
        # sentence_embeddings = get_embeddings("title_xlm")
        # _, I = report_title_index.search(np.array([xq]), k)
        sentence_embeddings = get_embeddings("title")
        _, I = report_title_index.search(xq, k)
        results = get_semantic_results(I[0], title_ids, xq, sentence_embeddings)
    elif checkboxes[1] == "4":
        sentence_embeddings = get_embeddings("keywords")
        _, I = report_keywords_index.search(xq, k)
        results = get_semantic_results(I[0], keywords_ids, xq, sentence_embeddings)
    elif checkboxes[2] == "5":
        sentence_embeddings = get_embeddings("abstract")
        _, I = report_abstract_index.search(xq, k)
        results = get_semantic_results(I[0], abstract_ids, xq, sentence_embeddings)
    elif checkboxes[3] == "6":
        sentence_embeddings = get_embeddings("body")
        _, I = report_body_index.search(xq, k)
        results = get_semantic_results(I[0], body_ids, xq, sentence_embeddings)
    else:
        sentence_embeddings = get_embeddings("title")
        _, I = report_title_index.search(xq, k)
        results = get_semantic_results(I[0], title_ids, xq, sentence_embeddings)
    # et = datetime.datetime.now()
    # elapsed_time = et - st  # cpu + io = full time
    # print(f"Execution time: {elapsed_time} seconds")
    # print(I)
    # print(I[0])
    return get_results(
        start_year,
        end_year,
        results,
        input_serial,
        people_list,
        supervisory,
        legislative,
        strategic,
    )


def syntactic_search(
    query,
    option,
    start_year,
    end_year,
    input_serial,
    people_list,
    supervisory,
    legislative,
    strategic,
    and_param,
    or_param,
    not_param,
    exact_param,
):
    global checkboxes
    fields = list()
    if checkboxes[0] == "3":
        fields.append("title^6")
    if checkboxes[1] == "4":
        fields.append("persian_keywords^5")
        fields.append("english_keywords^5")
    if checkboxes[2] == "5":
        fields.append("abstract^4")
    if checkboxes[3] == "6":
        fields.append("body^3")
    if and_param == "" and or_param == "" and not_param == "" and exact_param == "":
        if query == "":
            if input_serial is not None and input_serial.strip() != "":
                input_serial = replace_dash_with_alphabet(input_serial)
                search_obj = {
                    "size": k,
                    "query": {
                        "query_string": {
                            "default_field": "serial",
                            "query": f"*{input_serial}*",
                        }
                    },
                }
                input_serial = None
            else:  # people
                return get_results(
                    start_year,
                    end_year,
                    get_people(people_list, k),
                    None,
                    None,
                    supervisory,
                    legislative,
                    strategic,
                )
        else:
            search_obj = {
                "size": k,
                "query": {"query_string": {"query": query, "fields": fields}},
            }
    else:
        search_obj = get_search_obj(
            and_param, or_param, not_param, exact_param, fields, k
        )
    response = requests.get(
        BASE_URL + "reports/_search/",
        headers={"Content-Type": "application/json"},
        json=search_obj,
        timeout=30,
    )
    return get_results(
        start_year,
        end_year,
        get_syntactic_results(response.json()["hits"]["hits"]),
        input_serial,
        people_list,
        supervisory,
        legislative,
        strategic,
    )
