.. _config:

Configuration Process
=====================

.. module:: tg.configuration

TurboGears 2 provides a configuration system that attempts to be both
extremely flexible for power users and very simple to use for standard
projects.

Overview
--------

The application configuration is separated from the deployment specific information.  

In a TurboGears |version| application there is a config module,
containing several configuration specific python files --
these are done in python (not as INI files), because they actually setup
the TurboGears application and its associated WSGI middleware.

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
``.ini`` files, in order to make it totally declarative, and easy for
deployers who may not be python programmers.

Application Configuration Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each TurboGears application is configured by a :class:`tg.ApplicationConfigurator`,
usually a :class:`tg.FullStackApplicationConfigurator` ( or a :class:`tg.MinimalApplicationConfigurator`
in case of small or heavily custom apps).

Usually a configurator instance will be created within the
``config/app_cfg.py`` module.

The configurator is in charge of setting up the application configuration,
that will be available as a property of the applications created with
that configuration (``TGApp.config``) and as ``tg.config`` during requests.

.. note::

    Outside of requests, ``tg.config`` will refer to the configuration of
    the current process wide application. Which is the last application
    configured in the current process.

    Before any application is configured, ``tg.config`` will contain
    the default configuration values. You should usually avoid reading
    it before the ``milestones.config_ready`` milestone fired and you
    should prefer relying on ``initialized_config`` hook to ensure you
    access application configuration outside of a request.

Configuration Blueprint
~~~~~~~~~~~~~~~~~~~~~~~

The configuration is built from a **blueprint**, which is a set of
rules and default options that is used as the foundation for the
configuration being built.

On top of the blueprint, all the options provided through the ``.ini``
file are applied. Once all those options are configured the 
``initialized_config`` hook is fired and the components setup
process is started.

Some additional configuration can happen during the components
setup and the final configuration, as seen by the application, will
result from this last step. The ``config_setup`` hook is fired
at the end of this phase to signal that configuration setup completed.

Configuration in the INI files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. warning::
    If you set a value like enable_subsystem = false, it will be
    loaded into python as the string 'false' which if used in a
    conditional will give you a very wrong result

The correct way of loading boolean values for your use is

.. code-block:: python

   from tg.support.converters import asbool

   if asbool(config['enable_subsystem']):
      ... sub systems is enabled...

Configuration components, will instead take care of their own
variable conversion. Thus if it's an option declared by a component,
it will already be converted to the proper type.

Refer to :ref:`config-options` for all the components configuration
options.

.. _config_milestones:

Configuration Milestones
----------------------------

Since TurboGears 2.3 the configuration process got divided in various
milestones, each of those milestones is bound to an advancement in the
framework setup process.

Whenever a milestone is reached all the registered callbacks are fired
and the configuration process can continue. If the milestone is already
passed when a callback is registered, the callback gets instantly fired.

Milestone behave like :ref:`hooks <hooks_and_events>`, but they are not
bound to a specific application, they refer to the main process application
(in case multiple TG applications are running within the same process).

.. note::
    The ``tg.config`` object is available at import time but until the
    configuration file is parsed, it only contains the system
    defaults.  If you need to perform startup time setup based on the
    supplied configuration, you should do so in a milestone or in an hook.

Milestones are available through the ``tg.configuration.milestones``
module, the currently provided milestones are:

* ``milestones.config_ready`` - Configuration file has been loaded and is
  available in ``tg.config`` for the main application.
* ``milestones.renderers_ready`` - Renderers have been registered and all
  of them are available.
* ``milestones.environment_loaded`` - Full environment have been loaded
  but application has not been created yet.

Registering an action to be executed whenever a milestone is reach
can be done using :func:`tg.configuration.milestones._ConfigMilestoneTracker.register`
method of each milestone. The registered action takes no parameters.

Milestones are much like :ref:`Hooks<hooks_and_events>` but they are
only related to the configuration process. The major difference is that
*while an hook can fire multiple times a milestone can be reached only once*.

Milestones and Hooks order of execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The order of execution of the milestones and hooks provided during the
application startup process is:

* ``milestones.config_ready``
* *initialized_config Hook*
* ``milestones.renderers_ready``
* *config_setup Hook*
* ``milestones.environment_loaded``
* *configure_new_app Hook*
* *before_wsgi_middlewares Hook*
* *after_wsgi_middlewares Hook*

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
change is ``app_cfg.py``:

.. code-block:: python

    from tg import FullStackApplicationConfigurator

    import plain24
    from plain24 import model, lib

    base_config = FullStackApplicationConfigurator()

    # General configuration
    base_config.update_blueprint({
        # True to prevent dispatcher from striping extensions
        # For example /socket.io would be served by "socket_io"
        # method instead of "socket".
        'disable_request_extensions': False,

        # Set None to disable escaping punctuation characters to "_"
        # when dispatching methods.
        # Set to a function to provide custom escaping.
        'dispatch_path_translator': True,

        'package': plain24,
    })

    # ToscaWidgets configuration
    base_config.update_blueprint({
        'tw2.enabled': True,
    })

    # Rendering Engines Configuration
    base_config.update_blueprint({
        'renderers': ['json', 'kajiki'],
        'default_renderer': 'kajiki',
        'templating.kajiki.strip_text': False
    })

    # Configure Sessions, store data as JSON to avoid pickle security issues
    base_config.update_blueprint({
        'session.enabled': True,
        'session.data_serializer': 'json',
    })

    # Configure the base SQLALchemy Setup
    base_config.update_blueprint({
        'use_sqlalchemy': True,
        'model': plain24.model,
        'DBSession': plain24.model.DBSession,
    })

    [ ... ]

