.. _quickstarting:

Quickstarting A TurboGears |version| Project
============================================

.. highlight:: bash

:Status: Work in progress

.. contents:: Table of Contents
    :depth: 2

We assume that you have TurboGears installed and, if you installed it
in a virtual environment as recommended, that your virtualenv is activated.
See :ref:`downloadinstall` to get to this point.

TurboGears 2 extends the ``paster`` command-line tool to provide a
suite of tools for working with TurboGears 2 projects. A few will be
touched upon in this tutorial, check the ``paster --help`` command for
a full listing.

The very first tool you'll need is ``paster quickstart``, which
initializes a TurboGears 2 project.  You can go to whatever directory
you want and start a new TurboGears 2 project.

.. code-block:: bash

  $ paster quickstart

The ``paster quickstart`` command will create a basic project
directory for you to use to get started on your TurboGears 2
application. You'll be prompted for the name of the project (this is
the pretty name that human beings would appreciate), and the name of
the package (this is the less-pretty name that Python will like).

Here's what our choices for this tutorial look like::

    Enter project name: Helloworld
    Enter package name [helloworld]: helloworld
    Do you need authentication and authorization in this project? [yes]
    ...output...

This will create a new directory which contains a few files in a
directory tree, with some code already set up for you.

Let's go in there and you can take a look around.

.. code-block:: bash

   $ cd Helloworld

The ``setup.py`` file has a section which explicitly declares the
dependencies of your application.  The quickstart template has a few
built in dependencies, and as you add new python libraries to your
application's stack, you'll want to add them here too.

Then in order to make sure all those dependencies are installed you
will want to run.

.. code-block:: bash

   $ python setup.py develop

If you have just installed TurboGears and are in a relatively new
virtualenv, expect to see a bit of output about additional packages
being installed.


Create The Database
-------------------

Most applications will use a database, and since we specified we are
using "authentication" in our quickstart, we need a place to store
users and permissions.  Before you run your application for the first
time, you need to make sure the database is created and initialized.
The following command typically only needs to be run *once*.

.. code-block:: bash

      $ paster setup-app development.ini

With the quickstart command from above, you will see quite a bit of
output which shows you the SQL commands that create the authentication
tables and setup a default user/password for you::

      user: manager
      password: managepass

You don't need to understand all of this now, but here is a little
background about how "paster setup-app" knows what to do.  By default,
the database is created using SQLite_, and the data is stored in a
file, devdata.db, in the top level of your project.  The information
about what database driver is used is specified in the development.ini
file passed on the command line.  The code which adds the initial data
rows is in helloword/web_setup.py.  The command "paster setup-app"
ends up calling the function "setup_app" within this file.


Another key piece of TG2 application setup infrastructure is the
``paster setup-app`` command which takes a configuration file and runs
your project's websetup code in that context.  This allows you to use
setup-app to create database tables, pre-populate require data into
your database, and otherwise make things nice for people first setting
up your app.  If you take a look at your project's quickstart, you
will see a websetup Python script. Inside of this script, you will see
a single functon, setup_app, that is called when ``paster setup-app``
is run. Inside of this, you may do any setup you need to for your
application. The most common operations will be to add in basic data
to the database that is required to bootstrap your application.

.. note:: If it's the first time you're going to use the application,
  and you told quickstart to include authentication+authorizaiton, you
  will *have* to run ``setup-app`` to set it up (e.g., create a test
  database).

.. code-block:: bash

      $ paster setup-app development.ini

This will create the database using the information stored in the
development.ini file which by default makes single file SQLite
database in the local file system.  In addition to creating the
database, it runs whatever extra database loaders or other setup are
defined in {yourproject}.websetup:setup_app.

In a quickstarted project with Authorization enabled setup-app creates
a couple of basic users, groups, and permissions for you to use as an
example.  This code is found in {yourproject}.websetup:setup_app.
This code also shows how you can add new data automatically to the
database when the setup-app command is executed..

Run The Server
--------------

At this point your project should be operational, and you're ready to
start up the app.  To start a TurboGears 2 app, you need to be in the
top level of your project directory (`Helloworld`) and issue the
command ``paster serve`` to serve your new application.

.. code-block:: bash

    $ paster serve development.ini

As soon as that's done point your browser at http://localhost:8080/
and you'll see a nice welcome page.

.. note:: If you're exploring TurboGears 2 after using TurboGears 1
   you may notice a few things:

* The old config file `dev.cfg` file is now `development.ini`.
* By default the ``paster serve`` command is not in auto-reload mode as
  the CherryPy server used to be.  If you also want your application to
  auto-reload whenever you change a source code file just add the
  ``--reload`` option to ``paster serve``:

.. code-block:: bash

          $ paster serve --reload development.ini

You might also notice that paster serve can be run from any directory
as long as you give it the path to the right ini file.

In order to run the server in development mode, where your Python files are
reloaded automatically when they are changed, you typically use the
following command.

.. code-block:: bash

   paster serve --reload development.ini

If you take a look at the code that quickstart created you'll see that
there isn't much involved in getting up and running.  In particular,
you'll want to check out the files directly involved in displaying
this welcome page:

* `development.ini` contains the system configuration for development.
* `helloworld/controllers/root.py` contains the controller code to create the
  data for the welcome page along with usage examples for various tg2
  features.
* `helloworld/templates/index.html` is the template turbogears uses to render
  the welcome page from the dictionary returned by the root controller. It's
  standard XHTML with some simple namespaced attributes.
* `helloworld/public/` is the place to hold static files such as pictures,
  JavaScript, or CSS files.

You can easily edit development.ini to change the default server port
used by the built-in web server::

  [server:main]
  ...
  port = 8080

Just change 8080 to 80, and you'll be serving your app up on a
standard port (assuming your OS allows you to do this using your
normal account).

You might also wish to have paster listening on all IP addresses on
your machine. To do so, modify the line right above the port line (in
development.ini) to have the value 0.0.0.0, like so::

  [server:main]
  ...
  host = 0.0.0.0

What's Next?
------------

* If you are new to TurboGears you should likely continue on to
  :ref:`explorequickstart`
* You may wish to go directly to the :ref:`tutorials` which provide hands-on
  projects to guide you through learning TurboGears

.. _SQLite:  http://www.sqlite.org
