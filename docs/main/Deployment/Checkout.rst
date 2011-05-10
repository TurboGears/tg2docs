.. _deploy_checkout:

Deploy with a Source Code Checkout
==================================

.. note::

   This is *not* part of the :ref:`deploy_standard`, but is a commonly used
   alternative because of it uses familiar tools for most developers.

Assuming you are otherwise using the :ref:`deploy_standard`, the only change
involved in using a Source Code Checkout for your project instead of building
an egg is that you will check out the code (as the www-data user) and install
it using the `develop` option to setup.py.

.. code-block:: bash

   $ cd /usr/local/turbogears
   $ sudo -u www-data svn checkout file:///var/svn/myapp/production myapp
   $ cd myapp
   $ sudo -u www-data bash
   $ mkdir python-eggs
   $ source /usr/local/pythonenv/myapp/bin/activate
   $ python setup.py develop
   $ exit

by default modwsgi_deploy will have specified that `production.ini` is
in the root directory of this checkout. See :ref:`deploy_ini_scc` for
details on why you might **not** want that file to be checked into
your main repository.

Similarly, you will need to make sure that your Beaker session and cache
directories are not sub-directories of the source code checkout if you
are planning on deleting and re-checking-out the source for each release.
(See :ref:`deploy_ini_beaker` for details).
