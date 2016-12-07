Milestones
==========

This milestones are merely a map to inform everyone what we are trying to
accomplish and what to expect in future versions.

*   v3.0
    *   **Not released yet**.
    *   This package should have enough security to become **PCI Compliant**
    by its own. Although this doesn't mean we will save Cards in the system,
    we must be able to make sensitive transactions from the back-end.
    *   Use and manage **card points** for Santander, Scotiabank and
    Bancomer. (This are the only ones allowed by Openpay today).

*   v2.0
    *   **Not released yet**.
    *   This version will include the features related to managing
    **Bank Accounts**, **Payouts**, **Charges**, **Fees**, **Transferences**,
    etc.
    *   Improved **security** through out the system, to prevent the usage
    of the system by malicious users or bots. This will require a better
    understanding of how Django's security works, as well as managing the
    anti-fraud system used by Openpay.
    *   Rewrite of the **openpay-python** [library][openpay-git]. This is
    because the last modification of the same library was in 2014, and even
    though that package is really helpful for plain python, it was not improved
    throughout the years. We have the theory that the API used by Openpay was
    developed at the same time as the python and javascript official libraries,
    but only the javascript library has been maintained and improved with the
    new changes to the API. This cripples in a way the python package, which
    can be clearly seen in the API's operations which require the
    `device_session_id` value. Please refer to the created
    [issue][openpay-issue] to know more about the problems detected.


*   v1.0
    *   **Not released yet**.
    *   This version will be considered our **first stable version**. This
    means that the models will not have significant changes made to their
    fields. Although the functionality can be greatly improved or modified.
    *   The **Customer** model will be converted to an abstract model. In order
    to be able to connect it to your model User at will, but this would require
    a CustomUser model. I am searching a better way to do this.
    *   The **Webhooks Feature** will be completely connected and tested with
    the Openpay servers. In this way, we should be able to create Charges from
    Django and/or JavaScript, and be able to see all the recurring charges made
    automatically by the Openpay system. The Verification step of this feature
    should send an email to the developer so he can confirm the webhook inside
    the Openpay system, as well.
    *   Django **Internationalization** will be completed for English and
    quite a great part will be translated to Spanish.
    *   **Celery** will start being used to prevent communication bottlenecks
    with the Openpay API
    *   Populate your database with all the data saved inside your Openpay
    account using the command **openpaysync** by calling it from the
    `manage.py` file.



Owned and developed by
--------

[![StackShare][stack-shield]][stack-tech]


[![GRVTYlabs][logo]](www.grvtylabs.com)

[logo]: https://github.com/grvty-labs/django-openpay/blob/master/logo.png?raw=true "GRVTYlabs"
[stack-shield]: http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat
[stack-tech]: http://stackshare.io/letops/grvtylabs

[openpay-git]: https://github.com/open-pay/openpay-python/
[openpay-issue]: https://github.com/open-pay/openpay-python/issues/3
