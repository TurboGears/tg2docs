Upgrading Your TurboGears Project
====================================

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
