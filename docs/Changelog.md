Changelog
==========

This is **django-openpay**'s changelog: The place where you can read about the
new releases and how they could impact your current installations of this
package.


*   v1.0.0
    *   This version is considered our **first beta version** (v2.0
    will be the first stable version). This means that the models will
    not have significant changes made to their fields. Although the
    functionality can be greatly improved or modified.
    *   The trash has been dumped. No more empty or unnecessary files.
    All other files (like the `static`s) have been placed inside
    *testing*.
    *   We are working in improving the `wheels` files, to prevent the
    upload of our testing folders (like `django_openpay_repo`), which are
    not in this repository but apparently they are uploaded every time we
    publish this package, any help is welcome to solve this dumb problem.
    *   The **openpaysync** command has been greatly improved, but this
    required some modifications in the models methods.
    *   We renamed most of the methods to prevent collisions with the
    Django's defaults and to make more clear the use of the methods:
        *   Added the `op_fill` method, which will parse and fill the
        model instance with what has been pulled from the Openpay's
        system. This method works with what has already been pulled, it
        doesn't execute another *retrieve* from the Openpay's servers.
        *   The `retrieve` method was renamed to `op_load`, but works as
        before: request the latest data from the Openpay server and
        save it in a private variable.
        *   The `pull` method was renamed to `op_refresh` and works
        as always. It requests the object's data (using `op_load`) parses
        it (using `op_fill`) and, if the `save` parameter is `True`, it
        saves it to the DB immediately.
        *   The `push` has been renamed to `op_commit`. The only
        difference is that this method will execute an `op_fill` every
        time it is called. The reason behind this is: Openpay always
        responds to an object update with the new values, by doing an
        `op_fill` we can ensure that your instance is consistent with
        what Openpay has.
        *   The `remove` method was renamed to `op_dismiss`. Remember that
        not all Openpay's objects are destroyed, they are just hidden, so
        instead of *deleting* your objects from the database, try to
        just hide them and use the `op_dismiss`. In future versions
        (probably v1.2) we will have improved this aspect as much as we
        can.
        *   The private attribute `_openpay` was renamed to `_op_`.
        Although our intention was to use the *name mangling* option of
        Python, some generic functionality cannot work with that
        (`hasattr` and `getattr` cannot detect this kind of attributes),
        for now it is a useless change, but our intention is to completely
        hide it (v1.5), so beware.


*   v0.4.1
    *   I am so ashamed about this bug. I forgot a crucial part of the
    `AbstractCustomer` relation with the `Card` model. I also deleted the
    `pull` that was executed when creation a new object in all models, this
    cannot be, due to some fields that we MUST pull from the Openpay database.


*   v0.4.0
    *   Improved the `Plan` model. We added the **status** and multiple
    description fields. This fields just have one real purpose. Front-end
    representation. The **benefits** field is a JSONField which you can use
    as you please to display the features of each plan. The **excerpt** is a
    CharField limited to 250 characters, used to explain in a single line the
    plan.
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
