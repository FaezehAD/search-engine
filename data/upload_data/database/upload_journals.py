import pandas as pd
import os
import re
import json
import glob
from langdetect import detect, DetectorFactory
import arabic_reshaper
from bidi.algorithm import get_display

# from SE.models import *


DetectorFactory.seed = 0


def print_fa(text):
    print(get_display(arabic_reshaper.reshape(text)))


# are those texts for those profiles?
# set1: 101 without profile (empty profile), 122 without text (text column in relation file is empty)
# set2: 91 without profile (empty profile), 0 without text (text column in relation file is empty)

relation_df1 = pd.read_csv("./../../data/data_text/journal/set1/Relation_Pack1.csv")
relation_df2 = pd.read_csv("./../../data/data_text/journal/set2/relation.csv")

# relation_df1 = pd.read_csv("./data/data_text/journal/set1/Relation_Pack1.csv")
# relation_df2 = pd.read_csv("./data/data_text/journal/set2/relation.csv")

PROFILE_DIRECTORY1 = "./../../data/data_text/journal/set1/json-pack_1/"
TXT_DIRECTORY1 = "./../../data/data_text/journal/set1/txt-pack_1/"

# PROFILE_DIRECTORY1 = "./data/data_text/journal/set1/json-pack_1/"
# TXT_DIRECTORY1 = "./data/data_text/journal/set1/txt-pack_1/"

PROFILE_DIRECTORY2 = "./../../data/data_text/journal/set2/json-pack_2_Profile/N1000/"
TXT_DIRECTORY2 = "./../../data/data_text/journal/set2/txt_pack_2/txt/"


def read_json(file_name):
    json_str = ""
    with open(file_name, "r") as fp:
        for l in fp:
            l.replace("\n", "")
            json_str += l
    return json.loads(json_str)


def replace_u0026_with_ampersand(input_str):
    output_str = input_str.lower().replace("\u0026", "&")
    return output_str.replace("%5cu0026", "&")


def remove_u003c_and_u003e(input_str):
    return re.sub("<.*?>", "", input_str)


# for file_name in os.listdir(PROFILE_DIRECTORY1):
# data=read_json(PROFILE_DIRECTORY1 + file_name )

# for i, row in relation_df2.iterrows():
#     if pd.isnull(row["journal_text"]):
#         count+=1

# with open("journal_set2_exceptions.txt", "w") as exceptions:
#     exceptions.write("folder_name,file_name\n")


def get_journal_body(df, file_name, text_dir):
    journal_body = None
    for _, row in df.iterrows():
        journal_profile = row["journal_profile"]
        if journal_profile == file_name.strip()[0 : len(journal_profile)]:
            txt_file_path = glob.glob(text_dir + row["journal_text"] + ".txt")
            try:
                with open(txt_file_path[0], "r", encoding="utf_8") as file:
                    journal_body = file.read()
            except Exception:
                pass
            break
    return journal_body


def get_field(main_content, field_name):
    try:
        field = main_content[field_name]
        if field == "":
            raise Exception()
    except:
        field = None
    return field


def get_journal_info_type1(article):
    main_content = article["Journal"]
    try:
        journal_title_unknown = main_content["JournalTitle"]
        journal_title_lang = detect(journal_title)
        if journal_title_lang == "en":
            journal_title = journal_title_unknown
            journal_title_fa = None
        else:
            journal_title = None
            journal_title_fa = journal_title_unknown
        if journal_title == "":
            journal_title = None
        if journal_title_fa == "":
            journal_title_fa = None
    except:
        journal_title = None
        journal_title_fa = None
    journal_gregorian_pubdate_day = get_field(main_content["PubDate"], "Day")
    journal_gregorian_pubdate_month = get_field(main_content["PubDate"], "Month")
    journal_gregorian_pubdate_year = get_field(main_content["PubDate"], "Year")
    journal_publisher_name = get_field(main_content, "PublisherName")
    journal_publish_type = get_field(main_content["PubDate"], "-PubStatus")  # epublish
    journal_id_issn = get_field(main_content, "Issn")
    journal_volume = get_field(main_content, "Volume")
    journal_issue = get_field(main_content, "Issue")
    return (
        journal_title,
        journal_title_fa,
        journal_gregorian_pubdate_day,
        journal_gregorian_pubdate_month,
        journal_gregorian_pubdate_year,
        journal_publisher_name,
        journal_publish_type,
        journal_id_issn,
        journal_volume,
        journal_issue,
    )


