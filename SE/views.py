from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .similarity_search.search import *
from .similarity_search.utils.report_utils import *
from .similarity_search.utils.utils import *
from .similarity_search.utils.plagiarism import *
from .similarity_search.utils.compare_texts import *
from .similarity_search.utils.manage_variables import *
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pickle
from django.core.paginator import Paginator

with open("./data/config_variables/BASE_URL.pkl", "rb") as f:
    BASE_URL = pickle.load(f)

with open("./data/config_variables/DEFAULT_OPTION.pkl", "rb") as f:
    DEFAULT_OPTION = pickle.load(f)

with open("./data/config_variables/DEFAULT_CHECKBOXES.pkl", "rb") as f:
    DEFAULT_CHECKBOXES = pickle.load(f)

with open("./data/config_variables/DEFAULT_SEARCH_METHOD.pkl", "rb") as f:
    DEFAULT_SEARCH_METHOD = pickle.load(f)


normalizer = Normalizer()


def index(request):
    logout(request)
    request.session["checkboxes"] = DEFAULT_CHECKBOXES

    request.session["option"] = DEFAULT_OPTION

    with open("./data/config_variables/DEFAULT_QUERY_ID.pkl", "rb") as f:
        DEFAULT_QUERY_ID = pickle.load(f)
    request.session["query_id"] = DEFAULT_QUERY_ID

    request.session["search_method"] = DEFAULT_SEARCH_METHOD

    session_id = request.session.session_key
    print(f"session id: {session_id}")
    return render(
        request,
        "SE/index.html",
        context={"option": request.session.get("option", DEFAULT_OPTION)},
    )


def guide(request):
    return render(request, "SE/guide.html")


def get_req_type(request):
    data = None
    req_type = 4  # normal search
    try:
        data = json.load(request)
        if "date" in data:  # sort
            req_type = 1
        elif "is_correct" in data:  # feedback
            req_type = 2
        elif "result_id" in data:  # click
            req_type = 3
    except Exception:
        pass  # normal search
    return (req_type, data)


def search_results(request):
    session_id = request.session.session_key
    print(f"session id: {session_id}")
    req_type, data = get_req_type(request)
    if req_type == 1:
        departments = data["departments"]
        date = data["date"]
        ascending = data["ascending"]
        query = data["query"]
        if date == 1:
            if ascending == 1:
                is_available, results = get_date_ascending(request.session)
            else:
                is_available, results = get_date_descending(request.session)
        else:
            if ascending == 1:
                is_available, results = get_max_score(request.session)
            else:
                is_available, results = get_min_score(request.session)
        if len(departments) != 0:
            is_available, results = filter_departments(results, departments)
        return HttpResponse(
            render_to_string(
                "SE/search_results_partial.html",
                context={
                    "results": results,
                    "is_available": is_available,
                    "option": request.session.get("option", DEFAULT_OPTION),
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
        query_id = data["query_id"]
        result_id = data["result_id"]
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

    id_without_dash = get_id_without_dash()
    request.session["query_id"] = id_without_dash

    query = request.POST.get("query")
    request.session["query"] = query

    option = request.POST.get("options")
    request.session["option"] = option

    search_method = request.POST.get("search-method")

    people_list = list()
    start_year = end_year = -1
    checkboxes = list()
    checkboxes.append(request.POST.get("titles-checkbox", ""))
    checkboxes.append(request.POST.get("keywords-checkbox", ""))
    checkboxes.append(request.POST.get("abstracts-checkbox", ""))
    checkboxes.append(request.POST.get("bodies-checkbox", ""))

    if search_method:  # advanced search
        request.session["checkboxes"] = checkboxes
        request.session["search_method"] = search_method

    serial = verify_serial(
        convert_persian_number_to_english(request.POST.get("serial", ""))
    )
    request.session["serial"] = serial
    start_year = get_int(
        convert_persian_number_to_english(request.POST.get("start-year", "")), True
    )
    request.session["start_year"] = start_year
    end_year = get_int(
        convert_persian_number_to_english(request.POST.get("end-year", "")), False
    )
    request.session["end_year"] = end_year
    people_list.append(request.POST.get("people-1", ""))
    people_list.append(request.POST.get("people-2", ""))
    people_list.append(request.POST.get("people-3", ""))
    request.session["people_list"] = people_list

    supervisory = request.POST.get("supervisory-checkbox", "")
    request.session["supervisory"] = supervisory
    legislative = request.POST.get("legislative-checkbox", "")
    request.session["legislative"] = legislative
    strategic = request.POST.get("strategic-checkbox", "")
    request.session["strategic"] = strategic

    search_method = request.session.get("search_method", DEFAULT_SEARCH_METHOD)
    and_param = request.POST.get("and", "")
    request.session["and_param"] = and_param
    or_param = request.POST.get("or", "")
    request.session["or_param"] = or_param
    not_param = request.POST.get("not", "")
    request.session["not_param"] = not_param
    exact_param = request.POST.get("exact", "")
    request.session["exact_param"] = exact_param
    if search_method == "2" and query != "":
        is_available, results = semantic_search(
            request.session,
        )
    else:
        is_available, results = syntactic_search(
            request.session,
        )
    if option == "report":
        departments = get_departments_with_number(get_raw_results(request.session))
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
    search_checkboxes = request.session.get("checkboxes", DEFAULT_CHECKBOXES)
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
                    "result_id": str(r.doc.id),
                    "title": r.doc.title,
                    "click": False,
                    "feedback": "N",  # True, False, Neutral
                }
            )
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
        "timestamp": get_timestamp(),
    }
    requests.post(f"{BASE_URL}logs/_doc/{id_without_dash}", json=json_obj, timeout=30)
    requests.post(f"{BASE_URL}logs2/_doc/{id_without_dash}", json=json_obj, timeout=30)
    with open("./data/config_variables/SHOW_FEEDBACK.pkl", "rb") as f:
        SHOW_FEEDBACK = pickle.load(f)
    return render(
        request,
        "SE/search_results.html",
        context={
            "query": query,
            "results": results,
            "is_available": is_available,
            "departments": departments,
            "show_feedback": SHOW_FEEDBACK,
            "query_id": id_without_dash,
            "option": option,
        },
    )


