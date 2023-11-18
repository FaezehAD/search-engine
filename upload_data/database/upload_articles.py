import pandas as pd
from SE.models import *


df = pd.read_json("./data_text/AAoutput_04-08 15-17-26.json")
df2 = df.to_dict("records")

with open("./upload_data/database/article_exceptions.txt", "w") as exceptions:
    exceptions.write("")


def write_exception(exception_text):
    with open("./upload_data/database/article_exceptions.txt", "a") as exceptions:
        exceptions.write(str(exception_text) + "\n")


def get_pesian_phrase(keyword):
    try:
        phrase = PersianPhrase.objects.get(value=keyword)
    except PersianPhrase.DoesNotExist:
        phrase = PersianPhrase.objects.create(value=keyword)
    return phrase


for i in range(0, len(df2)):
    article_cites = df2[i]["cites"]
    if (article_cites == "ثبت نشده است." or article_cites == "ثبت نشده است" or
            article_cites == ""):
        article_cites = None
    article_references = df2[i]["references"]
    if (article_references == "ثبت نشده است." or article_references == "ثبت نشده است" or
            article_references == ""):
        article_references = None
    article_abstract = df2[i]["abstract"]
    if (article_abstract == "لطفا برای مشاهده چکیده به متن کامل (PDF) مراجعه فرمایید." or
        article_abstract == "لطفا برای مشاهده چکیده به متن کامل (pdf) مراجعه فرمایید." or
        article_abstract == "متن کامل این مقاله به زبان انگلیسی می باشد, لطفا برای مشاهده متن کامل مقاله به بخش انگلیسی مراجعه فرمایید.لطفا برای مشاهده متن کامل این مقاله اینجا را کلیک کنید" or
            article_abstract == ""):
        article_abstract = None
        continue
    year = df2[i]["info"]["year"]
    if year == "":
        article_year = -1
    else:
        try:
            article_year = int(year)
        except ValueError:
            article_year = -1
    if df2[i]["type"] != "همایش":
        continue

    article_seminar = df2[i]["info"]["seminar"]
    if article_seminar == "":
        article_seminar = None
    try:
        article = Article.objects.create(id=df2[i]["id"],
                                            article_type=df2[i]["type"],
                                            title=df2[i]["title"],
                                            end_date=None,
                                            executor=None,
                                            serial=None,
                                            journal_name=None,
                                            issue=None,
                                            start_page=None,
                                            end_page=None,
                                            volume=None,
                                            year=article_year,
                                            number=int(
                                                df2[i]["info"]["number"]),
                                            seminar=article_seminar,
                                            cites=article_cites,
                                            references=article_references,
                                            abstract=article_abstract,
                                            abstract_preprocessed=None,
                                            abstract_summary=None,
                                            body=None,
                                            body_preprocessed=None,
                                            body_summary=None)
    except Exception as e:
        write_exception(e)
        continue
    # elif df2[i]["type"] == "نشریه":
    #     article_volume = df2[i]["info"]["volume"]
    #     if article_volume == "-" or article_volume == " ":
    #         article_volume = None
    #     pages = df2[i]["info"]["pages"].strip()
    #     if pages == "-" or pages == "---":
    #         article_start_page = None
    #         article_end_page = None
    #     else:
    #         first = pages.split("-")[0]
    #         if first == "":
    #             article_start_page = None
    #         else:
    #             try:
    #                 article_start_page = int(first)
    #             except ValueError:
    #                 article_start_page = None
    #         second = pages.split("-")[1]
    #         if second == "":
    #             article_end_page = None
    #         else:
    #             try:
    #                 article_end_page = int(second)
    #             except ValueError:
    #                 article_end_page = None
    #     article_issue = df2[i]["info"]["issue"].strip()
    #     if article_issue == "-" or article_issue == "":
    #         article_issue = None
    #     article_name = df2[i]["info"]["Journal"]
    #     if article_name == "" or article_name == " ":
    #         article_name = None
    #     try:
    #         article = Article.objects.create(id=df2[i]["id"],
    #                                          article_type=df2[i]["type"],
    #                                          title=df2[i]["title"],
    #                                          end_date=None,
    #                                          executor=None,
    #                                          serial=None,
    #                                          journal_name=article_name,
    #                                          issue=article_issue,
    #                                          start_page=article_start_page,
    #                                          end_page=article_end_page,
    #                                          volume=article_volume,
    #                                          year=article_year,
    #                                          number=None,
    #                                          seminar=None,
    #                                          cites=article_cites,
    #                                          references=article_references,
    #                                          abstract=article_abstract,
    #                                          abstract_preprocessed=None,
    #                                          abstract_summary=None,
    #                                          body=None,
    #                                          body_preprocessed=None,
    #                                          body_summary=None)
    #     except Exception as e:
    #         write_exception(e)
    #         continue
    # elif df2[i]["type"] == "مقاله-پژوهشی" or df2[i]["type"] == "مقاله-نظارتی" or df2[i]["type"] == "مقاله":
    #     article_serial = df2[i]["info"]["serial"]
    #     if article_serial == "":
    #         article_serial = None
    #     article_executor = df2[i]["info"]["executor"]
    #     if article_executor == "":
    #         article_executor = None
    #     article_end_date = df2[i]["info"]["endDate"]
    #     if article_end_date == "":
    #         article_end_date = None
    #     try:
    #         article = Article.objects.create(id=df2[i]["id"],
    #                                          article_type=df2[i]["type"],
    #                                          title=df2[i]["title"],
    #                                          end_date=article_end_date,
    #                                          executor=article_executor,
    #                                          serial=article_serial,
    #                                          journal_name=None,
    #                                          issue=None,
    #                                          start_page=None,
    #                                          end_page=None,
    #                                          volume=None,
    #                                          year=article_year,
    #                                          number=None,
    #                                          seminar=None,
    #                                          cites=article_cites,
    #                                          references=article_references,
    #                                          abstract=article_abstract,
    #                                          abstract_preprocessed=None,
    #                                          abstract_summary=None,
    #                                          body=None,
    #                                          body_preprocessed=None,
    #                                          body_summary=None)
    #     except Exception as e:
    #         write_exception(e)
    #         continue
    authors_list = df2[i]["authors"]
    for author_name in authors_list:
        if author_name != "":
            try:
                author = Person.objects.get(pk=author_name)
            except Person.DoesNotExist:
                author = Person.objects.create(name=author_name)
            article.authors.add(author)
    keywords = df2[i]["keywords"]
    if keywords != "ثبت نشده است" and keywords != "ثبت نشده است." and keywords != "":
        if " _ " in keywords:
            splitted_keywords = keywords.split(" _ ")
            end_range = len(splitted_keywords) - 1
        elif "|" in keywords:
            splitted_keywords = keywords.split("|")
            end_range = len(splitted_keywords)
        else:
            splitted_keywords = keywords.split(" ")
            end_range = len(splitted_keywords)
        for i in range(0, end_range):
            keyword = splitted_keywords[i]
            article.persian_keywords.add(get_pesian_phrase(keyword))
