.. _tgdeployment:

Deployment
===========

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


Apache Deployment
-----------------

* :ref:`mod_wsgi <apache_mod_wsgi>` -- The
  mod_wsgi apache extension is a very efficient WSGI server, which
  provides automatic process monitoring, load balancing for
  multi-process deployments, as well as strong apache integration.

* :ref:`mod_proxy <apache_mod_proxy>` -- The mod_proxy
  extension provides a simple to set-up apache environment that
  proxies HTTP requests to your TurboGears |version| app.  It can
  be used to load balance across multiple machines.

* mod_rewrite -- Very similar to mod_proxy
  (in fact from the TurboGears side they are identical), but
  mod_rewrite can be somewhat more complex to setup itself.

* :ref:`FastCGI <FastCGI>` -- when apache extensions are not an option
  due to webhost restrictions (for example, the want to run suexec on all
  userspace scripts), you can create a FastCGI dispatcher that invokes the
  WSGI interface.

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

      Deployment/DeployWithAnEgg
      Deployment/ModProxy
      Deployment/lighttpd+fcgi
      Deployment/FastCGI

.. todo:: Difficulty: Hard. Document use of IIS with TurboGears thru a proxy.
.. todo:: Difficulty: Hard. Document usage of http://pypi.python.org/pypi/wsgisvc to deploy as a Win32 service