``app_cfg.py`` exists primarily so that ``application.py``
can import and use the ``base_config`` object to create the application
using that configurator.

The ``base_config`` object is the configurator in charge of preparing
the configuration of our application and creating it.

We've taken care to make sure that the entire setup of the
TurboGears framework is done in code which you as the
application developer control. You can easily customize it to your needs.
If the standard config flow we provide don't do what you need, you
can replace specific configuration components to get exactly the setup you want.

You can refer to :class:`.FullStackApplicationConfigurator` documentation
for the list of components enabled by default.

The ``base_config`` object that is created in ``app_cfg.py`` should be
used to set a blueprint with configuration values that belong to the
application itself and are required for all instances of this app, as
distinct from the configuration values that you set in the
``development.ini`` or ``production.ini`` files that are intended to
be editable by those who deploy the app.

As part of the app loading process the blueprint from ``base_config``
will be merged in with the config values from the .ini file you're using to
launch your app, and placed in ``tg.config``.

Configuring your application
----------------------------

The configurator object comes with a bunch of preregistered components
that automate the majority of what you need to do.
These shortcuts eliminate the need to provide your own setup methods
for configuring your TurboGears application.

To see the list of available configuration options refer to :ref:`config-options`.

Advanced Configuration
-------------------------

Sometimes you need to go beyond the basics of setting configuration
options.

You might want to replace behaviours of your application or add new
components that are not available in TurboGears by default.

That can be done by registering or replacing components in the configurator
object.

Registering New Components
~~~~~~~~~~~~~~~~~~~~~~~~~~

Registering new components is done through the :meth:`.FullStackApplicationConfigurator.register`
method. Provide the component to the method and a new instance of that component will be
bound to the configurator.

For example we might want to create a component that prints ``"Hello IPADDRESS"`` on each
new request. The way we would do that within app.cfg looks something like this::

    from tg.configurator import ConfigurationComponent, EnvironmentLoadedConfigurationAction
    from tg.support.converters import asbool

    class HelloWorldConfigurationComponent(ConfigurationComponent):
        """A component that will say hello world on each new request"""
        id = 'helloworld'

        def get_defaults(self):
            return {
                'helloworld.enabled': True
            }

        def get_coercion(self):
            return {
                'helloworld.enabled': asbool
            }

        def on_bind(self, configurator):
            from tg.appwrappers import ApplicationWrapper
            class HelloWorldApplicationWrapper(ApplicationWrapper):
                def __init__(self, handler, config):
                    super(HelloWorldApplicationWrapper, self).__init__(handler, config)

                    # The option will always be there because the
                    # HelloWorldConfigurationComponent declares a default for it
                    # and will always be a boolean value because a coercion
                    # is also declared.
                    self.enabled = config['helloworld.enabled']

                @property
                def injected(self):
                    return self.enabled

                def __call__(self, controller, environ, context):
                    print 'Hello %s' % (environ['REMOTE_HOST'], )
                    return self.next_handler(controller, environ, context)

            configurator.register_application_wrapper(HelloWorldApplicationWrapper, after=True)

Then, once our component is ready, we can register it within our application configurator::

    base_config = FullStackApplicationConfigurator()

    base_config.register(HelloWorldConfigurationComponent)

The configurator will use it during the configuration phase and will trigger any
associated action. Refer to :class:`.ConfigurationComponent` for details on
how a configuration component is made.

Replacing Components
~~~~~~~~~~~~~~~~~~~~

Currently registered component (including those registered by TG itself),
can be replaced using :meth:`.FullStackApplicationConfigurator.replace`.

Provided the component ``identifier`` (which is usually available in the
component class itself as the ``.id`` property) we can replace the
component that has that identifier with a new component.

.. note::

    When replacing components, make sure that the new component has
    the same ``.id`` attribute of the old one, while this is not required,
    it will cause confusion to have a component named ``"foobar"`` being
    registered for ``"somethingelse"``.

Suppose we have a component that prints ``"Ready to Fly!"`` when the
application is ready::

    class ReadyToFlyConfigurationComponent(ConfigurationComponent):
        """A component that print when the application is ready!"""
        id = "ready2fly"

        def get_actions(self):
            from tg.configurator import AppReadyConfigurationAction
            return (
                AppReadyConfigurationAction(self._print_ready),
            )

        def _print_ready(self, conf, app):
            print 'Ready to Fly!'
            return app

.. note::

    The ``AppReadyConfigurationAction`` is usually also the right
    time to add WSGI middlewares to your application as it allows
    you to return a new WSGI application in place of the original one.
    So you can't take for granted that the ``app`` your receive is
    actually a :class:`.TGApp`, but it can be any WSGI application
    that wraps the TGApp.

That component will be registered against the configurator::

   base_config.register(ReadyToFlyConfigurationComponent)

and from that moment on will be known by the configurator
with the ``ready2fly`` identifier.

Now, if we want to change its behaviour, and instead of printing
``"Ready to Fly!"`` we want to print ``"Ready for take off!"``,
we can sublcass the component, replace its ``_print_ready``
implementation and replace the component itself::

    class ReadyForTakeOffConfigurationComponent(ReadyToFlyConfigurationComponent):
        def _print_ready(self, conf, app):
            print 'Ready for take off!'
            return app

    base_config.replace("ready2fly", ReadyForTakeOffConfigurationComponent)

So, instead of the ``ReadyToFlyConfigurationComponent`` we will
use the ``ReadyForTakeOffConfigurationComponent``.

This can be used to replace also TurboGears provided components,
see :mod:`tg.configurator.components` for all components provided
by TurboGears.
