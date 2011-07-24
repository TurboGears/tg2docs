.. _jinja:

Why Jinja?
==========
Jinja provides yet another template rendering solution for TurboGears, but it
has a couple of advantages for specific situations: 

 * It is super fast, 
 * It's syntax was inspired by django-templates_ and `dojo's DTL`_ so if you are migrating from Django it's the natural choice. 
 * It lacks some of the most hated (anti)features of django templates. 
    * you can do template logic
    * Autoescaping is off by default.
 * It is sandboxable, so it's possible to let non-trusted users edit the templates.
 
TurboGears features missing in Jinja
````````````````````````````````````

Dotted Notation
---------------

Currently Jinja does not support dotted notation so if you're using
Jinja you will have to turn it off in app_cfg.py::

   base_config.use_dotted_templatenames = False
   
This means you'll write expose statements with path strings:: 

   @expose('index.html')
   
The standard start location is assumed to be your templates directiory, so if
you have admin page templates under an admin directory inside templates you'd
do::

   @expose('/admin/index.html')

Jinja1
------

The current TG renderer is for jinja2 and will not work with jinja1, jinja1 is deprecated and the author wants everyone to move to jinja2 :)

Using Jinja in TG2
``````````````````

TurboGears allows you to setup and use jinja templates by simply adding it to
the list of renderers to prepare in base_config::

  base_config.renderers.append('jinja')

You can also set it as the default renderer by setting::

   base_config.default_renderer = "jinja"

The `Jinja docs`_ cover template syntax very well, so we'll not repeat it here. Instead, we refer you
to their site.

Extensions
------------------

Jinja2 supports loading extensions to add new tags, this is supported on
TG2 by adding the import name to the extension list in base_config::

  base_config.jinja_extensions = ['jinja2.ext.i18n', 'jinja2.ext.loopcontrols']

The setting jinja_extensions is a list of strings, each string is the import name
of one extension, in this example 'jinja2.ext.i18n' is a module in our
python installation (which comes with jinja2).

More on jinja extensions on the `Jinja extension section`_ from the jinja documents.

Filters
-------------------

Jinja2 supports loading functions to add new filters, this is supported on
TG2 by adding the function directly to the filter list in base_config::

  base_config.jinja_filters = [my_filter, other_filter_function]

As you can see here we are using the functions directly, you can also have
jinja2 autoload your filters by creating a file called jinja_filters.py inside
the folder templatetools on you lib filter of you application.

More on jinja filters on the `Jinja custom filter section`_ from the jinja documents.


.. _django-templates: http://docs.djangoproject.com/en/dev/ref/templates/api
.. _dojo's DTL: http://dojotoolkit.org/book/dojo-book-0-9/part-5-dojox/dojox-dtl
.. _Jinja docs: http://jinja.pocoo.org/2/documentation/templates
.. _Jinja extension section: http://jinja.pocoo.org/docs/extensions/
.. _Jinja custom filter section: http://jinja.pocoo.org/docs/api/#custom-filters