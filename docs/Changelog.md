Changelog
==========

This is **django-openpay**'s changelog: The place where you can read about the
new releases and how they could impact your current installations of this
package.


*   v0.4.0
    *   Started the **openpaysync** command to the `manage.py` options. This
    command has the purpose to download everything from your Openpay account.
    By now it only pulls Plans, Customers, Subscriptions and Cards (it
    updates each instance if found in your Django database, else it will create
    it).
*   v0.3.0
    *   Added the reception and interpretation of the information received from
    Openpay through their **webhook**. A [Postman project][postman-pkg] has
    been created for local testing. [RequestBin][requestbin-page] was used to
    generate a [log][webhook-log] from which the Postman project was created.
    *   Created the `AbstractTransaction` model. This model will be useful to
    prevent code repetition as seen in the Openpay's documentation.
    *   Converted the `Customer` model to `abstract`. Now it is required to
    inherit from this model and to define in settings.py the variable
    `OPENPAY_CUSTOMER_MODEL`.
    *   Stopped using **Openpay-python** because it had way too many bugs when
    working with Charges. We forked the project and fixed the bugs. Can be
    found in `pip` as `OpenpayGrvty`.
    *   All the **migrations** have been deleted. This is due to the change
    in the `Customer` model, from a hard model to an `abstract` one (now known
    as `AbstractCustomer`).
    *   Improved the `Subscription` model. Previously this model didn't save
    the status of the subscriptions, because we thought that this would be
    available through the Openpay system's webhooks. But I was wrong. Now, to
    be able to see the subscription state and update it constantly, it is
    required to activate a **Celery** worker and beater. Thankfully you can
    check the *\_\_init\_\_.py* and the *celery.py* files in the *testing*
    folder. Bonus: I recommend you to use this nice Celery tutorial to
    better understand what it is needed, how we did it and how you can
    improve it: [here][celery-tutorial].
    *   If you started using our library before this point we recommend you to:
    Uninstall this library, uninstall the openpay library and reinstall
    everything without using cache. (If you are using pip, this shouldn't
    delete your migrations, so you don't have to worry about those). This fix
    is related to the fork we had to do from the Openpay's official library and
    how the namespaces collide with our fork.


*   v0.2.x > v0.2.1
    *   Only one **MAJOR** change. Stopped using the Openpay's official python
    library, forked it and started using our changes. This was because the
    official library has not been maintained in the last 3 years, they don't
    answer to the issues and we detected multiple (stupid) errors.
    *   Installation tests. Nothing really important, but there were several
    changes to the Milestones, Readme, Manifest, etc.


*   v0.2.1
    *   Apparently setuptools is no longer working with pip. This is just a
    fix on the upload of the dist package.


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
    *   Minor fix on internationalization by using `ugettext` and
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
    *   The **django-admin** now displays more information in each model's
    list.
    *   Added the `get_readonly_fields` function to all models, to prevent
    changes in the instances that will NOT be reflected in the Openpay Admin.
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




Owned and developed by
--------

[![StackShare][stack-shield]][stack-tech]


[![GRVTYlabs][logo]](www.grvtylabs.com)

[logo]: https://github.com/grvty-labs/django-openpay/blob/master/logo.png?raw=true "GRVTYlabs"
[stack-shield]: http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat
[stack-tech]: http://stackshare.io/letops/grvtylabs

[postman-pkg]: https://app.getpostman.com/run-collection/929685fa23a4a51f1a2f
[houndci-page]: https://houndci.com/
[requestbin-page]: https://requestb.in/
[webhook-log]: https://github.com/grvty-labs/django-openpay/blob/master/docs/log/webhook.md


[celery-tutorial]: https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/
