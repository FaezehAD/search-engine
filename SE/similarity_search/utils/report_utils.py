from SE.models import *
from .utils import *


def find_img_index(report_departments, departments):
    index = "4"
    for d in report_departments:
        d_name = d.name.strip()
        if (
            (d_name[0 : len(departments[0][0])] == departments[0][0])
            or (d_name[0 : len(departments[0][1])] == departments[0][1])
            or (d_name[0 : len(departments[0][2])] == departments[0][2])
        ):
            index = "0"
            break
        elif (
            (d_name[0 : len(departments[1][0])] == departments[1][0])
            or (d_name[0 : len(departments[1][1])] == departments[1][1])
            or (d_name[0 : len(departments[1][2])] == departments[1][2])
        ):
            index = "1"
            break
        elif d_name[0 : len(departments[2][0])] == departments[2][0]:
            index = "2"
            break
        elif d_name[0 : len(departments[3][0])] == departments[3][0]:
            index = "3"
            break
        elif (
            d_name[0 : len(departments[4][0])] == departments[4][0]
            or d_name[0 : len(departments[4][1])] == departments[4][1]
            or d_name[0 : len(departments[4][2])] == departments[4][2]
        ):
            index = "4"
            break
        elif d_name[0 : len(departments[5][0])] == departments[5][0]:
            index = "5"
            break
        elif d_name[0 : len(departments[6][0])] == departments[6][0]:
            index = "6"
            break
        elif d_name[0 : len(departments[7][0])] == departments[7][0]:
            index = "7"
            break
        elif d_name[0 : len(departments[8][0])] == departments[8][0]:
            index = "8"
            break
        elif d_name[0 : len(departments[9][0])] == departments[9][0]:
            index = "9"
            break
        elif d_name[0 : len(departments[10][0])] == departments[10][0]:
            index = "10"
            break
        elif d_name[0 : len(departments[11][0])] == departments[11][0]:
            index = "11"
            break
    return index


def get_report_details_context(
    identified_report, eitaa_url, image_content, departments, index
):
    return {
        "report": identified_report,
        "persian_keywords": identified_report.persian_keywords.all(),
        "english_keywords": identified_report.english_keywords.all(),
        "commenters": identified_report.commenters.all(),
        "commenters_out_of_center": identified_report.commenters_out_of_center.all(),
        "editors": identified_report.editors.all(),
        "editors_in_chief": identified_report.editors_in_chief.all(),
        "literary_editors": identified_report.literary_editors.all(),
        "technical_editors": identified_report.technical_editors.all(),
        "professional_editors": identified_report.professional_editors.all(),
        "colleagues": identified_report.colleagues.all(),
        "colleagues_out_of_center": identified_report.colleagues_out_of_center.all(),
        "consultants": identified_report.consultants.all(),
        "consultants_out_of_center": identified_report.consultants_out_of_center.all(),
        "scientific_consultants_group": identified_report.scientific_consultants_group.all(),
        "committee": identified_report.committee.all(),
        "committee_head": identified_report.committee_head.all(),
        "committee_members": identified_report.committee_members.all(),
        "committee_colleagues": identified_report.committee_colleagues.all(),
        "committee_consultants": identified_report.committee_consultants.all(),
        "supervisors": identified_report.supervisors.all(),
        "scientific_supervisors": identified_report.scientific_supervisors.all(),
        "summarizers": identified_report.summarizers.all(),
        "translators": identified_report.translators.all(),
        "regulators": identified_report.regulators.all(),
        "translators_and_compilers": identified_report.translators_and_compilers.all(),
        "translators_and_summarizers": identified_report.translators_and_summarizers.all(),
        "translators_and_gatherers": identified_report.translators_and_gatherers.all(),
        "compilers_and_regulators": identified_report.compilers_and_regulators.all(),
        "summarizers_and_compilers": identified_report.summarizers_and_compilers.all(),
        "real_people": identified_report.real_people.all(),
        "legal_people": identified_report.legal_people.all(),
        "producers": identified_report.producers.all(),
        "technical_session_chairpeople": identified_report.technical_session_chairpeople.all(),
        "infographics": identified_report.infographics.all(),
        "study_managers": identified_report.study_managers.all(),
        "lecturers": identified_report.lecturers.all(),
        "designers": identified_report.designers.all(),
        "layout_person": identified_report.layout_person.all(),
        "technical_experts": identified_report.technical_experts.all(),
        "aggregation": identified_report.aggregation.all(),
        "research_executors": identified_report.research_executors.all(),
        "applicants": identified_report.applicants.all(),
        "participants_in_intensive_group_discussions": identified_report.participants_in_intensive_group_discussions.all(),
        "participants_in_expertise_sessions": identified_report.participants_in_expertise_sessions.all(),
        "qr_code": image_content,
        "eitaa_url": eitaa_url,
        "main_image_index": index,
        "departments": departments,
    }


