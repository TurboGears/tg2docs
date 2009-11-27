.. _tgdeployment:

Deployment options
==================

TurboGears 2 provides a solid HTTP server built in, and for many
internal corporate deployments or low traffic sites you can just fire
up the TG2 app and point people at it.

This can be as simple as running::

  paster serve production.ini

But it's also likely that you may want to automatically restart your
TG2 app if the server reboots, or you may want to set it up as a
windows service. Unfortunately these things can be very operating
system specific, but fortunately they aren't TG2 specific.


Apache Deployment options:
---------------------------

* :ref:`Apache and mod_wsgi <apache_mod_wsgi>` -- the
  mod_wsgi apache extension is a very efficient WSGI server, which
  provides automatic process monitoring, load balancing for
  multi-process deployments, as well as strong apache integration.

* :ref:`Apache and mod_proxy <apache_mod_proxy>` -- The mod_proxy
  extension provides a simple to set-up apache environment that
  proxies HTTP requests to your TG2 app.  It can be used to load
  balance across multiple machines.
 
* modRewrite -- mod_rewrite deployment is very similar to mod_proxy
  (in fact from the TG2 side they are identical), but mod_rewrite can
  be somewhat more complex to setup itself.
  
* :ref:`FastCGI <FastCGI>`_ -- when apache extensions are not an option 
  due to webhost restrictions (for example, the want to run suexec on all 
  userspace scripts), you can create a FastCGI dispatcher that invokes the 
  WSGI interface. 

NGINX deployment
-----------------

Nginx is a very fast asynchronous web server that can be used in front
of TurboGears 2 in very high load environments.

* load balancing proxy
* NGINX mod_wsgi

.. todo:: Difficulty: Medium. Determine what the list above should be trying to tell
          us. Is this a list of items to be documented?

Packaging your app as an egg:
------------------------------

You may also want to package your app up as a redistributable egg, TG2
sets up everything that you need to do this.

 :ref:`tgeggdeployment`
 

Reference
---------

You can also find recipes for mounting a Turbogears app behind lots of
other servers in the 1.0 docs.  Generally these should "just work"
with TG2 as well.  The only exception is that the config file
production.ini is slightly different.

 * http://docs.turbogears.org/1.0/Deployment

.. todo:: Difficulty: Medium. Document the recipes for deployment, updating the 1.0 docs


.. todo:: Document usage of http://pypi.python.org/pypi/wsgisvc to deploy as a Win32 service 
