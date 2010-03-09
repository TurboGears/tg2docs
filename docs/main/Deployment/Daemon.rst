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

.. todo:: Provide sample init script
.. todo:: Provide sample upstart
.. todo:: Provide sample supervisord config
.. todo:: Difficulty: Hard. Document usage of http://pypi.python.org/pypi/wsgisvc to deploy as a Win32 service

.. _`supervisord`: http://supervisord.org/
.. _`upstart`: http://upstart.ubuntu.com/
