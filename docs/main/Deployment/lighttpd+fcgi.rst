.. _lighttpd_fcgi:

Lighttpd and FastCGI
====================

.. todo:: clean up the LightHTTPD + FastCGI deployment documentation
.. todo:: consolidate the 3 FastCGI documents (Mod-FastCGI, NGINX FastCGI
   and LightHTTPD FastCGI) as well as the Mod-Proxy stuff.

Lighttpd has strong build-in FastCGI support. This makes FCGI the method of choice to deploy a TurboGears2 application in a production environment.

In order to run a WSGI application you need a container implementing the FastCGI interface.
A common choice is flup::

    (tg2env) easy_install flup

Flup implements a multithreading fastcgi server.
Because of the Global Interpreter Lock (GIL) one Python process can only run one thread at once, but whenever a thread blocks, it releases the lock.
This is exactly the workload expected for a webserver.
If you want to use more than one physical core, start more python processes.

You need a script to start the FastCGI server with your application.
Additionally you have to load the paths to your virtual environment.

Create a new file ``dispatch.py`` and add the following commands.

To have your own installed modules loaded first, this part adds your virtual environment in front of the path::

    import sys

    prev_sys_path = list(sys.path)

    import site
    site.addsitedir('/path/to/tg2env/lib/python2.5/site-packages')

    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path


Now add your applications directory to the path::

    import os, sys
    sys.path.append('/path/to/your_application')


If you use a VPS you may want to limit the stack size to save memory. The linux kernel allocates 8 MB for each thread, but in most cases this much is not needed.
If you run into problems remove these lines::

    import thread
    thread.stack_size(524288)


Now load your application, instantiate a WSGIServer and run your application::

    from paste.deploy import loadapp
    wsgi_app = loadapp('config:/path/to/your_application/production.ini')

    if __name__ == '__main__':
        from flup.server.fcgi import WSGIServer
        WSGIServer(wsgi_app, minSpare=1, maxSpare=5, maxThreads=50).run()

The parameters ``minSpare``, ``maxSpare`` and ``maxThreads`` control how many threads will be launched.

.. highlight:: none

Now you need to configure Lighttpd to launch your application and communicate with it via fastcgi.
Enable fastcgi by loading its module::

    server.modules   += ( "mod_fastcgi" )

Include the following commands into the Lighttpd configuration file:

.. literalinclude:: lighttpd_fcgi.conf

The alias rules point to the static files within your application. These are now served by Lighttpd.

The next section configures the fastcgi server.

We set the server to communicate via sockets, which is faster than TCP, if you only use one physical machine.

The variable ``bin-path`` points to the applications dispatch script.

We add some variables to the environment. ``PYTHON_EGG_CACHE`` should point to a directory writeable to the server process. It is used to unpack egg files of dependencies. We also set the locale to "C". Other values may pose problems with gettext.

``max-proc`` controls how many fastcgi servers should be launched. This should not be greater than the number of physical cores.

You can control the url of your application by changing ``/web/path/to/app``.

If you want to bind it to the root directory, you have to leave the parameter empty. If you set it to "/" the requests for static content gets routed to your application and will fail. Either change static content to its own subdomain or add a special filter to the wsgi stack.

Add to production.ini in section ``[app:main]``::

    filter-with = proxy-prefix

And as an additional section::

    [filter:proxy-prefix]
    use = egg:PasteDeploy#prefix
    prefix = /

This will force the URL transmitted from Lighttpd to TurboGears to "/".

Reload lighttpd to enable the changes. You should now have a process named "dispatch.py" with several threads.
