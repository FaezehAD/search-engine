import pandas as pd
from SE.models import *
import os
import re

ids = set()
for i in range(0, len(df2)):
    ids.add(df2[i]["ID"])

ids_list = list()
for i in range(0, len(df2)):
    ids_list.append(df2[i]["ID"])


def clean_string(str):
    cleaned_str = re.sub(r"[^a-zA-Z0-9-]", "", str)
    return cleaned_str


limit_length = 14000

doc_dict = dict()

directory = "./data_text/report/txt/"
doc_list = list()
for filename in os.listdir(directory):
    filename = filename[:-4]
    clean_filename = clean_string(filename)
    if " " in filename or "$" in filename or "م" in filename:
        doc_dict[clean_filename] = filename
    doc_list.append(clean_filename)

df = pd.read_json("./data_text/report/info.json")
df2 = df.to_dict("records")

with open("./upload_data/database/report_exceptions.txt", "w") as exceptions:
    exceptions.write("")

with open("./upload_data/database/empty_abstract_and_body.txt", "w") as exceptions:
    exceptions.write("")

serials = list()

for i in range(0, len(df2)):
    try:
        report_serial = df2[i]["Info"]["شماره مسلسل"]
    except Exception:
        report_serial = None
    if report_serial is not None:
        serials.append(report_serial)


def get_person(person_name):
    try:
        person = Person.objects.get(
            pk=person_name)
    except Person.DoesNotExist:
        person = Person.objects.create(
            name=person_name)
    return person


def get_all_people(people_list):
    people = []
    for person_name in people_list:
        if person_name != "":
            people.append(get_person(person_name))
    return people


def get_english_phrase(keyword):
    try:
        phrase = EnglishPhrase.objects.get(value=keyword)
    except EnglishPhrase.DoesNotExist:
        phrase = EnglishPhrase.objects.create(value=keyword)
    return phrase


def get_pesian_phrase(keyword):
    try:
        phrase = PersianPhrase.objects.get(value=keyword)
    except PersianPhrase.DoesNotExist:
        phrase = PersianPhrase.objects.create(value=keyword)
    return phrase


