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
                    dbobj.currency = planJson['currency']
                    dbobj.status_after_retry = planJson['status_after_retry']
                    dbobj.retry_times = planJson['retry_times']
                    dbobj.repeat_unit = planJson['repeat_unit']
                    dbobj.trial_days = planJson['trial_days']
                    dbobj.repeat_every = planJson['repeat_every']
                    dbobj.status = planJson['status']
                    dbobj.creation_date = parse_datetime(
                        planJson['creation_date'])
                    dbobj.save()
                    dbPlans[planJson['id']] = dbobj.pk
        return dbPlans

    def cards(self, customer):
        dbCards = dict()
        cardsList = customer.op_cards()
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
                    dbobj.bank_name = cardJson['bank_name']
                    dbobj.brand = cardJson['brand']
                    dbobj.month = cardJson['expiration_month'][-2:]
                    dbobj.year = cardJson['expiration_year'][-2:]
                    dbobj.creation_date = parse_datetime(
                        cardJson['creation_date'])
                    dbobj.save()
                    dbCards[cardJson['id']] = dbobj.pk
        return dbCards

    def subscriptions(self, customer, plans, cards):
        subscriptionsList = customer.op_subscriptions()
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
                    dbobj.customer_id = customer.pk
                    dbobj.plan_id = plans[subscriptionJson['plan_id']]
                    dbobj.card_id = cards[subscriptionJson['card']['id']]
                    dbobj.cancel_at_period_end = \
                        subscriptionJson['cancel_at_period_end']
                    new_charge_date = parse_date(
                        subscriptionJson['charge_date'])
                    dbobj.latest_charge_date = dbobj.charge_date if \
                        dbobj.charge_date != new_charge_date else \
                        dbobj.latest_charge_date
                    dbobj.charge_date = new_charge_date
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
        return subscriptionsList.get('count', 0)

    def customers(self, plans):
        cardsNum = 0
        subsNum = 0
        print('Pulling Customers from Openpay ...')
        customerModel = djop.utils.get_customer_model()
        customersList = djop.openpay.Customer.all()
        if customersList.get('count', 0) > 0:
            for customerJson in customersList.get('data', []):
                try:
                    dbobj = customerModel.objects.get(
                        openpay_id=customerJson['id'])
                except customerModel.DoesNotExist:
                    dbobj = customerModel(openpay_id=customerJson['id'])
                finally:
                    dbobj.skip_signal = True
                    dbobj.op_refresh(save=True)
                    cards = self.cards(dbobj)
                    cardsNum += len(cards)
                    subs = self.subscriptions(dbobj, plans, cards)
                    subsNum += subs

        return customersList.get('count', 0), cardsNum, subsNum

    @transaction.atomic
    def handle(self, *args, **options):
        # print('Pulling Subscriptions from Openpay ...')
        # plansList = djop.openpay.Subscription.all()
        plans = self.plans()
        customers, cards, subs = self.customers(plans)

        print('{} plans pulled from Openpay.'.format(len(plans)))
        print('{} customers pulled from Openpay.'.format(customers))
        print('{} cards pulled from Openpay.'.format(cards))
        print('{} subscriptions pulled from Openpay.'.format(subs))
