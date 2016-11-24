from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    model = models.Address
    list_display = ('line1', 'line2', 'line3', 'city', 'state',
                    'country_code', 'postal_code')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = models.Customer
    list_display = ('code', 'first_name', 'last_name', 'email', 'phone_number',
                    'creation_date')


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    model = models.Card
    list_display = ('code', 'alias', 'holder', 'customer', 'creation_date')


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    model = models.Plan
    list_display = ('code', 'name', 'amount', 'repeat_every', 'repeat_unit',
                    'creation_date')


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = models.Subscription
    list_display = ('code', 'customer', 'plan', 'card', 'creation_date')


@admin.register(models.Charge)
class ChargeAdmin(admin.ModelAdmin):
    model = models.Charge
    list_display = ('code', 'customer', 'plan', 'card', 'amount',
                    'creation_date')
