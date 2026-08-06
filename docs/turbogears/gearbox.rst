.. _tg-gearbox:

======================
The GearBox Toolkit
======================

The GearBox toolkit is a set of commands available since TurboGears 2.3 that replaced the paster
command previously provided by pylons.

GearBox provides commands to create new full stack projects, serve PasteDeploy based applications,
initialize them and their database, run migrations and start an interactive shell to work with them.

Launching ``gearbox`` without a subcommand prints the top-level command help.
If you have any doubt about what you can do, run ``gearbox --help`` or
``gearbox help somecommand`` for detailed help for a specific subcommand.
Some commands are contributed by the current project and become available
after that project has been installed into the active Python environment.

QuickStart
======================

The ``gearbox quickstart`` command creates a new full stack TurboGears application,
just provide the name of your project to the command to create a new one::

    $ gearbox quickstart myproject

The quickstart command provides options to choose which template engine to use,
which database engine to use, and various other project settings::

    options:
      -a, --auth            add authentication and authorization support
      -n, --noauth          No authorization support
      -m, --mako            default templates mako
      -j, --jinja           default templates jinja
      -k, --kajiki          default templates kajiki
      -g, --genshi          default templates genshi
      -p PACKAGE, --package PACKAGE
                            package name for the code
      -s, --sqlalchemy      use SQLAlchemy as ORM
      -i, --ming            use Ming as ORM
      -x, --nosa            No SQLAlchemy
      --disable-migrations  disable alembic model migrations
      --skip-default-template
                            Disables Kajiki default templates
      --minimal-quickstart  Throw away example boilerplate from quickstart project

Current quickstarted projects use ``pyproject.toml`` packaging metadata.
Before running project-aware commands such as ``setup-app``, ``serve``,
``tgshell``, or project-provided commands, install the generated project into
the active environment from the project directory::

    $ cd myproject
    $ python -m pip install -e .

Use ``python -m pip install -e '.[testing]'`` instead when you also want to run
the generated test suite.

Setup-App
=======================

The ``gearbox setup-app`` command runs the ``websetup.setup_app`` function of your project
to initialize the database schema and data.

By default the ``setup-app`` command is run on the ``development.ini`` file.
Run it from an installed project directory.  Current quickstarts generate
``development.ini`` and ``test.ini``; use another file only if you have created
it yourself::

    $ python -m pip install -e .
    $ gearbox setup-app -c development.ini

Serve
=======================

The ``gearbox serve`` command starts a ``PasteDeploy`` web application defined by the provided
configuration file. By default the ``development.ini`` file is used. Run it
from an installed project directory, and use another config file only if you
have created it yourself::

    $ python -m pip install -e .
    $ gearbox serve -c development.ini --reload

The ``serve`` command provides a bunch of options to start the serve in daemon mode,
automatically restart the application whenever the code changes and many more::

    optional arguments:
      -c CONFIG_FILE, --config CONFIG_FILE
                            application config file to read (default:
                            development.ini)
      -n NAME, --app-name NAME
                            Load the named application (default main)
      -s SERVER_TYPE, --server SERVER_TYPE
                            Use the named server.
      --server-name SECTION_NAME
                            Use the named server as defined in the configuration
                            file (default: main)
      --daemon              Run in daemon (background) mode
      --pid-file FILENAME   Save PID to file (default to gearbox.pid if running in
                            daemon mode)
      --reload              Use auto-restart file monitor
      --reload-interval RELOAD_INTERVAL
                            Seconds between checking files (low number can cause
                            significant CPU usage)
      --monitor-restart     Auto-restart server if it dies
      --status              Show the status of the (presumably daemonized) server
      --user USERNAME       Set the user (usually only possible when run as root)
      --group GROUP         Set the group (usually only possible when run as root)
      --stop-daemon         Stop a daemonized server (given a PID file, or default
                            gearbox.pid file)

Changing HTTP Server
--------------------------

``gearbox serve`` will look for the ``[server:main]`` configuration section
to choose which server to run and one which port and address to listen.

Any ``PasteDeploy`` compatible server can be used, by default the ``egg:gearbox#wsgiref``
one is used, which is single threaded and based on python wsgiref implementation.

This server is idea for debugging as being single threaded removes concurrency issues
and keeps around request local data, but should never be used on production.

