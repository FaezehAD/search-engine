from SE.models import *


reports = list(Report.objects.all())

for r in reports:
    r.body_summary = None
    r.save()


print("finish!")



