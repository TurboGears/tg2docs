.. _templating:


Templating
==========

TurboGears enables template rendering though the :class:`tg.decorators.expose` decorator to
link controller methods to template and through the :func:`tg.render_template` function.

Each template is rendered using a *template engine*, TurboGears provides some builtin engines
but additional can be configured. The ``default_renderer`` for TurboGears applications is
``Genshi`` which permits to write templates in pure xhtml and validates them to detect issues
at compile time and prevent serving broken pages. For documentation on Genshi templates see
the :ref:`Genshi Template Language <genshi-language>`.

By default TurboGears references to templates using *dotted notation*, this is the path
of the template file in terms of python packages. This makes possible to refer to template
files independently from where the application is installed and started as it refers
to the python package where the template file is provided.

Typical dotted notation path looks like: **mypackage.templates.template_file** and it doesn't
include any extention. If an extension is provided TurboGears will try to read the path
as a file system path, not as a dotted notation path.

Explicit Engine in Exposition
-----------------------------

The ``@expose`` decorator template files will always be rendered using the ``default_renderer``
specified into the application configurator unless explicitly set. To explicitly provide
the template engine to use just prepend it to the template path in the form **engine:template_path**
like **genshi:mypackage.templates.template_file**.

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
    - **identity** which is the currently logged used when recognized
    - **tg.url** which is the utility function to create urls in TurboGears.

For a complete list of those variables refer to the :func:`tg.render_template` documentation.
You can add additional variable to every single template by setting a ``variable_provider``
function inside the Application Configurator (``app_cfg.base_config`` object).

This function is expected to return a ``dict`` with any variable that should be added
the default template variables. It can even replace existing variables.