On production system you might want to use ``egg:gearbox#cherrypy`` or ``egg:gearbox#gevent``
servers which run the application on CherryPy and Gevent, it is also possible to use
other servers like Waitress (``egg:waitress#main``) if available. Alternative
servers require their Python packages to be installed first; for example the
CherryPy and Gevent entries require the corresponding server dependencies.

TGShell
====================

Use ``gearbox tgshell`` from an installed TurboGears project root for runtime
checks. Pass an explicit configuration; use ``test.ini`` with an in-memory
quickstart database for isolated checks::

    gearbox tgshell -c test.ini debug.py

Omit ``debug.py`` for an interactive session. ``tgshell`` makes ``wsgiapp``
and TurboGears globals including ``config`` and ``request`` available. It
provides ``model`` only when the application has an importable
``<package>.model`` module. It provides ``app`` only when WebTest is installed;
``app`` is a WebTest ``TestApp`` around ``wsgiapp``.

``tgshell`` loads the configured WSGI app, then immediately requests
``/_test_vars``. That may run project imports, application startup, middleware,
and request hooks. ``tgshell`` itself does not run ``setup-app``, migrations,
or intentional database writes.

Inspect locals and make a fake HTTP request
--------------------------------------------

This recipe requires WebTest because it uses ``app``. From the generated
project root, install its testing extra first::

    $ python -m pip install -e '.[testing]'

Then use the recipe::

    print("locals:", wsgiapp)
    print("app:", app)
    print("package:", config["package_name"])

    response = app.get("/", status=302)
    print("HTTP status:", response.status_int)

    from tg.util.webtest import test_context
    with test_context(app, "/"):
        assert request.path == "/"
        print("request path:", request.path)

Use ``test_context`` only when code needs a separately scoped fake request.
Do not use TurboGears' old request context manager.

SQLAlchemy quickstart only
--------------------------

This deliberately creates a temporary ``TodoItem``, flushes it, and rolls the
transaction back. It leaves no record behind. Replace ``TodoItem`` for a
project that uses a different SQLAlchemy model::

    TodoItem = model.TodoItem
    print(model.DBSession.query(TodoItem).all())

    temporary = TodoItem(title="tgshell temporary item")
    model.DBSession.add(temporary)
    model.DBSession.flush()
    temporary_id = temporary.id
    assert model.DBSession.query(TodoItem).filter_by(id=temporary_id).one() is temporary

    model.DBSession.rollback()
    assert model.DBSession.query(TodoItem).filter_by(id=temporary_id).first() is None
    print("SQLAlchemy cleanup complete")

Ming quickstart only
--------------------

This deliberately creates a temporary ``TodoItem``, flushes it, then deletes
that exact object and clears the Ming session. It leaves no record behind.
Replace ``TodoItem`` for a project that uses a different Ming model::

    TodoItem = model.TodoItem
    print(TodoItem.query.find({}).all())

    temporary = TodoItem(title="tgshell temporary item")
    model.DBSession.flush()
    temporary_id = temporary._id
    assert TodoItem.query.find({"_id": temporary_id}).all() == [temporary]

    temporary.delete()
    model.DBSession.flush()
    model.DBSession.clear()
    assert TodoItem.query.find({"_id": temporary_id}).all() == []
    print("Ming cleanup complete")

Use ``tginfo`` for static inspection and ``tgshell`` for loaded-runtime
checks. Do not run ``setup-app``, migrations, or other database-mutating
commands unless changing that environment is intentional. The in-memory
``test.ini`` database is process-local. Its schema may need test setup; that
setup is not a normal debugging step.

Adding your own command
=======================

To add commands to available gearbox commands, add them to your project entry
points under the ``gearbox.commands`` group. Current quickstarted projects use
``pyproject.toml``; add an entry point like this and reinstall the project::

    [project.entry-points."gearbox.commands"]
    my-command = "sample_app.my_commands_module.my_command_module:MyCommandClass"

    $ python -m pip install -e .

Where your command class extends ``gearbox.command.Command``::

    # -*- coding: utf-8 -*-
    from gearbox.command import Command


    class MyCommandClass(Command):
        def take_action(self, parsed_args):
            print('Hello world')

.. _setuptools: https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins