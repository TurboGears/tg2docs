.. _hooks_and_events:

Hooks and Wrappers
=======================

TurboGears defines three ways to plug behaviors inside existing
applications and plugins: Hooks, Controller Wrappers and Application Wrappers.

**Hooks** work in an event registration and notification manner,
they permit to emit events and notify registered listeners which
are able to perform actions depending on the event itself.

**Controller Wrappers** sits between TurboGears and the controller body code,
they permit to extend controllers code much like a decorator, but can be
attached to third party controllers or application wide to any controller.

**Application Wrappers** are much like WSGI middlewares but behave and
work in the TurboGears context, so they receive the TurboGears context
and Request instead of the WSGI environ and are expected to return
a webob.Response object back.

Hooks
--------------------------

TurboGears allows you to attach callables to a wide set of events.
Most of those are available as both controller events and system
wide events.

To register a system wide even you can use the ``register`` method
of the ``tg.hooks`` object. As some hooks require being registered
before the application is running, it's common practice to
register them in your ``app_cfg.py`` file::

    def on_startup():
        print 'hello, startup world'

    def before_render(remainder, params, output):
        print 'system wide before render'

    # ... (base_config init code)
    tg.hooks.register('initialized_config', on_startup)
    tg.hooks.register('before_render', before_render)

To register controller based hooks you can use the event decorators::

    from tg.decorators import before_render

    def before_render_cb(remainder, params, output):
        print 'Going to render', output

    class MyController(TGController):
        @expose()
        @before_render(before_render_cb)
        def index(self, *args, **kw):
            return dict(page='index')

Or register them explicitly (useful when registering hooks
on third party controllers)::

    tg.hooks.register('before_render', before_render_cb, controller=MyController.index)

See :func:`tg.configuration.hooks.HooksNamespace.register` for more details on registering
hooks.

Apart from Hooks TurboGears also provide some
:ref:`Configuration Milestones<config_milestones>` you might want to have a look at
to check whenever it is more proper to register an action for a configuration milestone
or for an hook.

Available Hooks
####################

Configuration Hooks
~~~~~~~~~~~~~~~~~~~

* ``initialized_config(configurator, config)`` - new configuration got loaded by the application configurator, application not yet created.
  note that derived options that are configured during setup phase are not available here.
* ``config_setup(configurator, config)`` - configuration setup completed, application not yet created.
* ``configure_new_app(app)`` - new application got created by the application configurator.
  This is the only call that can guarantee to receive the :class:`.TGApp` instance before any
  middleware wrapping. To access configuration here use ``app.config``
* ``before_wsgi_middlewares(app) -> app`` - application wide only, called right after creating application,
  but before setting up most of the options and middleware.
  Must return the WSGI application itself.
  Can be used to wrap the application into WSGI middlewares that have to be executed after all TG ones.
* ``after_wsgi_middlewares(app) -> app`` - application wide only, called after finishing setting everything up.
  Must return the WSGI application iself.
  Can be used to wrap the application into WSGI middleware that have to be executed before the TG ones.
  Can also be used to modify the Application by mounting additional subcontrollers inside the RootController.

Request Life Cycle Hooks
~~~~~~~~~~~~~~~~~~~~~~~~

* ``before_validate(remainder, params)`` - Called before performing validation
* ``before_call(remainder, params)`` - Called after valdation, before calling the actual controller method
* ``before_render(remainder, params, output)`` - Called before rendering a controller template, ``output`` is the controller return value
* ``after_render(response)`` - Called after finishing rendering a controller template

Notifying Custom Hooks
##########################

Custom hooks can be notified using ``tg.hooks.notify``, listeners can register
for any hook name, so it as simple as notifying your own hook and documenting
them in your library documentation to make possible for other developers to listen
for them::

    tg.hooks.notify('custom_global_hook')

See :func:`tg.configuration.hooks.HooksNamespace.notify` for more details.


Controller Wrappers
------------------------------

Controller wrappers behave much like decorators, they sit between the controller
code and TurboGears. Whenever turbogears has to call that controller it will process
all the registered controller wrappers which are able to forward the request to the
next in chain or just directly return an alternative value from the controller.

Registering a controller wrapper can be done using
:meth:`.DispatchConfigurationComponent.register_controller_wrapper`.
It is possible to register a controller wrapper for a specific controller or
for the whole application, when registered to the whole application they will be
applied to every controller of the application or third party libraries::

    def controller_wrapper(next_caller):
        def call(*args, **kw):
            try:
                print 'Before handler!'
                return next_caller(*args, **kw)
            finally:
                print 'After Handler!'
        return call

    base_config.get_component('dispatch').register_controller_wrapper(controller_wrapper)

Due to the registration performance cost, controller wrappers
*can only be registered before the application started*.

See :meth:`.DispatchConfigurationComponent.register_controller_wrapper` for more details.

.. _appwrappers:

Application Wrappers
--------------------

Application wrappers are like WSGI middlewares but
are executed in the context of TurboGears and work
with abstractions like Request and Respone objects.

Application wrappers are callables built by passing
the next handler in chain and the current TurboGears
configuration.

They are usually subclasses of :class:`.ApplicationWrapper`
which provides the expected interface.

Every wrapper, when called, is expected to accept
the WSGI environment and a TurboGears context as parameters
and are expected to return a :class:`tg.request_local.Response`
instance::

    from tg.appwrappers.base import ApplicationWrapper

    class AppWrapper(ApplicationWrapper):
        def __init__(self, handler, config):
            super(AppWrapper, self).__init__(handler, config)

        def __call__(self, controller, environ, context):
            print 'Going to run %s' % context.request.path
            return self.next_handler(controller, environ, context)

Application wrappers can be registered from you application
configuration object in ``app_cfg.py``::

    base_config.register_application_wrapper(AppWrapper)

When registering a wrapper, it is also possible to specify after
which other wrapper it has to run if available::

    base_config.register_application_wrapper(AppWrapper, after=OtherWrapper)

Wrappers registered with ``after=False`` will run before any
other available wrapper (in order of registration)::

    base_config.register_application_wrapper(AppWrapper, after=False)

See :meth:`.ApplicationConfigurator.register_application_wrapper` for more details.