def verify_serial(input_serial):
    if all((char.isdigit() or char == "-") for char in input_serial) and any(
        char.isdigit() for char in input_serial
    ):
        return input_serial
    return ""


def verify_serials(results, input_serial):
    if results is None:
        return None
    if input_serial is None or input_serial == "":
        return results
    serial = input_serial.strip()
    length = len(results)
    i = 0
    while i < length:
        if serial not in results[i].doc.serial:
            results.pop(i)
            i = i - 1
            length = length - 1
        i = i + 1
    if len(results) == 0:
        return None
    return results


def get_report_people(report):
    report_people = list()
    report_people.append(list(report.commenters.all()))
    report_people.append(list(report.commenters_out_of_center.all()))
    report_people.append(list(report.editors.all()))
    report_people.append(list(report.editors_in_chief.all()))
    report_people.append(list(report.literary_editors.all()))
    report_people.append(list(report.technical_editors.all()))
    report_people.append(list(report.professional_editors.all()))
    report_people.append(list(report.colleagues.all()))
    report_people.append(list(report.colleagues_out_of_center.all()))
    report_people.append(list(report.consultants.all()))
    report_people.append(list(report.consultants_out_of_center.all()))
    report_people.append(list(report.scientific_consultants_group.all()))
    report_people.append(list(report.committee.all()))
    report_people.append(list(report.committee_head.all()))
    report_people.append(list(report.committee_members.all()))
    report_people.append(list(report.committee_colleagues.all()))
    report_people.append(list(report.committee_consultants.all()))
    report_people.append(list(report.supervisors.all()))
    report_people.append(list(report.scientific_supervisors.all()))
    report_people.append(list(report.summarizers.all()))
    report_people.append(list(report.translators.all()))
    report_people.append(list(report.regulators.all()))
    report_people.append(list(report.translators_and_compilers.all()))
    report_people.append(list(report.translators_and_summarizers.all()))
    report_people.append(list(report.translators_and_gatherers.all()))
    report_people.append(list(report.compilers_and_regulators.all()))
    report_people.append(list(report.summarizers_and_compilers.all()))
    report_people.append(list(report.real_people.all()))
    report_people.append(list(report.legal_people.all()))
    report_people.append(list(report.producers.all()))
    report_people.append(list(report.technical_session_chairpeople.all()))
    report_people.append(list(report.infographics.all()))
    report_people.append(list(report.study_managers.all()))
    report_people.append(list(report.lecturers.all()))
    report_people.append(list(report.designers.all()))
    report_people.append(list(report.layout_person.all()))
    report_people.append(list(report.technical_experts.all()))
    report_people.append(list(report.aggregation.all()))
    report_people.append(list(report.research_executors.all()))
    report_people.append(list(report.applicants.all()))
    report_people.append(list(report.participants_in_expertise_sessions.all()))
    report_people.append(list(report.participants_in_intensive_group_discussions.all()))
    return report_people


