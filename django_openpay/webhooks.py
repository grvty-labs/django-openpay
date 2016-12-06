from django.utils.dateparse import parse_datetime, parse_date

from . import models


def verification(body):
    print(body['verification_code'])


def chargeRefunded(body):
    transaction = body['transaction']
    customer = models.Customer.objects.get(
        openpay_id=transaction['customer_id'])
    card = models.Card.objects.get(
        openpay_id=transaction['card']['id'])
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
            'customer': models.Customer.objects.get(
                openpay_id=transaction['customer_id']),
            'card': models.Card.objects.get(
                openpay_id=transaction['card']['id'])
        })


def chargeCreated(body):
    transaction = body['transaction']
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
            'customer': models.Customer.objects.get(
                openpay_id=transaction['customer_id']),
            'card': models.Card.objects.get(
                openpay_id=transaction['card']['id'])
        })


def chargeSucceeded(body):
    transaction = body['transaction']
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
            'customer': models.Customer.objects.get(
                openpay_id=transaction['customer_id']),
            'card': models.Card.objects.get(
                openpay_id=transaction['card']['id'])
        })