def get_journal_article_info_type1(article):
    article_title = None
    article_title_fa = None
    try:
        article_title_unknown = get_field(article, "ArticleTitle")
        if article_title_unknown is not None:
            article_title_lang = detect(article_title_unknown)
            if article_title_lang == "en":
                article_title = article_title_unknown
            else:
                article_title_fa = article_title_unknown
    except:
        pass
    try:
        article_title_unknown = get_field(article, "VernacularTitle")
        if article_title_unknown is not None:
            article_title_lang = detect(article_title_unknown)
            if article_title_lang == "en":
                article_title = article_title_unknown
            else:
                article_title_fa = article_title_unknown
    except:
        pass
    article_english_keywords = list()
    article_persian_keywords = list()
    try:
        keywords_list = article["ObjectList"]["Object"]
        for keyword_container in keywords_list:
            keyword_unknown = get_field(keyword_container["Param"], "#content")
            if keyword_unknown is not None:
                keyword_lan = detect(keyword_unknown)
                if keyword_lan == "en":
                    article_english_keywords.append(keyword_unknown)
                else:
                    article_persian_keywords.append(keyword_unknown)
    except:
        pass
    article_publish_type = get_field(article, "PublicationType")
    article_gregorian_pubdate_day = get_field(article["History"]["PubDate"], "Day")
    article_gregorian_pubdate_month = get_field(article["History"]["PubDate"], "Month")
    article_gregorian_pubdate_year = get_field(article["History"]["PubDate"], "Year")
    article_authors = list()
    try:
        authors_list = article["AuthorList"]["Author"]
        for author_dict in authors_list:
            author = dict()
            author["first_name"] = get_field(author_dict, "FirstName")
            author["last_name"] = get_field(author_dict, "LastName")
            author["affiliation"] = get_field(author_dict, "Affiliation")
            article_authors.append(author)
    except:
        pass
    article_web_url = get_field(article["ArchiveCopySource"], "#content")
    article_language = get_field(article, "Language")
    article_start_page = get_field(article, "FirstPage")
    article_end_page = get_field(article, "LastPage")
    try:
        ids = article["ELocationID"]
        for id in ids:
            if id["-EIdType"] == "pii":
                article_id_pii = id["#content"]
            elif id["-EIdType"] == "doi":
                article_id_doi = id["#content"]
    except:
        article_id_pii = None
        article_id_doi = None
    article_abstract = None
    article_abstract_fa = None
    try:
        article_abstract_unknown = article["Abstract"]
        article_abstract_lan = detect(article_abstract_unknown)
        if article_abstract_lan == "en":
            article_abstract = remove_u003c_and_u003e(article_abstract_unknown)
        else:
            article_abstract_fa = remove_u003c_and_u003e(article_abstract_unknown)
    except:
        pass
    try:
        article_abstract_unknown = article["OtherAbstract"]["#content"]
        article_abstract_lan = detect(article_abstract_unknown)
        if article_abstract_lan == "en":
            article_abstract = remove_u003c_and_u003e(article_abstract_unknown)
        else:
            article_abstract_fa = remove_u003c_and_u003e(article_abstract_unknown)
    except:
        pass
    if article_abstract == "---":
        article_abstract = None
    if article_abstract_fa == "---":
        article_abstract_fa = None
    return (
        article_title,
        article_title_fa,
        article_english_keywords,
        article_persian_keywords,
        article_publish_type,
        article_gregorian_pubdate_day,
        article_gregorian_pubdate_month,
        article_gregorian_pubdate_year,
        article_authors,
        article_web_url,
        article_language,
        article_start_page,
        article_end_page,
        article_id_pii,
        article_id_doi,
        article_abstract,
        article_abstract_fa,
    )


