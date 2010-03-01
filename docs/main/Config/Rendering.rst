.. _renderingconfig:

Template Rendering Config Settings
==================================

:Status: Official

.. contents:: Table of Contents
   :depth: 2

The most common configuration change you'll likely want to make here
is to add a second template engine or change the template engine used
by your project.

By default TurboGears sets up the Genshi engine, but we also provide
out of the box support for Mako and Jinja. To tell TG to prepare these
templating engines for you all you need to do is install the package
and append 'mako' or 'jinja' to the renderer's list here in
app_config.

To change the default renderer to something other than Genshi, just
set the default_renderer to the name of the rendering engine.  So, to
add Mako to the list of renderers to prepare, and set it to be the
default, this is all you'd have to do::

  base_config.default_renderer = 'mako'
  base_config.renderers.append('mako')

Configuration Attributes
-------------------------

``base_config.default_renderer`` -- set to the name of the default
render function you want to use.

``base_config.renderers`` -- This is a list of render functions that
ought to be prepared for use in the app.  This is a shortcut for the
four renderers that TurboGears |version| provides out of the box.
TG provides renderers for: `'genshi'`, `'mako'`, `'jinja'`, and `'json'`.

In 2.1, If you would like to add additional renderers, you can
add it to the renderers list, and then provide a setup_mytl_renderer
method in your custom AppConfig, where mytl is the name of your
template language.


``base_config.use_legacy_renderer`` -- If ``True`` old style buffet
renderers will be used.  Don't set this unless you need buffet
renderers for some specific reason, buffet renderers are deprecated
and will probably be removed in 2.1.

``base_config.use_dotted_templatenames`` -- Generally you will not
want to change this.  But if you want to use the standard
genshi/mako/jinja file system based template search paths, set this to
`False`.  The main advantage of dotted template names is that it's
very easy to store template files in zipped eggs, but if you're not
using packaged TurboGears |version| app components there are some
advantages to the search path syntax.

``base_config.renderers`` -- a dictionary with the render function
name as the key, and the actual configured render function as the
value.  For the four standard renderers it's enough to just add the
name to ``base_config.renderers`` but for custom renderers you want to
set the renderer up, and set it in this dictionary directly.


Making a module available to all Genshi templates
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

Overriding AppConfig Rendering Methods
---------------------------------------

.. automethod:: tg.configuration.AppConfig.setup_default_renderer
.. automethod:: tg.configuration.AppConfig.setup_mako_renderer
.. automethod:: tg.configuration.AppConfig.setup_genshi_renderer
.. automethod:: tg.configuration.AppConfig.setup_jinja_renderer
.. automethod:: tg.configuration.AppConfig.setup_json_renderer
