from SE.models import *

departments = [
    [  # department_list
        "مطالعات زیربنایی و امور تولیدی",  
        " معاونت پژوهش های زیربنایی و امور تولیدی",  
        "مطالعات زیربنایی",  
    ],
    ["مطالعات انرژی، صنعت و معدن", "صنعت و معدن", "مطالعات انرژی"],
    ["مطالعات آموزش و فرهنگ"],
    ["مطالعات اجتماعی"],
    ["مطالعات اقتصادی", "مطالعات مالیه عمومی و توسعه مدیریت", "مطالعات بخش عمومی"],
    ["مطالعات بنیادین حکومتی"],
    ["مطالعات حقوقی"],
    ["مطالعات حکمرانی"],
    ["مطالعات سیاسی"],
    ["مطالعات فرهنگی"],
    ["مطالعات فناوری های نوین"],
    ["مطالعات مدیریت"],
    ["افکارسنجی ملت"],
]


def get_departments():
    global departments
    return departments


def get_indices(selected_departments):
    global departments
    indices = list()
    for d in selected_departments:
        for i in range(0, len(departments)):
            if d == departments[i][0]:
                indices.append(i)
    return indices


def get_none():
    global departments
    none_list = list()
    for department_list in departments:
        none_list.append((department_list[0], 0))
    return none_list


def get_departments_with_number(results):
    global departments
    if results is None:
        return get_none()
    departments_number = list()
    for department_list in departments:
        num = 0
        result_ids_list = list()
        for d in department_list:
            for result in results:
                result_id = result[0].id
                if result_id in result_ids_list:
                    continue
                for department in result[0].departments.all():
                    department_name = department.name.strip()[0 : len(d)]
                    if department_name == d:
                        result_ids_list.append(result_id)
                        num += 1
        departments_number.append((department_list[0], num))
    return departments_number


def filter_departments(results, selected_departments):
    global departments
    indices = get_indices(selected_departments)
    if results is None:
        return (False, None)
    length = len(results)
    i = 0
    while i < length:
        is_in_departments = False
        for d in results[i][0].departments.all():
            for index in indices:
                for department in departments[index]:
                    d_name = d.name.strip()[0 : len(department)]
                    if d_name == department:
                        is_in_departments = True
                        break
        if not is_in_departments:
            results.pop(i)
            i = i - 1
            length = length - 1
        i = i + 1
    if len(results) == 0:
        return (False, None)
    return (True, results)
