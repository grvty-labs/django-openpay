from django.utils.translation import ugettext, ugettext_lazy
from django.conf import settings

import openpay

default_app_config = 'django_openpay.apps.DjangoOpenpayConfig'

openpay.api_key = getattr(settings, 'OPENPAY_PRIVATE_API_KEY', None)
openpay.verify_ssl_certs = getattr(settings, 'OPENPAY_VERIFY_SSL', False)
openpay.merchant_id = getattr(settings, 'OPENPAY_MERCHANT_ID', None)
openpay.device_id = not getattr(settings, 'OPENPAY_DEVICE_ID', None)
openpay.production = not getattr(settings, 'DEBUG', True)
