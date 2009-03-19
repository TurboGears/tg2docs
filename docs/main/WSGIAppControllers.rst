Mounting WSGI Applications as TG Controllers
==============================================


WSGI apps as Controllers
--------------------------

TurboGears 2 also exposes a WSGI controller, which is a thin and extensible wrapper to easily mount WSGI apps.

It exposes 3 methods ``__init__``, ``default`` and ``delegate``. From those 99% of the time you will only need to modify ``__init__`` and/or ``delegate``.

The normal usage is to extend this class with your own, use ``__init__`` to build your app and store it in 
`self.app` then overwrite ``delegate`` if you need to modify the environment, the response or any other mangling.

For an extensive list of examples please see tgext.wsgiapps.
