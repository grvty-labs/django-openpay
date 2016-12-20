from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime, parse_date

from decimal import Decimal
import os
import random

import django_openpay as djop


class Command(BaseCommand):
    def plans(self):
        dbPlans = dict()
        print('Pulling Plans from Openpay ...')
        plansList = djop.openpay.Plan.all()
        if plansList.get('count', 0) > 0:
            for planJson in plansList.get('data', []):
                try:
                    dbobj = djop.models.Plan.objects.get(
                        openpay_id=planJson['id'])
                except djop.models.Plan.DoesNotExist:
                    dbobj = djop.models.Plan(
                        openpay_id=planJson['id'])
                finally:
                    dbobj.skip_signal = True
                    dbobj.name = planJson['name']
                    dbobj.amount = Decimal(planJson['amount'])
                    dbobj.status_after_retry = planJson['status_after_retry']
                    dbobj.retry_times = planJson['retry_times']
                    dbobj.repeat_unit = planJson['repeat_unit']
                    dbobj.trial_days = planJson['trial_days']
                    dbobj.repeat_every = planJson['repeat_every']
                    dbobj.creation_date = parse_datetime(
                        planJson['creation_date'])
                    dbobj.save()
                    dbPlans[planJson['id']] = dbobj.pk
        print('{} plans pulled from Openpay.'.format(
            plansList.get('count', 0)))
        return dbPlans

    def cards(self, customer):
        dbCards = dict()
        cardsList = customer._openpay.cards.all()
        if cardsList.get('count', 0) > 0:
            for cardJson in cardsList.get('data', []):
                try:
                    dbobj = djop.models.Card.objects.get(
                        openpay_id=cardJson['id'])
                except djop.models.Card.DoesNotExist:
                    dbobj = djop.models.Card(
                        openpay_id=cardJson['id'])
                finally:
                    dbobj.skip_signal = True
                    dbobj.customer_id = customer.pk
                    dbobj.card_type = cardJson['type']
                    dbobj.holder = cardJson['holder_name']
                    dbobj.number = cardJson['card_number'][-4:]
                    dbobj.month = cardJson['expiration_month'][-2:]
                    dbobj.year = cardJson['expiration_year'][-2:]
                    dbobj.creation_date = parse_datetime(
                        cardJson['creation_date'])
                    dbobj.save()
                    dbCards[cardJson['id']] = dbobj.pk
        return dbCards

    def subscriptions(self, customer, plans, cards):
        subscriptionsList = customer._openpay.subscriptions.all()
        if subscriptionsList.get('count', 0) > 0:
            for subscriptionJson in subscriptionsList.get('data', []):
                try:
                    dbobj = djop.models.Subscription.objects.get(
                        openpay_id=subscriptionJson['id'])
                except djop.models.Subscription.DoesNotExist:
                    dbobj = djop.models.Subscription(
                        openpay_id=subscriptionJson['id'])
                finally:
                    dbobj.skip_signal = True
                    dbobj.customer_id = customer.pk,
                    dbobj.plan_id = plans[subscriptionJson['plan_id']],
                    dbobj.card_id = cards[subscriptionJson['card']['id']]
                    dbobj.cancel_at_period_end = \
                        subscriptionJson['cancel_at_period_end']
                    dbobj.charge_date = parse_date(
                        subscriptionJson['charge_date'])
                    dbobj.period_end_date = parse_date(
                        subscriptionJson['period_end_date'])
                    dbobj.status = subscriptionJson['status']
                    dbobj.current_period_number = \
                        subscriptionJson['current_period_number']
                    dbobj.trial_end_date = parse_date(
                        subscriptionJson['trial_end_date'])
                    dbobj.creation_date = parse_datetime(
                        subscriptionJson['creation_date'])
                    dbobj.save()

    def customers(self, plans):
        dbCustomers = dict()
        print('\n\n\nPulling Customers from Openpay ...')
        customerModel = djop.utils.get_customer_model()
        customersList = djop.openpay.Customer.all()
        if customersList.get('count', 0) > 0:
            for customerJson in customersList.get('data', []):
                try:
                    dbobj = customerModel.objects.get(
                        openpay_id=customerJson['id']
                    )
                except customerModel.DoesNotExist:
                    dbobj = customerModel(openpay_id=customerJson['id'])
                finally:
                    dbobj.skip_signal = True
                    dbobj.pull(commit=True)
                    cards = self.cards(dbobj)
                    self.subscriptions(dbobj, plans, cards)

        print('{} customers pulled from Openpay.'.format(
            customersList.get('count', 0)))
        return dbCustomers

    @transaction.atomic
    def handle(self, *args, **options):
        # print('Pulling Subscriptions from Openpay ...')
        # plansList = djop.openpay.Subscription.all()
        plans = self.plans()
        customers = self.customers(plans)
