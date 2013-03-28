.. _requestflow:

A Request's Flow Through The TurboGears Stack
=============================================

This document is intended to help you understand how the various
components of TurboGears 2 work together, and what happens to a
web-request on the way into your controller code.

It may seem like there are a lot of layers here, and there are, but
most of the time you don't need to know anything about how they work,
just that they are there to do work for you.

The first thing that happens is that some WSGI (web server gateway
interface) compliant HTTP server recieves an HTTP message from
somebody, and it calls your TG application which is a WSGI app.

For those new to WSGI, it's a very simple interface that defines how
web servers interact with python methods or functions, or really any
callable.

The basic WSGI interface is this::

  def simple_app(environ, start_response):
      """Simplest possible application object"""
      status = '200 OK'
      response_headers = [('Content-type','text/plain')]
      start_response(status, response_headers)
      return ['Hello world!\n']

Fundamentally, WSGI means your python function gets called with two
things, an environ dictionary, and a start_response callable.  Before
your function returns, you have to pass a status, and a set of headers
to the start_response method, and then you're free to return a list
(or any itterable) of strings as the response body.

The environ dictionary, is a copy of the CGI spec's environment
(https://en.wikipedia.org/wiki/Common_Gateway_Interface).
And it has everything you need to know about the incoming request.

One more thing to know about WSGI is that it's easy for a python
function or method to take and environ and start_response to do some
stuff, and then to call another function that's also a WSGI app
(meaning it takes an environ and a start response).  When an
application like this sits between the "real" webserver and another
WSGI app, we call it middleware.

The TurboGears request/response cycle is composed of various bits of
middleware that help make writing web applicaitons easier for you.

Here's a quick outline of the stack, but we'll be going through the
pieces in a bit more detail as we go.
 
.. parsed-literal::

 WSGI Server
   **PasteCascade** - serves one of a list of WSGI apps. 
     **StaticFile Server** - serves static files from /public
  OR
     **TurboGears Application:** - the TG stack
 
     **Registry Manager** - sets up the request proxy, etc. 
       **Error Middleware** - if the path goes to ``_debug`` handle the request
         **Database Session Manager** - setup the ``DBSession``
           **Transaction Manager** - 
             **Authentication** - add info to the environ if user is authenticated
               **Authorization** - add more info to the environ for authorization. 
                 **ToscaWidgets** - nothing on the way in.  
                   **Cache** - sets up the cache 
                     **Session** - sets up the web session
                       **Routes** - parses the URL and adds info to environ
                         **Custom Middleware** - User defined middleware
                           **TurboGearsApp** -- calls WSGI style controller
                             **ObjectDispatchController** -- gets params, do validation, etc
                                **Your Controller Code** -- does anything!
                             **ObjectDispatchController** -- renders response, etc. 
                 **ToscaWidgets** - injects resources used by widgets
           **Transaction Manager** - commits or rolls back transaction 
         **Database Session Manager** - cleans up the DBSession
       **Error Middleware** - displays error pages, etc 
          
In total, this stack provides automatic database helpers, sessions,
authentication, authorization, caching, sessions, URL based dispatch,
and injection of CSS and JS resources into your app as required, and
generally makes web development easier.

.. parsed-literal::

    WSGI Server
      **PasteCascade** - Tries one app then the next    
        **StaticFile Server**
     OR
        **TurboGears Application Stack**

The first thing that gets called by the WSGI server on the way into
the TG stack is the PasteCascade.  Paste's Cascade app tries several
WSGI apps in order, if the first app returns an HTTP Not Found (404)
status code, it moves on to the second, and so on.  In the default TG
configuration the Cascade does two things 1) tries the StaticFile
Server which serves up static files from your public directory, 2)
tries the main TurboGears application.

Infrastructure And Error Handling:
----------------------------------

.. parsed-literal::

    **Registry Manager** - sets up the request proxy, etc.
      **Error Middleware** - if the path goes to _debug handle the request.
          {{ lots of stuff }}
      **Error Middlware** - redirect to nice pages on HTTP error codes, and produce debug pages/email for python errors. 
      
The next thing on the stack is the Registry Manager which sets up some
global objects that proxy to the current thread, and the current
request.  This is what allows you to do ``from tg import request`` and
then use that to manipulate just the current request.  It also has a
less-often used but still useful feature which allows you to put one
TurboGears application inside of another, and still have different
config objects, etc.  If you hear anybody talking about "Stacked
Object Proxies" or SOP's that's what this is.

The next layer on the stack is the error handling middleware.  This is
there to provide debugging helpers when python exceptions or other
application errors happen.  In debug mode this provides you with the
nice interactive debugger, and in production mode it's what logs
errors and sends out e-mails about the failures. Whenever a request
comes in that lives on the ``_debug`` path, the error handler
middleware looks up the info and responds directly.

Other than that error handling middleware doesn't do much on the way
in to the stack, but on the way out it catches errors saves data, and
does the right thing when ``_debug`` requests come in for that info.

SQLAlchemy Helpers:
-------------------

Inside the error handler, the next thing we setup is a couple of
database helpers:

.. parsed-literal::

    **Database Session Manager** - creates a DBSession for the request
        **Transaction Manager** - regesters a TransactionManager for the request. 
        {{ lots of stuff }}
        **Transaction Manager** - Commit the transaction
    **Database Session Manager** - Clear the DBSession. 

Inside the error handling middleware is a tiny little piece of
middleware that sets up a SQLAlchemy database session for this request
on the way in, and clears it out on the way out of the stack.  This
means that in TG2 by default you get a new DBSession for every
request, and everything is cleared away when you're done with it.
This keeps requests isolated, and matches the "stateless" pattern of
HTTP.

