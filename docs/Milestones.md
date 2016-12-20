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


Owned and developed by
--------

[![StackShare][stack-shield]][stack-tech]


[![GRVTYlabs][logo]](www.grvtylabs.com)

[logo]: https://github.com/grvty-labs/django-openpay/blob/master/logo.png?raw=true "GRVTYlabs"
[stack-shield]: http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat
[stack-tech]: http://stackshare.io/letops/grvtylabs

[openpay-git]: https://github.com/open-pay/openpay-python/
[openpay-issue]: https://github.com/open-pay/openpay-python/issues/3
