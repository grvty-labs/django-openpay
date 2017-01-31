from django.utils.dateparse import parse_datetime, parse_date
import logging

from . import models

logger = logging.getLogger(__name__)


def safeCopy(json, items):
    for k in json:
        if k in items:
            if json[k] is None:
                json[k] = ''
    return json


def verification(body):
    logger.info(body['verification_code'])


def chargeRefunded(body):
    card = None
    customer = None
    subscription = None
    transaction = safeCopy(body['transaction'], [
        'authorization', 'error_message', 'order_id', 'description'])
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
        if 'id' in transaction['card']:
            card = models.Card.objects.get(
                openpay_id=transaction['card']['id'])
        if not customer and 'customer_id' in transaction['card']:
            customer = models.get_customer_model().objects.get(
                openpay_id=transaction['card']['customer_id'])
    charge, created = models.Charge.objects.update_or_create(
        openpay_id=transaction['id'],
        defaults={
            'authorization': transaction['authorization'],
            'method': transaction['method'],
            'operation_type': transaction['operation_type'],
            'transaction_type': transaction['transaction_type'],
            'status': transaction['status'],
            'conciliated': transaction['conciliated'],
            'creation_date': parse_datetime(transaction['creation_date']),
            'operation_date': parse_datetime(transaction['operation_date']),
            'description': transaction['description'],
            'error_message': transaction['error_message'],
            'order_id': transaction['order_id'],
            'amount': transaction['amount'],
            'currency': transaction['currency'],
            'customer': customer,
            'card': card,
        })

    transaction = safeCopy(transaction['refund'], [
        'authorization', 'error_message', 'order_id', 'description'])
    refund, created = models.Refund.objects.update_or_create(
        openpay_id=transaction['id'],
        defaults={
            'authorization': transaction['authorization'],
            'method': transaction['method'],
            'operation_type': transaction['operation_type'],
            'transaction_type': transaction['transaction_type'],
            'status': transaction['status'],
            'conciliated': transaction['conciliated'],
            'creation_date': parse_datetime(transaction['creation_date']),
            'operation_date': parse_datetime(transaction['operation_date']),
            'description': transaction['description'],
            'error_message': transaction['error_message'],
            'order_id': transaction['order_id'],
            'amount': transaction['amount'],
            'currency': transaction['currency'],
            'customer': customer,
            'charge': charge,
        })


def chargeCancelled(body):
    card = None
    customer = None
    subscription = None
    transaction = safeCopy(body['transaction'], [
        'authorization', 'error_message', 'order_id', 'description'])
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
        if 'id' in transaction['card']:
            card = models.Card.objects.get(
                openpay_id=transaction['card']['id'])
        if not customer and 'customer_id' in transaction['card']:
            customer = models.get_customer_model().objects.get(
                openpay_id=transaction['card']['customer_id'])
    charge, created = models.Charge.objects.update_or_create(
        openpay_id=transaction['id'],
        defaults={
            'authorization': transaction['authorization'],
            'method': transaction['method'],
            'operation_type': transaction['operation_type'],
            'transaction_type': transaction['transaction_type'],
            'status': transaction['status'],
            'conciliated': transaction['conciliated'],
            'creation_date': parse_datetime(transaction['creation_date']),
            'operation_date': parse_datetime(transaction['operation_date']),
            'description': transaction['description'],
            'error_message': transaction['error_message'],
            'order_id': transaction['order_id'],
            'amount': transaction['amount'],
            'currency': transaction['currency'],
            'customer': customer,
            'card': card,
            'subscription': subscription
        })


def chargeCreated(body):
    card = None
    customer = None
    subscription = None
    transaction = safeCopy(body['transaction'], [
        'authorization', 'error_message', 'order_id', 'description'])
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
        if 'id' in transaction['card']:
            card = models.Card.objects.get(
                openpay_id=transaction['card']['id'])
        if not customer and 'customer_id' in transaction['card']:
            customer = models.get_customer_model().objects.get(
                openpay_id=transaction['card']['customer_id'])
    charge, created = models.Charge.objects.update_or_create(
        openpay_id=transaction['id'],
        defaults={
            'authorization': transaction['authorization'],
            'method': transaction['method'],
            'operation_type': transaction['operation_type'],
            'transaction_type': transaction['transaction_type'],
            'status': transaction['status'],
            'conciliated': transaction['conciliated'],
            'creation_date': parse_datetime(transaction['creation_date']),
            'operation_date': parse_datetime(transaction['operation_date']),
            'description': transaction['description'],
            'error_message': transaction['error_message'],
            'order_id': transaction['order_id'],
            'amount': transaction['amount'],
            'currency': transaction['currency'],
            'customer': customer,
            'card': card,
            'subscription': subscription
        })


def chargeSucceeded(body):
    card = None
    customer = None
    subscription = None
    transaction = safeCopy(body['transaction'], [
        'authorization', 'error_message', 'order_id', 'description'])
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
        if 'id' in transaction['card']:
            card = models.Card.objects.get(
                openpay_id=transaction['card']['id'])
        if not customer and 'customer_id' in transaction['card']:
            customer = models.get_customer_model().objects.get(
                openpay_id=transaction['card']['customer_id'])
    charge, created = models.Charge.objects.update_or_create(
        openpay_id=transaction['id'],
        defaults={
            'authorization': transaction['authorization'],
            'method': transaction['method'],
            'operation_type': transaction['operation_type'],
            'transaction_type': transaction['transaction_type'],
            'status': transaction['status'],
            'conciliated': transaction['conciliated'],
            'creation_date': parse_datetime(transaction['creation_date']),
            'operation_date': parse_datetime(transaction['operation_date']),
            'description': transaction['description'],
            'error_message': transaction['error_message'],
            'order_id': transaction['order_id'],
            'amount': transaction['amount'],
            'currency': transaction['currency'],
            'customer': customer,
            'card': card,
            'subscription': subscription
        })
