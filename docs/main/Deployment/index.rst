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
   it is installed.  If you are unsure about any process or idea,
   do not deploy until you *are* sure.

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
   Code
   DeployWithAnEgg

These sections describe non-standard approaches to deployment.  You
should not likely use these unless you are comfortable with web
development and deployment or you have some particular need which
is not met by the standard deployment pattern (above).

.. toctree::
   :maxdepth: 1

   Alternate
   Checkout
   Daemon
   ModProxy
   FastCGI
   lighttpd+fcgi
   nginx/index

.. todo:: Document processes for repeatable local-only releases: Local PyPI,
   PIP, recordeggs, whole-virtualenv checkin/checkout.
