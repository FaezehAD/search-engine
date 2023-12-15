import csv
from SE.models import *


all_reports = list(Report.objects.all())

data_to_write = list()
columns = list()
columns.append('id','serial')
data_to_write.append(columns)


for r in all_reports:
    if r.body == None:
        row = list()
        row.append(r.id)
        row.append(r.serial)
        data_to_write.append(row)

filename = 'all_reports_without_body.csv'

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data_to_write:
        csvwriter.writerow(row)


print(f"data_to_write successfully written to {filename}.")


