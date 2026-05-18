from django.apps import AppConfig


class PagesConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "apps.pages"

    def ready(self):

        from .scheduler import start
        start()

        import apps.pages.signals