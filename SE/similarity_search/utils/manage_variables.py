import pickle


def set_default_variables():
    SECRET_KEY = "django-insecure-_(shzvnhcno5_j=my*)8^u_mqx666s0vc66=p&c+yvava__g54"
    with open("./../../../data/config_variables/SECRET_KEY.pkl", "wb") as f:
        pickle.dump(SECRET_KEY, f)

    DEBUG = True
    with open("./../../../data/config_variables/DEBUG.pkl", "wb") as f:
        pickle.dump(DEBUG, f)

    BASE_URL = "http://elastic:@localhost:9200/"
    with open("./../../../data/config_variables/BASE_URL.pkl", "wb") as f:
        pickle.dump(BASE_URL, f)

    DB_NAME = "SE"
    with open("./../../../data/config_variables/DB_NAME.pkl", "wb") as f:
        pickle.dump(DB_NAME, f)

    DB_HOST = "localhost"
    with open("./../../../data/config_variables/DB_HOST.pkl", "wb") as f:
        pickle.dump(DB_HOST, f)

    DB_USER = "FaezehAD"
    with open("./../../../data/config_variables/DB_USER.pkl", "wb") as f:
        pickle.dump(DB_USER, f)

    DB_PASSWORD = "M0mtAz3"
    with open("./../../../data/config_variables/DB_PASSWORD.pkl", "wb") as f:
        pickle.dump(DB_PASSWORD, f)

    ELK_USER = "elastic"
    with open("./../../../data/config_variables/ELK_USER.pkl", "wb") as f:
        pickle.dump(ELK_USER, f)

    ELK_PASSWORD = ""
    with open("./../../../data/config_variables/ELK_PASSWORD.pkl", "wb") as f:
        pickle.dump(ELK_PASSWORD, f)

    ADMIN_USERNAME = "admin"
    with open("./../../../data/config_variables/ADMIN_USERNAME.pkl", "wb") as f:
        pickle.dump(ADMIN_USERNAME, f)

    ADMIN_PASSWORD = "nlpadmin1402"
    with open("./../../../data/config_variables/ADMIN_PASSWORD.pkl", "wb") as f:
        pickle.dump(ADMIN_PASSWORD, f)

    THRESHOLD = 60
    with open("./../../../data/config_variables/THRESHOLD.pkl", "wb") as f:
        pickle.dump(THRESHOLD, f)

    SHOW_FEEDBACK = "T"
    with open("./../../../data/config_variables/SHOW_FEEDBACK.pkl", "wb") as f:
        pickle.dump(SHOW_FEEDBACK, f)

    DEFAULT_OPTION = "report"
    with open("./../../../data/config_variables/DEFAULT_OPTION.pkl", "wb") as f:
        pickle.dump(DEFAULT_OPTION, f)

    DEFAULT_CHECKBOXES = ["3", "", "", "", "1"]
    with open("./../../../data/config_variables/DEFAULT_CHECKBOXES.pkl", "wb") as f:
        pickle.dump(DEFAULT_CHECKBOXES, f)

    DEFAULT_SEARCH_METHOD = "1"
    with open("./../../../data/config_variables/DEFAULT_SEARCH_METHOD.pkl", "wb") as f:
        pickle.dump(DEFAULT_SEARCH_METHOD, f)

    DEFAULT_QUERY_ID = None
    with open(
        "./../../../data/config_variables/DEFAULT_QUERY_ID.pkl", "wb"
    ) as f:
        pickle.dump(DEFAULT_QUERY_ID, f)

    DEFAULT_PEOPLE_LIST = list()
    with open(
        "./../../../data/config_variables/DEFAULT_PEOPLE_LIST.pkl", "wb"
    ) as f:
        pickle.dump(DEFAULT_PEOPLE_LIST, f)

def set_show_feedback(SHOW_FEEDBACK):
    with open("./data/config_variables/SHOW_FEEDBACK.pkl", "wb") as f:
        pickle.dump(SHOW_FEEDBACK, f)


def set_threshold(THRESHOLD):
    with open("./data/config_variables/THRESHOLD.pkl", "wb") as f:
        pickle.dump(THRESHOLD, f)


# set_default_variables()



# def get_SECRET_KEY():
#     with open("./../../../data/config_variables/SECRET_KEY.pkl", "rb") as f:
#         return pickle.load(f)

# def get_DEBUG():
#     with open("./../../../data/config_variables/DEBUG.pkl", "rb") as f:
#         return pickle.load(f)


# def get_BASE_URL():
#     with open("./../../../data/config_variables/BASE_URL.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DB_NAME():
#     with open("./../../../data/config_variables/DB_NAME.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DB_HOST():
#     with open("./../../../data/config_variables/DB_HOST.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DB_USER():
#     with open("./../../../data/config_variables/DB_USER.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DB_PASSWORD():
#     with open("./../../../data/config_variables/DB_PASSWORD.pkl", "rb") as f:
#         return pickle.load(f)


# def get_ELK_USER():
#     with open("./../../../data/config_variables/ELK_USER.pkl", "rb") as f:
#         return pickle.load(f)


# def get_ELK_PASSWORD():
#     with open("./../../../data/config_variables/ELK_PASSWORD.pkl", "rb") as f:
#         return pickle.load(f)


# def get_ADMIN_USERNAME():
#     with open("./../../../data/config_variables/ADMIN_USERNAME.pkl", "rb") as f:
#         return pickle.load(f)


# def get_ADMIN_PASSWORD():
#     with open("./../../../data/config_variables/ADMIN_PASSWORD.pkl", "rb") as f:
#         return pickle.load(f)


# def get_THRESHOLD():
#     with open("./../../../data/config_variables/THRESHOLD.pkl", "rb") as f:
#         return pickle.load(f)


# def get_SHOW_FEEDBACK():
#     with open("./../../../data/config_variables/SHOW_FEEDBACK.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DEFAULT_OPTION():
#     with open("./../../../data/config_variables/DEFAULT_OPTION.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DEFAULT_CHECKBOXES():
#     with open("./../../../data/config_variables/DEFAULT_CHECKBOXES.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DEFAULT_SEARCH_METHOD():
#     with open("./../../../data/config_variables/DEFAULT_SEARCH_METHOD.pkl", "rb") as f:
#         return pickle.load(f)


# def get_DEFAULT_RAW_RESULTS():
#     with open("./../../../data/config_variables/DEFAULT_RAW_RESULTS.pkl", "rb") as f:
#         return pickle.load(f)
