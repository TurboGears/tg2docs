.. _configo-ptions:

=====================
Configuration Options
=====================

This section reports a reference of various configuration options available inside
TurboGears app_cfg or .ini file.

For example if you want to enable isodates in your application JSON encoder
you might want to add to your ``app_cfg.base_config`` the following::

    base_config['json.isodates'] = True

Configuration options can usually be set both through the ``app_cfg.py``
or through your ``.ini`` file.

Authentication
==============

.. autoclass:: tg.configurator.components.auth.SimpleAuthenticationConfigurationComponent

.. autoclass:: tg.appwrappers.identity.IdentityApplicationWrapper

App Globals
===========

.. autoclass:: tg.configurator.components.app_globals.AppGlobalsConfigurationComponent

Caching
=======

.. autoclass:: tg.configurator.components.caching.CachingConfigurationComponent

.. autoclass:: tg.appwrappers.caching.CacheApplicationWrapper

Custom Error Pages
==================

.. autoclass:: tg.configurator.components.error_pages.ErrorPagesConfigurationComponent

.. autoclass:: tg.appwrappers.errorpage.ErrorPageApplicationWrapper

Debugging
=========

.. autoclass:: tg.configurator.components.debugger.DebuggerConfigurationComponent

Dispatch
========

.. autoclass:: tg.configurator.components.dispatch.DispatchConfigurationComponent

Error Reporting
===============

.. autoclass:: tg.configurator.components.error_reporting.ErrorReportingConfigurationComponent

Helpers
=======

.. autoclass:: tg.configurator.components.helpers.HelpersConfigurationComponent

Internationalization
====================

.. autoclass:: tg.configurator.components.i18n.I18NConfigurationComponent

.. autoclass:: tg.appwrappers.i18n.I18NApplicationWrapper

MimeTypes
=========

.. autoclass:: tg.configurator.components.mimetypes.MimeTypesConfigurationComponent

Ming MongoDB Support
====================

.. autoclass:: tg.configurator.components.ming.MingConfigurationComponent

.. autoclass:: tg.appwrappers.mingflush.MingApplicationWrapper

Paths
=====

.. autoclass:: tg.configurator.components.paths.PathsConfigurationComponent

Request Local Registry
======================

.. autoclass:: tg.configurator.components.registry.RegistryConfigurationComponent

Rendering Engines
=================

.. autoclass:: tg.configurator.components.rendering.TemplateRenderingConfigurationComponent

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

Seekable Request
================

.. autoclass:: tg.configurator.components.seekable_request.SeekableRequestConfigurationComponent

Sessions
========

.. autoclass:: tg.configurator.components.session.SessionConfigurationComponent

.. autoclass:: tg.appwrappers.session.SessionApplicationWrapper

Slow Requests Reporting
=======================

.. autoclass:: tg.configurator.components.slow_requests.SlowRequestsConfigurationComponent

SQLAlchemy
==========

.. autoclass:: tg.configurator.components.sqlalchemy.SQLAlchemyConfigurationComponent

Static Files
============

.. autoclass:: tg.configurator.components.statics.StaticsConfigurationComponent

ToscaWidgets2
=============

.. autoclass:: tg.configurator.components.toscawidgets2.ToscaWidgets2ConfigurationComponent

Transaction Manager
===================

.. autoclass:: tg.configurator.components.transactions.TransactionManagerConfigurationComponent

.. autoclass:: tg.appwrappers.transaction_manager.TransactionApplicationWrapper

JSON Encoding
=============

.. automethod:: tg.jsonify.JSONEncoder.configure
    :noindex:

Flash Messages
==============

.. automethod:: tg.flash.TGFlash.configure
    :noindex:
