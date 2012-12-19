=========================================
Pluggable Applications with TurboGears
=========================================

TurboGears 2.1.4 introduced support for pluggable applications using tgext.pluggable.
``tgext.pluggable`` is now the official supported way in TurboGears to create pluggable
reusable applications.
Currently only SQLAlchemy based applications are supported as pluggable applications.

Official documentation for ``tgext.pluggable`` can be found at: http://pypi.python.org/pypi/tgext.pluggable

Supported Features
==================================

Pluggable applications can define their own:

    * **controllers**, which will be automatically mounted when the application is purged.
    * **models**, which will be available inside and outside of the plugged application.
    * **helpers**, which can be automatically exposed in ``h`` object in application template.
    * **bootstrap**, which will be executed when `setup-app` is called.
    * **statics**, which will be available at their own private path.

Mounting a pluggable application
==================================

In your application config/app_cfg.py import plug from ``tgext.pluggable`` and
call it for each pluggable application you want to enable.

The plugged package must be installed in your environment.

.. code-block:: python

    from tgext.pluggable import plug
    plug(base_config, 'package_name')

Creating Pluggable Applications
===================================

``tgext.pluggable`` provides a **quickstart-pluggable** command
to create a new pluggable applications:

.. code-block:: bash

    $ gearbox quickstart-pluggable plugtest
    ...

The quickstarted application will provide an example on how to use
models, helpers, bootstrap, controllers and statics.


