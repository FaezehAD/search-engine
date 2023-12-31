#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


from django.core.management.commands.runserver import Command as runserver

# from django.db import reset_cache
# from django.db.models import Q
# from django.utils import timezone
# from django.contrib.sessions.models import Session

runserver.default_port = "8000"


# def delete_old_sessions(apps=None):

#     Session = apps.get_model("sessions")
#     now = timezone.now()

#     threshold_date = now - timezone.timedelta(
#         days=1
#     )  

#     Session.objects.filter(last_activity_date__lt=threshold_date).delete()

#     reset_cache(cache_type="session")


# if __name__ == "__main__":
#     from django.core.management import call

    # call(delete_old_sessions)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search_engine.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
