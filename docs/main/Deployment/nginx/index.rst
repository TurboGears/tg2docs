.. _nginx:

NGINX Web Server
-----------------

Nginx is a very fast asynchronous web server.  This means that it
handles all IO using non-blocking sockets rather than threads or
processes, which allows it to scale to extremely large numbers of
connected clients (on the order of 10,000 simultaneous clients).

Nginx support for WSGI applications (and TurboGears in particular)
is still very much experimental, but the following patterns may
work:

* can provide :ref:`reverse-proxy/load-balancing<nginx_load_balance>`
  for multiple Paste web-servers
* TurboGears should be compatible with `uWSGI`_, which should be
  compatible with Nginx, (this is a reverse-proxy setup as well)
* has `FastCGI support`_ which, with some effort likely can be used
  to host TurboGears |version|

.. toctree::
   :maxdepth: 1

   load_balance.rst

.. _`FastCGI support`: http://wiki.nginx.org/NginxSimplePythonFCGI
.. _`uWSGI`: http://projects.unbit.it/uwsgi/wiki/RunOnNginx

.. todo:: Need to test and document these options better
   if we're going to keep them in the official documentation.