def get_journal_info_type2(main_content):
    journal_title = get_field(main_content, main_content, "title")
    journal_title_fa = get_field(main_content, "title_fa")
    journal_short_title = get_field(main_content, "short_title")
    journal_jalali_pubdate_day = None
    journal_jalali_pubdate_month = None
    journal_jalali_pubdate_year = None
    journal_gregorian_pubdate_day = None
    journal_gregorian_pubdate_month = None
    journal_gregorian_pubdate_year = None
    try:
        journal_pubdates_list = main_content["pubdate"]
        for pubdate in journal_pubdates_list:
            journal_pubdate_type = pubdate["type"]
            if journal_pubdate_type == "jalali":
                journal_jalali_pubdate_day = pubdate["day"]
                journal_jalali_pubdate_month = pubdate["month"]
                journal_jalali_pubdate_year = pubdate["year"]
            elif journal_pubdate_type == "gregorian":
                journal_gregorian_pubdate_day = pubdate["day"]
                journal_gregorian_pubdate_month = pubdate["month"]
                journal_gregorian_pubdate_year = pubdate["year"]
    except:
        pass
    journal_publish_type = get_field(main_content, "publish_type")
    journal_article_type = get_field(main_content, "article_type")
    journal_hbi_system_user = get_field(main_content, "journal_hbi_system_user")
    journal_language = get_field(main_content, "language")
    journal_number = get_field(main_content, "number")
    journal_web_url = get_field(main_content, "web_url")
    journal_publish_edition = get_field(main_content, "publish_edition")
    journal_subject = get_field(main_content, "subject")
    journal_id_doi = get_field(main_content, "journal_id_doi")
    journal_id_iranmedex = get_field(main_content, "journal_id_iranmedex")
    journal_id_magiran = get_field(main_content, "journal_id_magiran")
    journal_id_science = get_field(main_content, "journal_id_science")
    journal_hbi_system_id = get_field(main_content, "journal_hbi_system_id")
    journal_id_nlai = get_field(main_content, "journal_id_nlai")
    journal_id_issn = get_field(main_content, "journal_id_issn")
    journal_id_issn_online = get_field(main_content, "journal_id_issn_online")
    journal_id_sid = get_field(main_content, "journal_id_sid")
    journal_id_pii = get_field(main_content, "journal_id_pii")
    journal_volume = get_field(main_content, "volume")
    return (
        journal_title,
        journal_title_fa,
        journal_short_title,
        journal_jalali_pubdate_day,
        journal_jalali_pubdate_month,
        journal_jalali_pubdate_year,
        journal_gregorian_pubdate_day,
        journal_gregorian_pubdate_month,
        journal_gregorian_pubdate_year,
        journal_publish_type,
        journal_article_type,
        journal_hbi_system_user,
        journal_language,
        journal_number,
        journal_web_url,
        journal_publish_edition,
        journal_subject,
        journal_id_doi,
        journal_id_iranmedex,
        journal_id_magiran,
        journal_id_science,
        journal_hbi_system_id,
        journal_id_nlai,
        journal_id_issn,
        journal_id_issn_online,
        journal_id_sid,
        journal_id_pii,
        journal_volume,
    )


