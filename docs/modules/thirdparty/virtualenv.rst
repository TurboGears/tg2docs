.. _virtualenv:

VirtualEnv
==========

``VirtualEnv`` is a tool that you can use to keep your Python path
clean and tidy.  It allows you to install new packages and all of
their dependencies into a clean working environment, thus eliminating
the possibility that installing turbogears or some other new package
will break your existing Python environment.

The other great advantage of VirtualEnv is that it allows you to run
multiple versions of the same package in parallel which is great for
running both the production version and the development version of an
application on the same machine.

People with a sys-admin background could consider VirtualEnv as a
variation of an OS jail (chroot) which is also good for security as
your installation is totally isolated. This makes VirtualEnv great for
deploying production sites.

We strongly advise you to install all your TurboGears apps inside a
VirtualEnv.  If you ask for support without a VirtualEnv to isolate
your packages we will usually ask you to go get VirtualEnv before
proceeding further.

Installing ``VirtualEnv``
-------------------------

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

Creating a VirtualEnv
---------------------

Basic VirtualEnv usage is as follows:

.. code-block:: bash

    $virtualenv example

Normally you will want to create a VirtualEnv which does not use system packages as
system packages can conflict with the TurboGears-installed packages.

.. code-block:: bash

    $virtualenv --no-site-packages example

You may also want to create a VirtualEnv that uses a version of Python other than the
default Python on your platform.

.. code-block:: bash

    $virtualenv -p python2.5 example

Activate Your VirtualEnv
------------------------

First go inside the VirtualEnv::

    $ cd tg2env

On Windows you activate a VirtualEnv with the command::

    Scripts\activate.bat

On UNIX you activate a VirtualEnv with the command:

.. code-block:: bash

    $ source bin/activate

If you are on Unix your prompt should change to indicate that you're
in a VirtualEnv.  It will look something like this::

    (tg2env)username@host:~/tg2env$

The net result of activating your VirtualEnv is that your PATH
variable now points to the tools in `tg2evn/bin` and your python will
look for libraries in `tg2evn/lib`.

Therefore you need to reactivate your VirtualEnv every time you want
to work on your ``tg2env`` environment.

Deactivating (Escaping) VirtualEnv
----------------------------------

On Win32, you deactivate the VirtualEnv via:

.. code-block:: bash

    Scripts\deactivate.bat

and on Linux:

.. code-block:: bash

    deactivate

Further Information
-------------------

The `VirtualEnv page` on PyPI provides links to usage, documentation
and the like.

.. _setuptools: http://pypi.python.org/pypi/virtualenv
