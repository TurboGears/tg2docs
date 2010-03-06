.. _tgdeployment:

Deployment
===========

Your code is somewhat useless if people cannot see it.  This document
describes how to deploy your TurboGears |version| application into
a production environment, that is, an environment suitable for use
by non-technical users.

.. note::
   If you are new to web development, you should likely stick with the
   :ref:`deploy_standard`.

If you are an old
hand, feel free to choose :ref:`deploy_alternate`.  TurboGears is
extremely flexible in how it can be run and this document only begins
to cover the available approaches.

What's Next
------------

* :ref:`deploy_standard` -- for those who want a flexible, robust installation
  using the most commonly used components, Apache, MySQL or PostgreSQL and
  a VirtualEnv-isolated TurboGears installation
* :ref:`deploy_alternate` -- for those who have specific deployment needs, such
  as restricted hosting environments, non-standard environments such as Windows,
  or simple preference for other components

.. toctree::
   :maxdepth: 1

   Standard
   Alternate
   Apache
   modwsgi+virtualenv
   DeployWithAnEgg
   nginx/index
   ModProxy
   Daemon
   FastCGI
   lighttpd+fcgi

.. todo:: Difficulty: Hard. Document use of IIS with TurboGears thru a proxy.
