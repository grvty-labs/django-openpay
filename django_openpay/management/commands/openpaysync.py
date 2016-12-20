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
                    dbobj.pull(commit=True)
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
                        openpay_id=cardJson['id'],
                    )
                except djop.models.Card.DoesNotExist:
                    dbobj = djop.models.Card(
                        openpay_id=cardJson['id'],
                        customer_id=customer.pk)
                finally:
                    dbobj.skip_signal = True
                    dbobj.pull(commit=True)
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
                        openpay_id=subscriptionJson['id'],
                        customer_id=customer.pk,
                        plan_id=plans[subscriptionJson['plan_id']],
                        card_id=cards[subscriptionJson['card']['id']]
                    )
                finally:
                    dbobj.skip_signal = True
                    dbobj.pull(commit=True)

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
