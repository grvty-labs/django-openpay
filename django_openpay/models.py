from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.utils.dateparse import parse_datetime, parse_date

from decimal import Decimal
from jsonfield import JSONField

from . import openpay, hardcode, ugettext_lazy, exceptions, ungettext_lazy
from .decorators import skippable
from .utils import get_customer_model


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

    @property
    def op_dismissable(self):
        if self.openpay_id:
            return True
        return False

    def op_commit(self):
        # Save the changes in the object directly to the openpay servers
        raise NotImplementedError

    def op_refresh(self, save=False):
        # Call the op_load, and op_fill always. This function is designed to
        # maintain the object updated with what is in the openpay server.
        self.op_load()
        self.op_fill()
        if save:
            self.save()

    def op_load(self):
        # Pull the Openpay data, always
        raise NotImplementedError

    def op_fill(self):
        # Only update the object's fields with the openpay data.
        # If the Openpay data has not been loaded, call op_load.
        raise NotImplementedError

    def op_dismiss(self, save=False):
        # Execute the removal of the openpay object (in the openpay server),
        # this same removal could be a logical or physical destruction, but the
        # way to call it is the same.
        if self.op_dismissable:
            if not hasattr(self, '_op_'):
                self.op_load()
            self._op_.delete()

            if save:
                self.skip_signal = True
                self.save()


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


# class Customer(AbstractOpenpayBase):
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

    def op_cards(self):
        if self.openpay_id:
            if not hasattr(self, '_op_'):
                self.op_load()
            return self._op_.cards.all()
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def op_subscriptions(self):
        if self.openpay_id:
            if not hasattr(self, '_op_'):
                self.op_load()
            return self._op_.subscriptions.all()
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def op_commit(self):
        if self.openpay_id:
            if not hasattr(self, '_op_'):
                self.op_load()
            self._op_.name = self.first_name
            self._op_.last_name = self.last_name if \
                self.last_name else None
            self._op_.email = self.email
            self._op_.phone_number = self.phone_number if \
                self.phone_number else None
            self._op_.address = self.address.json_dict if \
                self.address else None
            self._op_.save()

        else:
            self._op_ = openpay.Customer.create(
                name=self.first_name,
                last_name=self.last_name if self.last_name else None,
                email=self.email,
                phone_number=self.phone_number if self.phone_number else None,
                address=self.address.json_dict if self.address else None)
            self.openpay_id = self._op_.id
        self.op_fill()
        # We have a pre_save signal, so we dont need to save it manually

    def op_load(self):
        if self.openpay_id:
            self._op_ = openpay.Customer.retrieve(self.openpay_id)
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def op_fill(self):
        if not hasattr(self, '_op_'):
            self.op_load()
        self.first_name = self._op_.name
        self.last_name = self._op_.last_name
        self.email = self._op_.email
        self.phone_number = self._op_.phone_number
        self.creation_date = parse_datetime(
            self._op_.creation_date)

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
    instance.op_commit()


@receiver(pre_delete, sender=CustomerModel)
@skippable
def customer_postdelete(sender, instance, **kwargs):
    instance.op_dismiss()


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
    bank_name = models.CharField(
        default='',
        max_length=30,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Bank name'))
    brand = models.CharField(
        default=hardcode.card_brands_unknown,
        choices=hardcode.card_brands,
        max_length=20,
        blank=False,
        null=False,
        verbose_name=ugettext_lazy('Brand'))
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
                    'bank_name', 'brand', 'year', 'customer', 'creation_date']
        return ['openpay_id', 'card_type', 'holder', 'number', 'month', 'year',
                'bank_name', 'brand', 'customer', 'creation_date']

    @classmethod
    def create_with_token(cls, customerId, tokenId, deviceId, alias=''):
        card_op = openpay.Card.create(
            customer=customerId, token_id=tokenId, device_session_id=deviceId)
        customer = get_customer_model().objects.get(openpay_id=customerId)
        # The card addres cannot be consulted
        card = cls(
            openpay_id=card_op.id,
            alias=alias,
            customer=customer)
        card._op_ = card_op
        card.op_fill()
        card.save()
        return card

    def op_commit(self):
        raise NotImplementedError

    def op_load(self):
        if not self.customer or not self.customer.openpay_id:
            raise exceptions.OpenpayNoCustomer

        if self.openpay_id:
            self._op_ = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).cards.retrieve(
                self.openpay_id
            )

        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def op_fill(self):
        if not hasattr(self, '_op_'):
            self.op_load()
        self.card_type = self._op_.type
        self.holder = self._op_.holder_name
        self.number = self._op_.card_number[-4:]
        self.bank_name = self._op_.bank_name
        self.brand = self._op_.brand
        self.month = self._op_.expiration_month[-2:]
        self.year = self._op_.expiration_year[-2:]
        self.creation_date = parse_datetime(
            self._op_.creation_date)

    def __str__(self):
        if self.alias:
            return self.alias
        return '{customer}-{pk}'.format(customer=self.customer, pk=self.pk)


