Upgrading Your TurboGears Project
=================================

From 2.3.4 to 2.3.5
-------------------

Genshi Work-Around available for Python3.4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Genshi 0.7 suffers from a bug that prevents it from working on Python 3.4
and causes an Abstract Syntax Tree error, to work-around this issue
TurboGears provides the ``genshi.name_constant_patch`` option that
can be set to ``True`` to patch Genshi to work on Python 3.4.

Configuration Flow Refactoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In previous versions the ``AppConfig`` object won over the
*.ini file* options for practically everything, now the configurator
has been modified so that AppConfig options are used as a template
and for most options the *.ini file* wins over them.

There are still some options that are immutable and can only be
defined in the ``AppConfig`` itself, but most of them can now
be changed from the ini files.

Now the ``tg.config`` object will always be reconfigured from scratch
when an application is created. Previously each time an application
was created it incrementally modified the same config object leading
to odd behaviours. This should not impact your app unless you
called ``AppConfig.setup_tg_wsgi_app`` multiple times.

Another minor change is that ``AppConfig.after_init_config``
is now expected to accept a parameter with the configuration
dictionary. So if you implemented a custom ``after_init_config``
method it is required to acccept the config dictionary and
make configuration changes in it.

Application Wrappers now provide a clearly defined interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`.ApplicationWrapper` abstract base class has been defined
to provide a clear interface for application wrappers, all TurboGears
provided application wrappers now adhere this interface.

I18N Translations now provided through an Application Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`.I18NApplicationWrapper` now provides support for translation
detection from browser language and user session. This was previously
builtin into the TurboGears Dispatcher even though it was not related
to dispatching itself.

The behaviour should remain the same apart from the fact that
it is now executed before entering the TurboGears application
and that some options got renamed:

    - ``lang`` option has been renamed to ``i18n.lang``.
    - ``i18n_enabled`` has been renamed to ``i18n.enabled``
    - ``beaker.session.tg_avoid_touch`` option has been renamed to
      ``i18n.no_session_touch`` as it is only related to i18n.
    - ``lang_session_key`` got renamed to ``i18n.lang_session_key``.

For a full list of option available please refer to
:class:`.I18NApplicationWrapper` itself.

Session and Cache Middlewares replaced by Application Wrappers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``SessionMiddleware`` and ``CacheMiddleware`` were specialized
Beaker middleware for session and caching. To guarantee better
integration with TurboGears and easier configuration they have been
switched to Application Wrappers.

The ``use_sessions=True`` option got replaced by ``session.enabled=True``
and an additional ``cache.enabled=True`` option has been added.

For a full list of options refer to the :class:`.CacheApplicationWrapper`
and :class:`.SessionApplicationWrapper` references.

To deactivate the application wrappers and switch back to the
old middlewares, use::

    base_config['session.enabled'] = False
    base_config['use_session_middleware'] = True

and::

    base_config['cache.enabled'] = False
    base_config['use_cache_middleware'] = True

StatusCodeRedirect middleware replaced by ErrorPageApplicationWrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``StatusCodeRedirect`` middleware was inherited from Paste project,
and was in charge of intercepting status codes and redirect to an
error page in case of one of those.

So the ``status_code_redirect=True`` option got replaced by the
``errorpage.enabled=True`` option. For a full list of options refer
to the :class:`.ErrorPageApplicationWrapper` reference.

As ``StatusCodeRedirect`` worked at WSGI level it was pretty slow and
required to read the whole answer just to get the status code.
Also the TurboGears context (request, response, app_globals and so on)
were lost during the execution of the ``ErrorController``.

In ``2.3.5`` this got replaced by the :class:`.ErrorPageApplicationWrapper`,
which provides the same feature using an :ref:`appwrappers`.

If you are still relying on ``pylons.original_response`` key in your
``ErrorController`` make sure to uprade to the ``tg.original_response`` key,
otherwise it won't work anymore.

The change should be transparent for most users, in case you want to get back the
old ``StatusCodeRedirect`` behaviour you use the following option::

    base_config['status_code_redirect'] = True

