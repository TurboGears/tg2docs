.. _apache_mod_wsgi:

Apache Mod-WSGI
==================

The :ref:`deploy_apache` module `Mod-WSGI`_ provides a high-performance
environment in which to run TurboGears |version|.  It is part of the
:ref:`deploy_standard` which is recommended for new TurboGears users.

To install:

.. code-block:: bash

   $ sudo aptitude install apache2 libapache2-mod-wsgi

.. _`deploy_modwsgi_virtualenv`:

Mod-WSGI with VirtualEnv
------------------------

Mod-WSGI will create a new type of executable script and add a number
of Apache configuration directives which allow you to configure your
Mod-WSGI environment.  While you could, technically, use these scripts
as simple CGI-like scripts, we recommend using a :ref:`VirtualEnv`
based deployment pattern to allow you to install different versions of
packages for different applications or sites.

.. _`deploy_modwsgi_baseline`:

Baseline VirtualEnv
~~~~~~~~~~~~~~~~~~~

The recommended pattern for using Mod-WSGI with a :ref:`VirtualEnv`
is to create a "baseline" VirtualEnv which contains no packages at
all.  This "baseline" will be used to provide a "clean" environment
on top of which your application's environment will be layered.
(This done with the Apache `WSGIPythonHome` directive).

.. code-block:: bash

   $ sudo mkdir /usr/local/pythonenv
   $ cd /usr/local/pythonenv
   $ sudo virtualenv --no-site-packages BASELINE
   $ sudo chown -R www-data:www-data BASELINE

.. note::

   The "baseline" pattern works around limitations in the Mod-WSGI
   module which have been fixed in later versions of the module.
   However, the commonly-packaged versions of the module require
   these work-arounds to work reliably, so for now, we recommend
   this pattern for all new users.

.. _`deploy_modwsgi_appenv`:

Application-Specific VirtualEnv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you can create your application-specific VirtualEnv (normally
in the same `pythonenv` directory).

.. code-block:: bash

   $ sudo virtualenv --no-site-packages myapp
   $ sudo chown -R www-data:www-data myapp
   $ sudo -u www-data bash
   $ cd myapp
   $ source bin/activate
   $ easy_install -i http://www.turbogears.org/2.1/downloads/current/index tg.devtools
   $ mkdir python-eggs
   $ exit

.. note::

   The python-eggs directory is used by Mod-WSGI to unpack "zipped" eggs which
   contain binary extensions (.so files).  Python cannot load those packages
   unless they are on the file-system.  Configuring this directory will be
   automatically done in the .wsgi file created by the
   :ref:`deploy_modwsgi_deploy`.

Your application's lib/pythonX.X/site-packages directory will be added to the
WSGI environment's path via a `WSGIPythonPath` directive, and will be moved
to the front of the PythonPath by the .wsgi script in order to make it the
dominant source for packages.

.. note::

   You can use any VirtualEnv installation mechanism you like to set up
   the application's VirtualEnv.  See :ref:`altinstall` for other options
   such as PIP.  In particularly you may want to use a mechanism that
   allows you to explicitly control which packages are installed and
   keep local copies of them to prevent external dependencies.

.. warning::

   The tg.devtools package does *not* automatically install all of the
   dependencies of a QuickStarted TurboGears |version| package.  Your
   package should declare its dependencies so that when it is installed
   into the VirtualEnv it will pull in the required dependencies!

   See :ref:`deploy_code`

.. _`deploy_modwsgi_deploy`:

modwsgi_deploy Helper Script
----------------------------

While you can generate your Apache site-configuration files by
hand, new users will generally find this a somewhat daunting task.
The modwsgideploy project provides a small helper script which
has parameterized helper scripts which can generate an initial
Apache Mod-WSGI configuration file and .wsgi script.

.. code-block:: bash

   (tg2env)$ easy_install bzr
   (tg2env)$ bzr branch http://bazaar.launchpad.net/~mcfletch/modwsgideploy/parameterized/
   (tg2env)$ cd parameterized/trunk
   (tg2env)$ python setup.py develop
   (tg2env)$ paster modwsgi_deploy --help

.. code-block:: bash

   (tg2env)$ easy_install modwsgideploy
   (tg2env)$ paster modwsgi_deploy --help

.. todo:: When we have the branch integrated, replace with easy_install modwsgideploy

the script is heavily parameterized to allow you to configure your
site as desired.  If you want your site to be available as a sub-directory
of your main site, you can specify a mount-point (the default is /projectname).
If you want to set up VirtualHost support (where your server looks at the
requested host-name to determine which site to display), you can specify
the server-name on the command-line.

The script will create a directory (by default ./apache) which will contain
the .wsgi script and an Apache configuration file.  It will also (likely)
log a number of warnings telling you how to create your :ref:`deploy_modwsgi_baseline`,
your :ref:`deploy_modwsgi_appenv`, where to copy/checkout your project code,
and where to put your production config file.

The files generated will look like this::

    myapp
    |-- apache
    |   |-- README.txt
    |   |-- myapp
    |   |-- myapp.wsgi
    |   `-- test.wsgi

You should review and/or edit the generated files.  See the
:ref:`deploy_modwsgi_refs` for documentation on the contents of these
files.

.. note:: The config files assume that your application is deployed in the
   deployment location (`/usr/local/turbogears/` by default) in a directory
   named `myapp` with the config-file (`production.ini` by default) in that
   directory. The application's directory will be added to the PYTHONPATH,
   as will the VirtualEnv's directory.

   * See :ref:`deploy_ini`
   * See :ref:`deploy_code`

When you are finished, you can continue on to :ref:`deploy_apache_enable`.

Possible Issues
----------------

Print Statements
~~~~~~~~~~~~~~~~

If you have used print statements anywhere in your codebase, you can
expect your Mod-WSGI applications to crash.  Mod-WSGI will error out
if there is *any* attempt to write to stdout (which is what print does
by default).  Use the logging module instead of print throughout
your codebase.

Widget Resource Race Condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In multiple process load balanced deployments (such as this one) it is
very possible that a given request will pull resources from multiple
processes.

You may want to make sure that the TG controllers are loaded up even
before the first request comes in to handle this, so you should add::

  import paste.fixture
  app = paste.fixture.TestApp(application)
  app.get("/")

to the end of the wsgi-script that starts your application.

This will fetch the index page of your app, thus assuring that it's
ready to handle all of your requests immediately.  This avoids a
problem where your controller page is not yet loaded so widgets aren't
initialized, but a request comes in for a widget resource the
ToscaWidgets middleware doesn't have registered yet.

.. _`deploy_modwsgi_refs`:

References
----------
* `Mod-WSGI`_ the official home of the extension, including documentation
* `Mod-WSGI and VirtualEnvironments`_ discusses the recommended usage
  pattern and the various options involved
* `Mod-WSGI and Pylons`_ discusses the usage pattern with focus
  on how to integrate Pylons applications (TurboGears is built on Pylons)

What's Next
------------

* :ref:`deploy_apache_enable` enabling (running) your Apache ModWSGI site
* :ref:`deploy_standard` provides an overview of the recommended
  deployment pattern
* :ref:`deploy_apache` discusses alternatives to Mod-WSGI under Apache

.. _`Mod-WSGI`: http://code.google.com/p/modwsgi/
.. _`Mod-WSGI and VirtualEnvironments`: http://code.google.com/p/modwsgi/wiki/VirtualEnvironments
.. _`Mod-WSGI and Pylons`: http://code.google.com/p/modwsgi/wiki/IntegrationWithPylons
