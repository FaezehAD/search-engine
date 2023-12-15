from SE.models import *
from SE.similarity_search.utils.utils import *

all_reports = list(Report.objects.all())

for r in all_reports:
    report_serial = convert_persian_number_to_english(r.serial)
    r.serial = report_serial
    r.save()


