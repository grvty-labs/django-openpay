from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.dateparse import parse_datetime, parse_date

from decimal import Decimal
from jsonfield import JSONField

from . import openpay, hardcode, ugettext_lazy, exceptions
from .decorators import skippable


phone_validator = RegexValidator(
    regex=r'^\d{9,15}$',
    message=ugettext_lazy("The telephone number can only contain digits. "
                          " The maximum number of digits is 15.")
)

CustomerModel = settings.OPENPAY_CUSTOMER_MODEL


class AbstractOpenpayBase(models.Model):
    openpay_id = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('OpenPay ID'))
    # Not using auto_now_add because this is not the date from Django, but
    # the one from Openpay
    creation_date = models.DateTimeField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Creation date'))

    class Meta:
        abstract = True

    @classmethod
    def get_readonly_fields(self, instance=None):
        raise NotImplementedError

    def push(self):
        raise NotImplementedError

    def pull(self, commit=False):
        raise NotImplementedError

    def retrieve(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError


class Address(models.Model):
    city = models.TextField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('City'))
    state = models.TextField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('State'))
    line1 = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Street (Line 1)'))
    line2 = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Street (Line 2)'))
    line3 = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Street (Line 3)'))
    postal_code = models.IntegerField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Postal Code'))
    country_code = models.CharField(
        choices=hardcode.address_countrycodes,
        default='MX',
        max_length=5,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Country'))
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=ugettext_lazy('Creation date'))

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['creation_date']
        return ['creation_date']

    # Obtained and edited from:
    # https://goo.gl/SqkLbo
    @property
    def json_dict(self):
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
            elif f.name not in ['id', 'creation_date']:
                data[f.name] = f.value_from_object(self)
        return data


