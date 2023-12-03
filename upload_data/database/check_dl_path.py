import pandas as pd
import os
import re


def clean_string(str):
    cleaned_str = re.sub(r"[^a-zA-Z0-9-]", "", str)
    return cleaned_str


with open("./upload_data/database/with_title_without_down.txt", "w") as exceptions:
    exceptions.write("")
with open("./upload_data/database/with_title_with_down.txt", "w") as exceptions:
    exceptions.write("")


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
# df = pd.read_json("./data_text/report/one.json")
df2 = df.to_dict("records")

serials = list()

for i in range(0, len(df2)):
    try:
        report_serial = df2[i]["Info"]["شماره مسلسل"]
    except Exception:
        report_serial = None
    if report_serial is not None:
        serials.append(report_serial)


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
                with open(
                    (directory + file_title + ".txt"), "r", encoding="utf_8"
                ) as file:
                    buffer = file.read()
                    if len(buffer) > 300:
                        report_body = buffer
            except FileNotFoundError:
                file_title = doc_dict[file_title]
                with open(
                    (directory + file_title + ".txt"), "r", encoding="utf_8"
                ) as file:
                    buffer = file.read()
                    if len(buffer) > 300:
                        report_body = buffer
    report_dl_path = df2[i]["DLpath"]
    if report_dl_path == "":
        report_dl_path = None
    if (
        (
            (report_abstract is None and report_body is None)
            or (report_abstract is not None and len(report_abstract) > limit_length)
        )
        and df2[i]["Title"] != ""
        and df2[i]["Title"] is not None
        and report_dl_path is None
    ):
        if report_dl_path is None:
            with open(
                "./upload_data/database/with_title_without_down.txt", "a"
            ) as exceptions:
                exceptions.write(f"{df2[i]['ID']}\n")
        else:
            with open(
                "./upload_data/database/with_title_with_down.txt", "a"
            ) as exceptions:
                exceptions.write(f"{df2[i]['ID']}\n")


print('fin')


