.. _tgeggdeployment:

Deploying your TG application with an Egg and Easy Install
===========================================================

.. contents::
    :depth: 3


How to Build a .egg File for Your Project
------------------------------------------

An egg is Python's new distribution format, comparable to a ``.jar`` in Java.
It's basically a zip file with a particular directory structure containing the
code and a bit of metadata. You can get details on eggs directly from the
inventor at the `PEAK Developers' Center`_.

A freshly quickstarted project will have a ``setup.py`` file. This file allows
you to easily package your file for redistribution both for internal use and
for sharing on PyPI_. Creating an egg is as simple as
switching to your project directory and running::

    python setup.py bdist_egg

This will produce an egg file for the current version of your project in the
``./dist`` folder.


How to Install Your .egg
------------------------

The simplest way to use an egg is to copy it over to your production machine
and do::

    [sudo] easy_install *myapp*.egg

.. note:: If you do not have ``easy_install`` on the target machine, you need
   to install the setuptools_ package first to get it, either through your
   operating system's software package system or by downloading the
   bootstrapping program `ez_setup.py`_. Conveniently, ``ez_setup.py`` also
   takes the same arguments that ``easy_install`` takes, so ``python
   ez_setup.py *myapp*.egg`` will do the full install. Be sure to switch
   over to ``easy_install`` after the first run.


Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

As long as the ``setup.py`` lists TurboGears as a requirement (see the section
on `adding requirements`_), it should be possible for somebody to install your
application with just the egg and ``easy_install`` or ``ez_setup.py`` including
the installation of TurboGears itself and all its dependencies.

.. warning:: This is a nice feature for application deployment, but be aware that
    installing an egg can also upgrade TurboGears and other packages if the egg
    requires a later version than the system provides. If long term system
    stability is important to you, you may want to investigate solutions like
    virtualenv_.

    Please be also aware that by default the ``setup.py`` file of a quickstarted
    project will require a TurboGears version that is equal or newer than the
    version which was used to run ``paster quickstart``. This means if you
    install your application and TurboGears is not installed or only an older
    version than required, ``easy_install`` will fetch and install the newest
    TurboGears version it can find. **This includes beta versions and release
    candidates of future TurboGears versions with a higher major version number.**
    If you want to ensure that your application will only install a known good
    TurboGears version, you should add a more specific version constraint for
    TurboGears in ``setup.py`` (again, see `adding requirements`_ on how to do this).


Running Your Application
------------------------

TurboGears apps take advantage of the paster serve functionality by
providing a way to start the server as you would any other paste application

Once you have your application installed in the proper location simply
cd to that location and type the following command::

    $ paster serve production.ini

where ``production.ini`` is your production configuration file, which is covered in the
next section.


The Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get everything up and running, you also need a production configuration_ file
(usually called ``production.ini`` by convention) and pass the name of this file as the
first and only argument to your start script.


The Production Database
~~~~~~~~~~~~~~~~~~~~~~~

Your production configuration should specify location and parameters for the
production database_ that your project will use.

This can be the same database as the one you created with ``paster setup-app``
while developing your application. If you use a different database for production
(a wise decision) you will need to create the tables in the database, before using
it for the first time.

::

    paster setup-app production.ini

will create the necessary tables using the database specified in the deployment
configuration file ``production.ini``.


Daemonizing your Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you are satisfied with the running of your server, it makes sense to run it in
a background mode so that you may log off, leaving your server running.  Paste does this
with the --daemon argument.  It looks something like this::

    paster serve production.ini --daemon

To stop your application from running, simply type::

    paster serve production.ini --stop-daemon

.. _adding requirements:

How to Make Your Project's .egg Require Additional Packages
-----------------------------------------------------------

By specifying all your dependencies, not just TurboGears, ``easy_install`` can
completely automate your package setup. You specify dependencies by modifying
the ``requires`` argument in ``setup()`` in your ``setup.py`` file to include
the name of the package you need. Here is an example that adds the fictional
package ``FooBar`` as an installation requirement::


    setup(
        name="test",
        version=0.1,
        zip_safe=False,
        install_requires = [
            "TurboGears >= 2.0",
            "FooBar"
        ],
        ...

If you need a specific version of the package you can use comparison operators
against the version name. You can see that happening in the above example, as
this project depends on "TurboGears version 2.0 or greater". See the setuptools_
documentation for more information on declaring dependencies.


How to Make Your Project Available on PyPI
----------------------------------------------------

If you decide to share your creation with the world, the easiest way to do so
is by using the Python Package Index.  Before you can upload your project
to PyPI, you will need an account. You can create one on the `PyPI registration page`_.

.. _PyPI registration page: http://www.python.org/pypi?:action=register_form

After you have created an account, you will need to tell setuptools your
account information for uploading the file. See the `distutils documentation`_
for details on this.

Now that you have your account configured and you've updated the metadata in
``setup.py``, you need to register a page for your application. setuptools
can do this for you automatically with the following command::

    python setup.py register

Once you have everything configured, setuptools can upload your egg
automatically. Here is the command you need::

    python setup.py bdist_egg upload

Any eggs you created in the process should also be available in the ``dist/``
folder of your project.

You can also register projects and upload your eggs manually. This
`setuptools tutorial`_ should be enough to get you going.

.. _setuptools tutorial: http://wiki.python.org/moin/CheeseShopTutorial

References
--------------
Take a look at :ref:`basketweaver` to see how to make your own personal PYPI
for distribution within a closed environment.



.. _pypi: http://pypi.python.org
.. _cogbin: http://www.turbogears.org/cogbin/
.. _configuration: 1.0/Configuration
.. _database: 1.0/GettingStarted/UseDatabase
.. _distutils documentation: http://docs.python.org/dist/package-index.html
.. _entry point:
    http://peak.telecommunity.com/DevCenter/setuptools#extensible-applications-and-frameworks
.. _ez_setup.py: http://peak.telecommunity.com/dist/ez_setup.py
.. _peak developers' center: http://peak.telecommunity.com/DevCenter/PythonEggs
.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
.. _virtualenv: 1.0/InstallNonRoot



