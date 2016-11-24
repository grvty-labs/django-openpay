from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.dateparse import parse_datetime, parse_date

from decimal import Decimal

from . import openpay, hardcode, ugettext_lazy, exceptions

phone_validator = RegexValidator(
    regex=r'^\d{9,15}$',
    message=ugettext_lazy("The telephone number can only contain digits. "
                          " The maximum number of digits is 15.")
)


class Address(models.Model):
    city = models.TextField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('City')
    )
    state = models.TextField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('State')
    )
    line1 = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Street (Line 1)'),
    )
    line2 = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Street (Line 2)'),
    )
    line3 = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Street (Line 3)'),
    )
    postal_code = models.IntegerField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Postal Code')
    )
    country_code = models.CharField(
        choices=hardcode.address_countrycodes,
        default='MX',
        max_length=5,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Country')
    )

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return []
        return []

    def push(self):
        raise NotImplementedError

    def pull(self):
        raise NotImplementedError

    def retrieve(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    # TODO: From idless_dict

    # Obtained and edited from:
    # https://goo.gl/SqkLbo
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
        verbose_name=ugettext_lazy('OpenPay Code')
    )
    first_name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('First Name'),
    )
    last_name = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Last Name'),
    )
    email = models.EmailField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Email'),
    )
    phone_number = models.CharField(
        validators=[phone_validator],
        max_length=15,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Phone Number'),
    )
    address = models.OneToOneField(
        Address,
        blank=False,
        null=False,
        related_name='customer',
        verbose_name=ugettext_lazy('Address')
    )
    creation_date = models.DateTimeField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Creation date')
    )

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['code', 'creation_date']
        return ['code', 'creation_date']

    def push(self):
        if self.code:
            if not hasattr(self, '_openpay_obj'):
                self.retrieve()
            self._openpay_obj.name = self.first_name
            self._openpay_obj.last_name = self.last_name
            self._openpay_obj.email = self.email
            self._openpay_obj.phone_number = self.phone_number
            self._openpay_obj.address = self.address.to_idless_dict()
            self._openpay_obj.save()

        else:
            self._openpay_obj = openpay.Customer.create(
                name=self.first_name,
                last_name=self.last_name,
                email=self.email,
                phone_number=self.phone_number,
                address=self.address.to_idless_dict(),
            )
            self.code = self._openpay_obj.id
            self.pull()

    def pull(self):
        self.retrieve()
        self.first_name = self._openpay_obj.name
        self.last_name = self._openpay_obj.last_name
        self.email = self._openpay_obj.email
        self.phone_number = self._openpay_obj.phone_number
        self.creation_date = parse_datetime(
            self._openpay_obj.creation_date)

    def retrieve(self):
        if self.code:
            self._openpay_obj = openpay.Customer.retrieve(self.code)
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.code:
            if not hasattr(self, '_openpay_obj'):
                self.retrieve()
            self._openpay_obj.delete()

    @property
    def full_name(self):
        return '{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name)

    def __str__(self):
        return self.full_name


@receiver(pre_save, sender=Customer)
def customer_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    instance.email = instance.email.strip()
    instance.push()


@receiver(post_delete, sender=Customer)
def customer_postdelete(sender, instance, **kwargs):
    instance.remove()


