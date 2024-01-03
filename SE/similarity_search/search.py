import numpy as np
from sentence_transformers import SentenceTransformer, util
import requests
import copy
from SE.models import *
from .load_indices import *
from .sort_results import *
from .utils.utils import *
from .utils.report_utils import *
from .filter_departments import *
import pickle
from .utils.result import *
from elasticsearch import Elasticsearch


with open("./data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

with open("./data/config_variables/DEFAULT_OPTION.pkl", "rb") as f:
    DEFAULT_OPTION = pickle.load(f)

with open("./data/config_variables/DEFAULT_QUERY_ID.pkl", "rb") as f:
    DEFAULT_QUERY_ID = pickle.load(f)

with open("./data/config_variables/DEFAULT_PEOPLE_LIST.pkl", "rb") as f:
    DEFAULT_PEOPLE_LIST = pickle.load(f)

with open("./data/config_variables/ELK_USER.pkl", "rb") as f:
    ELK_USER = pickle.load(f)

with open("./data/config_variables/ELK_PASSWORD.pkl", "rb") as f:
    ELK_PASSWORD = pickle.load(f)

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(ELK_USER, ELK_PASSWORD),
    timeout=30,
)


def get_raw_results(request_session):
    with open("./data/config_variables/DEFAULT_QUERY_ID.pkl", "rb") as f:
        DEFAULT_QUERY_ID = pickle.load(f)
    query_id = request_session.get("query_id", DEFAULT_QUERY_ID)
    with open(f"./data/raw_results/{query_id}.pkl", "rb") as f:
        raw_results = pickle.load(f)
    new_raw = list()
    if raw_results is not None:
        for r in raw_results:
            new_raw.append(r)
    return new_raw


def get_min_score(request_session):
    option = request_session.get("option", DEFAULT_OPTION)
    return sort_results_cos_sim(
        get_raw_results(request_session), asc=False, option=option
    )


def get_max_score(request_session):
    option = request_session.get("option", DEFAULT_OPTION)
    return sort_results_cos_sim(
        get_raw_results(request_session), asc=True, option=option
    )


def get_date_ascending(request_session):
    option = request_session.get("option", DEFAULT_OPTION)
    raw_results = get_raw_results(request_session)
    if raw_results is None:
        return (False, None)
    is_available, results = sort_results_date(raw_results, asc=True, option=option)
    return (is_available, results)


def get_date_descending(request_session):
    option = request_session.get("option", DEFAULT_OPTION)
    raw_results = get_raw_results(request_session)
    if raw_results is None:
        return (False, None)
    is_available, results = sort_results_date(raw_results, asc=False, option=option)
    return (is_available, results)


with open("./SE/embeddings/report_keywords_indices.txt", "r") as f:
    keywords_ids = f.readlines()

# with open("./SE/embeddings/report_title_xlm_indices.txt", "r") as f:
with open("./SE/embeddings/report_title_indices.txt", "r") as f:
    report_title_ids = f.readlines()

with open("./SE/embeddings/report_abstract_indices.txt", "r") as f:
    abstract_ids = f.readlines()

with open("./SE/embeddings/report_body_indices.txt", "r") as f:
    body_ids = f.readlines()

report_keywords_index = load_report_index("keywords")
report_title_index = load_report_index("title")
article_title_index = load_article_index("title")
# report_title_index = load_report_index("title_xlm")
report_abstract_index = load_report_index("abstract")
report_body_index = load_report_index("body")

k = read_k()


def replace_dash_with_alphabet(string):
    return string.replace("-", "a")


def get_embeddings(embedding_type, request_session):
    option = request_session.get("option", DEFAULT_OPTION)
    sentence_embeddings = np.loadtxt(
        f"./SE/embeddings/{option}_{embedding_type}_embeddings.txt", dtype=np.float32
    )
    return sentence_embeddings


def get_semantic_results(indices, ids, xq, embeddings, option):
    results = list()
    ids_to_return = list()
    for item in indices:
        id = int(ids[int(item)].strip())
        if id in ids_to_return:
            continue
        ids_to_return.append(id)
        embedding = embeddings[int(item)]
        score = util.cos_sim(xq, embedding)
        if option == "report":
            result = Report.objects.get(pk=id)
            persian_keywords, english_keywords, departments = get_report_details(result)
        elif option == "article":
            result = Article.objects.get(pk=id)
            departments = list()
            persian_keywords, english_keywords = get_article_details(result)
        results.append(
            Result(
                result,
                round(score.item() * 100, 2),
                persian_keywords,
                english_keywords,
                departments,
            )
        )
    return results


def get_syntactic_results(response_hits, option):
    results = list()
    departments = list()
    for item in response_hits:
        if option == "report":
            result = Report.objects.get(pk=item["_id"])
            persian_keywords, english_keywords, departments = get_report_details(result)
        elif option == "article":
            result = Article.objects.get(pk=item["_id"])
            persian_keywords, english_keywords = get_article_details(result)
        # doc = item["_source"]
        # rate = es.similarity(query=query, doc=doc, method="cosine")
        results.append(
            Result(result, 200, persian_keywords, english_keywords, departments)
        )
    return results