@receiver(pre_save, sender=Card)
@skippable
def card_presave(sender, instance=None, **kwargs):
    instance.full_clean()


@receiver(post_delete, sender=Card)
@skippable
def card_postdelete(sender, instance, **kwargs):
    instance.op_dismiss()


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
    currency = models.CharField(
        default=hardcode.plan_currency_mxn,
        choices=hardcode.plan_currency,
        max_length=8,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Currency'))
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
        default=dict(),
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Benefits (as JSON)'))
    status = models.CharField(
        choices=hardcode.plan_status,
        default=hardcode.plan_status_active,
        max_length=9,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Status'))
    status_after_retry = models.CharField(
        choices=hardcode.plan_statusafter,
        default=hardcode.plan_statusafter_unpaid,
        max_length=11,
        blank=True,
        null=False,
        verbose_name=ugettext_lazy('Status when retries are exhausted'))
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

    @property
    def repeat_verbose(self):
        return ungettext_lazy(
            '%(repeat_unit)s',
            '%(repeat_every)d %(repeat_unit)s',
            self.repeat_every) % {
            'repeat_every': self.repeat_every,
            'repeat_unit': self.get_repeat_unit_display(),
        }

    @classmethod
    def get_readonly_fields(self, instance=None):
        if instance:
            return ['openpay_id', 'amount', 'currency', 'retry_times',
                    'status_after_retry', 'repeat_every', 'repeat_unit',
                    'creation_date']
        return ['openpay_id', 'creation_date']

    def op_commit(self):
        if self.openpay_id:
            if not hasattr(self, '_op_'):
                self.op_load()
            self._op_.name = self.name
            self._op_.trial_days = self.trial_days
            self._op_.save()

        else:
            self._op_ = openpay.Plan.create(
                name=self.name,
                amount=str(self.amount),
                currency=self.currency,
                status_after_retry=self.status_after_retry,
                retry_times=self.retry_times,
                repeat_unit=self.repeat_unit,
                trial_days=self.trial_days,
                repeat_every=self.repeat_every)
            self.openpay_id = self._op_.id
        self.op_fill()

    def op_load(self):
        if self.openpay_id:
            self._op_ = openpay.Plan.retrieve(self.openpay_id)
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def op_fill(self):
        if not hasattr(self, '_op_'):
            self.op_load()
        self.name = self._op_.name
        self.amount = Decimal(self._op_.amount)
        self.status_after_retry = self._op_.status_after_retry
        self.retry_times = self._op_.retry_times
        self.repeat_unit = self._op_.repeat_unit
        self.trial_days = self._op_.trial_days
        self.repeat_every = self._op_.repeat_every
        self.creation_date = parse_datetime(
            self._op_.creation_date)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Plan)
@skippable
def plan_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    instance.op_commit()


@receiver(post_delete, sender=Plan)
@skippable
def plan_postdelete(sender, instance, **kwargs):
    instance.op_dismiss()


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
    latest_charge_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Previous charge date'))
    charge_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=ugettext_lazy('Next charge date'))
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
                    'latest_charge_date', 'period_end_date', 'status',
                    'current_period_number', 'creation_date']
        return ['openpay_id', 'charge_date', 'period_end_date', 'status',
                'latest_charge_date', 'current_period_number', 'creation_date']

    @property
    def op_dismissable(self):
        if self.openpay_id and \
                self.status != hardcode.subscription_status_cancelled:
            return True
        return False

    def op_commit(self):
        if self.openpay_id:
            if not hasattr(self, '_op_'):
                self.op_load()
            self._op_.trial_end_date = \
                self.trial_end_date.isoformat()
            self._op_.card = None
            self._op_.card_id = self.card.openpay_id
            self._op_.cancel_at_period_end = \
                self.cancel_at_period_end
            self._op_.save()

        else:
            if not self.customer or not self.customer.openpay_id:
                raise exceptions.OpenpayNoCustomer
            if not self.card or not self.card.openpay_id:
                raise exceptions.OpenpayNoCard
            self._op_ = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).subscriptions.create(
                plan_id=self.plan.openpay_id,
                trial_end_date=self.trial_end_date.isoformat()
                if self.trial_end_date else None,
                card_id=self.card.openpay_id)
            self.openpay_id = self._op_.id
            if self.cancel_at_period_end:
                self._op_.cancel_at_period_end = \
                    self.cancel_at_period_end
                self._op_.save()
        self.op_fill()

    def op_load(self):
        if not self.customer or not self.customer.openpay_id:
            raise exceptions.OpenpayNoCustomer

        if self.openpay_id:
            self._op_ = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).subscriptions.retrieve(self.openpay_id)
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def op_fill(self):
        if not hasattr(self, '_op_'):
            self.op_load()
        self.cancel_at_period_end = \
            self._op_.cancel_at_period_end
        new_charge_date = parse_date(
            self._op_.charge_date)
        self.latest_charge_date = self.charge_date if \
            self.charge_date != new_charge_date else \
            self.latest_charge_date
        self.charge_date = new_charge_date
        self.period_end_date = parse_date(
            self._op_.period_end_date)
        self.status = self._op_.status
        self.current_period_number = self._op_.current_period_number
        self.trial_end_date = parse_date(
            self._op_.trial_end_date)
        self.creation_date = parse_datetime(
            self._op_.creation_date)

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
    instance.op_commit()


