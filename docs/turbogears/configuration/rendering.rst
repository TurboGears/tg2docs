.. _renderingconfig:

Template Rendering Config Settings
==================================

:Status: Official

.. contents:: Table of Contents
   :depth: 2

The most common configuration change you'll likely want to make here
is to add a second template engine or change the template engine used
by your project.

By default TurboGears sets up the Kajiki engine, but we also provide
out of the box support for Genshi, Mako and Jinja. To tell TG to prepare these
templating engines for you all you need to do is install the package
and append ``'mako'`` or ``'jinja'`` to the renderer's list here in
app_config.

To change the default renderer to something other than Kajiki, just
set the ``default_renderer`` to the name of the rendering engine.  So, to
add Mako to the list of renderers to prepare, and set it to be the
default, this is all you'd have to do::

  base_config.default_renderer = 'mako'
  base_config.renderers.append('mako')

Configuration Attributes
-------------------------

``base_config.default_renderer`` -- set to the name of the default
render function you want to use.

``base_config.renderers`` -- This is a list of rendering engines that
ought to be prepared for use in the app. To make it available in
your application you must specify here the name of the engine you
want to use.

TG provides built-in renderers for:
``'kajiki'``, ``'genshi'``, ``'mako'``, ``'jinja'``, ``'json'`` and ``'jsonp'``.

In 2.4.0 and newer versions, If you would like to add additional renderers, you can
add it to the renderers list, and then register a rendering engine factory
through the :meth:`.TemplateRenderingConfigurationComponent.register_engine`
method.

``base_config.use_dotted_templatenames`` -- Generally you will not
want to change this.  But if you want to use the standard
genshi/mako/jinja file system based template search paths, set this to
`False`.  The main advantage of dotted template names is that it's
very easy to store template files in zipped eggs, but if you're not
using packaged TurboGears |version| app components there are some
advantages to the search path syntax.


Making a module available to all Templates
---------------------------------------------------
Sometimes you want to expose an entire module to all of the templates
in your templates directory.  Perhaps you have a form library you
like to use, or a png-txt renderer that you want to wrap with <pre>.
This is possible in TG.

First, we must modify our app_cfg.py so that you can share your
link across all templates::

  base_config.variable_provider = helpers.add_global_tmpl_vars

Next, you want to modify the lib/helpers.py module of your application
to include the newly added ``add_global_tmpl_vars`` method::

  import mymodule

  def add_global_tmpl_vars():
       return dict(mymodule=mymodule)

That's pretty much it, you should have access to mymodule in every
template now.

Overriding Rendering Methods
----------------------------

Please have a look at :meth:`.TemplateRenderingConfigurationComponent.register_engine`
for information on how to setup custom rendering engines.
