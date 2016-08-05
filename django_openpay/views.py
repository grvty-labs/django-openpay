from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from . import openpay


@require_POST
@transaction.atomic
def cardSave(request):
    if request.is_ajax():
        token = request.body.get('token', False)
        deviceId = request.body.get('deviceId', False)
        if token and deviceId:

            # TODO: This is just a test, IMPROVE
            clientID = 'avd8o16jdmkyjxj5ufqb'  # SANDBOX client, so no problem for this test
            openpay.Card.create(customer=clientID, token_id=token,
                                device_session_id=deviceId)  # SUCCESS!!!

            return HttpResponse(status=200)
    return HttpResponse(status=400)
