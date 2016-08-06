from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils.dateparse import parse_datetime, parse_date

from decimal import Decimal

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

    def to_idless_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(
                        f.value_from_object(self).values_list('pk', flat=True)
                    )
            elif f.name != 'id':
                data[f.name] = f.value_from_object(self)
        return data


class Customer(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
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
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name=_ug('Creation date')
    )

    def retrieve(self):
        customer = openpay.Customer.retrieve(self.code)
        self.first_name = customer.name
        self.last_name = customer.last_name
        self.email = customer.email
        self.phone_number = customer.phone_number
        self.creation_date = parse_datetime(customer.creation_date)

    def save(self, *args, **kwargs):
        if self.code:
            customer = openpay.Customer.retrieve(self.code)
            customer.name = self.first_name
            customer.last_name = self.last_name
            customer.email = self.email
            customer.phone_number = self.phone_number
            customer.address = self.address.to_idless_dict()
            customer.save()
        else:
            customer = openpay.Customer.create(
                name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                phone_number=self.phone_number,
                address=self.address.to_idless_dict(),
            )
            self.code = customer.id

        self.retrieve()
        super(Customer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.code:
            customer = openpay.Customer.retrieve(self.code)
            customer.delete()
        super(Customer, self).delete(*args, **kwargs)

    def __str__(self):
        return '{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name)


class Card(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=_ug('OpenPay code')
    )
    alias = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=_ug('Alias')
    )
    card_type = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        verbose_name=_ug('Card type')
    )
    holder = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=_ug('Holder name')
    )
    number = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        verbose_name=_ug('Number')
    )
    month = models.CharField(
        max_length=3,
        blank=True,
        null=False,
        verbose_name=_ug('Expiration month')
    )
    year = models.CharField(
        max_length=3,
        blank=True,
        null=False,
        verbose_name=_ug('Expiration year')
    )
    customer = models.ForeignKey(
        Customer,
        blank=False,
        null=False,
        related_name='cards',
        verbose_name=_ug('Owner')
    )
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name=_ug('Creation date')
    )

    @classmethod
    def tokenized_create(cls, customerId, tokenId, deviceId, alias=''):
        card = openpay.Card.create(customer=customerId, token_id=tokenId,
                                   device_session_id=deviceId)
        if card.id:
            customer = Customer.objects.get(code=customerId)
            card = cls(
                code=card.id,
                alias=alias,
                card_type=card.type,
                holder=card.holder_name,
                number=card.card_number[-4:],
                month=card.expiration_month[-2:],
                year=card.expiration_year[-2:],
                creation_date=parse_datetime(card.creation_date),
                customer=customer,
                recovered=True
            )
            return card.save()

    def retrieve(self):
        card = openpay.Customer.retrieve(
            self.customer.code
        ).cards.retrieve(
            self.code
        )
        self.recovered = True
        self.card_type = card.type
        self.holder = card.holder_name
        self.number = card.card_number[-4:]
        self.month = card.expiration_month[-2:]
        self.year = card.expiration_year[-2:]
        self.creation_date = parse_datetime(card.creation_date)

    def save(self, *args, **kwargs):
        if self.code:
            self.retrieve()
        super(Card, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.code:
            card = openpay.Customer.retrieve(
                self.customer.code).cards.retrieve(self.code)
            if card:
                card.delete()
        super(Card, self).delete(*args, **kwargs)

    def __str__(self):
        if self.alias:
            return '{code} | {customer} | {alias}'.format(
                code=self.code, customer=self.customer, alias=self.alias)
        return '{code} | {customer}'.format(
            code=self.code, customer=self.customer)


class Plan(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
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
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name=_ug('Creation date')
    )

    def retrieve(self):
        plan = openpay.Plan.retrieve(self.code)
        self.name = plan.name
        self.amount = Decimal(plan.amount)
        self.status_after_retry = plan.status_after_retry
        self.retry_times = plan.retry_times
        self.repeat_unit = plan.repeat_unit
        self.trial_days = plan.trial_days
        self.repeat_every = plan.repeat_every
        self.creation_date = parse_datetime(plan.creation_date)

    def save(self, *args, **kwargs):
        if self.code:
            plan = openpay.Plan.retrieve(self.code)
            plan.name = self.name
            plan.amount = str(self.amount)
            plan.status_after_retry = self.status_after_retry
            plan.retry_times = self.retry_times
            plan.repeat_unit = self.repeat_unit
            plan.trial_days = self.trial_days
            plan.repeat_every = self.repeat_every
            plan.save()
        else:
            plan = openpay.Plan.create(
                name=self.name,
                amount=str(self.amount),
                status_after_retry=self.status_after_retry,
                retry_times=self.retry_times,
                repeat_unit=self.repeat_unit,
                trial_days=self.trial_days,
                repeat_every=self.repeat_every,
            )
            self.code = plan.id

        self.retrieve()

        super(Plan, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.code:
            plan = openpay.Plan.retrieve(self.code)
            plan.delete()
        super(Plan, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=_ug('OpenPay Code')
    )
    customer = models.ForeignKey(
        Customer,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=_ug('Customer')
    )
    card = models.ForeignKey(
        Card,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=_ug('Card')
    )
    plan = models.ForeignKey(
        Plan,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=_ug('Plan')
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=_ug('Cancel at the end of period')
    )
    trial_end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_ug('Trial days')
    )
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name=_ug('Creation date')
    )

    def retrieve(self):
        subscription = openpay.Customer.retrieve(
            self.customer.code
        ).subscriptions.retrieve(self.code)
        self.trial_end_date = parse_date(subscription.trial_end_date)
        self.cancel_at_period_end = subscription.cancel_at_period_end
        self.creation_date = parse_datetime(subscription.creation_date)

    def save(self, *args, **kwargs):
        if self.code:
            subscription = openpay.Customer.retrieve(
                self.customer.code
            ).subscriptions.retrieve(self.code)
            subscription.plan_id = self.plan.code
            subscription.trial_end_date = self.trial_end_date.isoformat()
            subscription.card = None
            subscription.card_id = self.card.code
            subscription.cancel_at_period_end = self.cancel_at_period_end
            subscription.save()
        else:
            subscription = openpay.Customer.retrieve(
                self.customer.code
            ).subscriptions.create(
                plan_id=self.plan.code,
                trial_end_date=self.trial_end_date.isoformat()
                if self.trial_end_date else None,
                card_id=self.card.code,
            )
            subscription.cancel_at_period_end = self.cancel_at_period_end
            subscription.save()
            self.code = subscription.id

        self.retrieve()
        super(Subscription, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.code:
            subscription = openpay.Customer.retrive(
                self.customer.code).subscriptions.retrieve(self.code)
            subscription.delete()
        super(Subscription, self).delete(*args, **kwargs)

    def __str__(self):
        return '{plan} | {customer}'.format(
            customer=self.customer,
            plan=self.plan)


class Charge(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=_ug('OpenPay Code')
    )
    description = models.TextField(
        blank=True,
        null=False,
        verbose_name=_ug('Description')
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        blank=False,
        null=False,
        verbose_name=_ug('Amount')
    )
    method = models.CharField(
        max_length=30,
        blank=True,
        null=False,
        verbose_name=_ug('Method')
    )
    # status
    # refund
    # currency
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
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name=_ug('Creation date')
    )
