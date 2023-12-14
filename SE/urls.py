from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index-page"),
    path("search", views.search_results, name="search-results-page"),
    path("advanced-search", views.advanced_search, name="advanced-search-page"),
    path("articles/<int:id>", views.article_details, name="article-detail-page"),
    path("reports/<int:id>", views.report_details, name="report-detail-page"),
    path("search-guide/", views.guide, name="guide-page"),
    # path("signup", views.signup, name="signup-page"),
    path("signin", views.signin, name="signin-page"),
    path("signout", views.signout, name="signout-page"),
    path("admin", views.admin_panel, name="admin-page"),
    path("admin/settings", views.settings_page, name="settings-page"),
    path("admin/logs", views.show_logs, name="logs-page"),
    path("admin/log/<str:id>", views.log_details, name="log-detail-page"),
    path(
        "plagiarism-detection/input",
        views.plagiarism_detection_input,
        name="plagiarism-detection-input-page",
    ),
    path(
        "plagiarism-detection/compare-texts/<str:input_title>/<str:id>",
        views.compare_texts,
        name="compare-texts-page",
    ),
    path(
        "plagiarism-detection/<str:input_title>",
        views.plagiarism_detection,
        name="plagiarism-detection-page",
    ),
]
