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

By default TurboGears configures the logging module so that all the
log messages from your application are displayed from ``DEBUG`` level
on. So even debug messages will be displayed.

This is specified at the end of the ``development.ini`` file.
When starting your application with ``gearbox`` it will automatically
load the logging configuration from your ``development.ini`` or provided
configuration file.

When you are deploying your application on ``mod_wsgi`` or any other environment
that doesn't rely on ``gearbox`` to run the application, remember to load
the logging configuration before creating the actual WSGI application:

.. code-block:: python

        APP_CONFIG = "/var/www/myapp/myapp/production.ini"

        #Setup logging
        import logging.config
        logging.config.fileConfig(APP_CONFIG)

        #Load the application
        from paste.deploy import loadapp
        application = loadapp('config:%s' % APP_CONFIG)

Otherwise the logging configuration will be different from the one
available when starting the application with ``gearbox`` and you might
end up not seeing logging messages.

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
