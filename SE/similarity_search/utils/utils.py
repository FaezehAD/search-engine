import arabic_reshaper
from bidi.algorithm import get_display
from .report_utils import *
from .article_utils import *


def print_fa(text):
    print(get_display(arabic_reshaper.reshape(text)))


def get_search_obj(and_param, or_param, not_param, exact_param, fields, k):
    new_fields = list()
    for field in fields:
        new_fields.append(field[:-2])
    fields = new_fields
    search_obj = {
        "size": k,
        "query": {"bool": {}},
    }
    if not_param != "":
        search_obj["query"]["bool"]["must_not"] = [
            {"match": {field: not_param}} for field in fields
        ]
    if or_param != "":
        search_obj["query"]["bool"]["should"] = [
            {"match": {field: or_param}} for field in fields
        ]
    if and_param != "":
        search_obj["query"]["bool"]["must"] = [
            {"match": {field: and_param}} for field in fields
        ]
    if exact_param != "":
        search_obj["query"]["bool"]["filter"] = [
            {"match_phrase": {field: exact_param}} for field in fields
        ]
    return search_obj


def convert_persian_number_to_english(strIn: str):
    E2P_map = {
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "۰": "0",
    }
    a = map(lambda ch: E2P_map[ch] if ch in E2P_map else ch, strIn)
    return "".join(list(a))


def get_int(number, is_start):
    if number != "":
        return int(float(number))
    if is_start:
        return -1
    return 1000000


def verify_people(results, people_list, option):
    if results is None:
        return None
    at_least_one = False
    if people_list is not None:
        for people in people_list:
            if people is not None and people != "":
                at_least_one = True
                break
    if not at_least_one:
        return results
    length = len(results)
    i = 0
    while i < length:
        person_exists = False
        if option == "report":
            result_people = get_report_people(results[i][0])  # 2D array
        elif option == "article":
            result_people = get_article_people(results[i][0])
        for result_list in result_people:
            for p in result_list:
                for person in people_list:
                    if person is not None and person != "":
                        if person.strip() in p.name:
                            person_exists = True
                            break
        if not person_exists:
            results.pop(i)
            i = i - 1
            length = length - 1
        i = i + 1
    if len(results) == 0:
        return None
    return results



def get_people(people_list, k, option):
    at_least_one = False
    if people_list is not None:
        for people in people_list:
            if people is not None and people != "":
                at_least_one = True
                break
    if not at_least_one:
        return None
    results = list()
    for people in people_list:
        if people is not None and people != "":
            if option == 'report':
                results.append(get_report_people_filter(people))
            elif option == 'article':
                results.append(get_article_people_filter(people))
    final_results = list()
    for r in results[0]:
        for result in r: # result = Article
            if option == 'report':
                persian_keywords, english_keywords, departments = get_report_details(result)
                final_results.append(
                    (result, 200, persian_keywords, english_keywords, departments)
                )
            elif option == 'article':
                persian_keywords, english_keywords = get_article_details(result)
                final_results.append(
                    (result, 200, persian_keywords, english_keywords, list())
                )
    if len(final_results) == 0:
        return None
    return final_results[0:k]

