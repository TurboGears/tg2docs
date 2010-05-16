.. _toscaconfig:

ToscaWidgets Config Settings
==================================

.. currentmodule:: tg.configuration

:Status: Official

.. contents:: Table of Contents
   :depth: 2

ToscaWidgets itself has a few different configuration settings.  Here's a few
ways you can modify the way ToscaWidgets renders content.

TW Minification
----------------

TW 0.9.9+ support resource variants.  This allows the developers to point TW at a different
javascript/css/image library in the event you want to change the js files that are used.  This
is usually employed in minification of the javascript files.  This is valuable when you want to
run "debug" mode on your js files in development, but "minified" on production for speedups.

You can set this variable in two ways.  Add the following line to your .ini file as::

   #for "minified" files
   toscawidgets.framework.resource_variant=min

   #for "debug" files
   toscawidgets.framework.resource_variant=debug

Note that this only works if your js wrapper has actually been set up to have multiple variants.
If the library does not have variants, this variable will be ignored.


Toscawidgets Versions
----------------------

TurboGears supports both the 0.9.x branches of ToscaWidgets and the 2.x TW code.
ToscaWidgets is currently at a crossroads, with the 0.9.x branch being a very stable
codebase, and TW2 providing speed benefits, easier use, and a simpler, easier to debug
codebase.  TW2 is currently in alpha, so it's up to you to determine it's level
of stability before usage.  TW and TW2 can be used simultaneously.  To use them,
modify the following config options:

``base_config.use_toscawidgets`` -- Set to False to turn off
Toscawidgets. (default is True)

``base_config.use_toscawidgets2`` -- Set to True to turn on
Toscawidgets2. (default is False)

What this does is to allow ToscaWidgets to provide hooks for both entry and exit.  On
entry, ToscaWidgets handles server requests that are directed directly to the widget
itself, bypassing the TG Controllers.  On exit, TW middleware provides resource injection,
which can actually insert links to resources like javascript files into your HTML code
automatically.  Both TW 0.9.x and TW 2.x support this usage.  There is more information
on [tw_middleware_] and [tw2_middleware_].

.. _tw_middleware: http://toscawidgets.org/documentation/ToscaWidgets/modules/resource_injector.html
.. _tw2_middleware: http://toscawidgets.org/documentation/tw2.core/core.html#middleware

``AppConfig`` Method Overrides
-----------------------------------

.. automethod:: AppConfig.add_tosca_middleware
.. automethod:: AppConfig.add_tosca2_middleware
