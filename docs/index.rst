.. TurboGears documentation master file, created by
   sphinx-quickstart on Sat Oct  9 23:14:01 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   turbogears/starting
   cookbook/cookbook
   reference/reference

The TurboGears documentation
============================

+----------------------------------------------+-------------------------------------------------+-------------------------------------------------+
| .. container:: part-tutorials                |  .. container:: part-recipes                    |  .. container:: part-reference                  |
|                                              |                                                 |                                                 |
|    :ref:`Get Started <tg-starting>`          |    :ref:`The CookBook <tg-cookbook>`            |    :ref:`TurboGears Reference <tg-reference>`   |
+----------------------------------------------+-------------------------------------------------+-------------------------------------------------+

Getting Started
==============================

TurboGears is a Python web framework based on the :ref:`ObjectDispatch <writing_controllers>` paradigm,
it is meant to make possible to write both small and concise applications in :ref:`Minimal mode <index-minimal>`
or complex application in :ref:`Full Stack mode <index-fullstack>`.

Installing TurboGears
------------------------------

TurboGears is meant to run inside python virtualenv and provides its own private index to
avoid messing with your system packages and to provide a reliable set of packages that will
correctly work together.

.. code-block:: bash

    $ virtualenv --no-site-packages tg2env
    $ source tg2env/bin/activate
    (tg2env)$ pip install -i http://tg.gy/current tg.devtools

Single File Application
------------------------------

.. _index-minimal:

TurboGears minimal mode makes possible to quickly create single file applications,
this makes easy to create simple examples and web services with a minimal set
of dependencies.

.. code-block:: python

    from wsgiref.simple_server import make_server
    from tg import expose, TGController, AppConfig

    class RootController(TGController):
         @expose()
         def index(self):
             return "<h1>Hello World</h1>"

    config = AppConfig(minimal=True, root_controller=RootController())

    print "Serving on port 8080..."
    httpd = make_server('', 8080, config.make_wsgi_app())
    httpd.serve_forever()

Full Stack Projects
--------------------------------

.. _index-fullstack:

For more complex projects TurboGears provides the so called full stack setup,
to manage full stack projects the :ref:`GearBox <tg-gearbox>` command is provided.

To try a full stack TurboGears application feel free to *quickstart* one and start
playing around:

.. code-block:: bash

    (tg2env)$ gearbox quickstart -n -x example
    (tg2env)$ cd example/
    (tg2env)$ python setup.py develop
    (tg2env)$ gearbox serve

Visiting *http://localhost:8080/index* you will see a ready made sample application
with a brief introduction to the framework itself.

Explore the :ref:`Getting Started <tg-starting>` section to get started with TurboGears!