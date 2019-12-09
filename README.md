**django-openpay**
==================

Important Notice
----------------

Save yourself and don't use Openpay. It is under your own risk to use Openpay, but this project has been deprecated for us (if you want to risk it and maintain this project, please let us know and we will transfer the project).

I have been trying to get a lot of things fixed, but Openpay's documentation is still incomplete, badly written and there are several issues on things that are out of what this library can control (and apparently even the Openpay team). There are 3 main reasons we have stopped working on this project:

1. Openpay has an antifraud system, which blocks certain cards and bank accounts when "something" happens (they say it is related to buying more than 7 times in 15 days). Openpay's support cannot actually tell you why it has happened, but this occurs with clients that have been using the system for a couple of months or a couple minutes. You can request an update to the antifraud policies for your account, so your users stop being blocked, but we have been requesting this change for over a year with no success (for a client of ours who is using this library).
2. The API documentation doesn't let you know a lot of things, (e.g. when the API doesn't have the info for a specific field sometimes it won't return the field or return it with `null`). We have been requesting changes and we have been invited to their offices to talk about the pains of the documentation, but that was 2 years ago and nothing has changed.
3. Openpay claims you could build a marketplace system with split-payment, there is nothing written down on how to achieve this but the validation team won't approve an application trying to sort this out because it "is not the right way to do it". If you ask that same validation team what they are looking for or any help to sort it out they will just give you the same API documentation from their website.
4. The webhooks are badly implemented, this is because sometimes the webhooks will be triggered twice (which will give you a "unique" constraint exception) and sometimes the webhook will send you all the information for a transaction EXCEPT for the payment id.

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

Then you will have to run the `python manage.py makemigrations` command. This
is necessary due to the problem that there is no default `Customer` model,
until you inherit from the `AbstractCustomer` and declare it inside the
settings.py variable `OPENPAY_CUSTOMER_MODEL`.

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


[![GRVTY][logo]](http://grvty.digital)

[logo]: http://grvty.digital/images/logos/repos-logo-1.png?raw=true "GRVTY"
[stack-shield]: http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat
[stack-tech]: http://stackshare.io/grvty/grvty

[openpay-git]: https://github.com/open-pay/openpay-python/
[openpay-page]: http://www.openpay.mx/en/
[pci-wiki-page]: https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard
[postman-svg]: https://run.pstmn.io/button.svg
[postman-pkg]: https://app.getpostman.com/run-collection/929685fa23a4a51f1a2f

[changelog]: https://github.com/grvty-labs/django-openpay/blob/master/docs/Changelog.md
[milestones]: https://github.com/grvty-labs/django-openpay/blob/master/docs/Milestones.md
[webhook-log]: https://github.com/grvty-labs/django-openpay/blob/master/docs/log/webhook.md
[license]: https://github.com/grvty-labs/django-openpay/blob/master/LICENSE
