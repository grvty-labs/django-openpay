from . import ugettext


class DjangoOpenpayError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class OpenpayObjectDoesNotExist(DjangoOpenpayError):
    def __init__(self):
        super(OpenpayObjectDoesNotExist, self).__init__(
            ugettext("This object's code does not exists inside the"
                     " OpenPay API.")
        )


class OpenpayNoCustomer(DjangoOpenpayError):
    def __init__(self):
        super(OpenpayNoCustomer, self).__init__(
            ugettext("This object does not have a related customer code and "
                     "cannot be saved in the OpenPay API.")
        )


class OpenpayNoCard(DjangoOpenpayError):
    def __init__(self):
        super(OpenpayNoCard, self).__init__(
            ugettext("This object does not have a related card code and "
                     "cannot be saved in the OpenPay API.")
        )


class OpenpayNotUserCard(DjangoOpenpayError):
    def __init__(self):
        super(OpenpayNotUserCard, self).__init__(
            ugettext("This Card does not belong to this Customer.")
        )
