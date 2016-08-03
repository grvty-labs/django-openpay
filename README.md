django-openpay
==============

Django app for online transactions
----------------------------------

[OpenPay](http://www.openpay.mx/en/) is an online gateway to execute online
payments using debit/credit cards or bank transferences. OpenPay allows to
create Plans for system memberships, with an autocharge system.

Django-Openpay is a django application (duh!) which integrates two OpenPay
libraries:

* The Python to manage Plans and Customers directly from django models

* The JavaScript library to manage online payouts and transactions, without
saving sensible information in your django application.

Installation
------------

To install this package from pip it is required to execute:

´pip install django-openpay´

To use the JSX files, you should have Webpack or Gulp installed to compile the
JSX to ES5 or ES6. But due to my inexperience for including NPM dependencies
in pip packages, you will require to install the openpay package:

´npm install openpay´

Disclaimer
---------

For the moment, django-openpay only includes certain models to manage
Customers and Plans, but not the Bank Accounts nor Cards for security reasons,
although this package includes JSX files to execute payouts from client-side.

GRVTYlabs 2016