def get_journal_article_info_type2(main_content):
    main_content = main_content["articleset"]["article"]
    article_title = get_field(main_content, "title")
    article_title_fa = get_field(main_content, "title_fa")
    article_content_type = get_field(main_content, "content_type")
    article_content_type_fa = get_field(main_content, "content_type_fa")
    article_english_keywords = list()
    article_persian_keywords = list()
    keywords_string = get_field(main_content, "keyword")
    keywords_fa_string = get_field(main_content, "keyword_fa")
    if keywords_string is not None:
        keywords_list = keywords_string.split(",")
        for english_keyword in keywords_list:
            english_keyword = english_keyword.strip()
            if ":" in english_keyword:
                english_keyword = english_keyword[(english_keyword.index(":") + 1) :]
            if english_keyword != "":
                article_english_keywords.append(english_keyword)
    if keywords_fa_string is not None:
        keywords_fa_list = keywords_fa_string.split(",")
        for persian_keyword in keywords_fa_list:
            persian_keyword = persian_keyword.strip()
            if ":" in persian_keyword:
                persian_keyword = persian_keyword[(persian_keyword.index(":") + 1) :]
            if persian_keyword != "":
                article_persian_keywords.append(persian_keyword)
    article_subject = get_field(main_content, "subject")
    article_subject_fa = get_field(main_content, "subject_fa")
    article_authors = list()
    try:
        authors_list = main_content["author_list"]["author"]
        for author_dict in authors_list:
            author = dict()
            author["first_name"] = get_field(author_dict, "first_name")
            author["first_name_fa"] = get_field(author_dict, "first_name_fa")
            author["last_name"] = get_field(author_dict, "last_name")
            author["last_name_fa"] = get_field(author_dict, "last_name_fa")
            author["middle_name"] = get_field(author_dict, "middle_name")
            author["middle_name_fa"] = get_field(author_dict, "middle_name_fa")
            author["suffix"] = get_field(author_dict, "suffix")
            author["suffix_fa"] = get_field(author_dict, "suffix_fa")
            author["code"] = get_field(author_dict, "code")
            author["email"] = get_field(author_dict, "email")
            author["orcid"] = get_field(author_dict, "orcid")
            author["core_author"] = (
                True if author_dict["coreauthor"] == "Yes" else False
            )
            author["affiliation"] = author_dict["affiliation"]
            author["affiliation_fa"] = author_dict["affiliation_fa"]
            article_authors.append(author)
    except:
        pass
    article_web_url = get_field(main_content, "web_url")
    if article_web_url is not None:
        article_web_url = replace_u0026_with_ampersand(article_web_url)
    article_language = get_field(main_content, "language")
    article_start_page = get_field(main_content, "start_page")
    article_end_page = get_field(main_content, "end_page")
    article_id_doi = get_field(main_content, "article_id_doi")
    try:
        article_abstract = remove_u003c_and_u003e(main_content["abstract"])
    except:
        article_abstract = None
    try:
        article_abstract_fa = remove_u003c_and_u003e(main_content["abstract_fa"])
    except:
        article_abstract_fa = None
    if article_abstract == "---":
        article_abstract = None
    if article_abstract_fa == "---":
        article_abstract_fa = None
    return (
        article_title,
        article_title_fa,
        article_content_type,
        article_content_type_fa,
        article_english_keywords,
        article_persian_keywords,
        article_subject,
        article_subject_fa,
        article_authors,
        article_web_url,
        article_language,
        article_start_page,
        article_end_page,
        article_id_doi,
        article_abstract,
        article_abstract_fa,
    )


