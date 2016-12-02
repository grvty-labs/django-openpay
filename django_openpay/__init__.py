from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext, ugettext_lazy

import openpay

default_app_config = 'django_openpay.apps.DjangoOpenpayConfig'


def get_customer_model():
    """
    Returns the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.OPENPAY_CUSTOMER_MODEL)
    except ValueError:
        raise ImproperlyConfigured(
            "OPENPAY_CUSTOMER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "OPENPAY_CUSTOMER_MODEL refers to model '%s' "
            "that has not been installed" % settings.OPENPAY_CUSTOMER_MODEL
        )


def start():
    OPENPAY_PRIVATE_API_KEY = getattr(
        settings, 'OPENPAY_PRIVATE_API_KEY', None)
    OPENPAY_VERIFY_SSL = getattr(settings, 'OPENPAY_VERIFY_SSL', None)
    OPENPAY_MERCHANT_ID = getattr(settings, 'OPENPAY_MERCHANT_ID', None)
    OPENPAY_DEVICE_ID = getattr(settings, 'OPENPAY_DEVICE_ID', None)
    DEBUG = getattr(settings, 'DEBUG', None)
    OPENPAY_BASICAUTH_USERS = getattr(
        settings, 'OPENPAY_BASICAUTH_USERS', None)

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
    if not OPENPAY_DEVICE_ID:
        raise ImproperlyConfigured(
            "OPENPAY_DEVICE_ID must be defined. (String)"
        )
    if DEBUG not in [True, False]:
        raise ImproperlyConfigured(
            "DEBUG must be defined. (Boolean)"
        )
    if not OPENPAY_BASICAUTH_USERS:
        raise ImproperlyConfigured(
            "OPENPAY_BASICAUTH_USERS must be defined. (Dict)"
        )

    openpay.api_key = OPENPAY_PRIVATE_API_KEY
    openpay.verify_ssl_certs = OPENPAY_VERIFY_SSL
    openpay.merchant_id = OPENPAY_MERCHANT_ID
    openpay.device_id = OPENPAY_DEVICE_ID
    openpay.production = not DEBUG

start()
