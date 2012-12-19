.. _tg-gearbox:

======================
The GearBox Toolkit
======================

The GearBox toolkit is a set of commands available since TurboGears 2.3 that replaced the paster
command previously provided by pylons.

GearBox provides commands to create new full stack projects, serve PasteDeploy based applications,
initialize them and their database, run migrations and start an interactive shell to work with them.

By default launching gearbox without any subcommand will start the interactive mode.
This provides an interactive prompt where gearbox commands, system shell commands and python statements
can be executed. If you have any doubt about what you can do simply run the ``help`` command to get
a list of the commands available (running ``help somecommand`` will provide help for the given sub command).

To have a list of all the available commands simply run ``gearbox --help``

QuickStart
======================

The ``gearbox quickstart`` command creates a new full stack TurboGears application,
just provide the name of your project to the command to create a new one::

    $ gearbox quickstart myproject

The quickstart command provides a bunch of options to choose which template engine to use, which
database engine to use various other options::

    optional arguments:
      -a, --auth            add authentication and authorization support
      -n, --noauth          No authorization support
      -m, --mako            default templates mako
      -j, --jinja           default templates jinja
      -k, --kajiki          default templates kajiki
      -g, --geo             add GIS support
      -p PACKAGE, --package PACKAGE
                            package name for the code
      -s, --sqlalchemy      use SQLAlchemy as ORM
      -i, --ming            use Ming as ORM
      -x, --nosa            No SQLAlchemy
      --disable-migrations  disable sqlalchemy-migrate model migrations
      --enable-tw1          use toscawidgets 1.x in place of 2.x version
      --skip-tw             Disables ToscaWidgets
      --noinput             no input (don't ask any questions)

Setup-App
=======================

The ``gearbox setup-app`` command runs the ``websetup.setup_app`` function of your project
to initialize the database schema and data.

By default the ``setup-app`` command is run on the ``development.ini`` file, to change this
provide a different one to the ``--config`` option::

    $ gearbox setup-app -c production.ini

Serve
=======================

The ``gearbox serve`` command starts a ``PasteDeploy`` web application defined by the provided
configuration file. By default the ``development.ini`` file is used, to change this provide
a different one to the ``--config`` option::

    $ gearbox serve -c production.ini --reload

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
other servers like Waitress (``egg:waitress#main``) if available.

TGShell
====================

The ``gearbox tgshell`` command will load a TurboGears application and start
an interactive shell inside the application.

The application to load is defined by the configuration file, by default
``development.ini`` is used, to load a different application or under a
different configuration provide a configuration file using the ``--config``
option::

    $ gearbox tgshell -c production.ini

The tgshell command provides an already active fake request which makes
possible to call functions that depend on ``tg.request``, it is also
provided an ``app``  object through which is possible to make requests::

    $ gearbox tgshell
    TurboGears2 Interactive Shell
    Python 2.7.3 (default, Aug  1 2012, 05:14:39)
    [GCC 4.6.3]

      All objects from myapp.lib.base are available
      Additional Objects:
      wsgiapp    -  This project's WSGI App instance
      app        -  WebTest.TestApp wrapped around wsgiapp

    >>> tg.request
    <Request at 0x3c963d0 GET http://localhost/_test_vars>
    >>> app.get('/data.json').body
    '{"params": {}, "page": "data"}'
    >>> model.DBSession.query(model.User).first()
    <User: name=manager, email=manager@somedomain.com, display=Example manager>

