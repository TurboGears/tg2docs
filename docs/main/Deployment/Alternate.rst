.. _deploy_alternate:

Alternate Deployment Patterns
=============================

This document attempts to discuss alternate patterns for deploying
TurboGears |version|.  It is written with the assumption that you
have at least read the :ref:`deploy_standard`, as most documents
will simply discuss the differences from a standard deployment.

.. note::

   New developers should likely use the :ref:`deploy_standard` (if possible).
   The choices involved in alternate installations can be daunting if you
   aren't yet familiar with the various components.

.. _deploy_web_server:

Web-Server Choice
------------------

The web-server, which actually receives and processes HTTP requests
from clients and converts them to WSGI requests for your TurboGears
project, can significantly impact the performance and scalability of
your site.

* :ref:`apache_mod_wsgi` -- the standard way to deploy on Apache
* :ref:`apache_mod_proxy` -- runs Apache as a front-end with
  a Paste web-server running on a local port.  Allows you to run
  the Paste server as *any* user
* :ref:`FastCGI` -- runs Apache as a front-end with a `FastCGI`
  process using Mod-Rewrite to make the CGI appear at the correct
  point in the server's URL-space.
* `paster serve production.ini` -- while not recommended for large
  or high-traffic sites, Paste's web-server can often serve for small
  internal sites with few users.  See :ref:`deploy_daemon` for a
  discussion of how to keep your server running.
* :ref:`Nginx` -- an alternative asynchronous high-performance web-server
  which can reverse-proxy TurboGears
* :ref:`Light HTTPD <lighttpd_fcgi>` -- has built-in FastCGI support, so can
  be used to reverse-proxy TurboGears
* `Twisted Web2`_ -- likely only of interest if you are already using
  Twisted for your application and simply want to host a TurboGears
  application within it.  Twisted's WSGI implementation is *not*
  heavily optimized, so should not be used for high-performance sites.
* MS-IIS users may want to experiment with the WSGI support from the
  `ISAPI-WSGI`_ project.

.. todo:: document use of `isapi-wsgi`_ with TurboGears
.. todo:: Difficulty: Hard. Document use of IIS with TurboGears thru a proxy.

.. _`Apache`: http://httpd.apache.org/
.. _`ISAPI-WSGI`: http://code.google.com/p/isapi-wsgi/

.. _deploy_which_database:

Database Choice
----------------

If you are using SQLAlchemy (the default ORM for TurboGears |version|),
then by-and-large your choice of database back-end is a matter of preference.

* :ref:`deploy_postgresql` -- is a robust, mature, well documented
  free database server which meets or exceeds most new user's needs.
* MySQL -- allows you to trade robustness (ACID compliance, for instance)
  for raw speed and some exotic features that are add-ons for PostgreSQL
* Oracle -- if your site is an Oracle shop with specialized Oracle admins
  it may be appropriate to use an Oracle DB for your TurboGears application
* SQLite -- can be used for *extremely* small sites (e.g. a local web-server
  intended solely to be used by a single user).  It is *extremely* easy to
  set up and comes with later versions of Python.
* MSSQL -- if you are already using MSSQL for your site, and have admins who
  maintain the servers, it may be appropriate to use MSSQL for your TurboGears
  application.

.. _`Twisted Web2`: http://blog.vrplumber.com/index.php?/archives/2421-TurboGears-as-a-Twisted-WSGI-Application-in-125-seconds.html

.. todo:: Add section on "repeatable deployment options"
