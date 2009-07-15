How to install TurboGears 2
===========================

This document provides several methods of installing TurboGears; the method you choose will depend on your level of experience and platform.

We recommend installing TurboGears 2 into a virtual environment which will prevent any interference with your system's installed packages and won't unknowingly upgrade any python libraries that your system needs.

If you want to build packages of TurboGears for your system please send an email to turbogears-trunk@googlegroups.com

Prerequisites for all methods
------------------------------

  1. Python
  2. Setuptools
  3. Database & Drivers
  4. other dependencies
  5. virtualenv

Python
~~~~~~~~

.. todo:: Write missing docs for installing tg2 using python 2.4 and python 2.6

TurboGears works with any version of python between 2.4 and 2.6. The most widely deployed version of python at the moment of this writing is version 2.5.  Both python 2.4 and python 2.6 require additional steps which will be covered in the appropriate sections.  Python 3.0 is currently unsupported due to lack of support in many of our upstream packages.

We recommend you use your system's default python install or follow the instructions provided here: http://python.org/download/

If you don't know which version of python you have installed you can find out with the following command:

.. code-block:: bash

   $ python --version
   Python 2.5.2

Installing setuptools
~~~~~~~~~~~~~~~~~~~~~~

On Windows
""""""""""

download http://peak.telecommunity.com/dist/ez_setup.py and then run it from the command line.

On Unix
""""""""

.. code-block:: bash

    $ wget http://peak.telecommunity.com/dist/ez_setup.py | sudo python

You may also use your system's package for setuptools.

On Unix (non-root)
""""""""""""""""""

TODO

Post Install
""""""""""""""

.. hint:: 
   You most likely want setuptools 0.6c9 or greater as this one provides fixes to work with svn1.5.  If you ever get an error regarding 'log' please run:
   
   $ easy_install -U setuptools

To confirm this worked run:
   
.. code-block:: bash

    $ python 
    >>> import setuptools
    >>> setuptools.__version__
    '0.6c9'

Installing Database and Drivers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. hint::
    The installation of the database backend is a topic outside of the scope of this document.

TurboGears uses SQLAlchemy as its default ORM (Object Relational Mapper) layer.  SQLAlchemy maintains excellent documentation on all the `engines supported`_.

Python 2.4 users will also need to install pysqlite_ themselves in order to use the sqlite database in the default configuration

.. _engines supported: http://www.sqlalchemy.org/docs/05/reference/dialects/index.html
.. _pysqlite: http://pypi.python.org/pypi/pysqlite/

Cygwin users can't use sqlite as it does not include the necessary binary file (``sqlite3.dll``).  If you want to run Cygwin you'll need to install a different database.

Installing non python dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will most likely need a C compiler and the python header files. Please see the appropriate section below.

Windows
""""""""

We include pre-compiled binaries for windows in our package index.

If you want to help us keep all binaries up to date please write to turbogears-trunk@googlegroups.com to become part of our windows egg building team

You may also want the `win32api`_ package as it provides some very useful tools for windows developers, the first you will encounter is the ability to make virtualenv work with paths that contain spaces.

.. _win32api: http://starship.python.net/crew/mhammond/win32/

See also pylunch

See also windows installer

Cygwin
"""""""
You must perform all operations, including setup operations, within DOS command windows, not Cygwin command window.

MacOS
""""""
Xcode is required to build some binary dependancies and is available on the OS X CD or at http://developer.apple.com/tools/xcode/.

Debian, Ubuntu 
"""""""""""""""
Debian derived Linux versions require ``python-dev`` and ``build-essential``::

    $ apt-get install python-dev
    $ apt-get install build-essential

RedHat, Fedora, CentOS
""""""""""""""""""""""""
Fedora users will need the ``python-devel`` rpm::

    $ yum install python-devel

Gentoo
"""""""

Nothing extra is required as Gentoo has a full development environment configured by default.

