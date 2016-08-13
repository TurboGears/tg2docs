.. _minimal-tutorial:

============================
Get Started with TurboGears2
============================

The fastest way to start using TurboGears is through the **minimal mode**, when using TurboGears with
minimal mode a default setup that minimizes dependencies and complexity is provided.

.. note::

    While minimal mode is well suited for small simple web applications or web services, for more complex
    projects moving to a package based configuration is suggested.

.. _minimal-setup:

Installing TurboGears2
======================

This tutorial takes for granted that you have a working Python environment
with Python2.6+ or Python3.3+, with `pip <http://www.pip-installer.org/en/latest/>`_
installed and you have a working browser to look at the web application
you are developing.

This tutorial doesn't cover Python at all. Check the `Python Documentation`_ page
for more coverage of Python.

Creating Virtual Environment
----------------------------

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

Installing TurboGears
---------------------

Now we are ready to install TurboGears itself:

.. parsed-literal::

    (tgenv)$ pip install TurboGears2

Hello World
===========

A TurboGears application consists of an ``AppConfig`` application configuration and an application ``RootController``.
The first is used to setup and create the application itself, while the latter is used to dispatch requests
and take actions.

For our first application we are going to define a controller with an index method that just tells *Hello World*.
Just create a new ``tgapp.py`` file and declare your ``RootController``::

    from tg import expose, TGController, AppConfig

    class RootController(TGController):
        @expose()
        def index(self):
            return 'Hello World'

Now to make TurboGears serve our controller we must create the actual application from an ``AppConfig``::

    config = AppConfig(minimal=True, root_controller=RootController())

    application = config.make_wsgi_app()

then we must actually serve the application::

    from wsgiref.simple_server import make_server

    print("Serving on port 8080...")
    httpd = make_server('', 8080, application)
    httpd.serve_forever()

Running ``python tgapp`` (the python module we just created) will start a server on port ``8080``
with the our hello world application, opening your browser and pointing it
to ``http://localhost:8080`` should present you with an Hello World text.

Serving Multiple Pages
======================

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
=================

Being able to serve text isn't usually enough for a web application, for more advanced output
using a template is usually preferred. Before being able to serve a template we need to install
a template engine and enable it.

The template engine used by TurboGears is :ref:`Kajiki-language` which is a fast and
validated template engine with python3 support. To install Kajiki simply run::

    (tgenv)$ pip install kajiki

Now that the template engine is available we need to enable it in TurboGears, doing so is as
simple as adding it to the list of the available engines inside our ``AppConfig``::

    config = AppConfig(minimal=True, root_controller=RootController())
    config.renderers = ['kajiki']

    application = config.make_wsgi_app()

Now our application is able to expose templates based on the Kajiki template engine,
to test them we are going to create an ``hello.xhtml`` file inside the same directory
where our application is available:

.. code-block:: html+genshi

    <html>
        <title>Hello</title>
        <py:if test="person">
            <h1>Hello ${person}</h1>
        </py:if><py:else>
            <h1>Hello World!</h1>
        </py:else>
    </html>

then the ``hello`` method will be changed to display the newly created template
instead of using a string directly::

    class RootController(TGController):
        @expose()
        def index(self):
            return 'Hello World'

        @expose('hello.xhtml')
        def hello(self, person=None):
            return dict(person=person)

Restarting the application and pointing the browser to ``http://localhost:8080/hello`` or
``http://localhost:8080/hello?person=MyName`` will display an hello page greeting the person
whose name is passed as parameter or the world itself if the parameter is missing.

Enabling Helpers
----------------

Helpers are python functions which render small HTML snippets that can be useful in your
templates. This might include your user avatar, a proper date formatter or whatever might
come in hand in your templates. Those are usually provided by turbogears with the ``h`` name
inside all your templates.

TurboGears2 usually provides the ``WebHelpers2`` package in applications quickstarted in
full stack mode, but this can be easily made available in minimal mode too.

First we are going to install the ``WebHelpers2`` package::

    $ pip install webhelpers2

Then we are going to import webhelpers2 and register it in our configuration as the application
helpers (any python module or object can be registered as the helpers)::

    import webhelpers2
    import webhelpers2.text
    config['helpers'] = webhelpers2