And inside that is the middleware portion of the automatic transaction
system.  When a request has updated the DBSession in any way (the in
memory copies of database data) a transaction is automatically
registered, and the Transaction Manager will handle it.  If a python
exception happens, an HTTP Error Code is returned,or
``transaction.doom()`` is called during the request, the transaction
will be rolled back on the way out.

There's a lot more to the transaction manager than just that, because
you can setup new TransactionManager classes for whatever you want.
You can write an e-mail module that does not send e-mail until the
database transaction is committed.  And if you have a database that
supports two-phase commits you can write transactions that span
multiple data sources.

ToscaWidgets:
-------------

.. parsed-literal::

   **ToscaWidgets** - nothing much on the way in.  
        {{ lots of stuff }}
   **ToscaWidgets** - inject resources into the generated
   
Nothing much on the way in.  Inject JS, and CSS resources used by
widgets in the main app.

Core Middleware: 
-----------------

.. parsed-literal::

    **Cache** - sets up the cache 
      **Session** - sets up the web session
        **Routes** - parses the URL and adds info to environ

The middleware outside of Core Middleware is optional and can often be
configured out via special config values in app_cfg.py, and can be
manipulated in any way you can imagine by subclassing AppConfig and
replacing the methods that set it up.  
TurboGears itself has code that requires that the core middleware
be in place, so you won't want to mess with this stuff without a good
reason.  This is particularly true of Routes which can only be
configured out of your app if you reimplement TGApp.
Please see 
`App Config General Options <Config.html#appconfig-general-options>`_
for more information on how to modify the core middleware.

The **Cache** middleware sets up a reference to the threadlocal cache
manager that turbogears uses to interface to whatever backend you're
using for caching.  The cache manager is injected into the environ so
that it's available to anything that happens in the request.  In the
future it's possible that this will no longer be middleware, and will
simply become another global object that is configured separately from
the WSGI stack.

The **Session** middleware also sets up a reference to a threadlocal
session manager, and at the moment both Session and Cache use the same
back-ends based on Beaker.

Finally the **Routes** middleware inspects the URL of the request, and
tries to map it to a series of "routes" which explain what controller
and controller method should be called to handle that request.  The
Routes middleware then puts this information into the controller so
that the TGApp can call the right method.

By default TG is setup with one route, that goes to the
"routes_placeholder" method on your RootController in the root.py
module.  This is a hint to TG's object dispatch controller to take
over and do dispatch to the right controller method in root's object
hierarchy.

User Defined Middleware:
------------------------

You can define custom middlware that does whatever you want it to do
and pass into the application constructor in ``middleware.py``.
 
To use a middleware before the TurboGears stack is processed you can
wrap the application returned by ``make_base_app`` function:

.. code-block:: python

    app = make_base_app(global_conf, full_stack=True, **app_conf)
    app = MyMiddleware(app)
    return app

To use a middleware that is TurboGears specific and wants to have the full
TurboGears stack available (session, authentication, database, etc...)
you can pass the middleware class to the ``make_base_app`` and it
will be created wrapping the application:

.. code-block:: python

    app = make_base_app(global_conf, full_stack=True, wrap_app=MyMiddleware, **app_conf)
    return app

If you prefer to have more control over where your middleware is
placed in the stack, you can do that by subclassing AppConfig or
overriding methods on the base_config object.

TurboGears App:
---------------

Looks up a WSGIController object based on the info from Routes and
calls it. By default this is an ObjectDispatchController that's pulled
into your app from lib/base so that you can override it if you need
to.

But if necessary, you can replace with something more application
specific.

ObjectDispatch Controller:
--------------------------

The ObjectDispatchController's job is to take the WSGI interface and
adapt it to the way TG methods behave (dealing with templates and
returned dicts, etc), and to do object based dispatch like CherryPy
did in TurboGears 1.

Dispatch:
~~~~~~~~~

The ObjectDispatchController's functionality is broken into three
basic pieces.  The root PylonsController implements a WSGI interface,
and actually calls the controller methods with params from routes.  TG
provides a :class:`DecoratedController
<tg.controllers.DecoratedController>`.  Decorated Controller allows
you to use TG1 style decorations (``@expose()``, ``@validate`` etc.)
on your controller methods, but does nothing for dispatch.

All of the dispatch is done by the :class:`Object Dispatch Controller
<tg.controllers.ObjectDispatchController>` and some associated
functions that help with lookup.

"Decoration":
~~~~~~~~~~~~~

The :class:`@expose <tg.decorators.expose>` and :class:`@validate
<tg.decorators.validate>` decorators in TG2 are not function wrappers
in the same way that they were in TG1.  They merely register
information about how that method ought to be called in it's
associated decorator diagram.  This is brought up here because they
influence the way that the Controller calls your code and handles the
response.  Expose determines how the dictonary returned by the
controller is rendered into a WSGI response.  If you return a string,
or a WebOb :class:`webob.Response` object, ``expose`` will not change
your returned results at all.


The ``@validate`` in turn makes sure the form post or get query
parameters are converted to python objects on the way in, or it will
redirect the request to an optional error handler method.

All this is covered in much more depth in the
:ref:`writing_controllers` methods doc.


Controller Methods:
-------------------

At this point we've arrived at your controller code, and it's run.
The details of all of this are covered here: :ref:`writing_controllers`

Hopefully this helps you understand the flow of the request through
the stack, and gives you some hints on how you can modify or customize
the stack to meet your needs.

For details on exactly how the stack is configured take a look at the
configuration docs at :ref:`config`.
