from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json

from . import openpay, models, webhooks, decorators


@require_POST
@transaction.atomic
def cardSave(request):
    if request.method == 'POST':
        body = None
        if request.is_ajax():
            body = json.loads(request.body.decode("utf-8"))
        else:
            body = request.POST
        token = body.get('token', False)
        deviceId = body.get('deviceId', False)
        customerId = body.get('customerId', False)
        if token and deviceId and customerId:
            card = models.Card.create_with_token(
                customerId=customerId,
                tokenId=token,
                deviceId=deviceId,
                alias=body.get('alias', ''))
            return HttpResponse()
    return HttpResponse(status=400)


@csrf_exempt
@require_POST
@decorators.basic_auth_required
@transaction.atomic
def webhook(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode("utf-8"))

        callFunctions = {
            'verification': webhooks.verification,
            'charge.refunded': webhooks.chargeRefunded,
            'charge.cancelled': webhooks.chargeCancelled,
            'charge.created': webhooks.chargeCreated,
            'charge.succeeded': webhooks.chargeSucceeded
            # TODO: Add pending webhooks:
            # 'charge.failed',
            # 'charge.rescored.to.decline',
            # 'subscription.charge.failed',
            # 'payout.created',
            # 'payout.succeeded',
            # 'payout.failed',
            # 'transfer.succeeded',
            # 'fee.succeeded',
            # 'fee.refund.succeeded',
            # 'spei.received',
            # 'chargeback.created',
            # 'chargeback.rejected',
            # 'chargeback.accepted',
            # 'order.created',
            # 'order.activated',
            # 'order.payment.received',
            # 'order.completed',
            # 'order.expired',
            # 'order.cancelled',
            # 'order.payment.cancelled',

        }
        option = callFunctions.get(body.get('type', ''), None)

        if option is not None:
            option(body)
        # TODO: Log the webhook
        return HttpResponse()

    return HttpResponse(status=400)