class Card(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('OpenPay code')
    )
    alias = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Alias')
    )
    card_type = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Card type')
    )
    holder = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Holder name')
    )
    number = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Number')
    )
    month = models.CharField(
        max_length=3,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Expiration month')
    )
    year = models.CharField(
        max_length=3,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Expiration year')
    )
    customer = models.ForeignKey(
        Customer,
        blank=False,
        null=False,
        related_name='cards',
        verbose_name=ugettext_lazy('Owner')
    )
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Creation date')
    )

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['code', 'card_type', 'holder', 'number', 'month', 'year',
                    'customer', 'creation_date']
        return ['code', 'card_type', 'holder', 'number', 'month', 'year',
                'customer', 'creation_date']

    @classmethod
    def tokenized_create(cls, customerId, tokenId, deviceId, alias=''):
        card_op = openpay.Card.create(customer=customerId, token_id=tokenId,
                                      device_session_id=deviceId)
        customer = Customer.objects.get(code=customerId)
        # The card addres cannot be consulted
        card = cls(
            code=card_op.id,
            alias=alias,
            card_type=card_op.type,
            holder=card_op.holder_name,
            number=card_op.card_number[-4:],
            month=card_op.expiration_month[-2:],
            year=card_op.expiration_year[-2:],
            creation_date=parse_datetime(
                card_op.creation_date),
            customer=customer
        )
        card._openpay_obj = card_op
        return card.save()

    def push(self):
        raise NotImplementedError

    def pull(self):
        self.retrieve()
        self.card_type = self._openpay_obj.type
        self.holder = self._openpay_obj.holder_name
        self.number = self._openpay_obj.card_number[-4:]
        self.month = self._openpay_obj.expiration_month[-2:]
        self.year = self._openpay_obj.expiration_year[-2:]
        self.creation_date = parse_datetime(
            self._openpay_obj.creation_date)

    def retrieve(self):
        if not self.customer or not self.customer.code:
            raise exceptions.OpenpayNoCustomer

        if self.code:
            self._openpay_obj = openpay.Customer.retrieve(
                self.customer.code
            ).cards.retrieve(
                self.code
            )

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.code:
            if not hasattr(self, '_openpay_obj'):
                self.retrieve()
            self._openpay_obj.delete()

    def __str__(self):
        if self.alias:
            return self.alias
        return '{customer}-{pk}'.format(customer=self.customer, pk=self.pk)


# TODO: Card creation without token
@receiver(pre_save, sender=Card)
def card_presave(sender, instance=None, **kwargs):
    instance.full_clean()


@receiver(post_delete, sender=Card)
def card_postdelete(sender, instance, **kwargs):
    instance.remove()


class Plan(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('OpenPay Code')
    )
    name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Name'),
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Amount')
    )
    retry_times = models.IntegerField(
        default=3,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Number of retries')
    )
    status_after_retry = models.CharField(
        choices=hardcode.plan_statusafter,
        default=hardcode.plan_statusafter_unpaid,
        max_length=15,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('When retries are exhausted')
    )
    trial_days = models.IntegerField(
        default=0,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Trial days')
    )
    repeat_every = models.IntegerField(
        default=1,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Frecuency Number')
    )
    repeat_unit = models.CharField(
        choices=hardcode.plan_repeatunit,
        default=hardcode.plan_repeatunit_month,
        max_length=15,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Frecuency Unit')
    )
    creation_date = models.DateTimeField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Creation date')
    )

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['code', 'amount', 'retry_times', 'status_after_retry',
                    'repeat_every', 'repeat_unit', 'creation_date']
        return ['code', 'creation_date']

    def push(self):
        if self.code:
            if not hasattr(self, '_openpay_obj'):
                self.retrieve()
            self._openpay_obj.name = self.name
            self._openpay_obj.trial_days = self.trial_days
            self._openpay_obj.save()

        else:
            self._openpay_obj = openpay.Plan.create(
                name=self.name,
                amount=str(self.amount),
                status_after_retry=self.status_after_retry,
                retry_times=self.retry_times,
                repeat_unit=self.repeat_unit,
                trial_days=self.trial_days,
                repeat_every=self.repeat_every,
            )
            self.code = self._openpay_obj.id
            self.pull()

    def pull(self):
        self.retrieve()
        self.name = self._openpay_obj.name
        self.amount = Decimal(self._openpay_obj.amount)
        self.status_after_retry = self._openpay_obj.status_after_retry
        self.retry_times = self._openpay_obj.retry_times
        self.repeat_unit = self._openpay_obj.repeat_unit
        self.trial_days = self._openpay_obj.trial_days
        self.repeat_every = self._openpay_obj.repeat_every
        self.creation_date = parse_datetime(
            self._openpay_obj.creation_date)

    def retrieve(self):
        if self.code:
            self._openpay_obj = openpay.Plan.retrieve(self.code)

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.code:
            if not hasattr(self, '_openpay_obj'):
                self.retrieve()
            self._openpay_obj.delete()

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Plan)
def plan_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    instance.push()


