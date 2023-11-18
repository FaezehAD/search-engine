from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .similarity_search.search import *
from .similarity_search.utils.report_utils import *
from .similarity_search.utils.utils import *
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
import requests
from decouple import config
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dotenv import *
import datetime
import pytz
from persiantools.jdatetime import JalaliDateTime
import uuid
from django.core.paginator import Paginator


# from django.contrib.auth.forms import UserCreationForm

threshold = config("THRESHOLD")
show_feedback = config("SHOW_FEEDBACK")
BASE_URL = config("BASE_URL")


def index(request):
    return render(
        request,
        "SE/index.html",
        context={"option": get_option()},
    )


def guide(request):
    return render(request, "SE/guide.html")


def get_req_type(request):
    try:
        data = json.load(request)
        if "date" in data:  # sort
            return (1, data)
        elif "is_correct" in data:  # feedback
            return (2, data)
        elif "result_id" in data:  # click
            return (3, data)
    except Exception:
        return (4, None)  # normal search


def search_results(request):
    global BASE_URL
    req_type, data = get_req_type(request)
    if req_type == 1:
        departments = data["departments"]
        date = data["date"]
        ascending = data["ascending"]
        query = data["query"]
        if date == 1:
            if ascending == 1:
                is_available, results = get_date_ascending()
            else:
                is_available, results = get_date_descending()
        else:
            if ascending == 1:
                is_available, results = get_max_score()
            else:
                is_available, results = get_min_score()
        if len(departments) != 0:
            is_available, results = filter_departments(results, departments)
        return HttpResponse(
            render_to_string(
                "SE/search_results_partial.html",
                context={
                    "results": results,
                    "is_available": is_available,
                    "option": get_option(),
                },
            )
        )

    elif req_type == 2:  # feedback
        result_id = data["result_id"]
        is_correct = data["is_correct"]
        query_id = data["query_id"]
        json_obj = {
            "script": {
                "source": "for (r in ctx._source.results) { if(r.result_id == params.result_id){r.feedback = params.feedback} }",
                "lang": "painless",
                "params": {
                    "result_id": str(result_id),
                    "feedback": "T" if is_correct else "F",
                },
            }
        }
        requests.post(f"{BASE_URL}logs/_update/{query_id}", json=json_obj)
        return HttpResponse()

    elif req_type == 3:  # click
        result_id = data["result_id"]
        query_id = data["query_id"]

        json_obj = {
            "script": {
                "source": "for (r in ctx._source.results) { if(r.result_id == params.result_id){r.click = params.click} }",
                "lang": "painless",
                "params": {"result_id": str(result_id), "click": True},
            }
        }
        requests.post(f"{BASE_URL}logs/_update/{query_id}", json=json_obj)

        return HttpResponse()

    # now req_type is 4

    query = request.POST.get("query")
    option = request.POST.get("options")
    print(f"option: {option}")
    set_option(option)
    search_method = request.POST.get("search-method")
    people_list = list()
    start_year = end_year = -1
    checkboxes = list()
    checkboxes.append(request.POST.get("titles-checkbox", ""))
    checkboxes.append(request.POST.get("keywords-checkbox", ""))
    checkboxes.append(request.POST.get("abstracts-checkbox", ""))
    checkboxes.append(request.POST.get("bodies-checkbox", ""))
    checkboxes.append(search_method)

    if search_method:  # advanced search
        set_checkboxes(checkboxes)
        set_search_method(search_method)

    serial = verify_serial(
        convert_persian_number_to_english(request.POST.get("serial", ""))
    )

    start_year = get_int(
        convert_persian_number_to_english(request.POST.get("start-year", "")), True
    )
    end_year = get_int(
        convert_persian_number_to_english(request.POST.get("end-year", "")), False
    )
    people_list.append(request.POST.get("people-1", ""))
    people_list.append(request.POST.get("people-2", ""))
    people_list.append(request.POST.get("people-3", ""))
    supervisory = request.POST.get("supervisory-checkbox", "")
    legislative = request.POST.get("legislative-checkbox", "")
    strategic = request.POST.get("strategic-checkbox", "")
    search_method = get_search_method()
    and_param = request.POST.get("and", "")
    or_param = request.POST.get("or", "")
    not_param = request.POST.get("not", "")
    exact_param = request.POST.get("exact", "")
    if search_method == "2" and query != "":
        is_available, results = semantic_search(
            query,
            option,
            start_year,
            end_year,
            serial,
            people_list,
            supervisory,
            legislative,
            strategic,
        )
    else:
        is_available, results = syntactic_search(
            query,
            option,
            start_year,
            end_year,
            serial,
            people_list,
            supervisory,
            legislative,
            strategic,
            and_param,
            or_param,
            not_param,
            exact_param,
        )
    if option == "report":
        departments = get_departments_with_number(get_raw_results())
    else:
        departments = list()
    # store log
    report_types = list()
    if strategic == "9":
        report_types.append("مطالعات راهبردی")
    if legislative == "8":
        report_types.append("تقنینی")
    if supervisory == "7":
        report_types.append("نظارتی")
    report_people = list()
    for p in people_list:
        if p is not None and p != "":
            report_people.append(p)
    search_fields = list()
    search_checkboxes = get_checkboxes()
    if search_checkboxes[0] == "3":
        search_fields.append("عنوان")
    if search_checkboxes[1] == "4":
        search_fields.append("کلیدواژه")
    if search_checkboxes[2] == "5":
        search_fields.append("چکیده")
    if search_checkboxes[3] == "6":
        search_fields.append("متن")
    results_list = list()
    if results is not None:
        for r in results:
            results_list.append(
                {
                    "result_id": str(r[0].id),
                    "title": r[0].title,
                    "click": False,
                    "feedback": "N",  # True, False, Neutral
                }
            )

    curr_time = datetime.datetime.now(pytz.timezone("Asia/Tehran"))
    hour = curr_time.hour
    minute = curr_time.minute
    second = curr_time.second
    curr_date = JalaliDateTime.now()
    formatted_date = curr_date.strftime("%Y-%m-%d")
    formatted_time = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    curr_timestamp = f"{formatted_date} {formatted_time}"
    print(curr_timestamp)
    unique_id = str(uuid.uuid4())
    id_without_dash = f"{unique_id[:8]}{unique_id[9:13]}{unique_id[14:18]}{unique_id[19:23]}{unique_id[24:]}"
    json_obj = {
        "is_semantic": (search_method == "2"),
        "main_query": query,
        "and_query": and_param,
        "or_query": or_param,
        "not_query": not_param,
        "exact_query": exact_param,
        "start_year": start_year,
        "end_year": end_year,
        "serial": serial,
        "report_types": report_types,
        "report_people": report_people,
        "search_fields": search_fields,
        "results": results_list,
        "timestamp": curr_timestamp,
    }
    requests.post(f"{BASE_URL}logs/_doc/{id_without_dash}", json=json_obj, timeout=30)

    return render(
        request,
        "SE/search_results.html",
        context={
            "query": query,
            "results": results,
            "is_available": is_available,
            "departments": departments,
            "show_feedback": config("SHOW_FEEDBACK"),
            "query_id": id_without_dash,
            "option": option,
        },
    )


