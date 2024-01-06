import arabic_reshaper
from bidi.algorithm import get_display
from .report_utils import *
from .article_utils import *
from .result import *
import uuid
from django.conf import settings
import os
from django import forms
from persiantools.jdatetime import JalaliDateTime
import pytz


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
            result_people = get_report_people(results[i].doc)  # 2D array
        elif option == "article":
            result_people = get_article_people(results[i].doc)
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
            if option == "report":
                results.append(get_report_people_filter(people))
            elif option == "article":
                results.append(get_article_people_filter(people))
    final_results = list()
    for r in results[0]:
        for result in r:
            departments = list()
            if option == "report":
                persian_keywords, english_keywords, departments = get_report_details(
                    result
                )
            elif option == "article":
                persian_keywords, english_keywords = get_article_details(result)
            final_results.append(
                Result(result, 200, persian_keywords, english_keywords, departments)
            )
    if len(final_results) == 0:
        return None
    return final_results[0:k]


def get_timestamp():
    curr_date = JalaliDateTime.now(pytz.timezone("Asia/Tehran"))
    formatted_date_time = curr_date.strftime("%y-%m-%d %H:%M:%S")
    return formatted_date_time


def get_id_without_dash():
    unique_id = str(uuid.uuid4())
    id_without_dash = f"{unique_id[:8]}{unique_id[9:13]}{unique_id[14:18]}{unique_id[19:23]}{unique_id[24:]}"
    return id_without_dash


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="متن ورودی را با فرمت txt. انتخاب کنید.",
        help_text="file size limit: 2.5 MB",
        allow_empty_file=True,
        widget=forms.FileInput(
            attrs={"accept": ".txt"},
        ),
        required=False,
    )
    input_text = forms.CharField(
        label="متن ورودی",
        widget=forms.Textarea(
            attrs={"placeholder": "متن خود را وارد کنید...", "cols": 40, "rows": 10}
        ),
        required=False,
    )
    input_keywords = forms.CharField(
        label="کلمات کلیدی ورودی (در هر خط یک کلمه کلیدی وارد کنید.)",
        widget=forms.Textarea(
            attrs={"placeholder": "کلمات کلیدی را وارد کنید...", "cols": 40, "rows": 6}
        ),
        required=False,
    )


def save_file(input_title, input_text, input_keywords):
    file_path = os.path.join(settings.MEDIA_ROOT, input_title)
    os.makedirs(file_path)
    with open(f"{file_path}/input_keywords.txt", "w") as f:
        f.write(str(input_keywords))
    with open(f"{file_path}/input_text.txt", "w") as f:
        f.write(str(input_text))


def split_string_by_newline(input_str):
    return input_str.splitlines()


def get_input_text(input_title):
    file_path = os.path.join(settings.MEDIA_ROOT, input_title)
    try:
        with open(f"{file_path}/input_text.txt", "r", encoding="utf_8") as file:
            input_text = file.read()
    except:
        input_text = ""
    return input_text


def get_input_keywords(input_title):
    input_keywords_list = list()
    file_path = os.path.join(settings.MEDIA_ROOT, input_title)
    try:
        with open(f"{file_path}/input_keywords.txt", "r", encoding="utf_8") as file:
            input_keywords_list = split_string_by_newline(file.read())
    except:
        input_keywords_list = list()
    return input_keywords_list