# set2
for folder_name in os.listdir(PROFILE_DIRECTORY2):
    print(f"now folder: {folder_name}")
    folder_mask = relation_df2["journal_folder"] == folder_name
    folder_df = relation_df2[folder_mask]
    for file_name in os.listdir(PROFILE_DIRECTORY2 + folder_name):
        journal = None
        data = read_json(PROFILE_DIRECTORY2 + folder_name + "/" + file_name)
        journal_type = -1
        try:
            main_content = data["ArticleSet"]
            journal_type = 1
        except:
            try:
                main_content = data["journal"]
                journal_type = 2
            except:
                continue

        if journal_type == 1:
            try:
                main_content = main_content["Article"]
                if type(main_content) == list:
                    for article in main_content:
                        (
                            journal_title,
                            journal_title_fa,
                            journal_gregorian_pubdate_day,
                            journal_gregorian_pubdate_month,
                            journal_gregorian_pubdate_year,
                            journal_publisher_name,
                            journal_publish_type,
                            journal_id_issn,
                            journal_volume,
                            journal_issue,
                        ) = get_journal_info_type1(article)
                        (
                            article_title,
                            article_title_fa,
                            article_english_keywords,
                            article_persian_keywords,
                            article_publish_type,
                            article_gregorian_pubdate_day,
                            article_gregorian_pubdate_month,
                            article_gregorian_pubdate_year,
                            article_authors,
                            article_web_url,
                            article_language,
                            article_start_page,
                            article_end_page,
                            article_id_pii,
                            article_id_doi,
                            article_abstract,
                            article_abstract_fa,
                        ) = get_journal_article_info_type1(article)
                else:
                    (
                        journal_title,
                        journal_title_fa,
                        journal_gregorian_pubdate_day,
                        journal_gregorian_pubdate_month,
                        journal_gregorian_pubdate_year,
                        journal_publisher_name,
                        journal_publish_type,
                        journal_id_issn,
                        journal_volume,
                        journal_issue,
                    ) = get_journal_info_type1(main_content)
                    (
                        article_title,
                        article_title_fa,
                        article_english_keywords,
                        article_persian_keywords,
                        article_publish_type,
                        article_gregorian_pubdate_day,
                        article_gregorian_pubdate_month,
                        article_gregorian_pubdate_year,
                        article_authors,
                        article_web_url,
                        article_language,
                        article_start_page,
                        article_end_page,
                        article_id_pii,
                        article_id_doi,
                        article_abstract,
                        article_abstract_fa,
                    ) = get_journal_article_info_type1(main_content)
            except:
                continue

        elif journal_type == 2:
            get_journal_info_type2(main_content)
            get_journal_article_info_type2(main_content)

        else:
            print(f"file: {file_name} in folder: {folder_name} is for none type!")

        # text_dir = TXT_DIRECTORY2 + folder_name + "/"
        # journal_body = get_journal_body(folder_df, file_name, text_dir)
        # if journal_body is None:
        #     with open("journal_set2_exceptions.txt", "a") as exceptions:
        #         exceptions.write(f"{folder_name},{file_name}\n")

        # try:
        #     journal=Journal.objects.create(
        #         id=,
        #         journal_jalali_pubdate_day=,
        #         journal_jalali_pubdate_month=,
        #         journal_jalali_pubdate_year =,
        #         journal_gregorian_pubdate_day = ,
        #         journal_gregorian_pubdate_month =,
        #         journal_gregorian_pubdate_year = ,
        #         journal_pub_status =,
        #         journal_publisher_name =,
        #         journal_publish_type =,
        #         journal_article_type = ,
        #         journal_hbi_system_user =,
        #         journal_id_doi =,
        #         journal_id_iranmedex =,
        #         journal_id_magiran =,
        #         journal_language =,
        #         journal_id_science = ,
        #         journal_number=,
        #         journal_title=,
        #         journal_title_fa=,
        #         journal_short_title=,
        #         journal_web_url=,
        #         journal_hbi_system_id=,
        #         journal_id_nlai=,
        #         journal_publish_edition=,
        #         journal_subject=,
        #         journal_id_issn=,
        #         journal_id_issn_online=,
        #         journal_id_sid=,
        #         journal_volume=,
        #         journal_issue=,
        #         journal_id_pii=,
        #         article_content_type=,
        #         article_content_type_fa=,
        #         article_english_keywords=,
        #         article_persian_keywords=,
        #         article_publish_type=,
        #         article_gregorian_pubdate_day=,
        #         article_gregorian_pubdate_month=,
        #         article_gregorian_pubdate_year=,
        #         article_pub_status=,
        #         article_subject=,
        #         article_subject_fa=,
        #         article_title=,
        #         article_title_fa=,
        #         article_vernacular_title=,
        #         article_web_url=,
        #         article_language=,
        #         elocation_id_pii=,
        #         article_dl_path=,
        #         article_start_page=,
        #         article_end_page=,
        #         article_id_doi=,
        #         article_abstract=,
        #         article_abstract_preprocessed=,
        #         article_abstract_summary=,
        #         article_abstract_fa=,
        #         article_abstract_fa_preprocessed=,
        #         article_abstract_fa_summary=
        #     )
        # except Exception as e:
        #     with open("./upload_data/database/journal2_add_to_database.txt", "a") as exceptions:
        #         exceptions.write(str(e) + "\n")
        #     continue