Keep in mind that the other options from :class:`.ErrorPageApplicationWrapper`
apply and are converted to options for the ``StatusCodeRedirect``
middleware.

Transaction Manager is now an application wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transaction Manager (the component in charge of committing or rolling back your
sqlalchemy transaction) is now replaced by :class:`.TransactionApplicationWrapper`
which is an application wrapper in charge of committing or rolling back the transaction.

So the ``use_transaction_manager=True`` option got replaced by
the ``tm.enabled=True`` option. For a full list of options refer to the
:class:`.TransactionApplicationWrapper` reference.

There should be no behavioural changes with this change, the only difference
is now that the transaction manager applies before the WSGI middlewares as
it is managed by TurboGears itself. So if your application was successfull
and there was an error in a middleware that happens after (for example
ToscaWidgets resource injection) the transaction will be commited anyway
as the code that created the objects and for which they should be committed
was successful.

If you want to recover back the *old TGTransactionManager middleware* you
can use the following option::

    base_config['use_transaction_manager'] = True


TurboGears provides its own ming ODMSession manager as an Application Wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The major change is that :class:`.MingApplicationWrapper` now behaves like SQLAlchemy
session when streaming responses.

The session is automatically flushed for you at the end of the request, in case of
stramed responses instead you will have to manually manage the session youself if
it is used inside the response generator as specified in :ref:`streaming-response`.

To recover the previous behavior set ``ming.autoflush=False`` and replace
the ``AppConfig.add_ming_middleware`` method with the following::

    def add_ming_middleware(self, app):
        import ming.odm.middleware
        return ming.odm.middleware.MingMiddleware(app)



From 2.3.3 to 2.3.4
-------------------

JSON Support no longer supports simplegeneric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To provide support for customization the ``json.isodates`` and ``json.custom_encoders``
options are now available during application configuration. Those are also available
in ``@expose('json')`` ``render_params``, see :ref:`tg-json`.

lang option is now fallback when i18n is enabled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TurboGears provided a ``lang`` configuration option which was only meaningful when
i18n was disabled with ``i18n_enabled = False``. The lang option would force the specified
language for the whole web app, independently from user session or browser languages.

Now the ``lang`` option when specified is used as the fallback language when i18n is
actually enabled (which is the default).

tg.util is now officially public
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As tg.util provided utilities that could be useful to app developers the module has been
cleaned up keeping only public features and is now documented at :mod:`tg.util`

From 2.3.2 to 2.3.3
----------------------

abort can now skip error/document and authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`tg.controllers.util.abort` can now provide a
pass-through abort which will answer as is instead of
being intercepted by authentication layer to redirect
to login page or by Error controller to show a custom
error page. This can be helpful when writing API
responses that should just provide output as is.

@require can now be used for allow_only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is now possible to use :func:`tg.decorators.require`
as value for controllers ``allow_only`` to enable
``smart_denial`` or provide a custom ``denial_handler``
for :ref:`controller_level_auth`

@require is now a TurboGears decoration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``@require`` decorator is now a TurboGears decoration, the order
it is applied won't matter anymore if other decorators are placed
on the controller.

@beaker_cache is now replaced by @cached
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``@beaker_cache`` decorator was meant to work on plain function,
the new ``@cached`` decorator is meant to work explicitly on TurboGears
controllers. The order the decorator is applied won't matter anymore
just like the other turbogears decorations.

``@beaker_cache`` is still provided, but it's use on controllers
is discouraged.

controller_wrappers now get config on call and not on construction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Whenever a controller wrapper is registered it won't get the
``app_config`` parameter anymore on construction, instead it will
receive the configuration as a parameter each time it is called.

The controller wrapper signature has changed as following::

    def controller_wrapper(next_caller):
        def call(config, controller, remainder, params):
            return next_caller(config, controller, remainder, params)
        return call

If you still need to access the application configuration into
the controller wrapper constructor, use ``tg.config``.

TurboGears will try to setup the controller wrapper with the new
method signature, if it fails it will fallback to the old controller
wrappers signature and provide a *DeprecationWarning*.

