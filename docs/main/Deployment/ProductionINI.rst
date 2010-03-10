.. _deploy_ini:

Production Config
=================

Your production config file looks much like your `development.ini` file,
but you will generally need to make a number of changes to make your config
"production ready".  There are a lot of warnings in this document because
there are a lot of ways to seriously compromise your security by
mis-handling or mis-configuring a `production.ini` file.

.. note::
   Throughout this document we'll refer to this file as `production.ini`.
   The file can be named anything you like, and there can be multiple versions,
   such as having `myapp-staging.ini` and `myapp-production.ini` to
   configure two different deployment branches of your application.

.. warning::

   You must *never* check your `production.ini` files into a
   publicly-accessible source-code control system!
   Doing so will violate your web-site's and potentially your
   server's security!  See :ref:`deploy_ini_scc`

Set debug=false
----------------

.. warning::

   You **MUST** set debug=false in your `production.ini`, Paste
   in debug mode provides interactive debugging which allows
   any user of the site to run arbitrary Python code!  This must **never**
   happen on a production site (or even a development site which is
   exposed to other machines), as it will give any visitor to the
   site complete control of your server.

In your configuration, you will find a line that looks like this in the
[DEFAULT] section:

.. code-block:: ini

   [DEFAULT]
   ...
   # WARNING == If debug is not set to false, you'll get the interactive
   # debugger on production, which is a huge security hole.
   debug = false

be *absolutely* sure that debug is set to false.  Similarly, there will
be another line (normally further down the file, in the app:main section)
which looks like this:

.. code-block:: ini

   [app:main]
   ...
   # WARNING: *THE LINE BELOW MUST BE UNCOMMENTED ON A PRODUCTION ENVIRONMENT*
   # Debug mode will enable the interactive debugging tool, allowing ANYONE to
   # execute malicious code after an exception is raised.
   set debug = false

again, be *absolutely* sure that `set debug = false` is uncommented and that
the value is false (not true).

Set full_stack to False
-----------------------

This is another security-related configuration element.  You should not
expose a full_stack enabled application to the Internet.

.. code-block:: ini

   [app:main]
   ...
   full_stack = false

.. todo:: verify whether this is still necessary in TurboGears |version|

Set Your Production Database URL
---------------------------------

You will need to alter the SQLAlchemy database URL to reflect your production
database.  See :ref:`deploy_db`.

.. warning::
   Keep in mind that anyone who has access to
   this file will now be able to connect to your database.  The
   SQLAlchemy URL includes the username and password to log in as
   your DB user.

   See :ref:`deploy_ini_scc`

Change Your Keys
----------------

There are a number of "private keys" configured in the config file.  You should
update each of these to a new value.  At minimum, the following keys should
be updated:

.. code-block:: ini

    [sa_auth]
    cookie_secret = long-string-of-digits-here

    [app:main]
    beaker.session.secret = long-string-of-digits-here

These values should not be shared.  See :ref:`deploy_ini_scc`

.. _deploy_ini_beaker:

Check File-Storage Locations
----------------------------

..  warning::

    This section does not apply if you are :ref:`deploying your code <deploy_code>`
    using an :ref:`egg <tgeggdeployment>` (which is the :ref:`deploy_standard`).
    It likely applies if you :ref:`deploy_checkout`.

You may be planning to replace your entire application checkout directory every time
you re-deploy your application, so things such as persistent session-storage,
and cache directories should be located outside your checkout.  By default the
quick-started application will use %(here)s variables to control where the
cache and session data is stored.  If your production.ini is in your source-code
checkout (see :ref:`deploy_ini_scc` for issues with this), this will be a
directory that will potentially be deleted frequently, and you will need to
specify an alternate location.

The appropriate location for application data-storage is somewhat open to
sysadmin preference, but a good default choice would be
`/var/local/myappname`, which would require config lines like this:

.. code-block:: ini

   [app:main]
   ...
   beaker.session.data_dir = /var/local/myapp/sessions
   beaker.cache.data_dir = /var/local/myapp/cache
   beaker.cache.lock_dir = /var/local/myapp/locks

You will need to create these directories and make them writable by the
www-data user.

See :ref:`caching` and :ref:`session` for discussions of the Beaker system
along with alternative deployment options, such as the use of :ref:`memcache`.

See :ref:`deploy_code`.

Check Log-file Options
----------------------

Generally speaking you will want to store your log files in the standard log
hierarchy for production systems.  You will also likely want to configure the
log files to use a `logging.handlers.RotatingFileHandler` to prevent your
application log-files from filling up your server's hard-disk.

.. code-block:: ini

   [handler_logfile]
   class = logging.handlers.RotatingFileHandler
   args = ('/var/log/myapp/myapp.log', 'a',1024*1024*50,3)
   level = WARN
   formatter = generic

You may want to set up multiple log-files with different logging levels
configured, or split out a particular type of log (such as access logs)
into a separate file.

You'll want to reduce the SQLAlchemy logging level to WARN in most cases:

.. code-block:: ini

   [logger_sqlalchemy]
   level = WARN

You will want to be sure that the /var/log/myapp directory exists, and is
writable by the www-data user.

.. code-block:: bash

   $ sudo mkdir /var/log/myapp
   $ sudo chown www-data:www-data /var/log/myapp

See :ref:`config_logging` for more details.

.. _deploy_ini_mountpoint:

Configure Proxy Mount Point
---------------------------

..  warning:: This section **only** applies to "proxied" sites, which are
    *not* part of the :ref:`deploy_standard`.

If you are **not** mounting your application at the root of your site
(i.e. you are mounting your application as a sub-site of some larger site)
**and** are using a non-embedded WSGI environment (such as a reverse proxy)
then you will need to configure TurboGears so that it knows how to
resolve application URLs from that base URL.

.. code-block:: ini

  # DO NOT DO THIS WITH MOD-WSGI!
  [app:main]
  ...
  filter-with = proxy-prefix

  [filter:proxy-prefix]
  use = egg:PasteDeploy#prefix
  prefix = /wherever_your_app_is mounted

See the `PasteDeploy Documentation`_ for details on the prefix middleware
being configured here.

.. _`PasteDeploy documentation`: http://pythonpaste.org/deploy/modules/config.html

Test your Config
-----------------

Your paster config-file is a regular config-file, and often you can run
it with the `Paste` web-server.  Keep in mind that your config file will
likely specify file-paths that only the www-data user can write to, so
you will likely need to run paster as the www-data user:

.. code-block:: bash

   $ sudo -u www-data server production.ini

.. _deploy_ini_scc:

Check In Your Config
--------------------

.. warning::

   Your `production.ini` contains secrets, keys, passwords, and everything
   else an attacker would need to crack your application and potentially
   your server.  Never check it into a publicly readable repository!
   Particularly, if you run an Open Source project, *never* check your
   `production.ini` into the main repository!

You will want to check your `production.ini` into source-code
control of some form, but before you add it to your project's
source-code project, consider the security implications of doing so.

Your production.ini includes your application's database connection
parameters (the SQLAlchemy URL).  If your organization's policies
preclude developers from having access to such information, you cannot
check the files into the project.  Even if they don't, if your database
is likely to hold personal, financial or other sensitive information,
you may find it prudent to store the `production.ini` in a separate
location so that the information can be controlled.

If you have a dedicated sysadmin team, they will often have a preexisting
configuration management system which can be used to store the
production.ini file.

.. note:: If *you* are your organization's entire technical team, you can
   likely check your `production.ini` directly into your application's
   repository, as long as that repository is not shared publically.

What's Next?
------------

* :ref:`deploy_db` -- you will normally have to run `paster setup-app` with your
  `production.ini` in order to initialize your database
* :ref:`deploy_modwsgi_deploy` -- if you are using the :ref:`deploy_standard`
  you will need to move your production.ini to expected location
