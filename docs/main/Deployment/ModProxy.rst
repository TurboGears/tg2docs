.. _apache_mod_proxy:

Running TurboGears |version| behind Apache with Mod Proxy
=========================================================

By running your TurboGears |version| application behind
:ref:`Apache <deploy_apache>` you can take advantage of Apache's
HTTPS abilities or have it serve your static files, but keep your
Paste server independent of the Apache server.

This can allow, for instance, wsgi applications to be run as
regular Unix users instead of under the www-data user account.

.. note:: We recommend the use of :ref:`apache_mod_wsgi` where
   possible, as it is part of the :ref:`deploy_standard` and
   should provide better performance in general.

TurboGears Configuration
------------------------

..  warning::
    You will need a :ref:`deploy_ini` for your application.  There
    are significant security implications to a Production Config file,
    do **not** just copy your development.ini file!

If you are not mounting your application at the "root" of your site,
you will need to configure a proxy filter in your `production.ini` file.
See :ref:`deploy_ini_mountpoint` for details.

Apache Configuration
--------------------

Here is how to configure Apache 2 as a reverse proxy for your
TurboGears2 application.

In Apache's ``httpd.conf`` uncomment the ``mod_proxy`` modules::

    LoadModule proxy_module modules/mod_proxy.so
    LoadModule proxy_connect_module modules/mod_proxy_connect.so
    LoadModule proxy_http_module modules/mod_proxy_http.so
    LoadModule proxy_balancer_module modules/mod_proxy_balancer.so

Also note, depending on your distribution, you first might need to
install the ``apache-mod_proxy`` packages.

In the virtual hosts section of the ``httpd.conf`` file or in the
include file for your virtual host (e.g. ``httpd-vhosts.conf``, but
make sure this is loaded), you would want to have something like this
for your site (adapt the server name, admin, log locations etc.)::

    NameVirtualHost *

    <VirtualHost *>
        ServerName mytgapp.blabla.com
        ServerAdmin here-your-name@blabla.com
        #DocumentRoot /srv/www/vhosts/mytgapp
        Errorlog /var/log/apache2/mytgapp-error_log
        Customlog /var/log/apache2/mytgapp-access_log common
        UseCanonicalName Off
        ServerSignature Off
        AddDefaultCharset utf-8
        ProxyPreserveHost On
        ProxyRequests Off
        ProxyPass /error/ !
        ProxyPass /icons/ !
        ProxyPass /favicon.ico !
        #ProxyPass /static/ !
        ProxyPass / http://127.0.0.1:8080/
        ProxyPassReverse / http://127.0.0.1:8080/
    </VirtualHost>

Uncomment the ``DocumentRoot`` and ``ProxyPass /static/`` lines if you
want to serve the directory with static content of your TurboGears
application directly by Apache. You will then also need to copy or
link this directory to the configured ``DocumentRoot`` directory.

Check that your Apache configuration has no problems::

    apachectl -S

or::

    apachectl configtest

If everything is ok, run::

        apachectl start

Finally, go to your TurboGears project directory and in a console
run::

        paster serve production.ini

.. note:: The above command assumes you have created a config file named ``production.ini``.

Now you should be able to see your webpage in full TurboGears glory at
the address configured as ``ServerName`` above.

Setting The Correct Charset
---------------------------

The default templates used by TurboGears specify ``utf-8`` as a
charset.  The Apache default charset, returned in the ``Content-Type``
header, is ``ISO-8859-1``.  This inconsistency will cause errors
during validation and incorrect rendering of some characters on the
client. Therefore we used the ``AddDefaultCharset utf-8`` directive
above to override the Apache default in the TurboGears virtual host
section.

TurboGears |version| also automatically sets the charset property by
modifying the ``Content-type`` HTTP header on each request that
returns ``text/*`` or ``application/json`` content types. Apache
notices this pre-existing header and passes it through.