def get_results(
    results,
    request_session,
):
    option = request_session.get("option", DEFAULT_OPTION)
    start_year = request_session.get("start_year", -1)
    end_year = request_session.get("end_year", -1)
    serial = request_session.get("serial", "")
    supervisory = request_session.get("supervisory", "")
    legislative = request_session.get("legislative", "")
    strategic = request_session.get("strategic", "")
    people_list = request_session.get("people_list", DEFAULT_PEOPLE_LIST)
    query_id = request_session.get("query_id", DEFAULT_QUERY_ID)
    if people_list is not None and len(people_list) != 0:
        results = verify_people(results, people_list, option)
    if option == "report":
        results = verify_types(
            verify_serials(
                results,
                serial,
            ),
            supervisory,
            legislative,
            strategic,
        )
    raw_results = copy.copy(
        delete_outdated_results(delete_min_rate(results), start_year, end_year)
    )
    with open(f"./data/raw_results/{query_id}.pkl", "wb") as f:
        pickle.dump(raw_results, f)
    return get_min_score(request_session)


def semantic_search(
    request_session,
):
    query = request_session.get("query", "")
    option = request_session.get("option", DEFAULT_OPTION)
    with open("./data/config_variables/DEFAULT_CHECKBOXES.pkl", "rb") as f:
        DEFAULT_CHECKBOXES = pickle.load(f)
    checkboxes = request_session.get("checkboxes", DEFAULT_CHECKBOXES)
    results = None
    # input_ids = tokenizer.encode(query, add_special_tokens=True, return_tensors="pt")
    # with torch.no_grad():
    #     output = model(input_ids)
    # xq = output.last_hidden_state.mean(dim=1).squeeze().numpy()
    xq = model.encode([query]).astype(np.float32)
    if option == "report":
        if checkboxes[0] == "3":
            sentence_embeddings = get_embeddings("title", request_session)
            _, I = report_title_index.search(xq, k)
            results = get_semantic_results(
                I[0], report_title_ids, xq, sentence_embeddings, option
            )
        elif checkboxes[1] == "4":
            sentence_embeddings = get_embeddings("keywords", request_session)
            _, I = report_keywords_index.search(xq, k)
            results = get_semantic_results(
                I[0], keywords_ids, xq, sentence_embeddings, option
            )
        elif checkboxes[2] == "5":
            sentence_embeddings = get_embeddings("abstract", request_session)
            _, I = report_abstract_index.search(xq, k)
            results = get_semantic_results(
                I[0], abstract_ids, xq, sentence_embeddings, option
            )
        elif checkboxes[3] == "6":
            sentence_embeddings = get_embeddings("body", request_session)
            _, I = report_body_index.search(xq, k)
            results = get_semantic_results(
                I[0], body_ids, xq, sentence_embeddings, option
            )
        else:
            sentence_embeddings = get_embeddings("title", request_session)
            _, I = report_title_index.search(xq, k)
            results = get_semantic_results(
                I[0], report_title_ids, xq, sentence_embeddings, option
            )
    elif option == "article":
        with open("./SE/embeddings/article_title_indices.txt", "r") as f:
            article_title_ids = f.readlines()
        article_sentence_embeddings = np.loadtxt(
            f"./SE/embeddings/article_title_embeddings.txt", dtype=np.float32
        )
        _, I = article_title_index.search(xq, k)
        results = get_semantic_results(
            I[0], article_title_ids, xq, article_sentence_embeddings, option
        )
    # et = datetime.datetime.now()
    # elapsed_time = et - st  # cpu + io = full time
    # print(f"Execution time: {elapsed_time} seconds")
    # print(I)
    # print(I[0])
    return get_results(
        results,
        request_session,
    )


def syntactic_search(
    request_session,
):
    query = request_session.get("query", "")
    option = request_session.get("option", DEFAULT_OPTION)
    input_serial = request_session.get("serial", "")
    people_list = request_session.get("people_list", DEFAULT_PEOPLE_LIST)
    with open("./data/config_variables/DEFAULT_CHECKBOXES.pkl", "rb") as f:
        DEFAULT_CHECKBOXES = pickle.load(f)
    checkboxes = request_session.get("checkboxes", DEFAULT_CHECKBOXES)
    and_param = request_session.get("and_param", "")
    or_param = request_session.get("or_param", "")
    not_param = request_session.get("not_param", "")
    exact_param = request_session.get("exact_param", "")
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
                    get_people(people_list, k, option),
                    request_session,
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
        f"{BASE_URL}{option}s/_search/",
        headers={"Content-Type": "application/json"},
        json=search_obj,
        timeout=30,
    )

    return get_results(
        get_syntactic_results(response.json()["hits"]["hits"], option),
        request_session,
    )
