.. _routesconfig:

Routes Config Settings
==============================================

:Status: Official

.. contents:: Table of Contents
   :depth: 2


If you are coming over from Pylons, or merging
an existing Pylons application into a TG application,
you might want to use your own routing scheme.   This is perfectly allowable,
TurboGears just sets up a very simple routing to kick off it's
Object Dispatch mechanism, but this can be augmented hower you desire.
One thing to note, if you plan on mounting TurboGears controllers
without using class instantiation, they must subclass a TurboGears
Controller, complete with Dispatcher.  Examples of classes like this are:
TGController, WSGIAppController, and RestController.


``AppConfig`` Method Overrides
-------------------------------

.. automethod:: tg.configuration.AppConfig.setup_routes