get_lang always returns a list
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since 2.3.2 ``get_lang`` supports the ``all`` option, which made possible
to ask TurboGears for all the languages requested by the user to return only
those for which the application supports translation (``all=False``).

When ``get_lang(all=True)`` was called, two different behaviors where
possible: Usually the whole list of languages requested by the user was
returned, unless the application supported no translations. In that case
``None`` was returned.

Now ``get_lang(all=True)`` behaves in a more predictable way and always
returns the whole list of languages requested by the user. In case i18n
is not enabled an empty list is returned.

From 2.3.1 to 2.3.2
----------------------

Projects quickstarted on 2.3 should work out of the box.

Kajiki support for TW2 removed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your application is using Kajiki as its primary rendering
engine, TW2 widget will now pick the first supported engine instead of Kajiki.

This is due to the fact that recent TW2 version removed support
for Kajiki.

AppConfig.setup_mimetypes removed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you were providing custom mimetypes by overriding the ``setup_mimetypes`` method
in ``AppConfig`` this is not supported anymore. To register custom mimetypes just
declare them in ``base_config.mimetype_lookup`` dictionary in your ``config/app_cfg.py``.

Custom rendering engines support refactoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you were providing a custom rendering engine through ``AppConfig.setup_NAME_renderer``
methods, those are now deprecated. While they should continue to work it is preferred
to update your rendering engine to the new factory based
:func:`tg.configuration.AppConfig.register_rendering_engine`

Chameleon Genshi support is now provided by an extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chameleon Genshi rendering support is now provided by ``tgext.chameleon_genshi``
instead of being bult-in inside TurboGears itself.

Validation error_handlers now call their hooks and wrappers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previous to 2.3.2 controller methods when used as error_handlers didn't
call their registered hooks and controller wrappers, not if an hook
or controller wrapper is attached to an error handler it will correctly
be called. Only exception is ``before_validate`` hook as error_handlers
are not validated.

AppConfig.add_dbsession_remover_middleware renamed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you were providing a custom ``add_dbsession_remover_middleware`` method
you should now rename it to ``add_sqlalchemy_middleware``.

Error Reporting options grouped in .ini file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error reporting options have been grouped in ``trace_errors`` options.

While previous option names continue to work for backward compatibility,
they will be removed in future versions. 
Email error sending options became::

    trace_errors.error_email = you@yourdomain.com
    trace_errors.from_address = turbogears@localhost
    trace_errors.smtp_server = localhost

    trace_errors.smtp_use_tls = true
    trace_errors.smtp_username = unknown
    trace_errors.smtp_password = unknown


From 2.3 to 2.3.1
----------------------

Projects quickstarted on 2.3 should work out of the box.

``AppConfig.register_hook`` Deprecation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``register_hook`` function in application configuration got deprecated
and replaced by ``tg.hooks.register`` and ``tg.hooks.wrap_controller``.

``register_hook`` will continue to work like before, but will be removed in
future versions. Check :ref:`Hooks<hooks_and_events>` Guide and upgrade
to tg.hooks based hooks to avoid issues on register_hook removal.

Exposition and Wrappers now resolved lazily
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to :ref:`Configuration Milestones<config_milestones>` support
controller exposition is now resolved lazily when the configuration
process has setup the renderers.
This enables a smarter exposition able to correctly behave even when controllers
are declared before the application configuration.

Application wrappers dependencies are now solved lazily too, this makes possible
to reorder them before applying the actual wrappers so that the order of
registration doesn't mapper when a wrapper ordering is specified.

Some methods in AppConfig got renamed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To provide a cleaner distinction between methods users are expected to
subclass to customize the configuration process and methods which
are part of TurboGears setup itself.

Validation error reporting cleanup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TurboGears always provided information on failed validations in a
unorganized manner inside ``tmpl_context.form_errors`` and other
locations.

Validation information are now reported in ``request.validation``
dictionary all together. ``tmpl_context.form_errors`` and
``tmpl_context.form_values`` are still available but deprecated.


