from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST

import json

from . import openpay, models


@require_POST
@transaction.atomic
def cardSave(request):
    if request.is_ajax():
        body = json.loads(request.body.decode("utf-8"))
        token = body.get('token', False)
        deviceId = body.get('deviceId', False)
        customerId = body.get('customerId', False)
        if token and deviceId and customerId:
            card = models.Card.tokenized_create(
                customerId=customerId,
                tokenId=token,
                deviceId=deviceId,
                alias=body.get('alias', '')
            )

            return HttpResponse(status=200)
    return HttpResponse(status=400)


@require_POST
@transaction.atomic
def chargeSave(request):
    if request.is_ajax():
        # body = json.loads(request.body.decode("utf-8"))
        # token = body.get('token', False)
        # deviceId = body.get('deviceId', False)
        # customerId = body.get('customerId', False)
        # if token and deviceId and customerId:
        #     card = models.Card.tokenized_create(
        #         customerId=customerId,
        #         tokenId=token,
        #         deviceId=deviceId,
        #         alias=body.get('alias', '')
        #     )
        #
        #     return HttpResponse(status=200)
        print('AJAX')
        print(request.body)
    else:
        print(request)
    return HttpResponse(status=200)
