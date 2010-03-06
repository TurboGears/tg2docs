.. _deploy_alternate:

Alternate Deployment Patterns
=============================

.. note::

   New developers should likely use the :ref:`deploy_standard` (if possible).
   The choices involved in alternate installations can be daunting if you
   aren't yet familiar with the various components.

Questions to answer for yourself:

* :ref:`deploy_web_server` -- what application will actually accept
  the http requests from the client?  This is normally a service that must
  be installed as "root" in order to claim the standard ports (80 or 443)
* :ref:`deploy_which_database` -- what server will you use to store your
  model data?
* :ref:`deploy_source` -- will you deploy with source-code-checkouts, built
  eggs, whole-application binary checkouts, zc.buildout packages,
  PIP packages or puppet scripts?

.. _deploy_web_server:

Web-Server Choice
------------------

The most common way to install TurboGears |version| for production use
is to use the `Apache`_ web-server running the mod_wsgi extension
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
  `ISAPI-WSGI`_ project.

.. todo:: document use of `isapi-wsgi`_ with TurboGears

.. _`Apache`: http://httpd.apache.org/
.. _`Nginx`: http://nginx.org/
.. _`ISAPI-WSGI`: http://code.google.com/p/isapi-wsgi/

.. _deploy_which_database:

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
