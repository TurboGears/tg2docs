.. _modwsgi_tutorial:

==========================================================
Running a TurboGears under Apache with ``mod_wsgi``
==========================================================

``mod_wsgi`` is an Apache module developed by Graham Dumpleton.
It allows ``WSGI`` programs to be served using the Apache web
server.

This guide will outline broad steps that can be used to get a TurboGears
application running under Apache via ``mod_wsgi``.

#.  The tutorial assumes you have Apache already installed on your
    system.  If you do not, install Apache 2.X for your platform in
    whatever manner makes sense.

#.  Once you have Apache installed, install ``mod_wsgi``.  Use the
    (excellent) `installation instructions
    <http://code.google.com/p/modwsgi/wiki/InstallationInstructions>`_
    for your platform into your system's Apache installation.

#.  Create a virtualenvironment with the specific TurboGears version
    your application depends on installed.

    .. parsed-literal::

        $ virtualenv /var/tg2env
        $ /var/tg2env/bin/pip install |private_index_path| tg.devtools

#.  Activate the virtualenvironment

    .. code-block:: bash

        $ source /var/tg2env/bin/activate
        (tg2env)$ #virtualenv now activated

#.  Install your TurboGears application.

    .. code-block:: bash

       (tg2env)$ cd /var/www/myapp
       (tg2env)$ python setup.py develop

#.  Within the application director, create a
    script named ``app.wsgi``.  Give it these contents:

    .. code-block:: python

        APP_CONFIG = "/var/www/myapp/myapp/production.ini"

        #Setup logging
        import logging.config
        logging.config.fileConfig(APP_CONFIG)

        #Load the application
        from paste.deploy import loadapp
        application = loadapp('config:%s' % APP_CONFIG)

#.  Edit your Apache configuration and add some stuff.

    .. code-block:: apache

        <VirtualHost *:80>
            ServerName www.site1.com

            WSGIProcessGroup www.site1.com
            WSGIDaemonProcess www.site1.com user=www-data group=www-data threads=4 python-path=/var/tg2env/lib/python2.7/site-packages
            WSGIScriptAlias / /var/www/myapp/app.wsgi

            #Serve static files directly without TurboGears
            Alias /images /var/www/myapp/myapp/public/images
            Alias /css /var/www/myapp/myapp/public/css
            Alias /js /var/www/myapp/myapp/public/js

            CustomLog logs/www.site1.com-access_log common
            ErrorLog logs/www.site1.com-error_log
        </VirtualHost>

#.  Restart Apache

    .. code-block:: bash

       $ sudo apache2ctl restart

#.  Visit ``http://www.site1.com/`` in a browser to access the application.

See the `mod_wsgi configuration documentation
<http://code.google.com/p/modwsgi/wiki/ConfigurationGuidelines>`_ for
more in-depth configuration information.
