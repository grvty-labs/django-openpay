django-openpay
==============

Django app for online transactions
----------------------------------

[OpenPay](http://www.openpay.mx/en/) is an online gateway to execute online
payments using debit/credit cards or bank transferences. OpenPay allows to
create Plans for system memberships, with an autocharge system.

Django-Openpay is a django application (duh!) which integrates two OpenPay
libraries:

*   The Python to manage Plans and Customers directly from django models

*   The JavaScript library to manage online payouts and transactions, without
saving sensible information in your django application.

Features
--------

Create directly from Django into OpenPay:

*   Customers
*   Plans
*   Subscriptions

Delete directly from Django into OpenPay:

*   Customers
*   Plans
*   Subscriptions
*   Cards

Create from JSX into OpenPay:

*   Cards

Reflect through webhooks from OpenPay into Django:

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

`  <script type='text/javascript' src='https://code.jquery.com/jquery-3.1.0.min.js'></script>`

`<script type='text/javascript' src='https://openpay.s3.amazonaws.com/openpay.v1.min.js'></script>`

`<script type='text/javascript' src='https://openpay.s3.amazonaws.com/openpay-data.v1.min.js'></script>`

TODOs
-----

*   Verify this package is PCI Compliant


Disclaimer
---------

**django-openpay** does not saves critical information in its django models,
it just saves the tokens to access the information from the OpenPay servers
and allows to modify the information contained inside OpenPay from Django.

**django-openpay** has not been tested for security vulnerabilities and does
not have an SSL certificate preconfiguration, this is the reason behind our
decision to create cards only from front-end.

GRVTYlabs 2016