def advanced_search(request):
    checkboxes = request.session.get("checkboxes", DEFAULT_CHECKBOXES)
    return render(
        request,
        "SE/advanced_search.html",
        context={
            "titles_checkbox": checkboxes[0],
            "keywords_checkbox": checkboxes[1],
            "abstracts_checkbox": checkboxes[2],
            "bodies_checkbox": checkboxes[3],
            "search_method": request.session.get(
                "search_method", DEFAULT_SEARCH_METHOD
            ),
            "option": request.session.get("option", "report"),
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
    image_content = None
    try:
        response = requests.get(report_url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all(
            "img", src=lambda src: src.startswith("https://rc.majlis.ir/")
        )
        response = requests.get([image["src"] for image in images][0])
        image_content = response.content
    except Exception as e:
        print(e)
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
        with open("./data/config_variables/ADMIN_USERNAME.pkl", "rb") as f:
            ADMIN_USERNAME = pickle.load(f)

        with open("./data/config_variables/ADMIN_PASSWORD.pkl", "rb") as f:
            ADMIN_PASSWORD = pickle.load(f)

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
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
def settings_page(request):
    with open("./data/config_variables/THRESHOLD.pkl", "rb") as f:
        threshold = pickle.load(f)
    with open("./data/config_variables/SHOW_FEEDBACK.pkl", "rb") as f:
        show_feedback = pickle.load(f)
    if request.method == "POST":
        threshold = int(request.POST.get("threshold"))
        show_feedback = request.POST.get("feedback")
        set_threshold(threshold)
        set_show_feedback(show_feedback)
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


def plagiarism_detection_input(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        input_keywords = request.POST.get("input_keywords", "")
        is_valid = False
        file_title = ""
        if input_keywords == "":
            form.add_error(None, "لطفا کلمات کلیدی را وارد کنید!")
        else:
            if len(request.FILES) == 0:
                input_text = request.POST.get("input_text", "")
                if input_text != "" and input_keywords != "":
                    file_title = str(get_id_without_dash() + "_" + get_timestamp())
                    save_file(file_title, input_text, input_keywords)
                    is_valid = True
                else:
                    form.add_error(None, "لطفا متن را وارد کنید!")
            else:  # there is a file
                if form.is_valid():
                    file = form.cleaned_data["file"]
                    print(file.name[-4:])
                    if file.name[-4:] != ".txt":
                        form.add_error(None, "لطفا فایل با فرمت txt. را وارد کنید!")
                    else:
                        content = file.read().decode("utf-8")
                        if content == "":
                            form.add_error(None, "لطفا فایل حاوی متن را وارد کنید!")
                        else:
                            file_title = file.name[:-4] + "_" + get_timestamp()
                            save_file(file_title, content, input_keywords)
                            is_valid = True
                else:
                    errors = form.errors
                    print(errors)
        if is_valid:
            return redirect("plagiarism-detection-page", input_title=file_title)
    else:  # GET
        form = UploadFileForm()
    return render(request, "SE/plagiarism_input.html", {"form": form})


def plagiarism_detection(request, input_title):
    input_text = get_input_text(input_title)
    input_keywords_list = get_input_keywords(input_title)
    results = check_plagiarism(input_text, input_keywords_list)
    is_available = len(results) != 0
    return render(
        request,
        "SE/plagiarism_detection.html",
        context={
            "input_title": input_title,
            "input_text": input_text,
            "input_keywords": input_keywords_list,
            "results": results,
            "is_available": is_available,
            "option": "report",
        },
    )


def compare_texts(request, input_title, id):
    global normalizer
    report = get_report_by_id(id)
    report_text = ""
    if report is not None:
        report_text = word_tokenize(report.body_preprocessed)
    input_text = word_tokenize(normalizer.normalize(get_input_text(input_title)))
    input_text_highlighted = compare_strings(input_text, report_text)
    report_text_highlighted = compare_strings(report_text, input_text)
    return render(
        request,
        "SE/compare_texts.html",
        context={
            "input_text": input_text_highlighted,
            "report_text": report_text_highlighted,
        },
    )
