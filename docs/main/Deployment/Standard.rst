.. _deploy_standard:

Standard Deployment Pattern
===========================

This is the recommended deployment pattern for new users.  It is not
necessarily optimal for all projects, it is intended to provide a good
set of defaults from which to later customize:

* :ref:`deploy_apache` -- installed from system packages on a Linux host
* :ref:`mod_wsgi <apache_mod_wsgi>` using a :ref:`deploy_modwsgi_baseline`
  to provide a clean execution environment for an :ref:`deploy_modwsgi_appenv`
* :ref:`deploy_db` -- such as PostgreSQL or MySQL
* :ref:`deploy_ini` -- being sure to `set debug=false` (very important!)
* :ref:`deploy_code` -- using a source-code checkout or an egg-based install
* :ref:`deploy_apache_enable` -- to make the site available

If you have other deployment needs, see the overall :ref:`tgdeployment`
documentation.
