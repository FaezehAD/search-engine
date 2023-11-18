from SE.models import *


def get_article_details(result):
    return (result.persian_keywords.all(), result.english_keywords.all())


def get_article_people(result):
    article_people = list()
    article_people.append(list(result.authors.all()))
    return article_people


def get_article_people_filter(person_name):
    article_people = list()
    article_people.append(
        list(Article.objects.filter(authors__name__contains=person_name))
    )
    return article_people
