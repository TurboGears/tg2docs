:mod:`pylons.templating` -- Render functions and helpers
========================================================

.. automodule:: pylons.templating

Module Contents
---------------

.. autofunction:: pylons_globals
.. autofunction:: cached_template
.. autofunction:: render_mako
.. autofunction:: render_genshi

Legacy Render Functions
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: render
.. autofunction:: render_response

Legacy Buffet Functions
^^^^^^^^^^^^^^^^^^^^^^^

.. autoexception:: BuffetError
.. autoclass:: Buffet
    :members:
.. autoexception:: TemplateEngineMissing
.. autoclass:: MyghtyTemplatePlugin
    :members:

.. glossary::

    app_globals   
        One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable.

    c
        .. todo:: define this term

    g
        .. todo:: define this term

    h
        .. todo:: define this term

    tmpl_content
        .. todo:: define this term, is it supposed to be tmpl_context ?

