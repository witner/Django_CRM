from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class AppCStarkConfig(AppConfig):
    name = 'app_c_stark'

    def ready(self):
        autodiscover_modules('stark')
