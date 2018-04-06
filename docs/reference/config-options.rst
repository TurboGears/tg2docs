=====================
Configuration Options
=====================

This section reports a reference of various configuration options available inside
TurboGears app_cfg or .ini file. As they are automatically extracted from the source
code this list might be incomplete until the whole configuration process is
updated to automatically declare the expected options.

For example if you want to enable isodates in your application JSON encoder
you might want to add to your ``app_cfg.base_config`` the following::

    base_config['json.isodates'] = True

All the configuration options provided by Application Wrappers can
usually be set both through the ``app_cfg.py`` or through your ``.ini`` file,
while *AppConfig* configuration options can only be set through the ``app_cfg.py``
unless explicitly stated otherwise.

Authentication
==============

.. autoclass:: tg.configuration.configurator.components.auth.SimpleAuthenticationConfigurationComponent

.. autoclass:: tg.appwrappers.identity.IdentityApplicationWrapper

App Globals
===========

.. autoclass:: tg.configuration.configurator.components.app_globals.AppGlobalsConfigurationComponent

Error Reporting
===============

.. autofunction:: tg.error.ErrorReporter

Slow Requests Reporting
=======================

.. autofunction:: tg.error.SlowReqsReporter

JSON Encoding
=============

.. automethod:: tg.jsonify.JSONEncoder.configure
    :noindex:

Flash Messages
==============

.. automethod:: tg.flash.TGFlash.configure
    :noindex:

Sessions
========

.. autoclass:: tg.appwrappers.session.SessionApplicationWrapper

Caching
=======

.. autoclass:: tg.appwrappers.caching.CacheApplicationWrapper

Internationalization
====================

.. autoclass:: tg.appwrappers.i18n.I18NApplicationWrapper

Transaction Manager
===================

.. autoclass:: tg.appwrappers.transaction_manager.TransactionApplicationWrapper

Custom Error Pages
==================

.. autoclass:: tg.appwrappers.errorpage.ErrorPageApplicationWrapper

Ming Session Manager
====================

.. autoclass:: tg.appwrappers.mingflush.MingApplicationWrapper

Rendering Engines
=================

Genshi
------

.. autoclass:: tg.renderers.genshi.GenshiRenderer

Kajiki
------

.. autoclass:: tg.renderers.kajiki.KajikiRenderer

Jinja2
------

.. autoclass:: tg.renderers.jinja.JinjaRenderer

Mako
----

.. autoclass:: tg.renderers.mako.MakoRenderer

JSON
----

.. autoclass:: tg.renderers.json.JSONRenderer