class AbstractCustomer(AbstractOpenpayBase):
    first_name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('First Name'))
    last_name = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Last Name'))
    email = models.EmailField(
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Email'))
    phone_number = models.CharField(
        validators=[phone_validator],
        max_length=15,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Phone Number'))
    address = models.OneToOneField(
        Address,
        blank=True,
        null=True,
        related_name='customer',
        verbose_name=ugettext_lazy('Address'))

    class Meta:
        abstract = True

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['openpay_id', 'creation_date']
        return ['openpay_id', 'creation_date']

    def push(self):
        if self.openpay_id:
            if not hasattr(self, '_openpay'):
                self.retrieve()
            self._openpay.name = self.first_name
            self._openpay.last_name = self.last_name if \
                self.last_name else None
            self._openpay.email = self.email
            self._openpay.phone_number = self.phone_number if \
                self.phone_number else None
            self._openpay.address = self.address.json_dict if \
                self.address else None
            self._openpay.save()

        else:
            self._openpay = openpay.Customer.create(
                name=self.first_name,
                last_name=self.last_name if self.last_name else None,
                email=self.email,
                phone_number=self.phone_number if self.phone_number else None,
                address=self.address.json_dict if self.address else None)
            self.openpay_id = self._openpay.id

    def pull(self, commit=False):
        self.retrieve()
        self.first_name = self._openpay.name
        self.last_name = self._openpay.last_name
        self.email = self._openpay.email
        self.phone_number = self._openpay.phone_number
        self.creation_date = parse_datetime(
            self._openpay.creation_date)
        if commit:
            self.save()

    def retrieve(self):
        if self.openpay_id:
            self._openpay = openpay.Customer.retrieve(self.openpay_id)
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.openpay_id:
            if not hasattr(self, '_openpay'):
                self.retrieve()
            self._openpay.delete()

    @property
    def full_name(self):
        return '{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name)

    def __str__(self):
        return self.full_name


@receiver(pre_save, sender=CustomerModel)
@skippable
def customer_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    instance.email = instance.email.strip()
    instance.push()


@receiver(post_delete, sender=CustomerModel)
def customer_postdelete(sender, instance, **kwargs):
    instance.remove()


class Card(AbstractOpenpayBase):
    alias = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Alias'))
    card_type = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Card type'))
    holder = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Holder name'))
    number = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Number'))
    month = models.CharField(
        max_length=3,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Expiration month'))
    year = models.CharField(
        max_length=3,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Expiration year'))
    customer = models.ForeignKey(
        CustomerModel,
        blank=False,
        null=False,
        related_name='cards',
        verbose_name=ugettext_lazy('Owner'))

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['openpay_id', 'card_type', 'holder', 'number', 'month',
                    'year', 'customer', 'creation_date']
        return ['openpay_id', 'card_type', 'holder', 'number', 'month', 'year',
                'customer', 'creation_date']

    @classmethod
    def tokenized_create(cls, customerId, tokenId, deviceId, alias=''):
        card_op = openpay.Card.create(customer=customerId, token_id=tokenId,
                                      device_session_id=deviceId)
        customer = Customer.objects.get(openpay_id=customerId)
        # The card addres cannot be consulted
        card = cls(
            openpay_id=card_op.id,
            alias=alias,
            card_type=card_op.type,
            holder=card_op.holder_name,
            number=card_op.card_number[-4:],
            month=card_op.expiration_month[-2:],
            year=card_op.expiration_year[-2:],
            creation_date=parse_datetime(
                card_op.creation_date),
            customer=customer)
        card._openpay = card_op
        return card.save()

    def push(self):
        raise NotImplementedError

    def pull(self, commit=False):
        self.retrieve()
        self.card_type = self._openpay.type
        self.holder = self._openpay.holder_name
        self.number = self._openpay.card_number[-4:]
        self.month = self._openpay.expiration_month[-2:]
        self.year = self._openpay.expiration_year[-2:]
        self.creation_date = parse_datetime(
            self._openpay.creation_date)
        if commit:
            self.save()

    def retrieve(self):
        if not self.customer or not self.customer.openpay_id:
            raise exceptions.OpenpayNoCustomer

        if self.openpay_id:
            self._openpay = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).cards.retrieve(
                self.openpay_id
            )

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.openpay_id:
            if not hasattr(self, '_openpay'):
                self.retrieve()
            self._openpay.delete()

    def __str__(self):
        if self.alias:
            return self.alias
        return '{customer}-{pk}'.format(customer=self.customer, pk=self.pk)


# TODO: Card creation without token
@receiver(pre_save, sender=Card)
@skippable
def card_presave(sender, instance=None, **kwargs):
    instance.full_clean()


@receiver(post_delete, sender=Card)
def card_postdelete(sender, instance, **kwargs):
    instance.remove()


class Plan(AbstractOpenpayBase):
    name = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Name'))
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Amount'))
    retry_times = models.IntegerField(
        default=3,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Number of retries'))
    excerpt = models.CharField(
        max_length=250,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Excerpt'))
    description = models.TextField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Description'))
    benefits = JSONField(
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Benefits (JSON)'))
    # status = models.CharField(
    #     choices=hardcode.plan_status,
    #     default=hardcode.plan_status_active,
    #     max_length=15,
    #     blank=True,
    #     null=False,
    #     verbose_name=ugettext_lazy('Status'))
    status_after_retry = models.CharField(
        choices=hardcode.plan_statusafter,
        default=hardcode.plan_statusafter_unpaid,
        max_length=15,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('When retries are exhausted'))
    trial_days = models.IntegerField(
        default=0,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Trial days'))
    repeat_every = models.IntegerField(
        default=1,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Frecuency Number'))
    repeat_unit = models.CharField(
        choices=hardcode.plan_repeatunit,
        default=hardcode.plan_repeatunit_month,
        max_length=15,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Frecuency Unit'))

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['openpay_id', 'amount', 'retry_times',
                    'status_after_retry', 'repeat_every', 'repeat_unit',
                    'creation_date']
        return ['openpay_id', 'creation_date']

    def push(self):
        if self.openpay_id:
            if not hasattr(self, '_openpay'):
                self.retrieve()
            self._openpay.name = self.name
            self._openpay.trial_days = self.trial_days
            self._openpay.save()

        else:
            self._openpay = openpay.Plan.create(
                name=self.name,
                amount=str(self.amount),
                status_after_retry=self.status_after_retry,
                retry_times=self.retry_times,
                repeat_unit=self.repeat_unit,
                trial_days=self.trial_days,
                repeat_every=self.repeat_every)
            self.openpay_id = self._openpay.id

    def pull(self, commit=False):
        self.retrieve()
        self.name = self._openpay.name
        self.amount = Decimal(self._openpay.amount)
        self.status_after_retry = self._openpay.status_after_retry
        self.retry_times = self._openpay.retry_times
        self.repeat_unit = self._openpay.repeat_unit
        self.trial_days = self._openpay.trial_days
        self.repeat_every = self._openpay.repeat_every
        self.creation_date = parse_datetime(
            self._openpay.creation_date)
        if commit:
            self.save()

    def retrieve(self):
        if self.openpay_id:
            self._openpay = openpay.Plan.retrieve(self.openpay_id)

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.openpay_id:
            if not hasattr(self, '_openpay'):
                self.retrieve()
            self._openpay.delete()

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Plan)
@skippable
def plan_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    instance.push()


@receiver(post_delete, sender=Plan)
def plan_postdelete(sender, instance, **kwargs):
    instance.remove()


class Subscription(AbstractOpenpayBase):
    customer = models.ForeignKey(
        CustomerModel,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=ugettext_lazy('Customer'))
    card = models.ForeignKey(
        Card,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=ugettext_lazy('Card'))
    plan = models.ForeignKey(
        Plan,
        blank=False,
        null=False,
        related_name='subscriptions',
        verbose_name=ugettext_lazy('Plan'))
    cancel_at_period_end = models.BooleanField(
        default=False,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Cancel at the end of period'))
    charge_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Charge date'))
    period_end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Period end date'))
    status = models.CharField(
        default=hardcode.subscription_status_trial,
        choices=hardcode.subscription_status,
        max_length=10,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Status'))
    current_period_number = models.IntegerField(
        default=0,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Trial days'))
    trial_end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Trial end date'))

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['openpay_id', 'customer', 'plan', 'charge_date',
                    'period_end_date', 'status', 'current_period_number',
                    'creation_date']
        return ['openpay_id', 'charge_date', 'period_end_date', 'status',
                'current_period_number', 'creation_date']

    def cancel_subscription(self):
        self.remove()

    def push(self):
        if self.openpay_id:
            if not hasattr(self, '_openpay'):
                self.retrieve()
            self._openpay.trial_end_date = \
                self.trial_end_date.isoformat()
            self._openpay.card = None
            self._openpay.card_id = self.card.openpay_id
            self._openpay.cancel_at_period_end = \
                self.cancel_at_period_end
            self._openpay.save()

        else:
            if not self.customer or not self.customer.openpay_id:
                raise exceptions.OpenpayNoCustomer
            if not self.card or not self.card.openpay_id:
                raise exceptions.OpenpayNoCard
            self._openpay = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).subscriptions.create(
                plan_id=self.plan.openpay_id,
                trial_end_date=self.trial_end_date.isoformat()
                if self.trial_end_date else None,
                card_id=self.card.openpay_id)
            if self.cancel_at_period_end:
                self._openpay.cancel_at_period_end = \
                    self.cancel_at_period_end
                self._openpay.save()
            self.openpay_id = self._openpay.id

    def pull(self, commit=False):
        self.retrieve()
        self.cancel_at_period_end = \
            self._openpay.cancel_at_period_end
        self.charge_date = parse_date(
            self._openpay.charge_date)
        self.period_end_date = parse_date(
            self._openpay.period_end_date)
        self.status = self._openpay.status
        self.current_period_number = self._openpay.current_period_number
        self.trial_end_date = parse_date(
            self._openpay.trial_end_date)
        self.creation_date = parse_datetime(
            self._openpay.creation_date)
        if commit:
            self.save()

    def retrieve(self):
        if not self.customer or not self.customer.openpay_id:
            raise exceptions.OpenpayNoCustomer

        if self.openpay_id:
            self._openpay = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).subscriptions.retrieve(self.openpay_id)

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        if self.openpay_id:
            if not hasattr(self, '_openpay'):
                self.retrieve()
            self._openpay.delete()

    def __str__(self):
        return '{plan} |> {customer}'.format(
            customer=self.customer,
            plan=self.plan)


@receiver(pre_save, sender=Subscription)
@skippable
def subscription_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    if instance.card.customer_id != instance.customer_id:
        raise exceptions.OpenpayNotUserCard
    instance.push()


@receiver(post_delete, sender=Subscription)
def subscription_postdelete(sender, instance, **kwargs):
    instance.remove()


class AbstractTransaction(AbstractOpenpayBase):
    authorization = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Authorization'))
    transaction_type = models.CharField(
        default=hardcode.transaction_ttype_charge,
        choices=hardcode.transaction_ttype,
        max_length=10,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Transaction Type'))
    operation_type = models.CharField(
        default=hardcode.transaction_otype_in,
        choices=hardcode.transaction_otype,
        max_length=4,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Operation Type'))
    method = models.CharField(
        default=hardcode.transaction_method_card,
        choices=hardcode.transaction_method,
        max_length=10,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Method'))
    order_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Order ID'))
    status = models.CharField(
        default=hardcode.transaction_status_inprogress,
        choices=hardcode.transaction_status,
        max_length=14,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Status'))
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=20,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Amount'))
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Description'))
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Error Message'))
    customer = models.ForeignKey(
        CustomerModel,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Customer'))
    currency = models.CharField(
        default=hardcode.transaction_currency_mxn,
        choices=hardcode.transaction_currency,
        max_length=8,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Currency'))
    # TODO: bank_account
    card = models.ForeignKey(
        Card,
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Card'))
    # TODO: card_points
    operation_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Operation date'))

    class Meta:
        abstract = True

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['openpay_id', 'authorization', 'transaction_type',
                    'operation_type', 'method', 'order_id', 'status', 'amount',
                    'description', 'error_message', 'customer', 'currency',
                    'card', 'operation_date', 'creation_date', ]
            # bank_account, card_points
        return ['openpay_id', 'authorization', 'transaction_type',
                'operation_type', 'status', 'error_message', 'operation_date',
                'creation_date', ]


class Charge(AbstractTransaction):
    conciliated = models.BooleanField(
        default=True,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Conciliated'))

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['conciliated', ] + super().get_readonly_fields(instance)
        return ['conciliated', ] + super().get_readonly_fields(instance)

    def capture_charge(self):  # FIXME: Openpay has an error with this, not us.
        if not self.openpay_id:
            raise exceptions.OpenpayObjectDoesNotExist
        if self.method != hardcode.transaction_method_card:
            raise exceptions.OpenpayNoCard

        if not hasattr(self, '_openpay'):
            self.retrieve()
        self._openpay.capture()

    def refund_charge(self):  # FIXME: Openpay has an error with this, not us.
        if not self.openpay_id:
            raise exceptions.OpenpayObjectDoesNotExist
        if self.method != hardcode.transaction_method_card:
            raise exceptions.OpenpayNoCard

        if not hasattr(self, '_openpay'):
            self.retrieve()
        self._openpay.refund()

    def push(self):
        if not self.openpay_id:
            if not self.customer or not self.customer.openpay_id:
                raise exceptions.OpenpayNoCustomer
            if not self.card or not self.card.openpay_id:
                raise exceptions.OpenpayNoCard
            self._openpay = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).charges.create(
                source_id=self.card.openpay_id,
                method=self.method,
                amount=str(self.amount),
                currency=self.currency,
                description=self.description,
                device_session_id=openpay.device_id,
                capture=True)
            self.openpay_id = self._openpay.id

    def pull(self, commit=False):
        # TODO: Pull Customer and Card
        self.retrieve()
        self.authorization = self._openpay.authorization
        self.operation_type = self._openpay.operation_type
        self.transaction_type = self._openpay.transaction_type
        self.status = self._openpay.status
        self.conciliated = self._openpay.conciliated
        self.operation_date = parse_datetime(
            self._openpay.operation_date)
        self.description = self._openpay.description
        self.error_message = self._openpay.error_message
        self.order_id = self._openpay.order_id
        self.amount = Decimal(self._openpay.amount)
        self.method = self._openpay.method
        self.currency = self._openpay.currency
        self.creation_date = parse_datetime(
            self._openpay.creation_date)
        if commit:
            self.save()

    def retrieve(self):
        if not self.customer or not self.customer.openpay_id:
            raise exceptions.OpenpayNoCustomer

        if self.openpay_id:
            self._openpay = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).charges.retrieve(self.openpay_id)

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def remove(self):
        raise NotImplementedError

    def __str__(self):
        return self.openpay_id


@receiver(pre_save, sender=Charge)
@skippable
def charge_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    if instance.card.customer_id != instance.customer_id:
        raise exceptions.OpenpayNotUserCard
    instance.push()


# This WILL FAIL. And that is the point: to prevent the deletion of charges
# @receiver(pre_delete, sender=Charge)
# def charge_predelete(sender, instance, **kwargs):
#     instance.remove()


class Refund(AbstractTransaction):
    charge = models.OneToOneField(
        Charge,
        blank=False,
        null=False,
        related_name='refund',
        verbose_name=ugettext_lazy('Charge'))
    conciliated = models.BooleanField(
        default=True,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Conciliated'))

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['charge', 'conciliated', ] + \
                super().get_readonly_fields(instance)
        return ['charge', 'conciliated', ] + \
            super().get_readonly_fields(instance)

    def __str__(self):
        return self.openpay_id
