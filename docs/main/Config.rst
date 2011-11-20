.. _config:

TurboGears 2 Configuration
==========================

.. module:: tg.configuration

TurboGears 2 provides a configuration system that attempts to be both
extremely flexible for power users and very simple to use for standard
projects.

Overview
--------

Like TurboGears 1, the application configuration is separated from the
deployment specific information.  In TurboGears |version| there is a
config module, containing several configuration specific python files --
these are done in python (not as INI files), because they actually setup
the TurboGears |version| application and its associated WSGI middleware.
Python provides an incredibly flexible config system with all kinds of
tools to keep you from having to repeat yourself.  But it comes with
some significant drawbacks, python is more complex than INI, and is less
declarative so can be less obvious.

But we believe these drawbacks are more than overcome by the power and
flexibility of python based configuration for the app because these
files are intended to be edited only by application developers, not by
those deploying the application. We've also worked hard to create an
environment that is generally declarative.

At the same time the deployment level configuration is done in simple
.ini files, in order to make it totally declarative, and easy for
deployers who may not be python programmers.

All of this is similar to Pylons and to TurboGears 1, but slightly
different from both.

Differences from TurboGears 1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In turbogears 1.x branches, the application specific configuration
variables were kept in a .ini file packaged inside the egg. For better
control over those variables, TurboGears |version| is now using a python
module that contains code.

The advantage of this new method is that the configuration can contain
complex python objects without adding a dependency on ConfigObj (which
was used in TG1).

One disadvantage of the new configuration system is that it does
not evaluate values in
the .ini files therefore all values are considered strings. This is
especially important when using boolean attributes and numbers as you
need to convert them before use inside your project. This will be
fixed in TurboGears 2.2 see `ticket #2240`_

.. _ticket #2240 : http://trac.turbogears.org/ticket/2240

Differences from Pylons
~~~~~~~~~~~~~~~~~~~~~~~

TurboGears |version| has done quite a bit of work to simplify the
config module in a standard Pylons quickstart, and to make the configuration
in those files as declarative as possible. This makes it easier to make small
updates to the config, and allows us to move some of the code into the
framework.

This is particularly important as it allows the framework to evolve
and change the middleware stack without forcing developers to
constantly update their code with every release.


Configuration in the INI files
------------------------------

A TurboGears quickstarted project will contain a couple of .ini files
which are used to define what WSGI app ought to be run, and to store
end-user created configuration values, which is just another way of
saying that the .ini files should contain *deployment specific*
options.

By default TurboGears provides a ``development.ini``, ``test.ini``,
and ``production.ini`` files.  These are standard ini file formats.

These files are standard INI files, as used by PasteDeploy.  The
individual sections are marked off with ``[]``'s.

.. seealso::
        Configuration file format **and options** are described in
        great detail in the `Paste Deploy documentation
        <http://pythonpaste.org/deploy/>`_.

Let's take a closer look at the ``development.ini`` file:

.. code:: wiki_root/development.ini
    :language: ini
    :section: default

If want to add some configuration option (let's say an administrator's
email) here is how you would do so. First you would edit your
``development.ini`` file and go to the end of the ``[app:main]``
section.

You can then choose a sensible name for your configuration key and add
it to the section::

  mail.from.administrator = someemail@somedomain.com

This would make sure this variable is now part of the configuration
and can be accessed from anywhere in your code. For example let's
imagine that you wanted to get this config option from a controller's
code::

  import tg
  admin_emailfrom = tg.config.get('mail.from.administrator', 'notconfigured@nodomain.com')

If the person who deployed your application forgot to add the variable
to his config file he would get the default value provided as the
second argument of the get() call.

.. note::
    The ``tg.config`` object is available at import time but until the
    configuration file is parsed, it only contains the system
    defaults.  If you need to perform startup time setup based on
    supplied configuration, you should do so in
    ``middleware.make_app()`` or in `lib/app_globals.py`.

.. warning::
    If you set a value like enable_subsystem = false, it will be
    loaded into python as the string 'false' which if used in a
    conditional will give you a very wrong result

The correct way of loading boolean values for your use is

.. code-block:: python

   from paste.deploy.converters import asbool
   if asbool(config['enable_subsystem']):
      ... sub systems is enabled...

The config module
-----------------
.. tip::
    A good indicator of whether an option should be set in the
    ``config`` directory code vs. the configuration file is whether or
    not the option is necessary for the functioning of the
    application. If the application won't function without the
    setting, it belongs in the appropriate `config/` directory
    file. If the option should be changed depending on deployment, it
    belongs in the ini files.

Our hope is that 90% of applications don't need to edit any of the
config module files, but for those who do, the most common file to
change is ``app_config.py``

.. code:: wiki_root/wiki20/config/app_cfg.py
    :language: python

app_cfg.py exists primarily so that middleware.py and environment.py
can import and use the ``base_config`` object.

The ``base_config`` object is an ``AppConfig()`` instance which allows
you to access its attributes like a normal object, or like a standard
python dictionary.

One of the reasons for this is that ``AppConfig()`` provides some
defaults in its ``__init__``.  But equally important it provides us
with several methods that work on the config values to produce the two
functions that set up your TurboGears app.

We've taken care to make sure that the entire setup of the
TurboGears |version| framework is done in code which you as the
application developer control. You can easily customize it to your needs.
If the standard config options we provide don't do what you need, you
can subclass and override ``AppConfig`` to get exactly the setup you want.

The ``base_config`` object that is created in ``app_cfg.py`` should be
used to set whatever configuration values that belong to the
application itself and are required for all instances of this app, as
distinct from the configuration values that you set in the
``development.ini`` or ``production.ini`` files that are intended to
be editable by those who deploy the app.

As part of the app loading process the ``base_config`` object will be
merged in with the config values from the .ini file you're using to
launch your app, and placed in ``tg.config`` (also known as
``pylons.config``).

As we mentioned previously, in addition to the attributes on the
``base_config`` object there are a number of methods which are used to
setup the environment for your application, and to create the actual
TurboGears WSGI application, and all the middleware you need.

You can override ``base_config``'s methods to further customize your
application's WSGI stack, for various advanced use cases, like adding
custom middleware at arbitrary points in the WSGI pipeline, or doing
some unanticipated (by us) application environment manipulation.

And we'll look at the details of how that all works in the advanced
configuration section of this document.

Configuring your application
----------------------------------------------

Here's are some of the more general purpose configuration attributes:

Configuration Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The configuration object has a number of attributes that automate
the majority of what you need to do with the config object.  These
shortcuts eliminate the need to provide your own setup methods
for configuring your TurboGears application.

Mimetypes
+++++++++++++

By default, only json/application and text/html are defined mimetypes.
If you would like to use additional mime-types you must register
them with your application's config. You can accomplish this by
adding the following code your your app_cfg.py file::

    base_config.mimetype_lookup = {'.ext':'my-mimetype'}


Hooks and Events
+++++++++++++++++++++

TurboGears allows you to attach callables to a wide set of events.
Most of those are available as both controller events and system
wide events.

To register a system wide even you can use the ``register_hook`` method
of the ``base_config`` object in your ``app_cfg.py`` file::
    
    def on_startup():
        print 'hello, startup world'

    def on_shutdown():
        print 'hello, shutdown world'

    def before_render(remainder, params, output):
        print 'system wide before render'

    # ... (base_config init code)

    base_config.register_hook('startup', on_startup) 
    base_config.register_hook('shutdown', on_shutdown)
    base_config.register_hook('before_render', before_render)

To register controller based hooks you can use the event decorators::

    from tg.decorators import before_render

    def before_render_cb(remainder, params, output):
        print 'Going to render', output

    class MyController(TGController):
        @expose()
        @before_render(before_render_cb)
        def index(self, *args, **kw):
            return dict(page='index')

