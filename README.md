**django-openpay**
==================

Django app for online transactions
----------------------------------

[Openpay][openpay-page] is an online gateway to execute online
payments using debit/credit cards or bank transferences. Openpay allows to
create Plans for system memberships, with an autocharge system.

Django-Openpay is a django application which integrates two Openpay
libraries:

*   The Python library to manage Plans, Charges, Subscriptions, Customers and
Cards (partially) from the django models.

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

4.  Reflect through webhooks from Openpay into Django:
    *   Charges

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

*   `OPENPAY_PRIVATE_API_KEY`
*   `OPENPAY_PUBLIC_API_KEY`
*   `OPENPAY_MERCHANT_ID`
*   `OPENPAY_VERIFY_SSL`
*   `OPENPAY_DEVICE_ID`


Versions Released
-----------------

*   v0.2.0
    *   **This version is not 100% compatible with the previous version**. This
    is because we had to modify, rename and add some of the models' fields.
    If you are using this package and you are not calling explicitly some of
    the fields, you should have no problem.
    *   Renamed `code` field to `openpay_id` in all models.
    *   All models now inherit from the `AbstractOpenpayBase` model to generate
    the code contracts across the models.
    *   Added the functions of `push`, `pull`, `retrieve` and `remove` to
    manage the communication with Openpay.
    *   Fixed the aspect of internationalization using `ugettext` and
    `ugettext_lazy`.
    *   Moved the functionality from the `save` function in all models to their
    corresponding signal. (In order to prevent errors from the `save`
    overwrite).
    *   Moved the functionality from the `delete` function in all models to
    their corresponding signal. (In order to prevent errors from the `delete`
    overwrite).
    *   New **exception types** added.
    *   Added the `OPENPAY_DEVICE_ID` variable to the settings, so we can
    create simple Charges from the Django Admin (using only Cards that were
    created previusly using tokens).
    *   The `django-admin` now displays more information in each model's list.
    *   Added the `get_readonly_fields` function to all models, to prevent
    changes in the instances that will NOT be reflected in the Openpay Admin.
    *   Improved the Charges model.
    *   The **testing** folder was included with some simple configurations to
    experiment with this package.
    *   **MANIFEST.in** was updated to prevent **setuptools** from uploading
    trash.
    *   This package's pull requests are now being checked by
    [Hound][houndci-page], please respect the code standards that will be set
    in the **.hound.yml** file.


*   v0.1
    *   Created the initial connections to the Openpay API.
    *   Create directly from Django into Openpay:
        *   Customers
        *   Plans
        *   Subscriptions
    *   Delete directly from Django into Openpay:
        *   Customers
        *   Plans
        *   Subscriptions
        *   Cards
    *   Create from JSX into Openpay:
        *   Cards
    *   Reflect through webhooks from Openpay into Django:
        *   Charges (Pending tests)


Milestones
----------
This milestones are merely a map to inform everyone what we are trying to
accomplish and what to expect in future versions.

*   v3.0
    *   **Not released yet**.
    *   This package should have enough security to become **PCI Compliant**
    by its own. Although this doesn't mean we will save Cards in the system, we
    must be able to make sensitive transactions from the back-end.

*   v2.0
    *   **Not released yet**.
    *   This version will include the features related to managing **Bank
    Accounts**, **Payouts**, **Charges**, **Fees**, **Transfers**, etc.
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
    *   The **Charges Webhook** will be completely connected and tested with the
    Openpay servers. In this way, we should be able to create Charges from
    Django and/or JavaScript, and be able to see all the recurring charges made
    automatically by the Openpay system.
    *   Django **Internationalization** will be completed for English and
    quite a great part will be translated to Spanish.
    *   **Celery** will start being used to prevent communication bottlenecks
    with the Openpay API
    *   Pull all the data saved inside Openpay to your database using the
    command **openpaysync** which will be callable using `manage.py`


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

[openpay-page]: http://www.openpay.mx/en/
[pci-wiki-page]: https://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard
[houndci-page]: https://houndci.com/
[openpay-git]: https://houndci.com/
[openpay-issue]: https://github.com/open-pay/openpay-python/issues/3
