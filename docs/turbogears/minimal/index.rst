.. _minimal-tutorial:

==========================================================
Hello TurboGears
==========================================================

The fastest way to start using TurboGears is through the **minimal mode**, when using TurboGears with
minimal mode a default setup that minimizes dependencies and complexity is provided.

.. note::

    While minimal mode is well suited for small simple web applications or web services, for more complex
    projects moving to a package based configuration is suggested. To start with a package based application
    the :ref:`20 Minutes Wiki Tutorial <wiki20>` tutorial is provided.

Play with TurboGears
========================

If you want to experiment with this tutorial without installing TurboGears on your local machine, feel free
to edit the `Basic TurboGears Example <http://runnable.com/Unq2c2CaTc52AAAm/basic-turbogears-example-for-python>`_ 
on Runnable and skip the :ref:`Setup <minimal-setup>` section.

This will provide a working TurboGears application in your browser you can freely edit and run.

.. _minimal-setup:

Setup
============================

First we are going to create a virtual environment where to install the framework, if you want to
proceed without using a virtual environment simply skip to :ref:`Install TurboGears <TurboGears2_install>`.
Keep in mind that using a virtual environment is the suggested way to install TurboGears without
messing with your system packages and python modules. To do so we need to install the ``virtualenv`` package::

    $ pip install virtualenv

Now the virtualenv command should be available and we can create and activate
a virtual environment for our TurboGears2 project::

    $ virtualenv tgenv
    $ . tgenv/bin/activate

If our environment got successfully created and activated we should end up with
a prompt that looks like::

    (tgenv)$

.. _TurboGears2_install:

Now we are ready to install TurboGears itself:

.. parsed-literal::

    (tgenv)$ pip install |private_index_path| TurboGears2

Hello World
======================

A TurboGears application consists of an ``AppConfig`` application configuration and an application ``RootController``.
The first is used to setup and create the application itself, while the latter is used to dispatch requests
and take actions.

For our first application we are going to define a controller with an index method that just tells *Hello World*::

    from tg import expose, TGController, AppConfig

    class RootController(TGController):
         @expose()
         def index(self):
             return 'Hello World'

now to make TurboGears serve our controller we must create the actual application from an ``AppConfig``::

    config = AppConfig(minimal=True, root_controller=RootController())

    application = config.make_wsgi_app()

then we must actually serve the application::

    from wsgiref.simple_server import make_server

    print "Serving on port 8080..."
    httpd = make_server('', 8080, application)
    httpd.serve_forever()

Running the Python module just created will start a server on port ``8080`` with the our hello world application,
opening your browser and pointing it to ``http://localhost:8080`` should present you with an Hello World text.

Greetings
========================

Now that we have a working application it's time to say hello to our user instead of greeting the world,
to do so we can extend our controller with an ``hello`` method which gets as a parameter the person to greet::

    class RootController(TGController):
        @expose()
        def index(self):
            return 'Hello World'

        @expose()
        def hello(self, person):
            return 'Hello %s' % person

Restarting the application and pointing the browser to ``http://localhost:8080/hello?person=MyName`` should
greet you with an **Hello MyName** text.

.. note::

    How and why requests are routed to the ``index`` and ``hello`` methods is explained in
    :ref:`Object Dispatch <objectdispatch>` documentation

Passing parameters to your controllers is as simple as adding them to the url with the same name
of the parameters in your method, TurboGears will automatically map them to function arguments
when calling an exposed method.

Serving Templates
=========================

Being able to serve text isn't usually enough for a web application, for more advanced output
using a template is usually preferred. Before being able to serve a template we need to install
a template engine and enable it.

The template engine we are going to use for this example is ``Jinja2`` which is a fast and
flexible template engine with python3 support. To install jinja simply run::

    (tgenv)$ pip install jinja2

Now that the template engine is available we need to enable it in TurboGears, doing so is as
simple as adding it to the list of the available engines inside our ``AppConfig``::

    config = AppConfig(minimal=True, root_controller=RootController())
    config.renderers = ['jinja']

    application = config.make_wsgi_app()

Now our application is able to expose templates based on the Jinja template engine,
to test them we are going to create an ``hello.jinja`` file inside the same directory
where our application is available:

.. code-block:: html+jinja

    <!doctype html>
    <title>Hello</title>
    {% if person %}
      <h1>Hello {{ person }}</h1>
    {% else %}
      <h1>Hello World!</h1>
    {% endif %}

then the ``hello`` method will be changed to display the newly created template
instead of using a string directly::

    class RootController(TGController):
        @expose()
        def index(self):
            return 'Hello World'

        @expose('hello.jinja')
        def hello(self, person=None):
            return dict(person=person)

Restarting the application and pointing the browser to ``http://localhost:8080/hello`` or
``http://localhost:8080/hello?person=MyName`` will display an hello page greeting the person
whose name is passed as parameter or the world itself if the parameter is missing.

Serving Statics
===============================

Even for small web applications being able to apply style through CSS or serving javascript
scripts is often required, to do so we must tell TurboGears to serve our static files and
from where to serve them::

    config = AppConfig(minimal=True, root_controller=RootController())
    config.renderers = ['jinja']
    config.serve_static = True
    config.paths['static_files'] = 'public'

    application = config.make_wsgi_app()

After restating the application, any file placed inside the ``public`` directory will be
served directly by TurboGears. Supposing you have a ``style.css`` file you can access
it as ``http://localhost:8080/style.css``.

Going Forward
===============================

While it is possible to manually enable more advanced features like the ``SQLAlchemy`` and ``Ming``
storage backends, the application ``helpers``, ``app_globals``, ``i18n`` and all the TurboGears
features through the ``AppConfig`` object, if you need them you probably want TurboGears
to create a full featured application through the ``gearbox quickstart`` command.

The :ref:`20 Minutes Wiki Tutorial <wiki20>` provides an introduction to more complex applications
enabled all the TurboGears features, follow it if you want to unleash all the features that
TurboGears provides!
