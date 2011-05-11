.. _deploy_code:

Deploying Your Project Code
===========================

There are a number of ways you can deploy your application's code in
production.  While there is an "officially" standard way to deploy
(via eggs), that pattern is not universally accepted.

Your application's code is likely to be the most frequently changed
component of your application (compared to the libraries that make up
TurboGears), so you will likely re-deploy your code many times,
possibly many times *per day*.

* :ref:`Deploy with an Egg<tgeggdeployment>` -- which can be installed
  via `easy_install` or `PIP` into your :ref:`deploy_modwsgi_appenv`
  with the :ref:`deploy_ini` being the only file in the
  deploy_modwsgi_deploy directory (`/usr/local/turbogears/myapp/` by
  default)
* :ref:`deploy_checkout` (often of a branch or a tag)
  directly into the `deployment` directory by the www-data user.  Note that
  this requires some changes to your .ini file!

What's Next?
------------

* :ref:`deploy_standard` provides an overview of the standard deployment process
