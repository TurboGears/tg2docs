.. _deploy_daemon:

Deploying as a Service/Daemon
=============================

If want to use TurboGears standalone (or behind a proxy like Apache's mod_proxy),
you need to make sure that the TurboGears server is started automatically.
On Un*x you can treat your app like every other system daemon by adding a
custom init script which starts the server automatically when your system boots.


.. todo:: Difficulty: Hard. Document usage of http://pypi.python.org/pypi/wsgisvc to deploy as a Win32 service
