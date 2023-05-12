from django.apps import AppConfig


class MainsectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainsection'

    def ready(self):
        from . import signals