def advanced_search(request):
    checkboxes = get_checkboxes()
    return render(
        request,
        "SE/advanced_search.html",
        context={
            "titles_checkbox": checkboxes[0],
            "keywords_checkbox": checkboxes[1],
            "abstracts_checkbox": checkboxes[2],
            "bodies_checkbox": checkboxes[3],
            "syntactic_radio": checkboxes[4],
            "option": get_option(),
        },
    )


def article_details(request, id):
    identified_article = get_object_or_404(Article, id=id)
    return render(
        request,
        "SE/article_details.html",
        context={
            "article": identified_article,
            "persian_keywords": identified_article.persian_keywords.all(),
            "english_keywords": identified_article.english_keywords.all(),
            "authors": identified_article.authors.all(),
        },
    )


def report_details(request, id):
    identified_report = get_object_or_404(Report, id=id)
    report_url = "https://rc.majlis.ir" + identified_report.path
    response = requests.get(report_url)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all(
        "img", src=lambda src: src.startswith("https://rc.majlis.ir/")
    )
    response = requests.get([image["src"] for image in images][0])
    image_content = response.content
    departments = get_departments()

    index = find_img_index(identified_report.departments.all(), departments)

    identified_report_departments = get_result_departments(identified_report)
    eitaa_url = f"https://eitaa.com/share/url?url={report_url}"
    return render(
        request,
        "SE/report_details.html",
        context=get_report_details_context(
            identified_report,
            eitaa_url,
            image_content,
            identified_report_departments,
            index,
        ),
    )