other Linux and unix
""""""""""""""""""""""

You'll need a working version of the GCC compiler installed, as well as the Python headers.  

Installing Virtualenv
~~~~~~~~~~~~~~~~~~~~~~~

We strongly advise you to install all your TurboGears apps inside a virtualenv.  If you ask for support without a virtualenv to isolate your packages we will usually ask you to go get virtualenv before proceeding further.

``virtualenv`` is a tool that you can use to keep your Python path clean and tidy.  It allows you to install new packages and all of their dependencies into a clean working environment, thus eliminating the possibility that installing turbogears or some other new package will break your existing Python environment.

The other great advantage of virtualenv is that it allows you to run multiple versions of the same package in parallel which is great for running both the production version and the development version of an application on the same machine.

People with a sys-admin background could consider virtualenv as a variation of an OS jail (chroot) which is also good for security as your installation is totally isolated. This makes virtualenv great for deploying production sites.

installing ``virtualenv``:

On Windows::

    easy_install virtualenv

On Unix:

.. code-block:: bash

    $ sudo easy_install virtualenv

On Unix (non-root):

.. code-block:: bash

    $ easy_install --install-dir=$HOME/lib/python2.5/ --script-dir=$HOME/bin/ virtualenv

will output something like:

.. code-block:: text

    Searching for virtualenv
    Reading http://pypi.python.org/simple/virtualenv/
    Best match: virtualenv 1.3.2
    Downloading http://pypi.python.org/packages/2.5/v/virtualenv/virtualenv-1.3.2-py2.5.egg#md5=1db8cdd823739c79330a138327239551
    Processing virtualenv-1.3.2-py2.5.egg
    .....
    Processing dependencies for virtualenv
    Finished processing dependencies for virtualenv

Installing TurboGears
------------------------

We provide several methods for installing TurboGears which depend on the level of control you want over it 

    1. tutorial (still not complete)
    2. tg2-bootstrap.py
    3. plain virtualenv
    4. using pip (experimental)
    5. development version


.. hint::
    Please note we are using ``tg2env`` as the name of the virtual environment.  This is simply a convention in our documentation, the name of the virtualenv depends totally on the user and should be named according to the project it contains.

Automatic Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~

If this is your first time using TurboGears you can use the bootstrap script.  `tg2-bootstrap.py` is a custom virtualenv script.  It will:

 * create a virtualenv for you 
 * install the latest TurboGears in it

Download and run the script with the following commands:

.. code-block:: bash

   wget http://www.turbogears.org/2.0/downloads/current/tg2-bootstrap.py
   python tg2-bootstrap.py --no-site-packages tg2env


Manual installation
~~~~~~~~~~~~~~~~~~~

First, ``cd`` to the directory where you want your virtual environment for TurboGears 2. Note the virtualenv will be created as a subdirectory here.

Now create a new virtual environment named `tg2env`

.. code-block:: bash

    $ virtualenv --no-site-packages tg2env

that produces something like this::

     Using real prefix '/usr/local'
     New python executable in tg2env/bin/python
     Installing setuptools............done.

Activate your virtualenv 
""""""""""""""""""""""""""

First go inside the virtualenv::

    $ cd tg2env

On Windows you activate a virtualenv with the command::

    Scripts\activate.bat

On Unix you activate a virtualenv with the command: 

.. code-block:: bash

    $ source bin/activate

If you are on Unix your prompt should change to indicate that you're in a virtualenv.
It will look something like this::

    (tg2env)username@host:~/tg2env$

The net result of activating your virtualenv is that your PATH variable now points to the tools in `tg2evn/bin` and your python will look for libraries in `tg2evn/lib`.

Therefore you need to reactivate your virtualenv every time you want to work on your ``tg2env`` environment. 

Install Turbogears 2
""""""""""""""""""""""""""

You'll be able to install the latest released version of TurboGears via:

.. code-block:: bash

    (tg2env)$ easy_install -i http://www.turbogears.org/2.0/downloads/current/index tg.devtools


.. warning :: if you are upgrading from a previous TG2 version your command should be:

    .. code-block:: bash

        (tg2env)$ easy_install -U -i http://www.turbogears.org/2.0/downloads/current/index tg.devtools

TurboGears and all of its dependencies should download and install themselves.
(This may take several minutes.)

Deactivating the environment
"""""""""""""""""""""""""""""