Available Hooks
####################

* ``startup()`` - application wide only, called when the application starts
* ``shutdown()`` - application wide only, called when the application exits
* ``before_config(app) -> app`` - application wide only, called after constructing the application,
    but before setting up most of the options and middleware.
    Must return the application itself.
    Can be used to wrap the application into middlewares that have to be executed having the full TG stack available.
* ``after_config(app) -> app`` - application wide only, called after finishing setting everything up.
    Must return the application iself.
    Can be used to wrap the application into middleware that have to be executed before the TG ones.
    Can also be used to modify the Application by mounting additional subcontrollers inside the RootController.
* ``before_validate(remainder, params)`` - Called before performing validation
* ``before_call(remainder, params)`` - Called after valdation, before calling the actual controller method
* ``before_render(remainder, params, output)`` - Called before rendering a controller template, ``output`` is the controller return value
* ``after_render(response)`` - Called after finishing rendering a controller template

Static Files
++++++++++++++++

``base_config.serve_static`` -- automatically set to ``True`` for you.
Set to False if you have set up apache, or nginx (or some other
server) to handles static files.

Request Extensions
+++++++++++++++++++++++

``base_config.disable_request_extensions`` -- by default this is false.
This means that TG will take the request, and strip anything off the end
of the last element in the URL that follows ".".  It will then take this
information, and assign an appropriate mime-type and store the data in the
tg.request.response_type and tg.request.response_ext variables.  By enabling
this flag, you disable this behavior, rendering TG unable to determine the
mime-type that the user is requesting automatically.


Stand Alone
+++++++++++++++

``base_config.stand_alone`` -- set this to ``False`` if you don't want
error handling, HTTP status code error pages, etc.  This is intended
for the case where you're embedding the TG app in some other WSGI app
which handles these things for you.


Cookie Secret
+++++++++++++++

The ``beaker.session.secret`` key of the ``base_config`` object
contains the secret used to store user sessions.  Pylons automatically
generates a random secret for you when you create a project.  If an
attacker gets his hands on this key, he will be able to forge a valid
session an use your application at though he was logged in.  In the
event of a security breach, you can change this key to invalidate all
user sessions.

Authentication Character Set
+++++++++++++++++++++++++++++

Set ``base_config.sa_auth.charset`` to define the character encoding for your
user's login.  This is especially important if you expect your users to have
non-ascii usernames and passwords.  To set it to utf-8, your add this to your
app_config.py file.::

   base_config.sa_auth.charset = 'utf-8'

Advanced Configuration
-------------------------

Sometimes you need to go beyond the basics of setting configuration
options.  We've created a number of methods that you can use to override the way
that particular pieces of the TurboGears |version| stack are configured.
The basic way you override the configuration within app.cfg looks something
like this::

    from tg.configuration import AppConfig
    from tw2.core.middleware import TwMiddleware

    class MyAppConfig(AppConfig):

        def add_tosca2_middleware(self, app):

            app = TwMiddleware(app,
                default_engine=self.default_renderer,
                translator=ugettext,
                auto_reload_templates = False
                )

            return app
    base_config = MyAppConfig()

    # modify base_config parameters below

The above example shows how one would go about overridding the toscawidgets2
middleware.  See the class definition below for more ideas on how you
could modify your own custom config

AppConfig General Options
---------------------------

.. autoclass:: AppConfig
   :members: init_config,
             add_core_middleware,
             add_error_middleware,
             setup_tg_wsgi_app,
             setup_helpers_and_globals,
             make_load_environment


More Configuration Options
------------------------------
These configuration options have been broken into sub pages for easier digestion.


.. toctree::
   :maxdepth: 1

   Config/Rendering
   Config/Authorization
   Config/Routes
   Config/ToscaWidgets
   Config/SQLAlchemy
