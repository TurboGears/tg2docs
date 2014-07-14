==================================
Creating Project Structure
==================================

.. hint::
    This tutorial has been written for TurboGears 2.3 on Python2.7. While it might work with
    previous or later versions, it has been tested only for version 2.3.

Setting up our Environment
===============================

If this is your first TurboGears2 project you need to create an environment and install
the TurboGears2 web framework to make the development commands available.

Completed version of this tutorial is available on 
http://runnable.com/U8P0CQTKHwNzQoYs/turbogears-wikier-tutorial-for-python.

If you want to play around with this tutorial without installing TurboGears on
your computer you can freely edit the *Runnable* version.

Creating the Environment
--------------------------------

First we are going to create a Virtual Environment where we will install the framework.
This helps keeping our system clean by not installing the packages system-wide.
To do so we need to install the ``virtualenv`` package::

    $ pip install virtualenv

Now the virtualenv command should be available and we can create and activate
a virtual environment for our TurboGears2 project::

    $ virtualenv tgenv
    $ . tgenv/bin/activate


If our environment got successfully created and activated we should end up with
a prompt that looks like::

    (tgenv)$

Installing TurboGears2
--------------------------------

TurboGears2 can be quickly installed by installing the TurboGears2 development tools.
This will install TurboGears2 itself and a bunch of commands useful when developing
TurboGears applications:

.. parsed-literal::

    (tgenv)$ pip install |private_index_path| tg.devtools

.. note::
    The `-i http://tg.gy/VERSION` option is used to make sure that we install
    TurboGears2 version and its dependencies at the right version. TurboGears2 
    doesn't usually enforce version dependencies to make it possible for developers
    to upgrade them if they need a bugfix or new features.
    It is suggested to always use the `-i` option to avoid installing incompatible packages.


Creating the Project
=============================

If the install correctly completed the ``gearbox quickstart`` command should be available
in your virtual environment::

    (tgenv)$ gearbox quickstart wikir

This will create a project called wikir with the default template engine and with authentication.
TurboGears2 projects usually share a common structure, which should look like::

     wikir
     ├── __init__.py
     ├── config       <-- Where project setup and configuration is located
     ├── controllers  <-- All the project controllers, the logic of our web application
     ├── i18n         <-- Translation files for the languages supported
     ├── lib          <-- Utility python functions and classes
     ├── model        <-- Database models
     ├── public       <-- Static files like CSS, javascript and images
     ├── templates    <-- Templates exposed by our controllers
     ├── tests        <-- Tests
     └── websetup     <-- Functions to execute at application setup like creating tables, a standard user and so on.


Installing Project and its Dependencies
-----------------------------------------

Before we can start our project and open it into a browser we must install any dependency
that is not strictly related to TurboGears itself. This can easily be achieved running the develop
command which will install into our environment the project itself and all its dependencies::

    (tgenv)$ cd wikir
    (tgenv)$ pip install -e .

Project depndencies are specified inside the ``setup.py`` file in the ``install_requires`` list.
Default project dependencies should look like::

    install_requires=[
        "TurboGears2 >= 2.3.0",
        "Genshi",
        "zope.sqlalchemy >= 0.4",
        "sqlalchemy",
        "sqlalchemy-migrate",
        "repoze.who",
        "tgext.admin >= 0.5.1",
        "repoze.who.plugins.sa",
        "tw2.forms",
        ]

*Genshi* dependency is the template engine our application is going to use, the *zope.sqlalchemy,
sqlalchemy and sqlalchemy-migrate* dependencies are there to provide support for SQLALchemy based
database layer. *repoze.who and repoze.who.plugins.sa* are used by the authentication
and authorization layer. *tgext.admin* and *tw2.forms* are used to generate administrative interfaces
and forms.

Serving our Project
----------------------------------------

.. note::
    If you skipped the ``pip install -e .`` command you might end up with an error that looks
    like: *pkg_resources.DistributionNotFound: tw2.forms: Not Found for: wikir (did you run python setup.py develop?)*
    This is because some of the dependencies your project has depend on the options you choose while
    quickstarting it.

You should now be able to start the newly create project with the ``gearbox serve`` command::

    (tgenv)$ gearbox serve --reload
    Starting subprocess with file monitor
    Starting server in PID 32797.
    serving on http://127.0.0.1:8080

.. note::
    The `--reload` option makes the server restart whenever a file is changed, this greatly speeds
    up the development process by avoiding having to manually restart the server whenever we need to try
    our changes.

Pointing your browser to http://127.0.0.1:8080/ should open up the TurboGears2 welcome page.
By default newly quickstarted projects provide a bunch of pages to guide the user through
some of the foundations of TurboGears2 web applications. Taking a look at the http://127.0.0.1:8080/about
page can provide a great overview of your newly quickstarted project.