When you are done working simply run the ``deactivate`` virtualenv shell command::

    (tg2env)user@host:~/tg2env$ deactivate 
    user@host:~/tg2env$

This isn't really needed but it's good practice if you want to switch your shell to do some other work.

Installation using pip (experimental)
~~~~~~~~~~~~~~~~~~~~~~~~~~

`pip`_ (or pip installs packages) is an experimental easy_install replacement. It provides many improvements over it's predecessor and aims to be a full replacement.

.. warning::
   pip is not supported under windows!
   
Just add the ``--pip`` flag to the bootstrap script::

  $ python tg2-bootstrap.py --no-site-packages --pip tg2env
   
.. _pip: http://pypi.python.org/pypi/pip

Installing the Development Version of Turbogears 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Getting Subversion
"""""""""""""""""""""

    * All major Linux distributions have this installed. The package is normally named ``subversion``
    * On windows you can download the `Subversion installer`_

.. _Subversion installer: http://subversion.tigris.org/getting.html

Getting the source
""""""""""""""""""""

Check out the latest code from the subversion repositories:

.. code-block:: bash

  (tg2dev)$ svn co http://svn.turbogears.org/projects/tg.devtools/trunk tgdevtools
  (tg2dev)$ svn co http://svn.turbogears.org/trunk tg2

Installing the sources
"""""""""""""""""""""""""

Tell setuptools to use these versions that you have just checked out via SVN:

* TurboGears 2 :

.. code-block:: bash

  (tg2dev)$ cd tg2
  (tg2dev)$ python setup.py develop

* TurboGears 2 developer tools:

.. code-block:: bash

  (tg2dev)$ cd ../tgdevtools
  (tg2dev)$ python setup.py develop

Source install via pip
"""""""""""""""""""""""""

use the ``--trunk`` flag to the bootstrap script::

  $ python tg2-bootstrap.py --no-site-packages --trunk tg2env

or install via pip manually 

.. code-block:: bash

   $ easy_install pip
   $ pip install -e svn+http://svn.turbogears.org/trunk
   $ pip install -e svn+http://svn.turbogears.org/projects/tg.devtools/trunk

Validate the installation
---------------------------

To check if you installed TurboGears 2 correctly, type

.. code-block:: bash

    (tg2env)$ paster --help

and you should see something like::

    Usage: paster [paster_options] COMMAND [command_options]

    Options:
      --version         show program's version number and exit
      --plugin=PLUGINS  Add a plugin to the list of commands (plugins are Egg
                        specs; will also require() the Egg)
      -h, --help        Show this help message

    Commands:
      create       Create the file layout for a Python distribution
      help         Display help
      make-config  Install a package and create a fresh config file/directory
      points       Show information about entry points
      post         Run a request for the described application
      request      Run a request for the described application
      serve        Serve the described application
      setup-app    Setup an application, given a config file

    TurboGears2:
      quickstart   Create a new TurboGears 2 project.
      tginfo       Show TurboGears 2 related projects and their versions

Notice the "TurboGears2" command section at the end of the output  -- this indicates that turbogears is installed in your current path.

Paster has replaced the old tg-admin command, and most of the tg-admin commands
have now been re-implemented as paster commands. For example, ``tg-admin quickstart``
command has changed to ``paster quickstart``, and ``tg-admin info`` command
has changed to ``paster tginfo``.

For a full list of turbogears commands see `Command Line reference <CommandLine.html>`_

What's next?
============

If you are new to turbogears you will want to continue with the `Quick Start Guide <QuickStart.html>`_

If you are a TG1 user be sure to check out our `What's new in TurboGears 2.0 <WhatsNew.html>`_ page to get a picture of what's changed in TurboGears2 so far.

.. todo:: Review this file for todo items.

