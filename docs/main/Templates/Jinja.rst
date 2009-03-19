Using Jinja in TG2
===================

.. warning: Currently Jinja does not support dotted notation so if you're using Jinja you will have to turn it off in app_cfg.py::

  base_config.use_dotted_templatenames = False

This means you'll write expose statements with path strings:: 

   @expose('index.html')
   
The standard start location is assumed to be your templates directiory, so if you have admin page templates under an admin directory inside templates you'd do::

   @expose('/admin/index.html')

Jinja provides yet another template rendering solution for TurboGears, but it has a couple of advantages for specific situations: 

 * It is sandboxable, so it's possible to let users edit the templates
 * It has a syntax similar to django-templates so if you are migrating from there life will be easier. 
 * It has a syntax similar to dojo's DTL (http://dojotoolkit.org/book/dojo-book-0-9/part-5-dojox/dojox-dtl), which can make some things easier. 
 
TurboGears allows you to setup and use jinja templates by simply adding it to the list of renderers to prepare in base_config::

  base_config.renderers.append('jinja')

You can also set it as the default renderer by setting::

   base_config.default_renderer = "jinja"
   
The Jinja docs cover template syntax very well, so we'll not repeat it here, but take a look here: 

http://jinja.pocoo.org/2/documentation/templates
