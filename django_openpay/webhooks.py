from django.utils.dateparse import parse_datetime, parse_date

from . import models


def verification(body):
    print(body['verification_code'])


def chargeRefunded(body):
    transaction = body['transaction']
    card = None
    customer = None
    subscription = None
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
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

    transaction = transaction['refund']
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
    transaction = body['transaction']
    card = None
    customer = None
    subscription = None
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
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
    transaction = body['transaction']
    card = None
    customer = None
    subscription = None
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
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
    transaction = body['transaction']
    card = None
    customer = None
    subscription = None
    if 'customer_id' in transaction:
        customer = models.get_customer_model().objects.get(
            openpay_id=transaction['customer_id'])
    if 'subscription_id' in transaction:
        subscription = models.Subscription.objects.get(
            openpay_id=transaction['subscription_id'])
    if 'card' in transaction:
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
