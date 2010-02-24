.. _altinstall:

Alternate Installation Process
==============================

This document provides instructions on how to install TurboGears in
ways which are not *necessarily* recommended for the new developer.
:ref:`downloadinstall` describes the recommended new-developer
installation environment.  This document also includes commonly
necessary tasks such as installing database drivers and upgrading
an existing TurboGears install.

This includes the following non-standard environments:

* :ref:`wininstall`
* :ref:`linuxrootinstall`
* :ref:`python24install`
* :ref:`pipinstall`
* :ref:`sourceinstall`

.. _wininstall:

32-bit Windows
--------------

.. note:: While Windows is a supported platform for TurboGears, it is not commonly
    used for deployments.  You may wish to consider setting up a virtual
    machine with a Debian or RPM-based Linux distribution so that your development
    environment is closer to your deployment environment.

Install Python (download and run an executable or MSI installer):

* `Python`_ -- choose version 2.6 or 2.5 for best results

Download http://peak.telecommunity.com/dist/ez_setup.py and then run it from the
command line with Python.  Note that you must install a specific version
of SetupTools.

::

    c:\working>c:\Python26\python.exe ez_setup.py "setuptools==0.6c9"

Once you have run the SetupTools installer, you can add the
c:\\Python26 and c:\\Python26\\Scripts
directories to your system path (in Control Panel/System/Advanced)
so that you can run Python and easy_install from the command line.

::

    c:\working>c:\Python26\Scripts\easy_install.exe virtualenv
    c:\working>c:\Python26\Scripts\virtualenv.exe example
    c:\working>cd example
    c:\working\example>Scripts\activate.bat
    (example) C:\working\example>easy_install.exe -i http://www.turbogears.org/2.1/downloads/current/index tg.devtools
    (example) C:\working\example>paster quickstart example
    (example) C:\working\example>cd example
    (example) C:\working\example\example>python setup.py develop
    (example) C:\working\example\example>paster setup-app development.ini
    (example) C:\working\example\example>paster serve development.ini

You should now be able to view http://localhost:8080 in a web browser.  You
can hit CTRL-C on the command-line to stop the server.

.. _`Python`: http://www.python.org/download/releases/
.. _`SetupTools`: http://pypi.python.org/pypi/setuptools


.. _linuxrootinstall:

Linux Root Install
------------------

.. note:: You are strongly encouraged to use a virtualenv-based environment for
    TurboGears, as this allows you to easily manage your TurboGears installation
    independent of your platform's release schedule.

On RedHat Enterprise Linux (RHEL) 5, you can install TurboGears from official
RPM packages via:

.. code-block:: bash

    yum install TurboGears2 python-tg-devtools

.. _python24install:

Python 2.4 Installation
-----------------------

Python 2.4 is missing a number of packages that TurboGears requires.  To
install these packages, you can use easy_install in your virtualenv.  While
Python 2.5 or 2.6 is recommended, some distributions, such as RHEL 5, use
Python 2.4 by default.  These instructions describe how to install TurboGears
as a non-root virtualenv, if you are using RHEL 5 and wish to install from
RPM see :ref:`linuxrootinstall` above:

.. code-block:: bash

    $ virtualenv --no-site-packages -p python2.6 tg2env
    $ cd tg2env/
    $ source bin/activate
    (tg2env)$ easy_install hashlib `pysqlite`_ uuid functools

.. warning:: For Python 2.4, you must make sure to install Beaker 1.4 or higher.
             Though it should be automatic, you may need to run this command to get it:

.. code-block:: bash

    $ easy_install -U beaker

You can continue to follow :ref:`downloadinstall` from this point forward.

.. _pysqlite: http://pypi.python.org/pypi/pysqlite/

.. _pipinstall:

Install Via PIP
---------------

`pip`_ (or pip installs packages) is an experimental easy_install
replacement. It provides many improvements over it's predecessor and
aims to be a full replacement.

.. warning:: pip is not supported under windows!

To install, simply use pip with the same index URL as for a standard
installation via setuptools:

.. code-block:: bash

    $ pip install -i http://www.turbogears.org/2.1/downloads/current/index -E tg2env tg.devtools

Which will create a tg2env VirtualEnv and install TurboGears into it.
From this point, switch to the VirtualEnv, activate it and continue
with the :ref:`downloadinstall`.  PIP can also be used to perform
a source install using Mercurial, see :ref:`sourceinstall` for details.

.. _pip: http://pypi.python.org/pypi/pip

.. _sourceinstall:

Source Install (Development Version)
------------------------------------

Generally you should not need to install a development version of TurboGears
unless you wish to contribute to the project (which is strongly encouraged).
TurboGears uses the Mercurial Distributed Version Control system hosted on
the BitBucket site.  For a detailed discussion of how to use Mercurial and
BitBucket see :ref:`bitbucket_tutorial`.

Getting Mercurial
~~~~~~~~~~~~~~~~~

* All major Linux distributions have this software packaged. The package
  is normally named ``mercurial``
* On windows you can download the `TortoiseHG installer`_
* On other platforms you may install the HG command line utility with an easy_install command:

.. code-block:: bash

    (tg2dev)$ easy_install mercurial

.. _TortoiseHG installer: http://mercurial.selenic.com/wiki/TortoiseHg

Getting The Source
~~~~~~~~~~~~~~~~~~

Check out the latest code from the subversion repositories:

.. code-block:: bash

  (tg2dev)$ hg clone http://hg.turbogears.org/tgdevtools-dev/ tgdevtools
  (tg2dev)$ hg clone http://hg.turbogears.org/tg-dev/ tg

Installing The Sources
~~~~~~~~~~~~~~~~~~~~~~

Tell setuptools to use these versions that you have just checked out
via Mercurial:

* TurboGears 2 :

.. code-block:: bash

  (tg2dev)$ cd tg
  (tg2dev)$ python setup.py develop -i http://www.turbogears.org/2.1/downloads/current/index

* TurboGears 2 developer tools:

.. code-block:: bash

  (tg2dev)$ cd ../tgdevtools
  (tg2dev)$ python setup.py develop -i http://www.turbogears.org/2.1/downloads/current/index

Source Install Via Pip
~~~~~~~~~~~~~~~~~~~~~~

This command tells PIP to install the two "trunk" distributions for the TurboGears
project as "editable" versions using the Mercurial URLs provided.

.. code-block:: bash

   $ easy_install pip sqlalchemy
   $ pip install -i http://www.turbogears.org/2.1/downloads/current/index -E tg2env \
        -e 'hg+http://bitbucket.org/turbogears/tg-dev/#egg=TurboGears2' \
        -e 'hg+http://bitbucket.org/turbogears/tgdevtools-dev/#egg=tg.devtools'
