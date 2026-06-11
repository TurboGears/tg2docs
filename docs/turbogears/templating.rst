.. _templating:


Templating
==========

TurboGears enables template rendering through the :class:`tg.decorators.expose` decorator to
link controller methods to template and through the :func:`tg.render_template` function.

For a complete reference of rendering configuration options, see
:ref:`Rendering Engines <renderingconfig>`.

Each template is rendered using a *template engine*, TurboGears provides some built-in engines
but additional engines can be configured. The ``default_renderer`` for TurboGears applications is
``Kajiki`` which permits to write templates in pure xhtml and validates them to detect issues
at compile time and prevent serving broken pages. For documentation on Kajiki templates see
the :ref:`Kajiki Template Language <kajiki-language>`.

By default TurboGears references to templates using *dotted notation*, this is the path
of the template file in terms of python packages. This makes possible to refer to template
files independently from where the application is installed and started as it refers
to the python package where the template file is provided.

A typical dotted notation path looks like **mypackage.templates.template_file**
and does not include any extension. With the default Kajiki renderer,
``mypackage.templates.sample`` resolves to the package template file
``templates/sample.xhtml``.

If an extension is provided, TurboGears treats the value as a filesystem-style
template name instead of dotted notation. Absolute filesystem paths with an
extension can be used directly. Relative paths are resolved by the renderer's
template search path, so ``mypackage/templates/sample.xhtml`` is not equivalent
to the dotted path ``mypackage.templates.sample``.

Explicit Engine in Exposition
-----------------------------

The ``@expose`` decorator template files will always be rendered using the ``default_renderer``
specified into the application configurator unless explicitly set. To explicitly provide
the template engine to use just prepend it to the template path in the form **engine:template_path**
like **kajiki:mypackage.templates.template_file**.

Refer to :ref:`Rendering Engines Configuration <renderingconfig>` documentation for information
on setting up available renderers and specifying the default one.

Template Variables
------------------

To pass template variables the controller is expected to return a ``dict`` with all the
variables inside. Those will be available inside the template with the same name.

In addition to variables explicitly specified by the user, TurboGears adds some additional
variables and utilities. The most useful one are probably:

    - **h** which is the lib.helpers module, this usually includes every utility function
      for formatting text and html in templates.
    - **request, response, tmpl_context, app_globals, config** which are the same available
      inside controllers.
    - **tg.url** which is the utility function to create urls in TurboGears.

Authentication information is available through the request when authentication
is enabled, but current quickstarts do not provide a guaranteed top-level
``identity`` template variable.

For a complete list of those variables refer to the :func:`tg.render_template` documentation.
You can add additional variables to every single template by setting a
``variable_provider`` function inside the Application Configurator
(``app_cfg.base_config`` object)::

    base_config.update_blueprint({
        'variable_provider': lambda: {'provided_value': 'available everywhere'},
    })

This function is expected to return a ``dict`` with any variables that should be
added to the default template variables. It can even replace existing variables.