Now the helpers are available in all our templates as ``h.helpername`` and in this case
we are going to use the ``text.truncate`` helper to truncate strings longer than 5 characters
in our ``hello.xhtml`` template:

.. code-block:: html+genshi

    <html>
        <title>Hello</title>
        <py:if test="person">
            <h1>Hello ${h.text.truncate(person, 5)}</h1>
        </py:if><py:else>
            <h1>Hello World!</h1>
        </py:else>
    </html>

By restarting the application you will notice that pointing the browser to
``http://localhost:8080/hello?person=World`` prints **Hello World** while pointing it to
``http://localhost:8080/hello?person=TurboGears`` will print ``Hello Tu...`` as TurboGears is
now properly truncated.

Serving Static Files
====================

Even for small web applications being able to apply style through CSS or serving javascript
scripts is often required, to do so we must tell TurboGears to serve our static files and
from where to serve them::

    config = AppConfig(minimal=True, root_controller=RootController())
    config.renderers = ['kajiki']
    config.serve_static = True
    config.paths['static_files'] = 'public'

    application = config.make_wsgi_app()

After restating the application, any file placed inside the ``public`` directory will be
served directly by TurboGears. Supposing you have a ``style.css`` file you can access
it as ``http://localhost:8080/style.css``.

Working With Database
=====================

TurboGears2 supports both SQL dbms through SQLAlchemy and MongoDB through Ming, both can be
enabled with some options and by providing a Model for the application.

The following will cover how to work with SQLAlchemy and extend the sample application to
log and retrieve a list of greeted people.
First we will need to enable SQLAlchemy support for our application::

    config['use_sqlalchemy'] = True
    config['sqlalchemy.url'] = 'sqlite:///devdata.db'

Now TurboGears will configure a SQLAlchemy engine for us, but it will require that we provide
a data model, otherwise it will just crash when starting up. This can be done by providing a
*database Session* and a model initialization function::

    from tg.util import Bunch
    from sqlalchemy.orm import scoped_session, sessionmaker

    DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))

    def init_model(engine):
        DBSession.configure(bind=engine)

    config['model'] = Bunch(
        DBSession=DBSession,
        init_model=init_model
    )

This will properly make our application work and able to interact with the database, but it won't
do much as we are not actually declaring any table or model to work with.

Accessing Data
--------------

To start working with tables and the data they contain we need to declare the table itself, this
can be done through the SQLAlchemy declarative layer by using a Declarative Base class::

    from sqlalchemy.ext.declarative import declarative_base

    DeclarativeBase = declarative_base()

From this class we can then inherit all our models::

    from sqlalchemy import Column, Integer, DateTime, String
    from datetime import datetime


    class Log(DeclarativeBase):
        __tablename__ = 'logs'

        uid = Column(Integer, primary_key=True)
        timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
        person = Column(String(50), nullable=False)

This will allow us to read and write rows from the ``logs`` table, but before we are able
to do so we must ensure that the table actually exists, which can be done by extending our
model initialization function to create the tables::

    def init_model(engine):
        DBSession.configure(bind=engine)
        DeclarativeBase.metadata.create_all(engine)  # Create tables if they do not exist

Now we can finally extend our controller to log the people we greet and provide us the
list of past greetings::

    class RootController(TGController):
        @expose(content_type='text/plain')
        def index(self):
            logs = DBSession.query(Log).order_by(Log.timestamp.desc()).all()
            return 'Past Greetings\n' + '\n'.join(['%s - %s' % (l.timestamp, l.person) for l in logs])

        @expose('hello.xhtml')
        def hello(self, person=None):
            DBSession.add(Log(person=person or ''))
            DBSession.commit()
            return dict(person=person)


Going Full Stack
================

While it is possible to manually enable the TurboGears features like the ``SQLAlchemy`` and ``Ming``
storage backends, the application ``helpers``, ``app_globals``, ``i18n`` features through the
:class:`AppConfig` object, if you need them you probably want to switch to **full stack** mode and
to create a full stack application through the ``gearbox quickstart`` command.

The :ref:`Full Stack Tutorial <wiki20>` provides an introduction to more complex applications
with all the TurboGears features enabled, follow it if you want to unleash all the features that
TurboGears provides!

.. _Python Documentation: http://www.python.org/doc
