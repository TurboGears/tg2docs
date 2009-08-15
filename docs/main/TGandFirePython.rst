
Using FirePython With TurboGears2
=================================

:Status: Work in progress

.. contents:: Table of Contents
    :depth: 2

FirePython is a sexy Python logger console integrated into Firebug.

Requires
--------

  - Firefox - http://www.mozilla.com/en-US/firefox/
  - Firebug - https://addons.mozilla.org/en-US/firefox/addon/1843
  - FireLogger - https://addons.mozilla.org/en-US/firefox/addon/11090


Installing Stuff
----------------

If you haven't installed TG2, you'll need to do that first (see
:ref:`downloadinstall`). Once you've got an up-to-date version of TG2,
you'll need to install FirePython and some dependancies, which you can
do by::

  easy_install firepython
  easy_install python-cjson
  easy_install jsonpickle

After that's done, you can create a new TG2 project in the normal
way::

  paster quickstart firepythontest
  ...
  cd firepythontest
  paster serve development.ini --reload

Your project should now be started, and you should be able to browse to it at http://127.0.0.1:8080

Adding FirePython Support
-------------------------

Now, you're ready to add FirePython Middleware to your app:

Edit firepythontest/config/middleware.py

Add::

    from firepython.middleware import FirePythonWSGI

Insert After line "app = make_base_app(global_conf, full_stack=True,
\**app_conf)"::

    app = FirePythonWSGI(app)

This will wrap your Turbogears App with FirePython, and any/all Log
messages will become available in Firebug.
