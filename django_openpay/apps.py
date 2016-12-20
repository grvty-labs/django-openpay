from django.apps import AppConfig
from . import ugettext_lazy


class DjangoOpenpayConfig(AppConfig):
    name = 'django_openpay'
    verbose_name = ugettext_lazy('Django Openpay')
