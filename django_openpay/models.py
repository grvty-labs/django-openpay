from django.db import models
from django.db.models.fields.related import ManyToManyField

from . import openpay, hardcode, _ug


# Obtained and edited from:
# http://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(
                    f.value_from_object(instance).values_list('pk', flat=True)
                )
        else:
            data[f.name] = f.value_from_object(instance)
    return data


class Address(models.Model):
    city = models.TextField(
        blank=False,
        null=False,
        verbose_name=_ug('City')
    )
    state = models.TextField(
        blank=False,
        null=False,
        verbose_name=_ug('State')
    )
    line1 = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=_ug('Street (Line 1)'),
    )
    line2 = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=_ug('Street (Line 2)'),
    )
    line3 = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=_ug('Street (Line 3)'),
    )
    postal_code = models.IntegerField(
        blank=False,
        null=False,
        verbose_name=_ug('Postal Code')
    )
    country_code = models.CharField(
        choices=hardcode.address_countrycodes,
        default='MX',
        max_length=5,
        blank=True,
        null=False,
        verbose_name=_ug('Country')
    )


class Customer(models.Model):
    code = models.CharField(
        max_length=100,
        verbose_name=_ug('OpenPay Code')
    )
    first_name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        verbose_name=_ug('First Name'),
    )
    last_name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        verbose_name=_ug('Last Name'),
    )
    email = models.EmailField(
        blank=False,
        null=False,
        verbose_name=_ug('Email'),
    )
    phone_number = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        verbose_name=_ug('Phone Number'),
    )
    address = models.OneToOneField(
        Address,
        blank=False,
        null=False,
        related_name='customer',
        verbose_name=_ug('Address')
    )

    def save(self, *args, **kwargs):
        if self.code is not None:
            customer = openpay.Customer.retrieve(self.code)
            customer.name = self.first_name
            customer.last_name = self.last_name
            customer.email = self.email
            customer.phone_number = self.phone_number
            customer.address = to_dict(self.address)
            customer.save()
        else:
            customer = openpay.Customer.create(
                name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                phone_number=self.phone_number,
                address=to_dict(self.address),
            )
            self.code = customer.id

        super(Customer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.code is not None:
            customer = openpay.Customer.retrieve(self.code)
            customer.delete()
        super(Customer, self).delete(*args, **kwargs)


class Card(models.Model):
    code = models.CharField(
        max_length=100,
        verbose_name=_ug('OpenPay Code')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_ug('Card Name')
    )
    customer = models.ForeignKey(
        Customer,
        blank=False,
        null=False,
        verbose_name=_ug('Owner')
    )

    def delete(self, *args, **kwargs):
        if self.code is not None:
            card = openpay.Customer.retrieve(
                self.customer.code).cards.retrieve(self.code)
            if card:
                card.delete()
        super(Card, self).delete(*args, **kwargs)


class Plan(models.Model):
    code = models.CharField(
        max_length=100,
        verbose_name=_ug('OpenPay Code')
    )
    name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        verbose_name=_ug('Name'),
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        blank=False,
        null=False,
        verbose_name=_ug('Amount')
    )
    retry_times = models.IntegerField(
        default=3,
        blank=True,
        null=False,
        verbose_name=_ug('Number of retries')
    )
    status_after_retry = models.CharField(
        choices=hardcode.plan_statusafter,
        default=hardcode.plan_statusafter_unpaid,
        max_length=15,
        blank=True,
        null=False,
        verbose_name=_ug('When retries are exhausted')
    )
    trial_days = models.IntegerField(
        default=0,
        blank=True,
        null=False,
        verbose_name=_ug('Trial days')
    )
    repeat_every = models.IntegerField(
        default=1,
        blank=True,
        null=False,
        verbose_name=_ug('Frecuency Number')
    )
    repeat_unit = models.CharField(
        choices=hardcode.plan_repeatunit,
        default=hardcode.plan_repeatunit_month,
        max_length=15,
        blank=True,
        null=False,
        verbose_name=_ug('Frecuency Unit')
    )
    hidden = models.BooleanField(
        default=False,
        verbose_name=_ug('Hidden')
    )

    def save(self, *args, **kwargs):
        if self.code is not None:
            plan = openpay.Plan.retrieve(self.code)
            plan.name = self.name
            plan.amount = self.amount
            plan.status_after_retry = self.status_after_retry
            plan.retry_times = self.retry_times
            plan.repeat_unit = self.repeat_unit
            plan.trial_days = self.trial_days
            plan.repeat_every = self.repeat_every
            plan.save()
        else:
            plan = openpay.Plan.create(
                name=self.name,
                amount=self.amount,
                status_after_retry=self.status_after_retry,
                retry_times=self.retry_times,
                repeat_unit=self.repeat_unit,
                trial_days=self.trial_days,
                repeat_every=self.repeat_every,
            )
            self.code = plan.id

        super(Plan, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.code is not None:
            plan = openpay.Plan.retrieve(self.code)
            plan.delete()
        super(Plan, self).delete(*args, **kwargs)


class Suscription(models.Model):
    code = models.CharField(
        max_length=100,
        verbose_name=_ug('OpenPay Code')
    )
    customer = models.ForeignKey(
        Customer,
        blank=False,
        null=False,
        verbose_name=_ug('Customer')
    )
    card = models.ForeignKey(
        Card,
        blank=False,
        null=False,
        verbose_name=_ug('Card')
    )
    plan = models.ForeignKey(
        Plan,
        blank=False,
        null=False,
        verbose_name=_ug('Plan')
    )
    cancel_at_end_period = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=_ug('Cancel at the end of period')
    )
    trial_days = models.IntegerField(
        default=0,
        blank=True,
        null=False,
        verbose_name=_ug('Trial days')
    )

    def save(self, *args, **kwargs):
        if self.code is not None:
            suscription = openpay.Customer.retrive(
                self.customer.code).suscriptions.retrieve(self.code)
        else:
            openpay.Customer.retrive(self.customer.code).suscriptions.create(
                plan_id=self.plan.code,
                trial_days=self.trial_days,
                card_id=self.card.code,
            )
