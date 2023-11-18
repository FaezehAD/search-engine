from decouple import config


def compare_years(first_year, second_year):
    if first_year > second_year:
        return 1
    elif second_year > first_year:
        return 2
    return 0


def comare_dates(
    first_year, first_month, first_day, second_year, second_month, second_day
):  # return greater index
    if first_year > second_year:
        return 1
    elif first_year < second_year:
        return 2
    elif first_month > second_month:
        return 1
    elif first_month < second_month:
        return 2
    elif first_day > second_day:
        return 1
    elif first_day < second_day:
        return 2
    else:
        return 0


def selection_sort(arr, date, asc, option):
    n = len(arr)
    if date:
        sort_asc = 1
        if asc:
            sort_asc = 2
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                first_result = arr[j][0]
                second_result = arr[min_index][0]
                if option == "report":
                    first_year = int(first_result.publication_date[:4])
                    first_month = int(first_result.publication_date[5:7])
                    first_day = int(first_result.publication_date[8:])
                    second_year = int(second_result.publication_date[:4])
                    second_month = int(second_result.publication_date[5:7])
                    second_day = int(second_result.publication_date[8:])
                    if (
                        comare_dates(
                            first_year,
                            first_month,
                            first_day,
                            second_year,
                            second_month,
                            second_day,
                        )
                        == sort_asc
                    ):
                        min_index = j
                elif option == "article":
                    if compare_years(first_result.year, second_result.year) == sort_asc:
                        min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
    else:
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                first_result = arr[j]
                second_result = arr[min_index]
                first_score = first_result[1]
                second_score = second_result[1]
                if asc:
                    if second_score > first_score:
                        min_index = j
                else:
                    if second_score < first_score:
                        min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def sort_results_date(results, asc, option):
    if results is None:
        return (False, None)
    length = len(results)
    i = 0
    while i < length:
        if option == "report":
            if results[i][0].publication_date == "":
                results.pop(i)
                i = i - 1
                length = length - 1
        elif option == "article":
            if results[i][0].year == "":
                results.pop(i)
                i = i - 1
                length = length - 1
        i = i + 1
    if len(results) == 0:
        return (False, None)
    return (True, selection_sort(results, True, asc, option))


def delete_min_rate(results):
    if results is None:
        return None
    threshold = int(config("THRESHOLD"))
    length = len(results)
    i = 0
    while i < length:
        if results[i][1] < threshold:
            results.pop(i)
            i = i - 1
            length = length - 1
        i = i + 1
    if len(results) == 0:
        return None
    return results


def sort_results_cos_sim(results, asc, option):
    if results is None:
        return (False, None)
    return (True, selection_sort(results, False, asc, option))


def delete_outdated_results(results, start_year, end_year):
    if results is None:
        return None
    length = len(results)
    i = 0
    while i < length:
        year = results[i][0].year
        if year < start_year or year > end_year:
            results.pop(i)
            i = i - 1
            length = length - 1
        i = i + 1
    if len(results) == 0:
        return None
    return results
