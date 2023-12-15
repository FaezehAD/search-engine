import csv
from SE.models import *


all_reports = list(Report.objects.all())

data_to_write = list(['id','serial'])


for r in all_reports:
    row = list()
    row.append(r.id)
    row.append(r.serial)
    data_to_write.append(row)

filename = 'all_reports.csv'

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in data_to_write:
        csvwriter.writerow(row)


print(f"data_to_write successfully written to {filename}.")


