from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message_be.apps'

    def ready(self):
        import message_be.apps.signals
