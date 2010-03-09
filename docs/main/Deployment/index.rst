.. _tgdeployment:

Deployment
===========

Your code is somewhat useless if people cannot see it.  This set of
documentation describes how to deploy your TurboGears |version|
application into a production environment, that is, an environment
suitable for use by non-technical users.

.. warning::

   Deploying a web application incorrectly can seriously compromise
   not just the application itself, but the entire server on which
   it is installed.

If you are new to web development, you should likely stick with the
:ref:`deploy_standard`. If you are an old hand, feel free to choose
:ref:`deploy_alternate`.  TurboGears is extremely flexible in how
it can be run and this documentation only begins to cover the
available approaches.

.. toctree::
   :maxdepth: 1

   Standard
   Apache
   ModWSGI
   DBServer
   ProductionINI
   Alternate
   DeployWithAnEgg
   nginx/index
   ModProxy
   Daemon
   FastCGI
   lighttpd+fcgi

.. todo:: Difficulty: Hard. Document use of IIS with TurboGears thru a proxy.
