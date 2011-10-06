.. _caching:

Caching
=======

Caching is a common techneque to achieve performance goals,
when a web application has to perform some operation that
could take a long time.  There are two major types of caching
used in Web Applications:

 * :ref:`Whole-page caching<http_caching>` --
   works at the HTTP protocol level to avoid entire requests to the
   server by having either the user's browser, or an intermediate
   proxy server (such as Squid) intercept the request and return
   a cached copy of the file.

 * Application-level caching -- works within the application server
   to cache computed values, often the results of complex database
   queries, so that future requests can avoid needing to re-caculate
   the values.

Most web applications can only make very selective use of HTTP-level caching,
such as for caching generated RSS feeds, but that use of HTTP-level
caching can dramatically reduce load on your server, particularly
when using an external proxy such as Squid and encountering a
high-traffic event (such as the `Slashdot Effect`).

For web applications, application-level caching provides a flexible way to
cache the results of complex queries so that the total load of a given
controller method can be reduced to a few user-specific or case-specific
queries and the rendering overhead of a template.  Even within templates,
application-level caching can be used to cache rendered HTML for those
fragments of the interface which are comparatively static, such as
database-configured menus, reducing potentially recursive database queries
to simple memory-based cache lookups.

.. _beaker_cache:

Application-level Caching (Beaker)
----------------------------------

TurboGears comes with application-level caching
middleware enabled by default in QuickStarted projects.  The
middleware, `Beaker <http://beaker.groovie.org>`_ is the same
package which provides Session storage for QuickStarted
projects.  Beaker is the standard cache framework of the
Pylons web framework, on which TurboGears |version| is based.

Beaker supports a variety of backends which can be used for
cache or session storage:

* memory -- per-process storage, extremely fast
* filesystem -- per-server storage, very fast, multi-process
* "DBM" database -- per-server storage, fairly fast, multi-process
* SQLAlchemy database -- per-database-server storage, integrated into
  your main DB infrastructure, so potentially shared, replicated, etc.,
  but generally slower than memory, filesystem or DBM approaches
* :ref:`memcache` -- (potentially) multi-server memory-based cache,
  extremely fast, but with some system setup requirements

Each of these backends can be configured from your
application's configuration file, and the resulting caches can be
used with the same API within your application.

Using the Cache
^^^^^^^^^^^^^^^

The configured `Beaker` cache is provided by the `pylons` module.
This is more properly thought of as a `CacheManager`, as it provides
access to multiple independent cache namespaces.  To access the
cache from within a controller module:

.. code-block:: python

    from tg import cache
    @expose()
    def some_action(self, day):
        # hypothetical action that uses a 'day' variable as its key

        def expensive_function():
            # do something that takes a lot of cpu/resources
            return expensive_call()

        # Get a cache for a specific namespace, you can name it whatever
        # you want, in this case its 'my_function'
        mycache = cache.get_cache('my_function')

        # Get the value, this will create the cache copy the first time
        # and any time it expires (in seconds, so 3600 = one hour)
        cachedvalue = mycache.get_value(
            key=day,
            createfunc=expensive_function,
            expiretime=3600
        )
        return dict(myvalue=cachedvalue)

The `Beaker` cache is a two-level namespace, with the keys at each level
being string values.  The call to cache.get_cache() retrieves a cache
namespace which will map a set of string keys to stored values.  Each value
that is stored in the cache must be `pickle-able
<http://docs.python.org/lib/module-pickle.html>`_.

Pay attention to the keys you are using to store your cached values.  You
need to be sure that your keys encode all of the information that the
results being cached depend upon in a unique manner.  In the example above,
we use `day` as the key for our cached value, on the assumption that this
is the only value which affects the calculation of `expensive_function`,
if there were multiple parameters involved, we would need to encode each of
them into the key.

.. note::
    The `Beaker` API exposed here requires that your functions for
    calculating complex values be callables taking 0 arguments.
    Often you will use a nested function to provide this interface
    as simply as possible.  This function will only be called if there
    is a `cache miss`, that is, if the cache does not currently have
    the given key recorded (or the recorded key has expired).

Other Cache Operations
^^^^^^^^^^^^^^^^^^^^^^

The cache also supports the removal values from the cache, using the key(s) to
identify the value(s) to be removed and it also supports clearing the cache
completely, should it need to be reset.

.. code-block:: python

    # Clear the cache
    mycache.clear()

    # Remove a specific key
    mycache.remove_value('some_key')

