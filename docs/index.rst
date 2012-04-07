.. TurboGears documentation master file, created by
   sphinx-quickstart on Sat Oct  9 23:14:01 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   tutorials
   extensions
   gettingtoknow
   recipesandfaq
   toc

The TurboGears documentation
============================

+----------------------------------------------+-------------------------------------------------+------------------------------------------------------------+-------------------------------------------------+----------------------------------------------+
| .. container:: part-tutorials                |  .. container:: part-recipes                    | .. container:: part-extending                              | .. container:: part-gears                       | .. container:: part-reference                |
|                                              |                                                 |                                                            |                                                 |                                              |
|    :ref:`Get Started <tutorials>`            |    :ref:`Recipes and Tips <recipes-and-faq>`    |    :ref:`Extensions and Tools <extensions-and-tools>`      |  :ref:`About TurboGears <getting-to-know>`      |    :ref:`Index and API Reference <genindex>` |
+----------------------------------------------+-------------------------------------------------+------------------------------------------------------------+-------------------------------------------------+----------------------------------------------+

The TurboGears Web Framework
==============================

TurboGears is an :ref:`ObjectDispatch <writing_controllers>` based Python web development framework made for rapid projects development.

.. code-block:: python

    from tg import expose
    from helloworld.lib.base import BaseController

    class RootController(BaseController):
         @expose()
         def index(self):
             return "<h1>Hello World</h1>"

TurboGears is meant to run inside python virtualenv and provides its own private index to
avoid messing with your system packages and to provide a reliable set of packages that will
correctly work together.

.. code-block:: bash

    $ virtualenv --no-site-packages tg2env
    $ source tg2env/bin/activate
    (tg2env)$ easy_install -i http://tg.gy/current tg.devtools

To try TurboGears feel free to *quickstart* a new TurboGears application and start
playing around:

.. code-block:: bash

    (tg2env)$ paster quickstart -n -x example
    (tg2env)$ cd example/
    (tg2env)$ python setup.py develop
    (tg2env)$ paster serve development.ini

Visiting *http://localhost:8080/index* you will see a ready made sample application
with a brief introduction to the framework itself.

Explore the :ref:`TurboGears Tutorials <tutorials>` to get started with TurboGears!