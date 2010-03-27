.. _deploy_apache:

Apache Web Server
==================

.. warning::

   You are deploying a web application.  This is an inherently risky
   process.  Apache, as with any other web-server, can be configured
   incorrectly to compromise the security of your machine.  You need
   to either become very familiar with Apache or rely on someone who
   is to keep your installation safe.  At a minimum you need to be
   sure that you update your server with security patches in a timely
   manner!

Apache is the most widely-deployed web-server on the planet, and it
is `well documented <Apache docs>`_.  This document simply introduces you to the
various features of the server and gives you an idea of how it is
normally used with TurboGears |version|.

.. note::
   Apache is part of the :ref:`deploy_standard` for TurboGears |version|.
   TurboGears uses the WSGI interface, which can be supported by Apache
   in a number of ways.  The mod_wsgi extension is the recommended
   implementation for new TurboGears users.

Installation
-------------

All major Linux platforms package Apache such that it can be
installed with a simple package-manager command.  For Debian/Ubuntu
machines this command looks like this:

.. code-block:: bash

    sudo aptitude install apache2

.. todo:: document Fedora/RHEL installation

which will install Apache and configure it to start automatically
on system startup.  Apache is configurable via a series of config
files installed in (normally) `/etc/apache2` with the directories
`sites-available` and `sites-enabled` being the two most commonly
altered.

Deployment Patterns
--------------------

Normally in an Apache deployment Apache is configured to serve your
application's static files folder directly.  This provides a
significant performance advantage over having TurboGears serve these
files.  Apache accesses the files directly from the disk and serves
them without needing to load them into memory all at once.

Similarly, Apache will tend to be used to provide the SSL encryption
layer for SSL-using sites.  Apache's SSL implementation is reasonably
fast and robust, and setup of SSL is well documented for the server.

WSGI Environment
------------------

There are 2 major strategies for providing TurboGears with a WSGI
environment using Apache.  The first is to embed TurboGears into the
Apache process with a "captive" WSGI-supporting module.  For this
strategy:

* Apache will manage the lifetime of your TurboGears application
* Normally to restart your application you will have to restart the Apache server
* Your code needs to be executable by the Apache user, normally `www-data`
* Your data directories need to be readable/writable by the Apache user
* The environment is somewhat restrictive (for instance, you cannot print to stdout)

There are two implementations of this strategy:

* :ref:`mod_wsgi <apache_mod_wsgi>` -- The
  mod_wsgi apache extension is a very efficient WSGI server, which
  provides automatic process monitoring, load balancing for
  multi-process deployments, as well as strong apache integration.
  **Strongly recommended** for new users, and is the
  :ref:`deploy_standard` for TurboGears |version|.
* :ref:`FastCGI <FastCGI>` -- when apache extensions are not an option
  due to web host restrictions (for example, admins want to run suexec on
  all userspace scripts), you can create a FastCGI dispatcher that invokes
  the WSGI interface.  Generally you should *not* use this mechanism unless
  no other mechanism is available.

The second strategy for deploying WSGI with Apache is to have
Apache "reverse proxy" or "redirect/rewrite" requests that come in on
the main port (80) to a separate TurboGears server process which is
running on a "high port" (for example, port 8080) solely on the
localhost (private) interface.  For this strategy:

* you are responsible for keeping your TurboGears process running, starting
  it at boot, and generally making sure that it can receive the requests
  from the Apache server.  See :ref:`deploy_daemon`.
* You can run the TurboGears process as any user you like, and you can even
  run it in a "screen" session during development
* You can easily restart the TurboGears process

There are two implementations of this strategy in Apache:

* :ref:`mod_proxy <apache_mod_proxy>` -- The mod_proxy
  extension provides a simple to set-up apache environment that
  proxies HTTP requests to your TurboGears |version| app.  It can
  be used to load balance across multiple machines.

* mod_rewrite -- Very similar to mod_proxy
  (in fact from the TurboGears side they are identical), but
  mod_rewrite can be somewhat more complex to setup.

.. _`deploy_apache_enable`:

Enable Your Apache Site
-----------------------

Once you have:

* setup your (:ref:`mod_wsgi <apache_mod_wsgi>`) environment
* :ref:`Deployed your Database <deploy_db>`
* :ref:`Deployed your Code <deploy_code>`
* :ref:`Created your Production INI <deploy_ini>` (including testing with the paster server)
* Tweaked your Apache config

You can copy the Apache config file to your Apache `sites-available`
directory, enable it, and restart Apache.

.. code-block:: bash

   $ sudo cp myapp/apache/myapp /etc/apache2/sites-available
   $ sudo chown root:root /etc/apache2/sites-available/myapp
   $ sudo a2ensite sitename
   $ sudo apache2ctl configtest
   $ sudo apache2ctl restart

You should now be able to load your site at the configured location
(by default `http://localhost/myapp`).  If your site doesn't appear,
check the Apache error log:

.. code-block:: bash

   $ less /var/log/apache2/error.log

normally either your Python application will have encountered an error
in the .wsgi script.  Pay particular attention to the PYTHONPATHS,
as this is one of the most common issues that prevents your site from
running.

What's Next
------------

* :ref:`mod_wsgi <apache_mod_wsgi>` -- the recommended deployment environment for Apache
* :ref:`deploy_standard` -- gives an overview of the standard installation pattern
* `Apache docs`_ -- the official Apache documentation

.. _`Apache docs`: http://httpd.apache.org/docs/
.. _`supervisord`: http://supervisord.org/
.. _`upstart`: http://upstart.ubuntu.com/