Template Caching
--------------------

Genshi Loader Cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``genshi`` will retrieve the templates from a cache if they have not changed. 
This cache has a default size of 25, when there are more than 25, 
the least recently used templates will be removed from this cache.

You can change this behavior by setting the ``genshi.max_cache_size`` option
into the development.ini:

.. code-block:: ini

    [app:main]
    genshi.max_cache_size=100    

Another speed boost can be achieved by disabling template automatic reloading
in ``app_cfg.py``.

.. code-block:: python

    base_config = AppConfig()
    base_config.auto_reload_templates = False


Prerendered Templates Caches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In templates, the cache ``namespace`` will automatically be set to the name of
the template being rendered. To cache a template you just have to return
the ``tg_cache`` option from the controller that renders the cached template.

``tg_cache`` is a dictionary that accepts the following keys:

 * key: The cache key. Default: None
 * expire: how long the cache must stay alive. Default: never expires
 * type: memory, dbm, memcached. Default: dbm

if any of the keys is available the others will default, if all three
are missing caching will be disabled.
For example to enable caching for 1 hour for the profile of an user:

.. code-block:: python

    @expose('myproj.templates.profile')
    def profile(self, username):
        user = DBSession.query(User).filter_by(user_name=user_name).first()
        return dict(user=user, tg_cache=dict(key=user_name, expire=3600))



Configuring Beaker
------------------

`Beaker` is configured in your QuickStarted application's main configuration
file in the app:main section.

To use memory-based caching:

.. code-block:: ini

    [app:main]
    beaker.cache.type = memory

To use file-based caching:

.. code-block:: ini

    [app:main]
    beaker.cache.type = file
    beaker.cache.data_dir = /tmp/cache/beaker
    beaker.cache.lock_dir = /tmp/lock/beaker

To use DBM-file-based caching:

.. code-block:: ini

    [app:main]
    beaker.cache.type = dbm
    beaker.cache.data_dir = /tmp/cache/beaker
    beaker.cache.lock_dir = /tmp/lock/beaker

To use SQLAlchemy-based caching you must provide the `url` parameter
for the `Beaker` configuration.  This can be any valid SQLAlchemy
URL, the `Beaker` storage table will be created by `Beaker` if
necessary:

.. code-block:: ini

    [app:main]
    beaker.cache.type = ext:database
    beaker.cache.url = sqlite:///tmp/cache/beaker.sqlite

.. _memcache:

Memcached
---------

Memcached allows for creating a pool of colaborating servers which
manage a single distributed cache which can be shared by large numbers of
front-end servers (i.e. TurboGears instances).  Memcached can be extremely
fast and scales up very well, but it involves an external daemon process
which (normally) must be maintained (and secured) by your sysadmin.

Memcached is a system-level daemon which is intended
for use solely on "trusted" networks, there is little or no security provided
by the daemon (it trusts anyone who can connect to it), so you should never
run the daemon on a network which can be accessed by the public!  To repeat,
do `not` run memcached without a firewall or other network partitioning
mechanism!  Further, be careful about storing any sensitive or
authentication/authorization data in memcache, as any attacker who can
gain access to the network can access this information.

Ubuntu/Debian servers will generally have memcached configured by default
to only run on the localhost interface, and will have a small amount of
memory (say 64MB) configured.  The `/etc/memcached.conf` file can be
edited to change those parameters.  The memcached daemon will also normally
be deactivated by default on installation.  A basic memcached installation
might look like this on an Ubuntu host:

.. code-block:: bash

    sudo apt-get install memcached
    sudo vim /etc/default/memcached
    # ENABLE_MEMCACHED=yes
    sudo vim /etc/memcached.conf
    # Set your desired parameters...
    sudo /etc/init.d/memcached restart
    # now install the Python-side client library...
    # note that there are other implementations as well...
    easy_install python-memcached

You then need to configure TurboGears/Pylon's beaker support to use the
memcached daemon in your .ini files:

.. code-block:: ini

    [app:main]
    beaker.cache.type = ext:memcached
    beaker.cache.url = 127.0.0.1:11211
    # you can also store sessions in memcached, should you wish
    # beaker.session.type = ext:memcached
    # beaker.session.url = 127.0.0.1:11211

You can have multiple memcached servers specified using `;` separators.
Usage, as you might imagine is the same as with any other `Beaker` cache
configuration (that is, to some extent, the point of the
Beaker Cache abstraction, after all):