def signin(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")

        user = None
        if username == config("ADMIN_USERNAME") and password == config(
            "ADMIN_PASSWORD"
        ):
            user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "/")
            return redirect(next_url)
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است!")
            return redirect("signin-page")

    else:  # request.method == "GET"
        return render(request, "SE/signin.html")


def signout(request):
    logout(request)
    return redirect("index-page")


@login_required
def admin_panel(request):
    return render(request, "SE/admin_panel.html")


@login_required
def settings(request):
    global threshold
    global show_feedback
    if request.method == "POST":
        threshold = int(float(request.POST.get("threshold")))
        show_feedback = request.POST.get("feedback")
        set_key(".env", "THRESHOLD", str(threshold))
        if show_feedback == "T":
            set_key(".env", "SHOW_FEEDBACK", "T")
        else:
            set_key(".env", "SHOW_FEEDBACK", "F")

        return redirect("admin-page")

    return render(
        request,
        "SE/settings.html",
        context={
            "show_feedback": show_feedback,
            "curr_threshold": threshold,
        },
    )


@login_required
def show_logs(request):
    if request.method == "POST":
        user_query = request.POST.get("query")
        if user_query == "":
            search_obj = {"query": {"match_all": {}}, "size": 10000}
        else:
            search_obj = {
                "query": {
                    "query_string": {
                        "fields": [
                            "main_query",
                            "and_query",
                            "or_query",
                            "not_query",
                            "exact_query",
                            "report_people",
                        ],
                        "query": f"*{user_query}*",
                    }
                },
            }
    else:
        search_obj = {"query": {"match_all": {}}, "size": 10000}
    response = requests.get(BASE_URL + "logs/_search", json=search_obj)
    logs = response.json()["hits"]["hits"]
    logs_list = list()
    for l in logs:
        log_results = l["_source"]["results"]
        clicked = correct = incorrect = 0
        for r in log_results:
            if r["click"] == True:
                clicked += 1
            if r["feedback"] == "T":
                correct += 1
            elif r["feedback"] == "F":
                incorrect += 1
        logs_list.append(
            {
                "log_id": l["_id"],
                "is_semantic": l["_source"]["is_semantic"],
                "main_query": l["_source"]["main_query"],
                "and_query": l["_source"]["and_query"],
                "or_query": l["_source"]["or_query"],
                "not_query": l["_source"]["not_query"],
                "exact_query": l["_source"]["exact_query"],
                "start_year": l["_source"]["start_year"],
                "end_year": l["_source"]["end_year"],
                "serial": l["_source"]["serial"],
                "report_types": l["_source"]["report_types"],
                "report_people": l["_source"]["report_people"],
                "search_fields": l["_source"]["search_fields"],
                "results": log_results,
                "clicked": clicked,
                "correct": correct,
                "incorrect": incorrect,
                "timestamp": l["_source"]["timestamp"],
            }
        )
    objects_per_page = 10
    paginator = Paginator(logs_list, objects_per_page)
    page_number = request.GET.get("page")
    try:
        paginated_objects = paginator.page(page_number)
    except:
        paginated_objects = paginator.page(1)

    return render(
        request, "SE/logs.html", context={"paginated_objects": paginated_objects}
    )


@login_required
def log_details(request, id):
    response = requests.get(f"{BASE_URL}logs/_doc/{id}")
    l = response.json()
    print(f'time: {l["_source"]["timestamp"]}')
    return render(
        request,
        "SE/log_details.html",
        context={
            "log": {
                "log_id": l["_id"],
                "is_semantic": l["_source"]["is_semantic"],
                "main_query": l["_source"]["main_query"],
                "and_query": l["_source"]["and_query"],
                "or_query": l["_source"]["or_query"],
                "not_query": l["_source"]["not_query"],
                "exact_query": l["_source"]["exact_query"],
                "start_year": l["_source"]["start_year"],
                "end_year": l["_source"]["end_year"],
                "serial": l["_source"]["serial"],
                "report_types": l["_source"]["report_types"],
                "report_people": l["_source"]["report_people"],
                "search_fields": l["_source"]["search_fields"],
                "results": l["_source"]["results"],
                "timestamp": l["_source"]["timestamp"],
            },
        },
    )
