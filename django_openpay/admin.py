from django.contrib import admin
from . import models, ugettext
from .utils import get_customer_model

CustomerModel = get_customer_model()


# Register your models here.
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    model = models.Address
    list_display = ('line1', 'line2', 'line3', 'city', 'state',
                    'country_code', 'postal_code')

    def get_readonly_fields(self, request, obj=None):
        return models.Address.get_readonly_fields(obj)


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    model = models.Card
    actions = ['refresh', 'dismiss', ]
    list_display = ('pk', 'openpay_id', 'alias', 'holder', 'customer',
                    'creation_date')

    def refresh(self, request, queryset):
        refreshed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_refresh(save=True)
            refreshed = refreshed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % refreshed
        self.message_user(
            request,
            "%s successfully refreshed." % message_bit
        )
    refresh.short_description = ugettext('Refresh selected instances')

    def dismiss(self, request, queryset):
        dismissed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_dismiss(save=True)
            dismissed = dismissed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % dismissed
        self.message_user(
            request,
            "%s successfully dismissed." % message_bit
        )
    dismiss.short_description = ugettext('Dismiss selected instances')

    def get_readonly_fields(self, request, obj=None):
        return models.Card.get_readonly_fields(obj)


@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    model = models.Plan
    actions = ['refresh', 'dismiss', ]
    list_display = ('name', 'openpay_id', 'status', 'amount', 'repeat_every',
                    'repeat_unit', 'creation_date')

    def refresh(self, request, queryset):
        refreshed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_refresh(save=True)
            refreshed = refreshed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % refreshed
        self.message_user(
            request,
            "%s successfully refreshed." % message_bit
        )
    refresh.short_description = ugettext('Refresh selected instances')

    def dismiss(self, request, queryset):
        dismissed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_dismiss(save=True)
            dismissed = dismissed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % dismissed
        self.message_user(
            request,
            "%s successfully dismissed." % message_bit
        )
    dismiss.short_description = ugettext('Dismiss selected instances')

    def get_readonly_fields(self, request, obj=None):
        return models.Plan.get_readonly_fields(obj)


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    model = models.Subscription
    actions = ['refresh', 'dismiss', ]
    list_display = ('pk', 'openpay_id', 'customer', 'plan', 'card',
                    'creation_date')

    def refresh(self, request, queryset):
        refreshed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_refresh(save=True)
            refreshed = refreshed + 1
        if refreshed == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % refreshed
        self.message_user(
            request,
            "%s successfully refreshed." % message_bit
        )
    refresh.short_description = ugettext('Refresh selected instances')

    def dismiss(self, request, queryset):
        dismissed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_dismiss(save=True)
            dismissed = dismissed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % dismissed
        self.message_user(
            request,
            "%s successfully dismissed." % message_bit
        )
    dismiss.short_description = ugettext('Dismiss selected instances')

    def get_readonly_fields(self, request, obj=None):
        return models.Subscription.get_readonly_fields(obj)


@admin.register(models.Refund)
class RefundAdmin(admin.ModelAdmin):
    model = models.Refund
    actions = ['refresh', 'dismiss', ]
    list_display = ('pk', 'openpay_id', 'customer', 'charge', 'amount',
                    'creation_date')

    def refresh(self, request, queryset):
        refreshed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_refresh(save=True)
            refreshed = refreshed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % refreshed
        self.message_user(
            request,
            "%s successfully refreshed." % message_bit
        )
    refresh.short_description = ugettext('Refresh selected instances')

    def dismiss(self, request, queryset):
        dismissed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_dismiss(save=True)
            dismissed = dismissed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % dismissed
        self.message_user(
            request,
            "%s successfully dismissed." % message_bit
        )
    dismiss.short_description = ugettext('Dismiss selected instances')

    def get_readonly_fields(self, request, obj=None):
        return models.Refund.get_readonly_fields(obj)


@admin.register(models.Charge)
class ChargeAdmin(admin.ModelAdmin):
    model = models.Charge
    actions = ['refresh', 'capture', 'refund', 'dismiss', ]
    list_display = ('pk', 'openpay_id', 'customer', 'card', 'amount',
                    'creation_date')

    def refresh(self, request, queryset):
        refreshed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_refresh(save=True)
            refreshed = refreshed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % refreshed
        self.message_user(
            request,
            "%s successfully refreshed." % message_bit
        )
    refresh.short_description = ugettext('Refresh selected instances')

    def capture(self, request, queryset):
        captured = 0
        for charge in queryset:
            charge.op_capture()
            captured = captured + 1
        if captured == 1:
            message_bit = "1 charge was"
        else:
            message_bit = "%s charges were" % captured
        self.message_user(
            request,
            "%s successfully captured." % message_bit
        )
    capture.short_description = ugettext('Capture selected charges')

    def refund(self, request, queryset):
        refunded = 0
        for charge in queryset:
            charge.op_refund()
            refunded = refunded + 1
        if refunded == 1:
            message_bit = "1 charge was"
        else:
            message_bit = "%s charges were" % refunded
            self.message_user(
                request,
                "%s successfully refunded." % message_bit
            )
    refund.short_description = ugettext('Refund selected charges')

    def dismiss(self, request, queryset):
        dismissed = 0
        for instance in queryset:
            instance.skip_signal = True
            instance.op_dismiss(save=True)
            dismissed = dismissed + 1
        if captured == 1:
            message_bit = "1 instance was"
        else:
            message_bit = "%s instances were" % dismissed
        self.message_user(
            request,
            "%s successfully dismissed." % message_bit
        )
    dismiss.short_description = ugettext('Dismiss selected instances')

    def get_readonly_fields(self, request, obj=None):
        return models.Charge.get_readonly_fields(obj)
