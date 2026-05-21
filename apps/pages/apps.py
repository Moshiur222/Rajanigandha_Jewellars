from django.apps import AppConfig
import os


class PagesConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.pages"

    def ready(self):

        if os.environ.get("RUN_MAIN") == "true":

            from .scheduler import start

            start()