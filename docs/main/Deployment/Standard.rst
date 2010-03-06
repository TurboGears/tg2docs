.. _deploy_standard:

Standard Deployment Pattern
===========================

This is the recommended deployment pattern for new users.  It is not
necessarily optimal for all projects, it is intended to provide a good
set of defaults from which to later customize:

* :ref:`deploy_apache` handling incoming http requests, Apache
  handles SSL and serving static files and can provide support for
  multiple sites on the same IP address (virtual hosts)
* :ref:`mod_wsgi <apache_mod_wsgi>` with :ref:`virtualenv` to host TurboGears
* standard :ref:`PostgreSQL` *or* :ref:`MySQL` database server installation
* :ref:`tgeggdeployment`

This uses the most common web server for Linux platforms (Apache), which
is well documented, robust, and widely available.  It also uses one of the
two most common Open Source databases which are again, well documented,
robust and widely available.  Using an egg to deploy your application means
that you can readily track your releases and revert to a previously released
version in the event of failure.

Deployment for the Impatient
----------------------------

* install Apache and your preferred database server
* install mod_wsgi for apache
* install modwsgideploy
* run paster modwsgi_deploy to generate template wsgi files
* edit template modwsgi files (apache/*yourproject*.wsgi)
* package your app as an egg
* create a BASELINE virtualenv in /usr/local/pythonenv
* create a new virtualenv based on BASELINE in /usr/local/turbogears
* install your egg into the new virtualenv
* change all of BASELINE and new virtualenv to www-data owner
* create a production.ini
  * make sure you set debug=False
  * setup database link
  * run your initial ``paster setup-app``
  * check into your etc tracking DB (e.g. etckeeper)
* create cache/session storage location
  * /var/local/*yourproject*/cache
  * /var/local/*yourproject*/sessions
* install/link apache configuration into apache /etc/apache2/sites-available
* restart apache

.. note::
   Most production configurations can only be done by a user
   with "root" permissions (e.g. sudo access) on the production box.
   This is a "feature" of Linux' multi-user security model which prevents
   rogue users/processes from hijacking the system's standard server ports.

.. code-block:: bash

   (tg2env)$ easy_install modwsgideploy
   (tg2env)$ paster modwsgi_deploy
   (tg2env)$ vim apache/*yourproject*.wsgi
   (tg2env)$ vim setup.py
   # Change version="0.1" to your version number
   (tg2env)$ python setup.py bdist_egg
   (tg2env)$ deactivate
   $ sudo aptitude install apache2 libapache2-mod-wsgi
   $ sudo mkdir /usr/local/pythonenv
   $ cd /usr/local/pythonenv
   $ sudo virtualenv --no-site-packages BASELINE
   $ sudo chown -R youruser BASELINE
   $ cd BASELINE/
   $ source bin/activate
   (BASELINE)$ easy_install -i http://www.turbogears.org/2.1/downloads/current/index tg.devtools

