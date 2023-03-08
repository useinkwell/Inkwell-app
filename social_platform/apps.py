from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_platform'

    def ready(self) -> None:

        from . import signals

        return super().ready()
        