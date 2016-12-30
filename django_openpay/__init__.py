from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext, ugettext_lazy, ungettext_lazy

import openpay

default_app_config = 'django_openpay.apps.DjangoOpenpayConfig'


def start():
    OPENPAY_PRIVATE_API_KEY = getattr(
        settings, 'OPENPAY_PRIVATE_API_KEY', None)
    OPENPAY_VERIFY_SSL = getattr(settings, 'OPENPAY_VERIFY_SSL', None)
    OPENPAY_MERCHANT_ID = getattr(settings, 'OPENPAY_MERCHANT_ID', None)
    OPENPAY_DEVICE_ID = getattr(settings, 'OPENPAY_DEVICE_ID', None)
    DEBUG = getattr(settings, 'DEBUG', None)
    # OPENPAY_BASICAUTH_USERS = getattr(
    #     settings, 'OPENPAY_BASICAUTH_USERS', None)
    OPENPAY_CUSTOMER_MODEL = getattr(
        settings, 'OPENPAY_CUSTOMER_MODEL', None)

    if not OPENPAY_PRIVATE_API_KEY:
        raise ImproperlyConfigured(
            "OPENPAY_PRIVATE_API_KEY must be defined. (String)"
        )
    if OPENPAY_VERIFY_SSL not in [True, False]:
        raise ImproperlyConfigured(
            "OPENPAY_VERIFY_SSL must be defined. (Boolean)"
        )
    if not OPENPAY_MERCHANT_ID:
        raise ImproperlyConfigured(
            "OPENPAY_MERCHANT_ID must be defined. (String)"
        )
    if not OPENPAY_DEVICE_ID or not (0 <= len(OPENPAY_DEVICE_ID) <= 31):
        raise ImproperlyConfigured(
            "OPENPAY_DEVICE_ID must be defined and must have a length between "
            "1 and 32 characters. (String)"
        )
    if DEBUG not in [True, False]:
        raise ImproperlyConfigured(
            "DEBUG must be defined. (Boolean)"
        )
    # if not OPENPAY_BASICAUTH_USERS:
    #     raise ImproperlyConfigured(
    #         "OPENPAY_BASICAUTH_USERS must be defined. (Dict)"
    #     )
    if not OPENPAY_CUSTOMER_MODEL:
        raise ImproperlyConfigured(
            "OPENPAY_CUSTOMER_MODEL must be defined. (String)"
        )

    openpay.api_key = OPENPAY_PRIVATE_API_KEY
    openpay.verify_ssl_certs = OPENPAY_VERIFY_SSL
    openpay.merchant_id = OPENPAY_MERCHANT_ID
    openpay.device_id = OPENPAY_DEVICE_ID
    openpay.production = not DEBUG

start()