def get_report_people_filter(person_name):
    report_people = list()
    report_people.append(
        list(Report.objects.filter(commenters__name__contains=person_name))
    )
    report_people.append(
        list(
            Report.objects.filter(commenters_out_of_center__name__contains=person_name)
        )
    )
    report_people.append(
        list(Report.objects.filter(editors__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(editors_in_chief__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(literary_editors__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(technical_editors__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(professional_editors__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(colleagues__name__contains=person_name))
    )
    report_people.append(
        list(
            Report.objects.filter(colleagues_out_of_center__name__contains=person_name)
        )
    )
    report_people.append(
        list(Report.objects.filter(consultants__name__contains=person_name))
    )
    report_people.append(
        list(
            Report.objects.filter(consultants_out_of_center__name__contains=person_name)
        )
    )
    report_people.append(
        list(
            Report.objects.filter(
                scientific_consultants_group__name__contains=person_name
            )
        )
    )
    report_people.append(
        list(Report.objects.filter(committee__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(committee_head__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(committee_members__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(committee_colleagues__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(committee_consultants__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(supervisors__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(scientific_supervisors__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(summarizers__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(translators__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(regulators__name__contains=person_name))
    )
    report_people.append(
        list(
            Report.objects.filter(translators_and_compilers__name__contains=person_name)
        )
    )
    report_people.append(
        list(
            Report.objects.filter(
                translators_and_summarizers__name__contains=person_name
            )
        )
    )
    report_people.append(
        list(
            Report.objects.filter(translators_and_gatherers__name__contains=person_name)
        )
    )
    report_people.append(
        list(
            Report.objects.filter(compilers_and_regulators__name__contains=person_name)
        )
    )
    report_people.append(
        list(
            Report.objects.filter(summarizers_and_compilers__name__contains=person_name)
        )
    )
    report_people.append(
        list(Report.objects.filter(real_people__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(legal_people__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(producers__name__contains=person_name))
    )
    report_people.append(
        list(
            Report.objects.filter(
                technical_session_chairpeople__name__contains=person_name
            )
        )
    )
    report_people.append(
        list(Report.objects.filter(infographics__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(study_managers__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(lecturers__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(designers__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(layout_person__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(technical_experts__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(aggregation__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(research_executors__name__contains=person_name))
    )
    report_people.append(
        list(Report.objects.filter(applicants__name__contains=person_name))
    )
    report_people.append(
        list(
            Report.objects.filter(
                participants_in_expertise_sessions__name__contains=person_name
            )
        )
    )
    report_people.append(
        list(
            Report.objects.filter(
                participants_in_intensive_group_discussions__name__contains=person_name
            )
        )
    )
    return report_people


def get_result_departments(result):
    departments = list(result.departments.all())
    for i in range(0, len(departments)):
        index = departments[i].name.find("فایل")
        if index != -1:
            departments[i].name = departments[i].name[0:index]
    return departments


def get_report_details(result):
    return (
        result.persian_keywords.all(),
        result.english_keywords.all(),
        get_result_departments(result),
    )


def verify_types(results, supervisory, legislative, strategic):
    if results is None:
        return None
    at_least_one = False
    if supervisory == "7":
        at_least_one = True
    elif legislative == "8":
        at_least_one = True
    elif strategic == "9":
        at_least_one = True
    if not at_least_one:
        return results
    length = len(results)
    i = 0
    while i < length:
        report_type = results[i].doc.report_type
        remain = False
        if supervisory == "7":
            if report_type == "نظارتی":
                remain = True
        if legislative == "8":
            if report_type == "تقنینی":
                remain = True
        if strategic == "9":
            if report_type == "مطالعات راهبردی":
                remain = True
        if not remain:
            results.pop(i)
            i = i - 1
            length = length - 1
        i = i + 1
    if len(results) == 0:
        return None
    return results


def get_report_by_id(id):
    try:
        return Report.objects.get(pk=id)
    except Report.DoesNotExist:
        return None
