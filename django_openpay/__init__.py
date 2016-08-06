from django.utils.translation import ugettext as _ug
from django.conf import settings

import openpay

default_app_config = 'django_openpay.apps.DjangoOpenpayConfig'

# OPENPAY_PRIVATE_API_KEY
# OPENPAY_PUBLIC_API_KEY
# OPENPAY_MERCHANT_ID
# OPENPAY_VERIFY_SSL

openpay.api_key = getattr(
    settings, 'OPENPAY_PRIVATE_API_KEY', 'pk_f0660ad5a39f4912872e24a7a660370c'
)
openpay.verify_ssl_certs = getattr(settings, 'OPENPAY_VERIFY_SSL', False)
openpay.merchant_id = getattr(
    settings, 'OPENPAY_MERCHANT_ID', 'mzdtln0bmtms6o3kck8f'
)
openpay.production = not getattr(settings, 'DEBUG', True)
