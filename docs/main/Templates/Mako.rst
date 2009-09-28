.. _mako:

Why Mako?
=========

Mako provides another template rendering solution for TurboGears, it has a
couple of advantages:

 * Is very fast! (as fast as some C engines)
 * Provides namespaces that behave just like regular python code
 * Contains callable blocks
 * It can be be used to generate non-html markup as neither the template or the output needs to be valid html.
 * It the default in Pylons so people migrating will probably want to keep it

For more information see http://www.makotemplates.org

However it has one mayor tradeoff. The main reason for it's speed gain over genshi is the lack of "(x)html" validation. Some see this as 
an advantage some as a disavantage. This can be mitigated with the use of a validator during development.
 
Using Mako in TG2
`````````````````

TurboGears allows you to setup and use Mako templates by simply adding it to
the list of renderers to prepare in base_config::

  base_config.renderers.append('mako')

You can also set it as the default renderer by setting::

   base_config.default_renderer = "mako"
   
The `Mako docs <http://www.makotemplates.org/docs/syntax.html>`_ cover template
syntax very well, so we'll not repeat it. Instead, we refer you to their site.
