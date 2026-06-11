.. _context-and-registry:

===========================
Context and Registry
===========================

TurboGears provides a **request context** and a **registry** system to manage
request-specific data in a thread-safe way. This is essential for WSGI applications
that need to handle multiple concurrent requests.

Purpose
=======

In a multi-threaded or multi-process WSGI server (like Gunicorn, uWSGI, or mod_wsgi),
each request is handled by a different thread or process. This creates a challenge:
how can application code access request-specific data (like the current request object,
the response, or the database session) using simple global names like ``tg.request``
without data from different requests getting mixed up?

The **context** and **registry** systems solve this problem by providing:

1. **Thread-local storage**: Each thread gets its own isolated copy of request data
2. **Global access patterns**: Code can use simple names like ``tg.request``, ``tg.response``,
   ``tg.session`` without needing to pass these objects around explicitly
3. **Automatic cleanup**: Request-specific data is automatically cleaned up after each
   request to prevent memory leaks

Context
=======

The **TurboGears context** is a container for all the request-specific objects that
are available during request processing. It provides access to:

- ``tg.request``: The current :class:`~tg.request_local.Request` object
- ``tg.response``: The current :class:`~tg.request_local.Response` object
- ``tg.app_globals``: Application-wide globals (shared across requests)
- ``tg.session``: The current user session (if enabled)
- ``tg.cache``: The cache for the current request
- ``tg.tmpl_context``: Template context for the current request
- ``tg.translator``: The i18n translator for the current request
- ``tg.url``: URL generation utilities
- ``tg.config``: The application configuration

These objects are accessible from anywhere in your application code during a request,
without needing to pass them as parameters. For example:

.. code-block:: python

    import tg

    class MyController(TGController):
        @expose()
        def index(self):
            # Access request data directly
            user_agent = tg.request.user_agent
            
            # Set response properties
            tg.response.content_type = 'application/json'
            
            # Access session
            visit_count = tg.session.get('visit_count', 0) + 1
            tg.session['visit_count'] = visit_count
            
            return {'visits': visit_count}

Registry
========

The **registry** is the underlying mechanism that makes the context work in a
thread-safe way. It:

1. **Creates a new context** at the start of each request
2. **Registers request-specific objects** (request, response, session, etc.) with that context
3. **Provides access** to those objects through global proxies
4. **Cleans up** the context at the end of each request

The registry is automatically managed by TurboGears and requires no configuration
for typical use cases. It is implemented as a WSGI middleware that wraps your
application.

Configuration
=============

The registry behavior can be configured through the following options in your
``.ini`` file or ``app_cfg``:

- ``registry_streaming``: When enabled (default: ``True``), the registry cleanup
  is deferred until the end of streaming responses. This allows middleware and
  application code to access request data even while the response is being
  streamed to the client.

- ``debug``: When enabled (default: ``False``), the registry preserves objects
  even after exceptions, making it possible to inspect the request state during
  debugging.

See :ref:`config-options` for more details on these options.

Important Considerations
========================

Thread Safety
-------------

The context and registry systems are designed to be thread-safe. Each thread
gets its own isolated context, so you don't need to worry about concurrent
requests interfering with each other when using ``tg.request``, ``tg.response``,
etc.

However, **be careful with background threads**: If you spawn a background thread
from within a request, that thread will inherit the parent request's context.
This can lead to unexpected behavior if the background thread outlives the
original request. If you need to work with background threads, consider:

1. Passing explicit copies of the data you need to the background thread
2. Using ``tg.request._current_obj()`` to get the actual object (not the proxy)
   and pass it explicitly
3. Creating a new, isolated context for the background thread

Testing Outside Controllers
===========================

When writing unit tests that use TurboGears features outside of a request
context (for example, testing utility functions that use ``tg.url`` or ``tg.i18n``),
you need to establish a fake context. See :ref:`testing` for details on
using ``test_context`` or ``/_test_vars``.

Middleware and WSGI
-------------------

The registry is implemented as a WSGI middleware (``RegistryManager``) that
is automatically added to your TurboGears application. This means it works
seamlessly with any WSGI-compliant server (Gunicorn, uWSGI, Waitress, mod_wsgi,
etc.).

If you're writing custom WSGI middleware that needs to access TurboGears
context data, make sure your middleware runs **inside** the TurboGears
application (i.e., after the RegistryManager in the middleware stack).

Performance
-----------

The context and registry systems have minimal overhead. The proxies (``tg.request``,
``tg.response``, etc.) use a thread-local lookup to get the current object, which
is very fast. The cleanup at the end of each request ensures that memory is
reclaimed promptly.

For high-performance applications, the main thing to watch out for is
unintentional object retention. If you store references to request-specific
objects (like the request or session) in places that outlive the request, you
can prevent the registry from cleaning them up properly.

Summary
=======

- **Context**: A container for request-specific objects, accessed through global
  names like ``tg.request``, ``tg.response``, etc.
- **Registry**: The mechanism that manages contexts in a thread-safe way, creating
  a new one for each request and cleaning up afterwards
- **Purpose**: Enable simple, thread-safe access to request data without explicit
  parameter passing
- **Use**: Just use ``tg.request``, ``tg.response``, etc. in your code - the
  context and registry handle the rest automatically
