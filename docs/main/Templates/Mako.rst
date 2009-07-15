Using Mako in TG2
====================

Mako provides another template rendering solution for TurboGears, but it has a couple of advantages for specific situations: 

 * It is very fast
 * and is what's used by Pylons
 
TurboGears allows you to setup and use Mako templates by simply adding it to the list of renderers to prepare in base_config::

  base_config.renderers.append('mako')

You can also set it as the default renderer by setting::

   base_config.default_renderer = "mako"
   
The Mako docs cover template syntax very well, so we'll not repeat it, but if you're interested in using mako take a look here: 

http://www.makotemplates.org/docs/syntax.html
.. todo:: Review this file for todo items.

