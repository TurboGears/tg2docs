.. _alternative_templates:

Templating Options
==================

TurboGears has a very simple and flexible template system located at :mod:`tg.render`. 
Which is a tiny wrapper around :mod:`pylons.templating` to provide dotted template lookup support.

Built in renderers
------------------

We currently support the following template engines out of the box. 

 .. toctree::
    :maxdepth: 1

    Genshi
    Mako
    Jinja

All you need to do to use any one of these template engines is to add it to the list of renderers to prepare in app_cfg.py::

    base_config.renderers.append('jinja')
    
and then specify that you want to use that particular engine in the ``@expose`` declaration::

    @expose('genshi:myproject.templates.index')
    def foo(self, *args, **kwargs)
        pass

We have docs on some of the specifics of each of these template engines: 


Writing your own render function
--------------------------------

.. todo:: Difficulty: Medium. Document writing your own render function for templates