@receiver(post_delete, sender=Plan)
def plan_postdelete(sender, instance, **kwargs):
    instance.remove()


class Subscription(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('OpenPay Code')
    )
    customer = models.ForeignKey(
        Customer,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=ugettext_lazy('Customer')
    )
    card = models.ForeignKey(
        Card,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=ugettext_lazy('Card')
    )
    plan = models.ForeignKey(
        Plan,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=ugettext_lazy('Plan')
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Cancel at the end of period')
    )
    trial_end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Trial days')
    )
    creation_date = models.DateTimeField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Creation date')
    )

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['code', 'customer', 'plan', 'creation_date']
        return ['code', 'creation_date']

    def push(self):
        if self.code:
            if not hasattr(self, '_openpay_obj'):
                self.retrieve()
            self._openpay_obj.trial_end_date = \
                self.trial_end_date.isoformat()
            self._openpay_obj.card = None
            self._openpay_obj.card_id = self.card.code
            self._openpay_obj.cancel_at_period_end = \
                self.cancel_at_period_end
            self._openpay_obj.save()

        else:
            if not self.customer or not self.customer.code:
                raise exceptions.OpenpayNoCustomer
            if not self.card or not self.card.code:
                raise exceptions.OpenpayNoCard
            self._openpay_obj = openpay.Customer.retrieve(
                self.customer.code
            ).subscriptions.create(
                plan_id=self.plan.code,
                trial_end_date=self.trial_end_date.isoformat()
                if self.trial_end_date else None,
                card_id=self.card.code,
            )
            if self.cancel_at_period_end:
                self._openpay_obj.cancel_at_period_end = \
                    self.cancel_at_period_end
                self._openpay_obj.save()
            self.code = self._openpay_obj.id
            self.pull()

    def pull(self):
        self.retrieve()
        self.trial_end_date = parse_date(
            self._openpay_obj.trial_end_date)
        self.cancel_at_period_end = \
            self._openpay_obj.cancel_at_period_end
        self.creation_date = parse_datetime(
            self._openpay_obj.creation_date)

    def retrieve(self):
        if not self.customer or not self.customer.code:
            raise exceptions.OpenpayNoCustomer

        if self.code:
            self._openpay_obj = openpay.Customer.retrieve(
                self.customer.code
            ).subscriptions.retrieve(self.code)

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.code:
            if not hasattr(self, '_openpay_obj'):
                self.retrieve()
            self._openpay_obj.delete()

    def __str__(self):
        return '{plan} |> {customer}'.format(
            customer=self.customer,
            plan=self.plan)


@receiver(pre_save, sender=Subscription)
def subscription_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    instance.push()


@receiver(post_delete, sender=Subscription)
def subscription_postdelete(sender, instance, **kwargs):
    instance.remove()


class Charge(models.Model):
    code = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('OpenPay Code')
    )
    description = models.TextField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Description')
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Amount')
    )
    method = models.CharField(
        max_length=30,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Method')
    )
    # status
    # refund
    # currency
    customer = models.ForeignKey(
        Customer,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Customer')
    )
    card = models.ForeignKey(
        Card,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Card')
    )
    plan = models.ForeignKey(
        Plan,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Plan')
    )
    creation_date = models.DateTimeField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Creation date')
    )

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['code', 'description', 'amount', 'method', 'customer',
                    'card', 'plan', 'creation_date']
        return ['code', 'creation_date']
    def push(self):
        raise NotImplementedError

    def pull(self):
        raise NotImplementedError

    def retrieve(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError
