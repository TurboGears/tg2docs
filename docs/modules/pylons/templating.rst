:mod:`pylons.templating` -- Render functions and helpers
========================================================

.. automodule:: pylons.templating

Module Contents
---------------

.. autofunction:: pylons_globals
.. autofunction:: cached_template
.. autofunction:: render_mako
.. autofunction:: render_genshi

.. glossary::

    app_globals
        One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable. Useful for any given object which
        should be shared across the application.

    c
        The template context object, available when a template is
        being processed. :data:`c` is an alias for
        :data:`tmpl_context`


    g
        The application globals object. :data:`g` is an alias for
        :data:`app_globals`

    h
        A reference to the project helpers module.

    tmpl_context
        The template context object, a place to store all the data for
        use in a template. This includes form data, user identity, and
        the like.

