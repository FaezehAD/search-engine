from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=191, primary_key=True)


class EnglishPhrase(models.Model):
    value = models.TextField()


class PersianPhrase(models.Model):
    value = models.TextField()


class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    article_type = models.CharField(max_length=50, blank=True, default="نشریه")
    title = models.TextField(null=True)
    authors = models.ManyToManyField(Person, related_name="article_authors")

    english_keywords = models.ManyToManyField(
        EnglishPhrase, related_name="article_english_keywords"
    )
    persian_keywords = models.ManyToManyField(
        PersianPhrase, related_name="article_persian_keywords"
    )
    end_date = models.CharField(max_length=100, null=True)
    executor = models.CharField(max_length=191, null=True)
    serial = models.CharField(max_length=100, null=True)

    journal_name = models.CharField(max_length=191, null=True)
    issue = models.CharField(max_length=191, null=True)
    start_page = models.IntegerField(null=True)
    end_page = models.IntegerField(null=True)
    volume = models.CharField(max_length=191, null=True)

    year = models.IntegerField(null=True)

    number = models.IntegerField(null=True)
    seminar = models.CharField(max_length=191, null=True)

    cites = models.TextField(null=True)
    references = models.TextField(null=True)

    abstract = models.TextField(null=True)
    abstract_preprocessed = models.TextField(null=True)
    abstract_summary = models.TextField(null=True)

    body = models.TextField(null=True)
    body_preprocessed = models.TextField(null=True)
    body_summary = models.TextField(null=True)


class Department(models.Model):
    name = models.CharField(max_length=191, primary_key=True)


class Report(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=191, unique=True, null=True)
    title = models.TextField(null=True)
    publication_date = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)
    serial = models.CharField(max_length=100, null=True)
    report_type = models.CharField(max_length=25, null=True)
    publish_type = models.CharField(max_length=45, null=True)
    dl_path = models.CharField(max_length=191, null=True, unique=True)

    originality = models.BooleanField(null=True)
    multiple_editions = models.BooleanField(null=True)

    departments = models.ManyToManyField(Department, related_name="report_departments")

    english_keywords = models.ManyToManyField(
        EnglishPhrase, related_name="report_english_keywords"
    )
    persian_keywords = models.ManyToManyField(
        PersianPhrase, related_name="report_persian_keywords"
    )

    # roles
    commenters = models.ManyToManyField(
        Person, related_name="report_commenters"
    )  # اظهارنظرکننده
    commenters_out_of_center = models.ManyToManyField(
        Person, related_name="report_commenters_out_of_center"
    )  # اظهارنظر کنندگان خارج از مرکز

    editors = models.ManyToManyField(Person, related_name="report_editors")  # ویراستار
    editors_in_chief = models.ManyToManyField(
        Person, related_name="report_editors_in_chief"
    )  # سرویراستار
    literary_editors = models.ManyToManyField(
        Person, related_name="report_literary_editors"
    )  # ویراستار ادبی
    technical_editors = models.ManyToManyField(
        Person, related_name="report_technical_editors"
    )  # ویراستار فنی
    professional_editors = models.ManyToManyField(
        Person, related_name="report_professional_editors"
    )  # ویراستار تخصصی

    colleagues = models.ManyToManyField(
        Person, related_name="report_colleagues"
    )  # همکاران
    colleagues_out_of_center = models.ManyToManyField(
        Person, related_name="report_colleagues_out_of_center"
    )  # همکاران خارج از مرکز

    consultants = models.ManyToManyField(
        Person, related_name="report_consultants"
    )  # مشاور
    consultants_out_of_center = models.ManyToManyField(
        Person, related_name="report_consultants_out_of_center"
    )  # مشاوران خارج از مرکز
    scientific_consultants_group = models.ManyToManyField(
        Person, related_name="report_scientific_consultants"
    )  # گروه مشاوران علمی

    committee = models.ManyToManyField(
        Person, related_name="report_committee"
    )  # کارگروه
    committee_head = models.ManyToManyField(
        Person, related_name="report_committee_heads"
    )  # رئیس کارگروه
    committee_members = models.ManyToManyField(
        Person, related_name="report_committee_members"
    )  # اعضای کارگروه
    committee_colleagues = models.ManyToManyField(
        Person, related_name="report_committee_colleagues"
    )  # همکاران کارگروه
    committee_consultants = models.ManyToManyField(
        Person, related_name="report_committee_consultants"
    )  # مشاور کارگروه

    supervisors = models.ManyToManyField(
        Person, related_name="report_supervisors"
    )  # ناظران
    scientific_supervisors = models.ManyToManyField(
        Person, related_name="report_scientific_supervisors"
    )  # ناظر علمی

    summarizers = models.ManyToManyField(
        Person, related_name="report_summarizers"
    )  # خلاصه کننده
    translators = models.ManyToManyField(
        Person, related_name="report_translators"
    )  # ترجمه، مترجم
    regulators = models.ManyToManyField(
        Person, related_name="report_regulators"
    )  # تنظیم کننده
    translators_and_compilers = models.ManyToManyField(
        Person, related_name="report_translators_and_compilations"
    )  # ترجمه و تدوین کنندگان
    translators_and_summarizers = models.ManyToManyField(
        Person, related_name="report_translators_and_summarizers"
    )  # ترجمه و تلخیص کنندگان
    translators_and_gatherers = models.ManyToManyField(
        Person, related_name="report_translators_and_gatherers"
    )  # ترجمه و تالیف
    compilers_and_regulators = models.ManyToManyField(
        Person, related_name="report_compilers_and_regulators"
    )  # تدوین و تنظیم
    summarizers_and_compilers = models.ManyToManyField(
        Person, related_name="report_summarizers_and_compilers"
    )  # تلخیص و تدوین

    real_people = models.ManyToManyField(
        Person, related_name="report_real_people"
    )  # اشخاص حقیقی
    legal_people = models.ManyToManyField(
        Person, related_name="report_legal_people"
    )  # اشخاص حقوقی
    producers = models.ManyToManyField(
        Person, related_name="report_producers"
    )  # تهیه و تدوین، کاری از، تهیه شده
    technical_session_chairpeople = models.ManyToManyField(
        Person, related_name="report_technical_session_chairpeople"
    )  # مسئول نشست تخصصی
    infographics = models.ManyToManyField(
        Person, related_name="report_infographics"
    )  # گرافیک اطلاع رسان
    study_managers = models.ManyToManyField(
        Person, related_name="report_study_managers"
    )  # مدیر مطالعه
    lecturers = models.ManyToManyField(
        Person, related_name="report_lecturers"
    )  # سخنران
    designers = models.ManyToManyField(Person, related_name="report_designers")  # طراح
    layout_person = models.ManyToManyField(
        Person, related_name="report_layout_person"
    )  # صفحه آرا
    technical_experts = models.ManyToManyField(
        Person, related_name="report_technical_experts"
    )  # کارشناس فنی
    aggregation = models.ManyToManyField(
        Person, related_name="report_aggregation"
    )  # جمعبندی
    research_executors = models.ManyToManyField(
        Person, related_name="report_research_executors"
    )  # مجری تحقیق
    applicants = models.ManyToManyField(
        Person, related_name="report_applicants"
    )  # متقاضی
    participants_in_expertise_sessions = models.ManyToManyField(
        Person, related_name="report_participants_in_expertise_sessions"
    )  # شرکت کنندگان در نشست های کارشناسی
    participants_in_intensive_group_discussions = models.ManyToManyField(
        Person,
        related_name="report_participants_in_intensive_group_discussion_sessions",
    )  # شرکت کنندگان در بحث گروهی متمرکز

    abstract = models.TextField(null=True)
    abstract_preprocessed = models.TextField(null=True)
    abstract_summary = models.TextField(null=True)

    body = models.TextField(null=True)
    body_preprocessed = models.TextField(null=True)
    body_summary = models.TextField(null=True)


class JournalAuthor(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    first_name_fa = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    last_name_fa = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True)
    middle_name_fa = models.CharField(max_length=50, null=True)
    suffix = models.CharField(max_length=50, null=True)
    suffix_fa = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True, unique=True)
    orcid = models.CharField(max_length=50, null=True, unique=True)
    core_author = models.BooleanField()
    affiliation = models.CharField(max_length=50, null=True)
    affiliation_fa = models.CharField(max_length=50, null=True)


class Journal(models.Model):
    title = models.TextField(null=True)
    title_fa = models.TextField(null=True)
    short_title = models.CharField(max_length=25, null=True)
    jalali_pubdate_day = models.CharField(max_length=2, null=True)
    jalali_pubdate_month = models.CharField(max_length=2, null=True)
    jalali_pubdate_year = models.CharField(max_length=4, null=True)
    gregorian_pubdate_day = models.CharField(max_length=2, null=True)
    gregorian_pubdate_month = models.CharField(max_length=2, null=True)
    gregorian_pubdate_year = models.CharField(max_length=4, null=True)
    publisher_name = models.CharField(max_length=40, null=True)
    publish_type = models.CharField(max_length=20, null=True)
    article_type = models.CharField(max_length=30, null=True)
    hbi_system_user = models.CharField(max_length=20, null=True)
    language = models.CharField(max_length=10, null=True)
    number = models.CharField(max_length=20, null=True)
    web_url = models.CharField(max_length=50, null=True, unique=True)
    publish_edition = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=40, null=True)
    id_doi = models.CharField(max_length=20, null=True, unique=True)
    id_iranmedex = models.CharField(max_length=20, null=True)
    id_magiran = models.CharField(max_length=20, null=True)
    id_science = models.CharField(max_length=20, null=True)
    hbi_system_id = models.CharField(max_length=30, null=True)
    id_nlai = models.CharField(max_length=50, null=True)
    id_issn = models.CharField(max_length=20, null=True, unique=True)
    id_issn_online = models.CharField(max_length=20, null=True, unique=True)
    id_sid = models.CharField(max_length=20, null=True, unique=True)
    id_pii = models.CharField(max_length=20, null=True, unique=True)
    volume = models.CharField(max_length=10, null=True)
    issue = models.CharField(max_length=50, null=True)


class JournalArticle(models.Model):
    web_url = models.CharField(max_length=50, primary_key=True)
    title = models.TextField(null=True)
    title_fa = models.TextField(null=True)
    content_type = models.CharField(max_length=30, null=True)
    content_type_fa = models.CharField(max_length=30, null=True)
    english_keywords = models.ManyToManyField(
        EnglishPhrase, related_name="journal_english_keywords"
    )
    persian_keywords = models.ManyToManyField(
        PersianPhrase, related_name="journal_persian_keywords"
    )
    publish_type = models.CharField(max_length=15, null=True)
    gregorian_pubdate_day = models.CharField(max_length=2, null=True)
    gregorian_pubdate_month = models.CharField(max_length=2, null=True)
    gregorian_pubdate_year = models.CharField(max_length=4, null=True)
    subject = models.CharField(max_length=40, null=True)
    subject_fa = models.CharField(max_length=40, null=True)
    authors = models.ManyToManyField(
        JournalAuthor, related_name="journal_article_authors"
    )
    language = models.CharField(max_length=10, null=True)
    start_page = models.CharField(max_length=5, null=True)
    end_page = models.CharField(max_length=5, null=True)
    id_pii = models.CharField(max_length=20, null=True, unique=True)
    id_doi = models.CharField(max_length=20, null=True, unique=True)
    abstract = models.TextField(null=True)
    abstract_preprocessed = models.TextField(null=True)
    abstract_summary = models.TextField(null=True)
    abstract_fa = models.TextField(null=True)
    abstract_fa_preprocessed = models.TextField(null=True)
    abstract_fa_summary = models.TextField(null=True)
