import arabic_reshaper
from bidi.algorithm import get_display


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
    if number != '':
        return int(float(number))
    if is_start:
        return -1
    return 1000000