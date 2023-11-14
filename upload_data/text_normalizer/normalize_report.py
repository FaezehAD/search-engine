import pandas as pd
from SE.models import *
from upload_data.text_normalizer import normalizer


normalizer = normalizer.Normalizer()

all_reports = list(Report.objects.all())

for i in range(0, len(all_reports)):
    print(i)
    report = all_reports[i]
    abstract = report.abstract
    body = report.body
    preprocessed_abs = None
    preprocessed_body = None
    if abstract is not None:
        preprocessed_abs = normalizer.normalize(abstract)
    if body is not None:
        preprocessed_body = normalizer.normalize(body)
    report.abstract_preprocessed = preprocessed_abs
    report.body_preprocessed = preprocessed_body
    report.save()

