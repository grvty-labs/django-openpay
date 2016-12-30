# Obtained and edited from:
# https://goo.gl/0lW3Di
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

import base64
import binascii
from urllib.parse import unquote_plus

from . import ugettext_lazy


def get_customer_model():
    """
    Returns the Customer model that is active in this project.
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


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self):
        super(HttpResponseUnauthorized, self).__init__()
        realm = getattr(settings, 'BASICAUTH_REALM', 'Secure resource')
        self['WWW-Authenticate'] = 'Basic realm="{}"'.format(realm)


def extract_basicauth(authorization_header, encoding='utf-8'):
    splitted = authorization_header.split(' ')
    if len(splitted) != 2:
        return None

    auth_type, auth_string = splitted

    if 'basic' != auth_type.lower():
        return None

    try:
        b64_decoded = base64.b64decode(auth_string)
    except (TypeError, binascii.Error):
        return None
    try:
        auth_string_decoded = b64_decoded.decode(encoding)
    except UnicodeDecodeError:
        return None

    splitted = auth_string_decoded.split(':')

    if len(splitted) != 2:
        return None

    username, password = map(unquote_plus, splitted)
    return username, password


def validate_request(request):
    # Check an incoming request.
    # Returns:
    #     - None if authentication failed
    #     - the validated username otherwise
    if not getattr(settings, 'OPENPAY_BASICAUTH_USERS', None):
        return True

    if 'HTTP_AUTHORIZATION' not in request.META:
        return None

    authorization_header = request.META['HTTP_AUTHORIZATION']
    ret = extract_basicauth(authorization_header)
    if not ret:
        return None

    username, password = ret

    if settings.OPENPAY_BASICAUTH_USERS.get(username) != password:
        return None

    return username
