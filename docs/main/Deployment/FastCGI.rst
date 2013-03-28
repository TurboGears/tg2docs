.. _FastCGI:

FastCGI/WSGI -- Running TurboGears |version| behind Apache
==========================================================

..  warning::
    We recommend that, where possible, you use :ref:`apache_mod_wsgi`
    as that is part of the :ref:`deploy_standard`

FastCGI is an appropriate choice when:

* mod_wsgi and mod_python are not available
* you cannot run the Pylons/Paste web-server directly on port 80 (likely
  because Apache is already running on port 80)
* mod_fcgi and mod_rewrite *are* available (common)

Because TurboGears implements the WSGIServer interface, we can use
`flup`_ to interface between FastCGI and Pylons.  We'll also show you
how to use :ref:`virtualenv` in this setup.

Apache Configuration
--------------------

Discussing what Apache directives should be set is beyond the scope of this
document, but `mod_fastcgi` and `mod_rewrite` should be enabled.  Most webhosts
have the latter enabled by default; some require you to explicitly enable
FastCGI via their control panel (Dreamhost is one such host).

Installation
------------

If you setup your own virtualenv according to the instructions on the
installation page, you will need to install `flup`_, with:

.. code-block:: bash

    $ easy_install flup

If you are not using virtualenv, check to see if flup is installed or not
with `import flup`.

.. _`flup`: http://trac.saddi.com/flup

Dispatch scripts
----------------

Keeping your TurboGears install in a web-accessible directory is strictly
unnecessary; the only files we will need to add to forward FastCGI are
`dispatch.fcgi` and an `.htaccess` file.

dispatch.fcgi
~~~~~~~~~~~~~

In the `dispatch.fcgi` file, you will need the following boilerplate code:

.. code-block:: python

    #!/usr/bin/env python
    turbogears = '/usr/local/turbogears/myapp'
    inifile = 'production.ini'
    import sys, os
    sys.path.insert(0, turbogears)
    from paste.deploy import loadapp
    wsgi_app = loadapp('config:' + turbogears + '/' + inifile
    if __name__ == '__main__':
        from flup.server.fcgi import WSGIServer
        WSGIServer(wsgi_app).run()

There are three locations in this file that you may need to edit:

1. The `turbogears` variable should be set to the location of your
   TurboGears codebase, i.e. where you can find such files as `development.ini`
   and `setup.py`

2. The `inifile` variable should be set to the name of the configuration file
   you would like to be loaded on this server.

3. The shebang line (`#!/usr/bin/env python`) should be modified to use
   the virtualenv Python interpreter, if you are using such an environment.

This loader file is different from the Pylons flup file, please be careful!
Also, you need to make this file executable, with::

    $ chmod 0755 dispatch.fcgi

.htaccess
~~~~~~~~~

You will need to add the following lines to your `.htaccess` file::

    Options +ExecCGI
    AddHandler fastcgi-script .fcgi
    RewriteEngine On
    RewriteRule   ^(dispatch\.fcgi/.*)$  - [L]
    RewriteRule   ^(.*)$  dispatch.fcgi/$1 [L]

You can also setup static content with an extra RewriteRule before the
last line:

    RewriteRule   ^(static/.*)$ - [L]

The first two lines (Options and AddHandler) may not be strictly necessary,
depending on your web server's configuration.

Proxy Mount Point Fix
~~~~~~~~~~~~~~~~~~~~~

Using this method, Turbogears/Pylons wrongly thinks that dispatch.fcgi
is a part of the URL. See :ref:`deploy_ini_mountpoint` for how to fix
this in your production.ini.

Maintenance
-----------

Checking if it worked
~~~~~~~~~~~~~~~~~~~~~

The most obvious metric for success is whether or not your site displays
on your browser. However, you can also check with `ps aux | grep dispatch`
to see if your FastCGI executable is still running.

Rebooting
~~~~~~~~~

Because FastCGI processes are persistent, even when you update your Python
files the old code will still be running.  Usually, the following command
from your shell will be sufficient to kill the process::

    $ killall -u username dispatch.fcgi

If dispatch.fcgi is running as the Apache user, i.e. www-data, you'll need
to create a short Python stub script to call from the web in order to execute
this command. (Also, your host is doing it wrong.)

Debugging
~~~~~~~~~

FastCGI is notoriously difficult to debug. There are variants of dispatch.fcgi
which add lots of informative debugging output; you can also rename the file
to dispatch.cgi and run as a CGI module (it will not be as fast, but will be
reloaded every request).
