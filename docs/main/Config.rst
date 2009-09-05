.. _config:

TurboGears 2 Configuration
==========================

TurboGears 2 provides a configuration system that attempts to be both
extremely flexible for power users and very simple to use for standard
projects.

Overview
--------

Like TurboGears 1, the application configuration is separated from the
deployment specific information.  In TG2 there is a config module,
containing several configuration specific python files -- these are
done in python (not as INI files), because they actually setup the TG2
application and its associated WSGI middleware. Python provides an
incredibly flexible config system with all kinds of tools to keep you
from having to repeat yourself.  But it comes with some significant
drawbacks, python is more complex than INI, and is less declarative so
can be less obvious.

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
variables was kept in a .ini file packaged inside the egg. For better
control over those variables, TG2 is now using a python module that
contains code.

The advantage of this new method is that the configuration can contain
complex python objects without adding a dependency on ConfigObj (which
was used in TG1).

One disadvantage of the system is that it does not evaluates values in
the .ini files therefore all values are considered strings. This is
especially important when using boolean atributes and numbers as you
need to convert them before use inside your project. This will be
fixed in TG2.1 see `ticket #2240`_

.. _ticket #2240 : http://trac.turbogears.org/ticket/2240

Differences from Pylons
~~~~~~~~~~~~~~~~~~~~~~~

TG2 has done quite a bit of work to simplify the config module in a
standard pylons quickstart, and to make the configuration in those
files as declarative as possible. This makes it easier to make small
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
saying that the .ini files should contain \deployment specific\
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

..warning ::
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

We've taken care to make sure that the entire setup of the TG2
framework is done in code which you as the application developer
control. You can easily customize it to your needs.  If the standard
config options we provide don't do what you need, you can subclass and
override ``AppConfig`` to get exactly the setup you want.

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

As we said, in addition to the attributes on the ``base_config``
object there are a number of methods which are used to setup the
environment for your application, and to create the actual Turbogears
WSGI application, and all the middleware you need.

You can override ``base_config``'s methods to further customize your
application's WSGI stack, for various advanced use cases, like adding
custom middleware at arbitrary points in the WSGI pipeline, or doing
some unanticipated (by us) application environment manipulation.

And we'll look at the details of how that all works in the advanced
configuration section of this document.

Setting up the base configuration for your app
----------------------------------------------

The most common configuration change you'll likely want to make here
is to add a second template engine or change the template engine used
by your project.

By default TurboGears sets up the Genshi engine, but we also provide
out of the box support for Mako, Jinja and Chameleon-Genshi. To tell
TG to prepare these templating engines for you all you need to do is
install the package and append 'mako' or 'jinja' to the renderer's
list here in app_config.  For Chameleon the installation is more
complex but the steps are the same.

To change the default renderer to something other than Genshi, just
set the default_renderer to the name of the rendering engine.  So, to
add Mako to the list of renderers to prepare, and set it to be the
default, this is all you'd have to do::

  base_config.default_renderer = 'mako'
  base_config.renderers.append('mako')

Here's a full list of the configuration options:

Template rendering config settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``base_config.default_renderer`` -- set to the name of the default
render function you want to use.

``base_config.renderers`` -- This is a list of render functions that
ought to be prepared for use in the app.  This is a shortcut for the
four renderers that TG2 provides out of the box. The four allowed
values are `'genshi'`, `'chamelion_genshi'`, `'mako'`, and `'jinja'`.

``base_config.use_legacy_renderer`` -- If ``True`` old style buffet
renderers will be used.  Don't set this unless you need buffet
renderers for some specific reason, buffet renderers are deprecated
and will probably be removed in 2.1.

``base_config.use_dotted_templatenames`` -- Generally you will not
want to change this.  But if you want to use the standard
genshi/mako/jinja file system based template search paths, set this to
`False`.  The main advantage of dotted template names is that it's
very easy to store template files in zipped eggs, but if you're not
using packaged TG2 app components there are some advantages to the
search path syntax.

``base_config.renderers`` -- a dictionary with the render function
name as the key, and the actual configured render function as the
value.  For the four standard renderers it's enough to just add the
name to ``base_config.renderers`` but for custom renderers you want to
set the renderer up, and set it in this dictionary directly.

Turning on and off features
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``base_config.serve_static`` -- automatically set to ``True`` for you.
Set to False if you have set up apache, or nginx (or some other
server) to handles static files.

``base_config.stand_alone`` -- set this to ``False`` if you don't want
error handling, HTTP status code error pages, etc.  This is intended
for the case where you're embedding the TG app in some other WSGI app
which handles these things for you.

``base_config.use_toscawidgets`` -- Set to False to turn off
Toscawidgets.

``base_config.use_transaction_manager`` -- Set to False to turn off the
Transaction Manager and handle transactions yourself.


Advanced Configuration
======================

Sometimes you need to go beyond the basics of setting configuration
options.

Modifying the environment loader and middleware stack
-----------------------------------------------------

We've created a number of methods that you can use to override the way
that particular pieces of the TG2 stack are configured.


.. automodule:: tg.configuration
.. autoclass::  AppConfig
   :members:



Embedding a TG app inside another TG app
----------------------------------------

One place where you'll have to be aware of how all of this works is
when you programatically setup one TurboGears app inside another.

In that case, you'll need to create your own ``base_config`` like
object to use when configuring the inside WSGI application instance.
 
Fortunately, this can be as simple as creating your own
``base_config`` object from AppConfig(), creating your own app_conf
and global dictionaries, and creating an environment loader::

  load_environment = my_conf_object.make_load_environment()
  make_wsgi_app = my_conf_object.setup_tg_wsgi_app(load_environment)
  final_app = make_wsgi_app(global_conf, app_conf)

Using Config outside of a quickstarted project:
-----------------------------------------------

.. todo:: Document how to use config outside of a quickstarted project
