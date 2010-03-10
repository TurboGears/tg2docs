.. _deploy_daemon:

Deploying as a Service/Daemon
=============================

If want to use TurboGears standalone (i.e. use the Paste web server as your
primary web-server), or behind a proxy, such as
:ref:`Apache Mod-Proxy <apache_mod_proxy>` or the :ref:`nginx`
you need to make sure that the TurboGears server is started automatically.
There are a number of options to accomplish this:

* `Upstart`_ -- used on newer Linux hosts
* `Sys-V Init` -- traditional Unix/Linux init system
* `supervisord`_ -- separate daemon with ability to monitor and restart

Which one you choose is likely up to your familiarity level with the
particular tool.

.. note::
   For *extremely* small non-critical sites, it can sometimes be expedient
   to use the `screen` tool to start a `paster serve production.ini`
   process and then disconnect from the screen.  This isn't recommended,
   as a power-cycle of the machine will require you to rush back from
   your vacation to ssh in and re-start the server, but sometimes you
   do this kind of thing just to get the job done *now*.

.. todo:: Provide sample init script
.. todo:: Provide sample upstart
.. todo:: Provide sample supervisord config
.. todo:: Difficulty: Hard. Document usage of http://pypi.python.org/pypi/wsgisvc to deploy as a Win32 service

.. _`supervisord`: http://supervisord.org/
.. _`upstart`: http://upstart.ubuntu.com/
