==========================================================
Setting up logging in your Application
==========================================================

TurboGears relies on the standard Python ``logging`` module,
so to add logging to your application simply add the following
lines at the begin of your files:

.. code-block:: python

    import logging
    log = logging.getLogger(__name__)

Then you can report logging messages with the standard logger
methods: ``log.warning()``, ``log.info()``, ``log.error()``,
``log.exception()`` and so on:

.. code-block:: python

    class SimpleController(TGController):

        @expose()
        def simple(self):
            log.debug("My first logged controller!")
            return "OK"

Refer to the Python :ref:`Logger documentation <python:logger>` for additional details.

By default a quickstarted TurboGears application includes a logging
configuration at the end of the ``development.ini`` file.  That
configuration displays messages from your application from ``DEBUG``
level on.

PasteDeploy's ``loadapp()`` only creates the WSGI application.  It does
not apply the ``[loggers]``, ``[handlers]`` and ``[formatters]`` sections
from the ``.ini`` file.  Those sections are read by Python's
``logging.config.fileConfig()`` or by a command that calls it for you.

Configuring individual loggers
=================================

The logging section in ``development.ini`` and ``production.ini`` uses
Python's standard :ref:`logging configuration file format <python:logging-config-fileformat>`.
Add every configured logger, handler and formatter to its corresponding
``keys`` list, then add a matching section for each one:

.. code-block:: ini

    [loggers]
    keys = root, sqlalchemy, beaker

    [handlers]
    keys = console

    [formatters]
    keys = generic

    [logger_root]
    level = INFO
    handlers = console

    [logger_sqlalchemy]
    level = DEBUG
    handlers = console
    qualname = sqlalchemy.engine
    propagate = 0

    [logger_beaker]
    level = DEBUG
    handlers = console
    qualname = beaker
    propagate = 0

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

    [formatter_generic]
    format = %(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] %(message)s

The name after ``logger_`` is only the local key used in the ``[loggers]``
list.  ``qualname`` is the real Python logger name.  For example,
``sqlalchemy.engine`` controls SQL query logging.  Use ``propagate = 0``
when the logger has its own handler; otherwise the same message can also
propagate to the root logger and appear twice.

TurboGears quickstarts usually configure application and library loggers
with ``handlers =`` and no explicit ``propagate`` value.  That lets the
messages flow to the root logger and reuse the root handler.

When the ``.ini`` logging section is loaded
=============================================

``gearbox serve``
    Loads logging automatically from the provided configuration file before
    it creates the WSGI application.  This is why logger changes in
    ``development.ini`` are visible when you run ``gearbox serve``.

``gunicorn --paste production.ini``
    Current Gunicorn checks the PasteDeploy file for a ``[loggers]`` section
    and uses that file as its logging configuration by default.  If this is
    not happening in your Gunicorn version, pass ``--log-config production.ini``.
    If you load the TurboGears app in your own Python module with ``loadapp()``
    and run Gunicorn against that module, then Gunicorn's PasteDeploy shortcut
    is not involved and you must configure logging yourself.

``waitress`` with PasteDeploy
    If Waitress is started through ``gearbox serve`` or another PasteDeploy
    runner that configures logging, the ``.ini`` logging section is applied
    by that runner.  If you write a standalone script that does
    ``loadapp('config:production.ini')`` and then ``waitress.serve(app)``,
    ``loadapp()`` does not configure logging and Waitress will not apply your
    per-logger settings for you.

``mod_wsgi`` or a standalone WSGI script
    The WSGI script is responsible for configuring logging before it creates
    the application:

    .. code-block:: python

        import os
        import logging.config

        from paste.deploy import loadapp

        APP_CONFIG = "/var/www/myapp/myapp/production.ini"

        logging.config.fileConfig(
            APP_CONFIG,
            {"__file__": APP_CONFIG, "here": os.path.dirname(APP_CONFIG)},
            disable_existing_loggers=False,
        )
        application = loadapp('config:%s' % APP_CONFIG)

    ``mod_wsgi`` will usually send ``sys.stderr`` to Apache's ``ErrorLog``,
    but it does not read the TurboGears logging sections by itself.

Use the manual ``fileConfig()`` pattern whenever your entry point calls
``paste.deploy.loadapp()`` directly instead of using a server command that
explicitly documents that it loads PasteDeploy logging.  If your
``loadapp()`` URI includes a section name such as ``production.ini#admin``,
pass only the filename to ``fileConfig()`` and keep the section name for
``loadapp()``.

Logging Output
=================================

In the default configuration all your logging output goes to ``sys.stderr``.
What exactly that is depends on your deployment environment.

In case of ``mod_wsgi`` it will be redirected to the Apache ``ErrorLog``,
but in case your environment doesn't provide a convenient way to
configure output location your can set it up through the ``development.ini``
in the ``[handler_console]`` section:


.. code-block:: ini

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

For example to change it to log to a specific file you can replace the
``StreamHandler`` with a ``FileHandler``:

.. code-block:: ini

    [handler_console]
    class = FileHandler
    args = ('application.log', 'a')
    level = NOTSET
    formatter = generic

.. note::

    Please not that the best practice is not to change the ``console`` handler
    but creating a new handler and switch the various loggers to it.

WSGI Errors Output
=================================

The WSGI standard defines a ``wsgi.errors`` key in the environment
which can be used to report application errors. As this feature is
only available during a request (when the WSGI environment is provided),
applications won't usually rely on it, preferring instead the logging
module which is always available.

Please note that many WSGI middlewares will log to it, instead of using the logging module,
such an example is the ``backlash`` error reporting middleware used
by TurboGears for its errorware stack.

Setting up ``wsgi.errors`` is usually a task that your application server
does for you, and will usually point to the same location ``sys.stderr`` points
to. So your ``wsgi.errors`` and ``logging`` outputs should be available at
the same destination.

In case your deploy environment isn't setting up ``wsgi.errors`` correctly or you
changed the logging output you might have to change where ``wsgi.errors`` points too.

This has to be done by code, replacing the ``environ['wsgi.errors']`` key,
on every request, with a stream object.
Being it ``sys.stderr`` or something else.

It is usually best practice to leave both the logging output on ``sys.stderr`` and
``wsgi.errors`` as is, as they will usually end up at the same location on most
application servers. Then you can tune the output from the application server
configuration itself.

In case of ``gearbox serve``, ``wsgi.errors`` will point to ``sys.stderr`` which is then
redirected to a logfile, if provided with the ``--log-file`` option.

In case of ``mod_wsgi`` they will both point to the Apache ``ErrorLog`` file so you
can tune your whole logging output configuration from Apache itself.
