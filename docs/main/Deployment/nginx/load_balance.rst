.. _nginx_load_balance:

Load Balancing TG with NGINX
==============================

.. contents::
    :depth: 2


Nginx_ is a fast and light HTTP server, reverse proxy, load balancer (and more).

.. _nginx: http://nginx.net/


Using Nginx as a Reverse Proxy
------------------------------

It's pretty simple to get TurboGears set up behind a Nginx server so that
it proxies requests to the CherryPy server. Here is a sample configuration that
not only proxies to your TurboGears application, but serves static content with
Nginx and load balances between two TurboGears application instances as well.

.. todo:: references CherryPy, update for TG |version|

::

    http {
        # boilerplate nginx config ...

        upstream mycluster {
            server 127.0.0.1:8080;
            server 127.0.0.1:8081;
        }

        server {
            listen 80;

            # static files
            location ^~ /static/  {
                root /path/to/YourProject/package;
            }
            location = /favicon.ico  {
                root /path/to/YourProject/package/public/images;
            }

            # proxy to turbogears app
            location / {
                proxy_pass          http://mycluster;
                proxy_redirect      off;
                proxy_set_header    Host $host;
                proxy_set_header    X-Real-IP $remote_addr;
                proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
            }
        }
    }

Next you need to setup a couple TurboGears backends that will comprise the cluster:

Create a copy of your project's production .ini file (prod.ini)  Under the server:main section,
find and change the following line::

    port = 8080

to::

    port = 8081

Start both instances of your app::

    $ paster serve prod.ini &
    $ paster serve prod2.ini &

*That's it!* Nginx should now be passing requests across both backends transparently.


References
----------

You can find more information and recipes for setting up Nginx on the
`English Nginx wiki`_.

.. _english nginx wiki: http://wiki.codemongers.com/