From 2.2 to 2.3
----------------------

Projects quickstarted on 2.2 should mostly work out of the box.

GearBox replaced PasteScript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just by installing gearbox itself your TurboGears project will be able to use gearbox system wide
commands like ``gearbox serve``, ``gearbox setup-app`` and ``gearbox makepackage`` commands.
These commands provide a replacement for the paster serve, paster setup-app and paster create commands.

The main difference with the paster command is usually only that gearbox commands explicitly set the
configuration file using the ``--config`` option instead of accepting it positionally.  By default gearbox
will always load a configuration file named `development.ini`, this mean you can simply run ``gearbox serve``
in place of ``paster serve development.ini``

Gearbox HTTP Servers
++++++++++++++++++++++++++

If you are moving your TurboGears2 project from paster you will probably end serving your
application with Paste HTTP server even if you are using the ``gearbox serve`` command.

The reason for this behavior is that gearbox is going to use what is specified inside
the **server:main** section of your *.ini* file to serve your application.
TurboGears2 projects quickstarted before 2.3 used Paste and so the projects is probably
configured to use Paste#http as the server. This is not an issue by itself, it will just require
you to have Paste installed to be able to serve the application, to totally remove the Paste
dependency simply replace **Paste#http** with **gearbox#wsgiref**.

Enabling GearBox migrate and tgshell commands
+++++++++++++++++++++++++++++++++++++++++++++++++

