Upgrading Your TurboGears Project
====================================

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