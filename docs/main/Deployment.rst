.. _tgdeployment:

Deployment
===========

Your code is somewhat useless if people cannot see it.  This document
describes how to deploy your TurboGears |version| application into
a production environment, that is, an environment suitable for use
by non-technical users.

.. note::
   Most production configurations can only be done by a user
   with "root" permissions (e.g. sudo access) on the production box.
   This is a "feature" of Linux' multi-user security model which prevents
   rogue users/processes from hijacking the system's standard server ports.

There are a lot of questions you will need to answer to decide how to
deploy your application.  If you are new to web development, you should
likely stick with the :ref:`deploy_standard`.  If you are an old
hand, feel free to choose :ref:`deploy_alternate`.  TurboGears is
extremely flexible in how it can be run and this document only begins
to cover the available approaches.

.. _deploy_standard:

Standard Deployment Pattern
----------------------------

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

.. _deploy_alternate:

Alternate Deployment Patterns
------------------------------

Questions to answer for yourself:

* :ref:`deploy_web_server` -- what application will actually accept
  the http requests from the client?  This is normally a service that must
  be installed as "root" in order to claim the standard ports (80 or 443)
* :ref:`deploy_which_database` -- what server will you use to store your
  model data?
* :ref:`deploy_ssl` -- will you require SSL connections for your entire
  application?
* :ref:`deploy_source` -- will you deploy with source-code-checkouts, built
  eggs, whole-application binary checkouts, zc.buildout packages,
  PIP packages or puppet scripts?

.. _deploy_web_server:

Web-Server Choice
------------------

The most common way to install TurboGears |version| for production use
is to use the `Apache`_ web-server running the `mod_wsgi`_ extension
to host TurboGears in a reasonably performant easily deployed
and flexible configuration.

There are many other approaches to deploying a production environment,
and choosing which approach is best for your needs is a non-trivial
task.

* Apache with mod_wsgi tends to be the "default" choice.  It is widely
  available, well documented, stable and easily supported by Linux
  sysadmins in production environments.
* Apache with mod_proxy or mod_rewrite can be used to have Apache handle
  "the rest" of your site, while passing only your TurboGears application's
  requests through to a Paster server running on a non-privileged port.
* Apache with FastCGI can be used if necessary, such as when you do not have
  control of your Apache server or a policy requires suexec or the like for
  all "user" scripts.
* `Nginx`_ is often preferred by those who need speed above all else
* The built-in Paster server will occasionablly be used by those
  who are deploying small internal sites with no more than a handful
  of users.
* IIS users may want to experiment with the WSGI support from the
  `ISAPI-WSGI project`_.

.. todo:: document use of isapi-wsgi with TurboGears

.. _`Apache`: http://httpd.apache.org/
.. _`Nginx`: http://nginx.org/
.. _`ISAPI-WSGI`: http://code.google.com/p/isapi-wsgi/

Database Choice
----------------

Normally users choose either MySQL or PostgreSQL as their production
database back-end, but Oracle or MSSQL can also be used.  The built-in
SQLite database should not be used for production sites as a general
rule.  Obviously if you have used MongoDB/Ming you will need to deploy
against a MongoDB database instead.


TurboGears 2 provides a solid HTTP server built in, and for many
internal corporate deployments or low traffic sites you can just fire
up the TurboGears |version| app and point people at it.

This can be as simple as running::

  paster serve production.ini

But it's also likely that you may want to automatically restart your
TurboGears |version| app if the server reboots, or you may want to set
it up as a windows service. Unfortunately these things can be very
operating system specific, but fortunately they aren't
TurboGears specific.



NGINX Deployment
-----------------

Nginx is a very fast asynchronous web server that can be used in front
of TurboGears |version| in very high load environments.

   .. toctree::
      :maxdepth: 1

      Deployment/nginx/load_balance.rst

Another alternative that has yet to be explored by the doc crew is
`uWSGI <http://projects.unbit.it/uwsgi/wiki/RunOnNginx>`_.

Packaging your Application as an Egg
------------------------------------

You may also want to package your app up as a redistributable egg,
TurboGears |version| sets up everything that you need to do this.

 :ref:`tgeggdeployment`


Integrating with the init system on Un*x (SysV style)
---------------------------------------------------------

If want to use TurboGears standalone (or behind a proxy like Apache's mod_proxy),
you need to make sure that the TurboGears server is started automatically.
On Un*x you can treat your app like every other system daemon by adding a
custom init script which starts the server automatically when your system boots.


Reference
----------

   .. toctree::
      :maxdepth: 1

      Deployment/Apache
      Deployment/modwsgi+virtualenv
      Deployment/DeployWithAnEgg
      Deployment/ModProxy
      Deployment/lighttpd+fcgi
      Deployment/FastCGI

.. todo:: Difficulty: Hard. Document use of IIS with TurboGears thru a proxy.
.. todo:: Difficulty: Hard. Document usage of http://pypi.python.org/pypi/wsgisvc to deploy as a Win32 service

