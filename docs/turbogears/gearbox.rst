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

The ``gearbox tgshell`` command will load a TurboGears application and start
an interactive shell inside the application.

The application to load is defined by the configuration file, by default
``development.ini`` is used, to load a different application or under a
different configuration provide a configuration file using the ``--config``
option::

    $ gearbox tgshell -c development.ini

The tgshell command provides an already active fake request which makes
possible to call functions that depend on ``tg.request``, it is also
provided an ``app``  object through which is possible to make requests::

    $ gearbox tgshell
    TurboGears2 Interactive Shell
    Python 3.x (...)

      All objects from myapp.lib.base are available
      Additional Objects:
      wsgiapp    -  This project's WSGI App instance
      app        -  WebTest.TestApp wrapped around wsgiapp

    >>> tg.request
    <Request at 0x3c963d0 GET http://localhost/_test_vars>
    >>> app.get('/data.json').body
    b'{"page": "data", "params": {}}'
    >>> model.DBSession.query(model.User).first()
    <User: name=manager, email=manager@somedomain.com, display=Example manager>

Running Scripts from Command Line
---------------------------------

You will notice that writing a python script that depends on TurboGears and
running from the command line will fail with an error.

Suppose you have a script like::

    import tg
    print('Hello From', tg.request.path)

Saving it as ``myscript.py`` and running it will fail with TurboGears
complaining about a missing context::

    $ python myscript.py
    Traceback (most recent call last):
      File "myscript.py", line 2, in <module>
        print('Hello From', tg.request.path)
      File "/Users/amol/wrk/tg/tg2/tg/support/objectproxy.py", line 19, in __getattr__
        return getattr(self._current_obj(), attr)
      File "/Users/amol/wrk/tg/tg2/tg/request_local.py", line 214, in _current_obj
        return getattr(context, self.name)
      File "/Users/amol/wrk/tg/tg2/tg/support/objectproxy.py", line 19, in __getattr__
        return getattr(self._current_obj(), attr)
      File "/Users/amol/wrk/tg/tg2/tg/support/registry.py", line 72, in _current_obj
        'thread' % self.____name__)
    TypeError: No object (name: context) has been registered for this thread

That because we are trying to access the current request (``tg.request``) but we are outside
of a web application, so no request exists.

**TGShell** command solves this problem as it uses same features described in
:ref:`testing_outside_controllers` to run any script inside a fake request::

    $ gearbox tgshell myscript.py
    15:30:13,925 INFO  [tgext.debugbar] Enabling Debug Toolbar
    15:30:13,953 INFO  [auth] request classification: browser
    15:30:13,953 INFO  [auth] -- repoze.who request started (/_test_vars) --
    15:30:13,953 INFO  [auth] no identities found, not authenticating
    15:30:13,953 INFO  [auth] no challenge required
    15:30:13,953 INFO  [auth] -- repoze.who request ended (/_test_vars) --
    Hello From /_test_vars

So through **TGShell** it's also possible to run turbogears based scripts
like you were inside an HTTP request for a controller.


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