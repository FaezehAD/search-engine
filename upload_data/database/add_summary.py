import pandas as pd
from SE.models import *
import os

directory = "./data_text/report/final_output_data/"

with open("./upload_data/database/report_summary_exceptions.txt", "w") as exceptions:
    exceptions.write("")


for filename in os.listdir(directory):
    print(filename)
    id = int(filename[:-5])
    try:
        report = Report.objects.get(id=id)
    except Report.DoesNotExist:
        with open(
            "./upload_data/database/report_summary_exceptions.txt", "a"
        ) as exceptions:
            exceptions.write(f"{id}\n")
        continue
    try:
        df = pd.read_json(directory + filename)
        df2 = df.to_dict("records")
        report.body_summary = df2[0]["generated_summary"]
        report.save()
    except Exception as e:
        with open(
            "./upload_data/database/report_summary_exceptions.txt", "a"
        ) as exceptions:
            exceptions.write(f"{id} {e}\n")


print("finish!")



