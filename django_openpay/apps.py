from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DjangoOpenpayConfig(AppConfig):
    name = 'django_openpay'
    verbose_name = _('Django OpenPay')