References
^^^^^^^^^^

    * `Beaker Caching <http://beaker.groovie.org/caching.html>`_ -- discussion of use of Beaker's caching services
    * `Beaker Configuration <http://beaker.groovie.org/configuration.html>`_ -- the various parameters which can be used to configure Beaker in your config files
    * `Memcached <http://www.danga.com/memcached/>`_ -- the memcached project
    * `Python Memcached <http://www.tummy.com/Community/software/python-memcached/>`_ -- Python client-side binding for memcached
    * `Caching for Performance <http://web.archive.org/web/20060424171425/http://www.webperformance.org/caching/caching_for_performance.pdf>`_
      -- Stephen Pierzchala's general introduction to the concept of
      caching in order to improve web-site performance

.. _http_caching:

HTTP-Level Caching
------------------

HTTP supports caching of whole responses (web-pages,
images, script-files and the like).  This kind of caching
can dramatically speed up web-sites where the bulk of the
content being served is largely static, or changes predictably,
or where some commonly viewed page (such as a home-page) requires
complex operations to generate.

HTTP-level caching is handled by external services, such as
a `Squid <http://www.squid-cache.org/>`_ proxy or the user's
browser cache.  The web application's role in HTTP-level caching
is simply to signal to the external service what level of caching
is appropriate for a given piece of content.

.. note::

    If *any* part of you page has to be dynamically generated,
    even the simplest fragment, such as a user-name, for each
    request HTTP caching likely will not work for you.  Once the
    page is HTTP-cached, the application server will not recieve any
    further requests until the cache expires, so it will not
    generally be able to do even minor customizations.

.. _etag:

Browser-side Caching with ETag
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

HTTP/1.1 supports the :term:`ETag` caching system that
allows the browser to use its own cache instead of requiring regeneration of
the entire page. ETag-based caching avoids repeated generation of content but
if the browser has never seen the page before, the page will still be
generated. Therefore using ETag caching in conjunction with one of the other
types of caching listed here will achieve optimal throughput and avoid
unnecessary calls on resource-intensive operations.

Caching via ETag involves sending the browser an ETag header so that it knows
to save and possibly use a cached copy of the page from its own cache, instead
of requesting the application to send a fresh copy.

The :func:`etag_cache` function will set the proper HTTP headers if the browser
doesn't yet have a copy of the page. Otherwise, a 304 HTTP Exception will be
thrown that is then caught by Paste middleware and turned into a proper 304
response to the browser. This will cause the browser to use its own
locally-cached copy.

:func:`etag_cache` returns `pylons.response` for legacy purposes
(`tg.response` should be used directly instead).

ETag-based caching requires a single key which is sent in the ETag HTTP header
back to the browser. The `RFC specification for HTTP headers
<http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html>`_ indicates that an
ETag header merely needs to be a string. This value of this string does not
need to be unique for every URL as the browser itself determines whether to use
its own copy, this decision is based on the URL and the ETag key.

.. code-block:: python

    from tg.controllers.util import etag_cache
    def my_action(self):
        etag_cache('somekey')
        return render('/show.myt', cache_expire=3600)

Or to change other aspects of the response:

.. code-block:: python

    from tg.controllers.util import etag_cache
    from tg import response
    def my_action(self):
        etag_cache('somekey')
        response.headers['content-type'] = 'text/plain'
        return render('/show.myt', cache_expire=3600)

.. note::
    In this example that we are using template caching in addition to ETag
    caching. If a new visitor comes to the site, we avoid re-rendering the
    template if a cached copy exists and repeat hits to the page by that user
    will then trigger the ETag cache. This example also will never change the
    ETag key, so the browsers cache will always be used if it has one.

The frequency with which an ETag cache key is changed will depend on the web
application and the developer's assessment of how often the browser should be
prompted to fetch a fresh copy of the page.

.. glossary::

    ETag
        `From Wikipedia <http://en.wikipedia.org/wiki/HTTP_ETag>`_ An ETag
        (entity tag) is an HTTP response header returned by an HTTP/1.1
        compliant web server used to determine change in content at a given
        URL.

.. todo:: Add links to Beaker region (task-specific caching mechanisms) support.
.. todo:: Document what the default Beaker cache setup is for TG |version| quickstarted projects (file-based, likely).
.. todo:: Provide code-sample for use of cache within templates
