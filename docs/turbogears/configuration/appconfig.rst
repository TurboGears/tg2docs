.. _config:

TurboGears 2 Configuration
==========================

.. module:: tg.configuration

TurboGears 2 provides a configuration system that attempts to be both
extremely flexible for power users and very simple to use for standard
projects.

Overview
--------

The application configuration is separated from the
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
change is ``app_config.py``:

.. code-block:: python

    from tg.configuration import AppConfig
    import wiki20
    from wiki20 import model
    from wiki20.lib import app_globals, helpers

    base_config = AppConfig()
    base_config.renderers = []

    base_config.package = wiki20

    #Set the default renderer
    base_config.default_renderer = 'genshi'
    base_config.renderers.append('genshi')

    #Configure the base SQLALchemy Setup
    base_config.use_sqlalchemy = True
    base_config.model = wiki20.model
    base_config.DBSession = wiki20.model.DBSession

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
launch your app, and placed in ``tg.config``.

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
contains the secret used to store user sessions.  TurboGears automatically
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
middleware.  See the :py:class:`AppConfig` for more ideas on how you
could modify your own custom config