for i in range(0, len(df2)):
    print(i)
    report = None
    report_abstract = df2[i]["Abstract"]
    if report_abstract == "":
        report_abstract = None
    try:
        report_publication_date = df2[i]["Info"]["تاریخ انتشار"]
    except Exception:
        report_publication_date = None
    try:
        report_year = int(df2[i]["Info"]["سال"])
    except Exception:
        report_year = -1
    try:
        report_serial = df2[i]["Info"]["شماره مسلسل"]
    except Exception:
        report_serial = None
    report_body = None
    report_originality = False
    report_multiple_editions = False
    if report_serial is not None:
        if serials.count(report_serial) > 1:
            report_multiple_editions = True
        file_title = None
        if report_serial in doc_list:
            file_title = report_serial
            report_originality = True
        else:
            if "-" in report_serial:
                index = report_serial.index("-")
                report_serial = report_serial[:index]
            if (report_serial + "-1") in doc_list:
                file_title = report_serial + "-1"
            elif (report_serial + "-2") in doc_list:
                file_title = report_serial + "-2"
            elif (report_serial + "-3") in doc_list:
                file_title = report_serial + "-3"
            elif (report_serial + "-4") in doc_list:
                file_title = report_serial + "-4"
            elif (report_serial + "-5") in doc_list:
                file_title = report_serial + "-5"
            elif (report_serial + "-6") in doc_list:
                file_title = report_serial + "-6"
            elif (report_serial + "-7") in doc_list:
                file_title = report_serial + "-7"
            elif (report_serial + "-8") in doc_list:
                file_title = report_serial + "-8"
            elif (report_serial + "-9") in doc_list:
                file_title = report_serial + "-9"
            elif (report_serial + "-10") in doc_list:
                file_title = report_serial + "-10"
        if file_title is not None:
            try:
                with open((directory + file_title + ".txt"), "r", encoding="utf_8") as file:
                    buffer = file.read()
                    if len(buffer) > 300:
                        report_body = buffer
            except FileNotFoundError:
                file_title = doc_dict[file_title]
                with open((directory + file_title + ".txt"), "r", encoding="utf_8") as file:
                    buffer = file.read()
                    if len(buffer) > 300:
                        report_body = buffer
    if (report_abstract is None and report_body is None) or (
            report_abstract is not None and len(report_abstract) > limit_length):
        with open("./upload_data/database/empty_abstract_and_body.txt", "a") as exceptions:
            exceptions.write(f"{df2[i]["ID"]}\n")
        continue
    try:
        r_type = df2[i]["Info"]["نوع"]
    except Exception:
        r_type = None
    if r_type == "":
        r_type = None
    report_publish_type = df2[i]["PublishType"]
    if report_publish_type == "":
        report_publish_type = None
    report_dl_path = df2[i]["DLpath"]
    if report_dl_path == "":
        report_dl_path = None
        if report_publish_type == "انتشار عمومی":
            report_publish_type = "عدم دسترسی به متن"
    try:
        report = Report.objects.create(id=int(df2[i]["ID"]),
                                       path=df2[i]["Path"],
                                       title=df2[i]["Title"],
                                       publication_date=report_publication_date,
                                       year=report_year,
                                       serial=report_serial,
                                       report_type=r_type,
                                       publish_type=report_publish_type,
                                       dl_path=report_dl_path,
                                       abstract=report_abstract,
                                       abstract_preprocessed=None,
                                       abstract_summary=None,
                                       body=report_body,
                                       body_preprocessed=None,
                                       body_summary=None,
                                       originality=report_originality,
                                       multiple_editions=report_multiple_editions)
    except Exception as e:
        with open("./upload_data/database/report_exceptions.txt", "a") as exceptions:
            exceptions.write(str(e) + "\n")
        continue
    departments_list = df2[i]["Departments"]
    if departments_list != "":
        for department_name in departments_list:
            if department_name != "":
                try:
                    department = Department.objects.get(pk=department_name)
                except Department.DoesNotExist:
                    department = Department.objects.create(
                        name=department_name)
                report.departments.add(department)
    keywords_list = df2[i]["Keywords"]
    persian_key_list = None
    english_key_list = None
    if len(keywords_list) > 0:
        try:
            persian_key_list = keywords_list["فارسی"]
        except Exception:
            pass
        try:
            english_key_list = keywords_list["انگلیسی"]
        except Exception:
            pass
    if persian_key_list is not None:
        for keyword in persian_key_list:
            if keyword != "" and keyword != "/":
                report.persian_keywords.add(get_pesian_phrase(keyword))
    if english_key_list is not None:
        for keyword in english_key_list:
            if keyword != "" and keyword != "/":
                report.english_keywords.add(get_english_phrase(keyword))
    for key, value in df2[i]["Roles"].items():
        if len(value) > 0:
            if key == "اظهارنظر کننده":
                report.commenters.add(*(get_all_people(value)))
            elif key == "اظهار نظرکنندگان خارج از مرکز":
                report.commenters_out_of_center.add(*(get_all_people(value)))
            elif key == "ویراستار":
                report.editors.add(*(get_all_people(value)))
            elif key == "سرویراستار":
                report.editors_in_chief.add(*(get_all_people(value)))
            elif key == "ویراستار ادبی":
                report.literary_editors.add(*(get_all_people(value)))
            elif key == "ویراستار فنی":
                report.technical_editors.add(*(get_all_people(value)))
            elif key == "ویراستار تخصصی":
                report.professional_editors.add(*(get_all_people(value)))
            elif key == "همکاران":
                report.colleagues.add(*(get_all_people(value)))
            elif key == "همکاران خارج از مرکز":
                report.colleagues_out_of_center.add(*(get_all_people(value)))
            elif key == "مشاور":
                report.consultants.add(*(get_all_people(value)))
            elif key == "مشاوران خارج از مرکز":
                report.consultants_out_of_center.add(*(get_all_people(value)))
            elif key == "گروه مشاوران علمی":
                report.scientific_consultants_group.add(
                    *(get_all_people(value)))
            elif key == "کارگروه":
                report.committee.add(*(get_all_people(value)))
            elif key == "رئیس کارگروه":
                report.committee_head.add(*(get_all_people(value)))
            elif key == "اعضای کارگروه":
                report.committee_members.add(*(get_all_people(value)))
            elif key == "همکاران کارگروه":
                report.committee_colleagues.add(*(get_all_people(value)))
            elif key == "مشاور کارگروه":
                report.committee_consultants.add(*(get_all_people(value)))
            elif key == "ناظران":
                report.supervisors.add(*(get_all_people(value)))
            elif key == "ناظر علمی":
                report.scientific_supervisors.add(*(get_all_people(value)))
            elif key == "خلاصه کننده":
                report.summarizers.add(*(get_all_people(value)))
            elif key == "ترجمه" or key == "مترجم":
                report.translators.add(*(get_all_people(value)))
            elif key == "تنظیم کننده":
                report.regulators.add(*(get_all_people(value)))
            elif key == "ترجمه و تدوین کنندگان":
                report.translators_and_compilers.add(*(get_all_people(value)))
            elif key == "ترجمه و تلخیص کنندگان":
                report.translators_and_summarizers.add(
                    *(get_all_people(value)))
            elif key == "ترجمه و تالیف":
                report.translators_and_gatherers.add(*(get_all_people(value)))
            elif key == "تدوین و تنظیم":
                report.compilers_and_regulators.add(*(get_all_people(value)))
            elif key == "تلخیص و تدوین":
                report.summarizers_and_compilers.add(*(get_all_people(value)))
            elif key == "اشخاص حقیقی":
                report.real_people.add(*(get_all_people(value)))
            elif key == "اشخاص حقوقی":
                report.legal_people.add(*(get_all_people(value)))
            elif key == "تهیه و تدوین" or key == "کاری از" or key == "تهیه شده":
                report.producers.add(*(get_all_people(value)))
            elif key == "مسئول نشست تخصصی":
                report.technical_session_chairpeople.add(
                    *(get_all_people(value)))
            elif key == "گرافیک اطلاع رسان":
                report.infographics.add(*(get_all_people(value)))
            elif key == "مدیر مطالعه":
                report.study_managers.add(*(get_all_people(value)))
            elif key == "سخنران":
                report.lecturers.add(*(get_all_people(value)))
            elif key == "طراح":
                report.designers.add(*(get_all_people(value)))
            elif key == "صفحه آرا":
                report.layout_person.add(*(get_all_people(value)))
            elif key == "کارشناس فنی":
                report.technical_experts.add(*(get_all_people(value)))
            elif key == "جمعبندی":
                report.aggregation.add(*(get_all_people(value)))
            elif key == "مجری تحقیق":
                report.research_executors.add(*(get_all_people(value)))
            elif key == "متقاضی":
                report.applicants.add(*(get_all_people(value)))
            elif key == "شرکت کنندگان در نشست های کارشناسی":
                report.participants_in_expertise_sessions.add(
                    *(get_all_people(value)))
            elif key == "شرکت کنندگان در بحث گروهی متمرکز":
                report.participants_in_intensive_group_discussions.add(
                    *(get_all_people(value)))

