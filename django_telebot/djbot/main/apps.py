from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.core.management import commands


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'