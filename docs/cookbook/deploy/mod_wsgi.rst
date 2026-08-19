.. _modwsgi_tutorial:

==========================================================
Running TurboGears under Apache with ``mod_wsgi``
==========================================================

``mod_wsgi`` is an Apache module developed by Graham Dumpleton.
It allows ``WSGI`` programs to be served using the Apache web
server.

This guide outlines broad steps for running a TurboGears application under
Apache via ``mod_wsgi``. TurboGears application settings belong in the
application's deployment-specific ``.ini`` file; Apache and ``mod_wsgi``
settings belong in the Apache configuration.

#.  The tutorial assumes you have Apache already installed on your
    system. If you do not, install Apache 2.X for your platform in
    whatever manner makes sense.

#.  Once you have Apache installed, install ``mod_wsgi``. Use the
    `mod_wsgi installation instructions
    <https://modwsgi.readthedocs.io/en/develop/installation.html>`_ for
    your platform and Apache installation.

#.  Create a virtual environment with the TurboGears project dependencies
    installed.

    .. code-block:: bash

       $ python3 -m venv /var/tg2env
       $ /var/tg2env/bin/python -m pip install --upgrade pip
       $ /var/tg2env/bin/python -m pip install tg.devtools

#.  Activate the virtual environment and install your TurboGears application
    using the current project packaging commands.

    .. code-block:: bash

       $ source /var/tg2env/bin/activate
       (tg2env)$ cd /var/www/myapp
       (tg2env)$ python -m pip install -e .
       (tg2env)$ cp development.ini production.ini

    Edit ``production.ini`` and set ``debug = false`` in its ``[DEFAULT]``
    section. The generated ``development.ini`` enables debug mode; do not use
    that setting for a public deployment.

    .. code-block:: ini

        [DEFAULT]
        debug = false

#.  Within the application directory, create a script named ``app.wsgi``.
    Give it these contents:

    .. code-block:: python

        import logging.config
        import os

        from paste.deploy import loadapp

        APP_CONFIG = "/var/www/myapp/production.ini"

        logging.config.fileConfig(
            APP_CONFIG,
            {"__file__": APP_CONFIG, "here": os.path.dirname(APP_CONFIG)},
            disable_existing_loggers=False,
        )
        application = loadapp("config:%s" % APP_CONFIG)

    The ``application`` callable is the WSGI entry point that Apache loads.
    The explicit ``fileConfig`` call applies the logging sections in the
    PasteDeploy configuration before the application is created.

#.  Edit your Apache configuration and add the ``mod_wsgi`` settings. The
    ``python-home`` value selects the virtual environment; ``python-path``
    points at the installed project's source directory. The static aliases
    let Apache serve static files without sending them through TurboGears.

    .. code-block:: apache

        <VirtualHost *:80>
            ServerName www.site1.com

            WSGIProcessGroup www.site1.com
            WSGIDaemonProcess www.site1.com user=www-data group=www-data threads=4 python-home=/var/tg2env python-path=/var/www/myapp
            WSGIScriptAlias / /var/www/myapp/app.wsgi

            # Serve static files directly without TurboGears
            Alias /images /var/www/myapp/myapp/public/images
            Alias /css /var/www/myapp/myapp/public/css
            Alias /js /var/www/myapp/myapp/public/js

            CustomLog logs/www.site1.com-access_log common
            ErrorLog logs/www.site1.com-error_log
        </VirtualHost>

#.  Restart Apache so it loads the new WSGI entry point and daemon process.

    .. code-block:: bash

       $ sudo apache2ctl restart

#.  Visit ``http://www.site1.com/`` in a browser to access the application.

See the `mod_wsgi configuration documentation
<https://modwsgi.readthedocs.io/en/develop/configuration.html>`_ for
more in-depth configuration information.
