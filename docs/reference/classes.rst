=====================
Classes and Functions
=====================

This page provides a quick access reference to the classes and functions provided by TurboGears

Decorators
==========

.. automodule:: tg.decorators
    :members:

.. autoclass:: tg.caching.cached_property


Validation
==========

.. autoclass:: tg.decorators.validate
    :noindex:

.. automodule:: tg.validation
    :members:

Authorization
=============

.. autoclass:: tg.decorators.require
    :noindex:

.. automodule:: tg.predicates
    :members:

Pagination
==========

.. autoclass:: tg.decorators.paginate
    :noindex:

.. autoclass:: tg.support.paginate.Page
    :members:

Configuration
=============

.. autoclass:: tg.FullStackApplicationConfigurator
    :members:

.. autoclass:: tg.MinimalApplicationConfigurator
    :members:

.. autoclass:: tg.wsgiapp.TGApp
    :members:

WebFlash
========

.. automodule:: tg.flash
    :members:

Rendering
=========

.. autofunction:: tg.render_template

.. automodule:: tg.render
    :members:
    :exclude-members: render

.. autoclass:: tg.renderers.base.RendererFactory
    :members:

.. autoclass:: tg.jsonify.JSONEncoder
    :members:

.. autofunction:: tg.jsonify.encode

.. autofunction:: tg.jsonify.encode_iter

Request & Response
==================

.. autoclass:: tg.request_local.Request
    :members:

.. autoclass:: tg.request_local.Response
    :members:

.. autoclass:: crank.dispatchstate.DispatchState
    :members:

    DispatchState instance for current request is made available in TurboGears2
    as ``tg.request.dispatch_state`` as soon as the dispatch process is completed.

Hooks
=====

.. autoclass:: tg.configuration.hooks.HooksNamespace
    :members:

.. autoclass:: tg.appwrappers.base.ApplicationWrapper
    :members:
    :special-members:

Milestones
==========

.. autoclass:: tg.configuration.milestones._ConfigMilestoneTracker
    :members:

Internationalization
====================

.. automodule:: tg.i18n
    :members:

Controller Utilities
====================

.. automodule:: tg.controllers.util
    :members:

General Utilities
=================

.. automodule:: tg.util.bunch
    :members:

.. automodule:: tg.util.dates
    :members:

.. automodule:: tg.util.decorators
    :members:

.. automodule:: tg.util.files
    :members:

.. automodule:: tg.util.html
    :members:

.. automodule:: tg.util.lazystring
    :members:

.. automodule:: tg.util.webtest
    :members:

.. automodule:: tg.util.sqlalchemy
    :members:

.. automodule:: tg.util.ming
    :members:

.. automodule:: tg.util.misc
    :members:

.. automodule:: tg.configuration.utils
    :members:


