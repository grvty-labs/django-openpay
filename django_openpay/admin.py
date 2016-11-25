from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    model = models.Address
    list_display = ('line1', 'line2', 'line3', 'city', 'state',
                    'country_code', 'postal_code')

    def get_readonly_fields(self, request, obj=None):
        return models.Address.get_readonly_fields(obj)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = models.Customer
    list_display = ('openpay_id', 'first_name', 'last_name', 'email',
                    'phone_number', 'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Customer.get_readonly_fields(obj)


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    model = models.Card
    list_display = ('openpay_id', 'alias', 'holder', 'customer',
                    'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Card.get_readonly_fields(obj)


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    model = models.Plan
    list_display = ('openpay_id', 'name', 'amount', 'repeat_every',
                    'repeat_unit', 'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Plan.get_readonly_fields(obj)


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = models.Subscription
    list_display = ('openpay_id', 'customer', 'plan', 'card', 'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Subscription.get_readonly_fields(obj)


@admin.register(models.Charge)
class ChargeAdmin(admin.ModelAdmin):
    model = models.Charge
    list_display = ('openpay_id', 'customer', 'plan', 'card', 'amount',
                    'creation_date')

    def get_readonly_fields(self, request, obj=None):
        return models.Charge.get_readonly_fields(obj)