@receiver(post_delete, sender=Subscription)
@skippable
def subscription_postdelete(sender, instance, **kwargs):
    instance.op_dismiss()


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
    subscription = models.ForeignKey(
        Subscription,
        blank=True,
        null=True,
        related_name='charges',
        verbose_name=ugettext_lazy('Subscription'))
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

    def op_capture(self):
        if not self.openpay_id:
            raise exceptions.OpenpayObjectDoesNotExist
        if self.method != hardcode.transaction_method_card:
            raise exceptions.OpenpayNoCard

        if not hasattr(self, '_op_'):
            self.op_load()
        self._op_.capture()

    def op_refund(self, amount=None):
        if not self.openpay_id:
            raise exceptions.OpenpayObjectDoesNotExist
        if self.method != hardcode.transaction_method_card:
            raise exceptions.OpenpayNoCard

        if not hasattr(self, '_op_'):
            self.op_load()
        self._op_.refund(amount) if amount else self._op_.refund()

    def op_commit(self):
        if not self.openpay_id:
            if not self.customer or not self.customer.openpay_id:
                raise exceptions.OpenpayNoCustomer
            if not self.card or not self.card.openpay_id:
                raise exceptions.OpenpayNoCard
            self._op_ = openpay.Customer.retrieve(
                self.customer.openpay_id
            ).charges.create(
                source_id=self.card.openpay_id,
                method=self.method,
                amount=str(self.amount),
                currency=self.currency,
                description=self.description,
                device_session_id=openpay.device_id,
                capture=True)
            self.openpay_id = self._op_.id
        self.op_fill()

    def op_load(self):
        if self.openpay_id:
            if self.customer and self.customer.openpay_id:
                try:
                    self._op_ = openpay.Customer.retrieve(
                        self.customer.openpay_id
                    ).charges.retrieve(self.openpay_id)
                except openpay.error.InvalidRequestError:
                    self._op_ = openpay.Charge.retrieve_as_merchant(
                        self.openpay_id)
            else:
                self._op_ = openpay.Charge.retrieve_as_merchant(
                    self.openpay_id)
        else:
            raise exceptions.OpenpayObjectDoesNotExist

    def op_fill(self):
        if not hasattr(self, '_op_'):
            self.op_load()
        self.authorization = self._op_.authorization
        self.operation_type = self._op_.operation_type
        self.transaction_type = self._op_.transaction_type
        self.status = self._op_.status
        self.conciliated = self._op_.conciliated
        self.operation_date = parse_datetime(
            self._op_.operation_date)
        self.description = self._op_.description
        self.error_message = self._op_.error_message
        self.order_id = self._op_.order_id
        self.amount = Decimal(self._op_.amount)
        self.method = self._op_.method
        self.currency = self._op_.currency
        self.creation_date = parse_datetime(
            self._op_.creation_date)
        if hasattr(self._op_, 'subscription_id'):
            self.subscription = Subscription.objects.get(
                openpay_id=self._op_.subscription_id)
        if hasattr(self._op_, 'customer_id'):
            self.customer = get_customer_model().objects.get(
                openpay_id=self._op_.customer_id)
        if hasattr(self._op_, 'card'):
            self.card = Card.objects.get(
                openpay_id=self._op_.card.id)
            if not self.customer and hasattr(self._op_.card, 'customer_id'):
                self.customer = get_customer_model().objects.get(
                    openpay_id=self._op_.card.customer_id)

    def op_dismiss(self):
        raise NotImplementedError

    def __str__(self):
        return self.openpay_id


@receiver(pre_save, sender=Charge)
@skippable
def charge_presave(sender, instance=None, **kwargs):
    instance.full_clean()
    if instance.card.customer_id != instance.customer_id:
        raise exceptions.OpenpayNotUserCard
    instance.op_commit()


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
