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

User Identity
=============

.. autoclass:: tg.appwrapper.identity.IdentityApplicationWrapper

Transaction Manager
===================

.. autoclass:: tg.appwrappers.transaction_manager.TransactionApplicationWrapper

Custom Error Pages
==================

.. autoclass:: tg.appwrappers.errorpage.ErrorPageApplicationWrapper

Ming Session Manager
====================

.. autoclass:: tg.appwrappers.mingflush.MingApplicationWrapper
