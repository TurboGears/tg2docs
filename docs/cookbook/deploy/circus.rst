.. _circus_tutorial:

==========================================================
Running a TurboGears under ``Circus`` and ``Chaussette``
==========================================================

``Circus`` is a process & socket manager.
It can be used to monitor and control processes and sockets, when paired
with the ``Chaussette`` WSGI server it can became a powerful tool to
deploy your application and manage any related process your applications needs.

Circus can take care of starting your memcached, redis, database server or
batch process with your application itself providing a single point where
to configure the full application environment.

This guide will outline broad steps that can be used to get a TurboGears
application running under ``Chaussette`` through ``Circus``.

#.  The tutorial assumes you have ``Circus`` already installed on your system.
    If you do not, install it in whatever manner makes sense for your environment.

    A possible way is by performing:

    .. code-block:: bash

        $ pip install circus

#.  Create a virtual environment with the specific TurboGears version
    your application depends on installed.

    .. code-block:: bash

        $ virtualenv /var/tg2env
        $ /var/tg2env/bin/pip install -i http://tg.gy/current tg.devtools

#.  Activate the virtual environment

    .. code-block:: bash

        $ source /var/tg2env/bin/activate
        (tg2env)$ #virtualenv now activated

#.  Once you have the environment enabled you will need to install the ``Chaussette``
    WSGI Server:

    .. code-block:: bash

        (tg2env)$ pip install chaussette

#.  Chaussette supports many backends to serve the requests. The default one is based on
    ``wsgiref``, which is not really fast.
    Have a look at the `Chaussette Documentation <http://chaussette.readthedocs.org/en/latest/>`_
    for the available backends: ``waitress``, ``gevent``, ``meinheld`` and many more are supported.

    For this tutorial we are going to use ``Waitress``, which is a multithreaded WSGI server,
    so we need to install it inside virtual environment:

    .. code-block:: bash

        (tg2env)$ pip install waitress

#.  Now the environment is ready for deploy, you just need to install the TurboGears application.

    .. code-block:: bash

       (tg2env)$ cd /var/www/myapp
       (tg2env)$ python setup.py develop

#.  We now create a circus configuration file with the informations required to load
    and start your application. This can be performed using the ``gearbox deploy-circus``
    command from `gearbox-tools <http://pypi.python.org/pypi/gearbox-tools>`_ package or by manually writing it:

    .. code-block:: ini

        [circus]
        check_delay = 5
        endpoint = tcp://127.0.0.1:5555
        debug = true

        [env:myapp]
        PATH=/var/tg2env/bin:$PATH
        VIRTUAL_ENV=/var/tg2env

        [watcher:myapp]
        working_dir = /var/www/myapp
        cmd = chaussette --backend waitress --fd $(circus.sockets.myapp) paste:production.ini
        use_sockets = True
        warmup_delay = 0
        numprocesses = 1

        stderr_stream.class = FileStream
        stderr_stream.filename = /var/log/circus/myapp.log
        stderr_stream.refresh_time = 0.3

        stdout_stream.class = FileStream
        stdout_stream.filename = /var/log/circus/myapp.log
        stdout_stream.refresh_time = 0.3

        [socket:myapp]
        host = localhost
        port = 8080

#.  Now start circus with the configuration file, after being started it will load
    your application:

    .. code-block:: bash

       $ circusd circus.ini

       2013-02-15 18:19:54 [20923] [INFO] Starting master on pid 20923
       2013-02-15 18:19:54 [20923] [INFO] sockets started
       2013-02-15 18:19:54 [20923] [INFO] myapp started
       2013-02-15 18:19:54 [20923] [INFO] Arbiter now waiting for commands

#.  Visit ``http://localhost:8080/`` in a browser to access the application.
    You can now proxy it behind Apache, Nginx or any other web server or even use
    the `VHostino <https://github.com/amol-/vhostino>`_ project for circus
    to serve multiple applications through virtual hosts

See the `circus documentation <http://circus.readthedocs.org/en/latest/>`_ for
more in-depth configuration information.