To enable ``gearbox migrate`` and ``gearbox tgshell`` commands make sure that your *setup.py* `entry_points`
look like::

    entry_points={
        'paste.app_factory': [
            'main = makonoauth.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ]
    }

The **paste.app_factory** section will let ``gearbox serve`` know how to create the application that
has to be served. Gearbox relies on PasteDeploy for application setup, so it required a paste.app_factory
section to be able to correctly load the application.

While the **gearbox.plugins** section will let *gearbox* itself know that inside that directory the tg.devtools
commands have to be enabled making ``gearbox tgshell`` and ``gearbox migrate`` available when we run gearbox
from inside our project directory.

Removing Paste dependency
+++++++++++++++++++++++++++++++++++++++++++++++

When performing ``python setup.py develop`` you will notice that Paste will be installed.
To remove such dependency you should remove the ``setup_requires`` and ``paster_plugins``
entries from your setup.py::

    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools']

WebHelpers Dependency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your project used WebHelpers, the package is not a turbogears dependency anymore,
you should remember to add it to your ``setup.py`` dependencies.

Migrations moved from sqlalchemy-migrate to Alembic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to sqlalchemy-migrate not supporting SQLAlchemy 0.8 and Python 3, the migrations
for newly quickstarted projects will now rely on Alembic. The migrations are now handled
using ``gearbox migrate`` command, which supports the same subcommands as the ``paster migrate`` one.

The ``gearbox sqla-migrate`` command is also provided for backward compatibility for projects that need
to keep using sqlalchemy-migrate.

Pagination module moved from tg.paginate to tg.support.paginate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pagination code, which was previously imported from webhelpers, is now embedded in the
TurboGears distribution, but it changed its exact location.
If you are using ``tg.paginate.Page`` manually at the moment, you will have to fix your imports to
be ``tg.support.paginate.Page``.

Anyway, you should preferrably use the decorator approach with ``tg.decorators.paginate`` -
then your code will be independent of the TurboGears internals.

From 2.1 to 2.2
----------------------

Projects quickstarted on 2.1 should mostly work out of the box.

Main points of interest when upgrading from 2.1 to 2.2 are related to some features deprecated in 2.1
that now got removed, to the new ToscaWidgets2 support and to the New Authentication layer.

Both ToscaWidgets2 and the new auth layer are disabled by default, so they should not get in
your way unless you explicitly want.

Deprecations now removed
~~~~~~~~~~~~~~~~~~~~~~~~~~

``tg.url`` changed in release 2.1, in 2.0 parameters for the url could be passed as
paremeters for the ``tg.url`` function. This continued to work in 2.1 but provided a
DeprecationWarning. Since 2.1 parameters to the url call must be passed in the ``params``
argument as a dictionary. Support for url parameters passed as arguments have been totally
removed in 2.2

``use_legacy_renderer`` option isn't supported anymore. Legacy renderers (Buffets) got
deprecated in previous versions and are not available anymore in 2.2.

``__before__`` and ``__after__`` controller methods got deprecated in 2.1 and are not
called anymore, make sure you switched to the new ``_before`` and ``_after`` methods.

Avoiding ToscaWidgets2
~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to keep using ToscaWidgets1 simply don't install ToscaWidgets2 in your enviroment.

If your project has been quickstarted before 2.2 and uses ToscaWidgets1 it can continue to
work that way, by default projects that don't enable tw2 in any way will continue to use
ToscaWidgets1.

If you install tw2 packages in your environment the admin interface, sprox, crud and all the
functions related to form generation will switch to ToscaWidgets2.
This will force you to enable tw2 wit the ``use_toscawidgets2`` option, otherwise they will
stop working.

So if need to keep using ToscaWidgets1 only, don't install any tw2 package.

Mixing ToscaWidgets2 and ToscaWidgets1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mixing the two widgets library is perfectly possible and can be achieved using both the
``use_toscawidgets`` and ``use_toscawidgets2`` options. When ToscaWidgets2 is installed
the admin, sprox and the crud controller will switch to tw2, this will require you to
enable the ``use_toscawidgets2`` option.

If you manually specified any widget inside Sprox forms or CrudRestController
you will have to migrate those to tw2. All the other forms in your application can keep
being ToscaWidgets1 forms and widgets.

Moving to ToscaWidgets2
~~~~~~~~~~~~~~~~~~~~~~~~~~

Switching to tw2 can be achieved by simply placing the ``prefer_toscawidgets2`` option in
your ``config/app_cfg.py``. This will totally disable ToscaWidgets1, being it installed or
not. So all your forms will have to be migrated to ToscaWidgets2.

New Authentication Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~

2.2 release introduced a new authentication layer to support repoze.who v2 and prepare for
moving forward to Python3. When the new authentication layer is not in use, the old one
based on repoze.what, repoze.who v1 and repoze.who-testutil will be used.

As 2.1 applications didn't explicitly enable the new authentication layer they should
continue to work as before.

Switching to the new Authentication Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Switching to the new authentication layer should be quite straightforward for applications
that didn't customize authentication. The new layer gets enabled only when a
``base_config.sa_auth.authmetadata`` object is present inside your ``config/app_cfg.py``.

To switch a plain project to the new authentication layer simply add those lines to your
``app_cfg.py``::

    from tg.configuration.auth import TGAuthMetadata

    #This tells to TurboGears how to retrieve the data for your user
    class ApplicationAuthMetadata(TGAuthMetadata):
        def __init__(self, sa_auth):
            self.sa_auth = sa_auth
        def get_user(self, identity, userid):
            return self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(user_name=userid).first()
        def get_groups(self, identity, userid):
            return [g.group_name for g in identity['user'].groups]
        def get_permissions(self, identity, userid):
            return [p.permission_name for p in identity['user'].permissions]

    base_config.sa_auth.authmetadata = ApplicationAuthMetadata(base_config.sa_auth)

If you customized authentication in any way, you will probably have to port forward all your
customizations, in this case, if things get too complex you can keep remaining on the old
authentication layer, things will continue to work as before.

After enabling the new authentication layer you will have to switch your repoze.what imports
to tg imports::

    #from repoze.what import predicates becames
    from tg import predicates

All the predicates previously available in repoze.what should continue to be available.
Your project should now be able to upgrade to repoze.who v2, before doing that remember to remove
the following packages which are not in use anymore and might conflict with repoze.who v2:

    * repoze.what
    * repoze.what.plugins.sql
    * repoze.what-pylons
    * repoze.what-quickstart
    * repoze.who-testutil

The only repoze.who packages you should end up having installed are:

    * repoze.who-2.0
    * repoze.who.plugins.sa
    * repoze.who_friendlyform
