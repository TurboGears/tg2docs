.. _downloadinstall:

TurboGears |version| Standard Installation
===========================================

This document is intended to get the new developer up-and-running
quickly with TurboGears |version|.  It assumes that you will follow the
recommended installation procedures and preferred setup.
:ref:`altinstall` covers non-standard installation procedures
such as for :ref:`wininstall`.

The setup here is a development environment which uses the Paste
web-server which is easy to set up, but isn't normally used in
production save for very low-traffic sites.  For instructions on
setting up a production environment, see :ref:`tgdeployment`.

Recommended Installation Environment
------------------------------------

We will assume here that you are installing into this environment:

    * Linux Operating System (Debian or RPM based)
    * GCC (or another C compiler for your platform, XCode for OS-X,
      Mingw32 or VisualStudio for Win32)
    * Python 2.5 or 2.6 (see also :ref:`python24install`)
    * Python headers for building C extensions (often split into a "dev"
      package on Linux distributions)
    * SetupTools_ (version 0.6c9) (or Distribute_ 0.6c9 or above)
    * a :ref:`virtualenv` isolated environment

.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _Distribute: http://pypi.python.org/pypi/distribute

System Package Installation
---------------------------

For Debian/Ubuntu systems:

.. code-block:: bash

    $ sudo aptitude install build-essential python-dev python-setuptools python-virtualenv

For RHEL systems (see :ref:`python24install`):

.. code-block:: bash

    $ su -c 'rpm -Uvh http://download.fedora.redhat.com/pub/epel/5/i386/epel-release-5-3.noarch.rpm'
    $ yum install gcc sqlite-devel
    $ yum --enablerepo=epel-testing install python-virtualenv

For Fedora systems:

.. code-block:: bash

    $ yum install gcc sqlite-devel python-virtualenv


Installation for the Impatient
------------------------------

Here's the whole process for the impatient.  It sets up a VirtualEnv, installs
TurboGears 2.1 into the environment, creates a new quick-started project and
runs that project with the Paste web server:

.. code-block:: bash

    $ virtualenv --no-site-packages -p python2.6 tg2env
    $ cd tg2env/
    $ source bin/activate
    (tg2env)$ easy_install -i http://www.turbogears.org/2.1/downloads/current/index tg.devtools
    (tg2env)$ paster quickstart example
    (tg2env)$ cd example/
    (tg2env)$ python setup.py develop
    (tg2env)$ nosetests
    (tg2env)$ paster setup-app development.ini
    (tg2env)$ paster serve development.ini
    (tg2env)$ deactivate
    $

.. note:: If you are using Python 2.4, such as on RHEL 5, see :ref:`python24install`

Explaining the Installation Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: This section is just a longer explanation of the process above.

This sets up a Python 2.6 VirtualEnv, substitute -p python2.5 if you
wish to use that version.  The use of --no-site-packages prevents
conflicts with any packages installed into the platform directories.
(See :ref:`virtualenv` for details on VirtualEnv)

.. hint:: Please note we are using ``tg2env`` as the name of the
   virtual environment.  This is simply a convention in our
   documentation, the name of the virtualenv is up to you, and is
   normally your project or product name, or a descriptive name
   such as "testing", "trunk" or "staging".

.. code-block:: bash

    $ virtualenv --no-site-packages -p python2.6 tg2env

Here we activate the VirtualEnv, the activation "switches into" the
isolated environment and makes future setup.py or easy_install operations
affect just this VirtualEnv.

.. code-block:: bash

    $ cd tg2env/
    $ source bin/activate

This command installs TurboGears 2.1 into the VirtualEnv.  The -i argument
tells easy_install to lookup the packages involved by treating that page
as providing the index page which declares the appropriate package versions
(and provides links to them).  The "current" URL fragment can be replaced
with, for instance, "2.1b1" to pull in precisely the first 2.1 beta.  Your
projects will normally use a particular version of TurboGears.

.. code-block:: bash

    (tg2env)$ easy_install -i http://www.turbogears.org/2.1/downloads/current/index tg.devtools

A large number of packages will be installed.  These are the officially
required packages which define TurboGears itself.  The Pylons/Paste package
provides the "paster" command, which we will use to set up an example project.

.. code-block:: bash

    (tg2env)$ paster quickstart example
    # accept all defaults
    (tg2env)$ cd example/

The following command will install your new package into your VirtualEnv and
will download a number of packages which are not technically part of TurboGears,
but which provide useful features for the quick-started application.

.. code-block:: bash

    (tg2env)$ python setup.py develop
    # more stuff installed here
    (tg2env)$ nosetests

The nosetests command runs the quickstarted application's test-suite.  This
step is optional, but is a good smoke-test to see if you have installed
correctly.
Here we create our example application's database (an SQLite database) and
then serve it on the default port (8080).

.. code-block:: bash

    (tg2env)$ paster setup-app development.ini
    (tg2env)$ paster serve development.ini

Point your web-browser at http://localhost:8080/ when satisfied that you are
running correctly, hit CTRL-C to exit from the tg2env virtualenv

.. code-block:: bash

    (tg2env)$ deactivate
    $

Running the Installed Environment
---------------------------------

Each time you want to work with your TurboGears install, you need to
re-activate the VirtualEnv.

.. code-block:: bash

    $ cd tg2env/
    $ source bin/activate
    $ cd example/
    (tg2env)$ paster serve development.ini

.. _upgrading:

Upgrading TurboGears
--------------------

To upgrade an existing TurboGears installation, activate the VirtualEnv and
pass the -U flag to easy_install with the "index" URL for the new version
to which you would like to upgrade:

.. code-block:: bash

    easy_install -U -i http://www.turbogears.org/2.1/downloads/current/index tg.devtools

which will update each dependency which has been upgraded.  Note that it will
*not* uninstall the previous versions of the packages.

.. _dbdriverinstall:

Install a Database Driver
-------------------------

.. hint:: The installation of the database backend is a topic outside
   of the scope of this document.

TurboGears uses SQLAlchemy as its default ORM (Object Relational
Mapper) layer.  SQLAlchemy maintains excellent documentation on all
the `engines supported`_.

Here are the easy_install commands for two of the most common free SQL
databases.  We provide these here because they are very common, yet
the pypi_ packages have different names than you might expect.

.. code-block:: bash

    easy_install MySQL-python

    easy_install psycopg2

.. _pypi: http://pypi.python.org

SQLAlchemy also has support for PyGreSQL and the 0.6 version will support pg8000
which is a fully python driver for postgres.  TG plans to support these when SA 0.6
is released.

.. _engines supported: http://www.sqlalchemy.org/docs/05/reference/dialects/index.html

Cygwin users can't use sqlite as it does not include the necessary
binary file (``sqlite3.dll``).  If you want to run Cygwin you'll need
to install a different database.

What's Next?
------------

    * If you are new to TurboGears you will want to continue with the
        :ref:`Quick Start Guide <quickstarting>`.
    * If you are a TG1 user be sure to check out our
        :ref:`What's new in TurboGears 2 <whatsnew>` page to get a
        picture of what's changed in TurboGears2.

.. toctree::
   :maxdepth: 2

   AltInstall

