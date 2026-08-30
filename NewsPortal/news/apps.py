import os

from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from .scheduler import start
            start()