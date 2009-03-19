Alternative Template engines in TG2
======================================

.. highlight:: python

TurboGears has a very simple and flexible template system. 

Built in renderers 
----------------------

We support four template engines out of the box. 

 * Genshi (the default)
 * chamelion.genshi (just like the default, but faster and more complicated to install)
 * Mako, which is fast flexible, the default in Pylons, and well suited to text templates. 
 * Jinja2, which is pretty fast, flexible, and sandbox-able so "less trusted" individuals can write Jinja templates. 

All you need to do to use any one of these template engines is to add it to the list of renderers to prepare in app_cfg.py::

    base_config.renderers.append('jinja')
    
and then specify that you want to use that particular engine in the ``@expose`` declaration::

    @expose('gensh:myproject.templates.index')
    def foo(self, *args, **kwargs)
        pass

We have docs on some of the specifics of each of these template engines: 

 .. toctree::
    :maxdepth: 2

    Genshi
    ChameleonGenshi
    Mako
    Jinja


Writing your own render function
------------------------------------

TODO