**django-openpay**
==================

Django app for online transactions
----------------------------------

[OpenPay][openpay-page] is an online gateway to execute online
payments using debit/credit cards or bank transferences. OpenPay allows to
create Plans for system memberships, with an autocharge system.

Django-Openpay is a django application (duh!) which integrates two OpenPay
libraries:

*   The Python to manage Plans and Customers directly from django models

*   The JavaScript library to manage online payouts and transactions, without
saving sensitive information in your django application.

Features
--------

1.  Create directly from Django into OpenPay:
    *   Customers
    *   Plans
    *   Subscriptions

2.  Delete directly from Django into OpenPay:
    *   Customers
    *   Plans
    *   Subscriptions
    *   Cards

3.  Create from JSX into OpenPay:
    *   Cards

4.  Reflect through webhooks from OpenPay into Django:
    *   Charges

Installation
------------

To install this package from pip it is required to execute:

`pip install django-openpay`

To use the JSX files, you should have Webpack or Gulp installed to compile the
JSX to ES5 or ES6. But due to my inexperience for including NPM dependencies
in pip packages, you will require to install `react` and `react-dom` by
hand. Although we could have used the Node package of OpenPay and prevent some
manual configuration, we have no idea of how the security is managed inside
the Node package to be used directly from front-end.

To use the JSX file, be sure to include in your HTML head:

    <script type='text/javascript' src='https://code.jquery.com/jquery-3.1.0.min.js'></script>
    <script type='text/javascript' src='https://openpay.s3.amazonaws.com/openpay.v1.min.js'></script>
    <script type='text/javascript' src='https://openpay.s3.amazonaws.com/openpay-data.v1.min.js'></script>

This package requires to have knowledge of your Openpay's public, private and
merchant keys. To do this you just have to put your keys inside the
`settings.py` file of your Django project using the following variables:

*   `OPENPAY_PRIVATE_API_KEY`
*   `OPENPAY_PUBLIC_API_KEY`
*   `OPENPAY_MERCHANT_ID`
*   `OPENPAY_VERIFY_SSL`

TODOs
-----

*   Verify this package is PCI Compliant
*   Webhooks to display Charges
*   Bank Accounts
*   Transferences
*   Fees
*   Payouts
*   Celery to prevent bottlenecks

Versions
--------

*   v0.2
    *   Fixed the aspect of internationalization using `ugettext` and
    `ugettext_lazy`.
    *   Moved the functionality from the `save` in all models to their
    corresponding signal. (In order to prevent errors from the `save`
    overwrite).
    *   New exceptions types added.
    *   The `django-admin` now displays more information in each model's list.
    *   The `testing` folder was included with some simple configurations to
    experiment with this package.
    *   `MANIFEST.in` was updated to prevent `setuptools` from uploading trash.


*   v0.1
    *   Created the initial connections to the Openpay API.
    *   Create directly from Django into OpenPay:
        *   Customers
        *   Plans
        *   Subscriptions
    *   Delete directly from Django into OpenPay:
        *   Customers
        *   Plans
        *   Subscriptions
        *   Cards
    *   Create from JSX into OpenPay:
        *   Cards
    *   Reflect through webhooks from OpenPay into Django:
        *   Charges (Pending tests)

Disclaimer
---------

**django-openpay** does not saves critical information in its django models,
it just saves the tokens to access the information from the OpenPay servers
and allows to modify the information contained inside OpenPay from Django.

**django-openpay** has not been tested for security vulnerabilities and does
not have an SSL certificate preconfiguration, this is the reason behind our
decision to create cards only from front-end.

Owned and developed by
--------

[![StackShare][stack-shield]][stack-tech]

[![GRVTYlabs][logo]](www.grvtylabs.com)

[logo]: https://github.com/grvty-labs/django-openpay/blob/master/logo.png?raw=true "GRVTYlabs"
[stack-shield]: http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat
[stack-tech]: http://stackshare.io/letops/grvtylabs
[openpay-page]: http://www.openpay.mx/en/
