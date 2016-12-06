**django-openpay**
==================

Django app for online transactions
----------------------------------

[Openpay][openpay-page] is an online gateway to execute online
payments using debit/credit cards or bank transferences. Openpay allows to
create Plans for system memberships, with an autocharge system.

Django-Openpay is a django application created to wrap the current library of
[Openpay for Python][openpay-git]. Django-Openpay integrates two Openpay
libraries:

*   The Python library to manage Plans, Charges, Subscriptions, Customers and
Cards (partially) directly through django models.

*   The JavaScript library to manage payouts, transfers and cards without
saving sensitive information in your django application. (Giving us the relief
of not having to make our Django system [PCI Compliant][pci-wiki-page])

Features
--------

1.  Create directly from Django into Openpay:
    *   Customers
    *   Plans
    *   Subscriptions
    *   Charges

2.  Delete directly from Django into Openpay:
    *   Customers
    *   Plans
    *   Subscriptions
    *   Cards

3.  Create from JSX into Openpay:
    *   Cards

4.  Reflect updates through webhooks from Openpay into Django:
    *   Charges

5.  Refund or Capture Charges.


Installation
------------

To install this package from pip it is required to execute:

`pip install django-openpay`

This package includes JSX and JS files to be able to use the JavaScript library
without further delay.

To use the JSX files, you should have Webpack or Gulp installed to compile the
JSX to ES5 or ES6. But due to my inexperience for including NPM dependencies
in pip packages, you will require to install `react` and `react-dom` by
hand. Although we could have used the Node package of Openpay and prevent some
manual configuration, we have no idea of how the security is managed inside
the Node package to be used directly from front-end.

To use the JSX file, be sure to include in your HTML head:

    <script type='text/javascript' src='https://code.jquery.com/jquery-3.1.0.min.js'></script>
    <script type='text/javascript' src='https://openpay.s3.amazonaws.com/openpay.v1.min.js'></script>
    <script type='text/javascript' src='https://openpay.s3.amazonaws.com/openpay-data.v1.min.js'></script>

This package requires to have knowledge of your Openpay's public, private and
merchant keys. To do this you just have to put your keys inside the
`settings.py` file of your Django project using the following variables:

```python
OPENPAY_PRIVATE_API_KEY='string'
OPENPAY_PUBLIC_API_KEY='string'
OPENPAY_MERCHANT_ID='string'
OPENPAY_VERIFY_SSL=True  # or False
OPENPAY_DEVICE_ID='string'
OPENPAY_CUSTOMER_MODEL='string'
```

The `AbstractCustomer` model is a model which can be inherited from. This was
done because you may want to make your `User` model the customer, or manage a
team of users as one customer. It is up to you, just remember to use all the
fields described in the abstract, or (in case you want to rename the fields)
set them to `None` and overwrite the `pull` and `push` methods.

In order to be able to use the Webhooks feature, you need to link your Openpay
project to a specific url of your project (which calls the
`'django_openpay.views.webhook'` view), inside the Openpay system. Remember
that this package tries to make everything as secure as possible and, for that
same reason, you need to activate the BasicAuth option in the Openpay system
when you are creating the webhook, using a username and a password (it must NOT
be a Django user). That same username and password will be added directly in
your django settings file inside the the variable `OPENPAY_BASICAUTH_USERS`.
This variable should be used like:

```python
OPENPAY_BASICAUTH_USERS = {
  "username": "password"
}
```


Testing
-------

[![Run in Postman][postman-svg]][postman-pkg]



Other docs
----------

*   [Changelog][changelog]
*   [Milestones][milestones]
*   [Webhook log][webhook-log]
*   [LICENSE][license]



Disclaimer
---------

**django-openpay** doesn't save critical information in its django models.
All the information that can be saved inside the models without needing to be
PCI Compliant is being saved. The most sensitive information is being accessed
from the Openpay servers by using access tokens.

**django-openpay** has not been tested for security vulnerabilities yet and does
not have an SSL certificate preconfiguration, this is the reason behind our
decision to be able to create cards only in the front-end.



Owned and developed by
--------

[![StackShare][stack-shield]][stack-tech]


[![GRVTYlabs][logo]](www.grvtylabs.com)

[logo]: https://github.com/grvty-labs/django-openpay/blob/master/logo.png?raw=true "GRVTYlabs"
[stack-shield]: http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat
[stack-tech]: http://stackshare.io/letops/grvtylabs

[openpay-git]: https://github.com/open-pay/openpay-python/
[openpay-page]: http://www.openpay.mx/en/
[pci-wiki-page]: https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard
[postman-svg]: https://run.pstmn.io/button.svg
[postman-pkg]: https://app.getpostman.com/run-collection/929685fa23a4a51f1a2f

[changelog]: https://github.com/grvty-labs/django-openpay/blob/master/docs/Changelog.md
[milestones]: https://github.com/grvty-labs/django-openpay/blob/master/docs/Milestones.md
[webhook-log]: https://github.com/grvty-labs/django-openpay/blob/master/docs/log/webhook.md
[license]: https://github.com/grvty-labs/django-openpay/blob/master/LICENSE
