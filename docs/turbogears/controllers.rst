.. _writing_controllers:

=================================
Request Dispatching & Controllers
=================================

The nerve center of your TurboGears application is **the
controller**. It ultimately handles all user actions, because every
HTTP request arrives here first. The controller acts on the request
and can call upon other TurboGears components (the template engines,
database layers, etc.) as its logic directs.

Basic Dispatch
-----------------------

When the TurboGears server receives an HTTP request, the requested URL
is mapped as a call to your controller code located in the
``controllers`` package. Page names map to other controllers or
methods within the controller class.

For example:

================================== ============================
URL                                Maps to
================================== ============================
``http://localhost:8080/index``    ``RootController.index()``
``http://localhost:8080/mypage``   ``RootController.mypage()``
================================== ============================

Index and Catch-All pages
----------------------------

Suppose using ``gearbox quickstart`` you generate a TurboGears project
named "HelloWorld". Your default controller code would be created in
the file ``HelloWorld/helloworld/controllers/root.py``.

Modify the default ``root.py`` to read as follows:

.. code-block:: python

    """Main Controller"""
    from helloworld.lib.base import BaseController
    from tg import expose, flash
    #from tg import redirect, validate
    #from helloworld.model import DBSession

    class RootController(BaseController):
         @expose()
         def index(self):
             return "<h1>Hello World</h1>"

         @expose()
         def _default(self, *args, **kw):
             return "This page is not ready"


When you load the root URL ``http://localhost:8080/index`` in your web
browser, you'll see a page with the message "Hello World" on it. In
addition, any of `these URLs`_ will return the same result.

Implementing A Catch-All Url Via The ``_default()`` Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

URLs not explicitly mapped to other methods of the controller will
generally be directed to the method named ``_default()``. With the
above example, requesting any URL besides ``/index``, for example
``http://localhost:8080/hello``, will return the message "This page is
not ready".

Adding More Pages
~~~~~~~~~~~~~~~~~

When you are ready to add another page to your site, for example at
the URL

   ``http://localhost:8080/anotherpage``

add another method to class RootController as follows::

    @expose()
    def anotherpage(self):
        return "<h1>There are more pages in my website</h1>"

Now, the URL ``/anotherpage`` will return:

**There are more pages in my website**


Line By Line Explanation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    """Main Controller"""
    from helloworld.lib.base import BaseController
    from tg import expose, flash
    from tg.i18n import ugettext as _
    #from tg import redirect, validate
    #from helloworld.model import DBSession

First you need to import the required modules.

There's a lot going on here, including some stuff for internationalization.
But we're going to gloss over some of that for now.  The key thing to notice is
that you are importing a BaseController, which your RootController must inherit
from.   If you're particularly astute, you'll have noticed that you import this
BaseController from the lib module of your own project, and not from TurboGears.

TurboGears provides :ref:`ObjectDispatch <objectdispatch>` system through
the TGController class which is imported in the lib
folder of the current project (HelloWorld/helloworld/lib) so that you
can modify it to suit the needs of your application. For example, you
can define actions which will happen on every request, add parameters
to every template call, and otherwise do what you need to the request
on the way in, and on the way out.

The next thing to notice is that we are importing ``expose`` from ``tg``.

``BaseController`` classes and the expose decorator are the basis of TurboGears
controllers.   The ``@expose`` decorator declares that your method should be
*exposed to the web*, and provides you with the ability to say how the results
of the controller should be rendered.

The other imports are there in case you do internationalization,
use the HTTP redirect function, validate inputs/outputs, or use the models.

.. code-block:: python

    class RootController(BaseController):

``RootController`` is the required standard name for the
RootController class of a TurboGears application and it should inherit
from the ``BaseController`` class. It is thereby specified as the
request handler class for the website's root.

In TurboGears 2 the web site is represented by a tree of controller
objects and their methods, and a TurboGears website always grows out
from the ``RootController`` class.

.. code-block:: python

    def index(self):
        return "<h1>Hello World</h1>"

.. _these urls:

We'll look at the methods of the ``RootController`` class next.

The ``index`` method is the start point of any TurboGears controller
class.  Each of the URLs

* http://localhost:8080
* http://localhost:8080/
* http://localhost:8080/index

is mapped to the ``RootController.index()`` method.

If a URL is requested and does not map to a specific method, the
``_default()`` method of the controller class is called::

    def _default(self):
        return "This page is not ready"


In this example, all pages except the `these urls`_ listed above will
map to the _default method.

As you can see from the examples, the response to a given URL is
determined by the method it maps to.

.. code-block:: python

    @expose()

The ``@expose()`` seen before each controller method directs
TurboGears controllers to make the method accessible through the web
server. Methods in the controller class that are *not* "exposed" can
not be called directly by requesting a URL from the server.

There is much more to @expose(). It will be our access to TurboGears
sophisticated rendering features that we will explore shortly.

Exposing Templates
-------------------------

As shown above, controller methods return the data of your website. So far, we
have returned this data as literal strings. You could produce a whole site by
returning only strings containing raw HTML from your controller methods, but it
would be difficult to maintain, since Python code and HTML code would not be
cleanly separated.


Expose + Template == Good
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable a cleaner solution, data from your TurboGears controller can be
returned as strings, **or** as a dictionary.

With ``@expose()``, a dictionary can be passed from the controller to a template
which fills in its placeholder keys with the dictionary values and then returns
the filled template output to the browser.

Template Example
~~~~~~~~~~~~~~~~~~~~~~~~

A simple template file called ``sample`` could be made like
this:

.. code-block:: html

    <html>
      <head>
    <title>TurboGears Templating Example</title>
      </head>
      <body>
          <h2>I just want to say that ${person} should be the next
            ${office} of the United States.</h2>
      </body>
    </html>

The ``${param}`` syntax in the template indicates some undetermined
values to be filled.

We provide them by adding a method to the controller like this ...

.. code-block:: python

    @expose("helloworld.templates.sample")
    def example(self):
        mydata = {'person':'Tony Blair','office':'President'}
        return mydata

... then the following is made possible:

* The web user goes to ``http://localhost:8080/example``.
* The ``example`` method is called.
* The method ``example`` returns a Python ``dict``.
* @expose processes the dict through the template file named
  ``sample.html``.
* The dict values are substituted into the final web response.
* The web user sees a marked up page saying:

  **I just want to say that Tony Blair should be the next President of the United States.**

Template files can thus house all markup information, maintaining clean
separation from controller code.

For more on templating have a look at :ref:`Templating <templating>`

SubControllers And The URL Hierarchy
------------------------------------

Sometimes your web-app needs a URL structure that's more than one
level deep.

TurboGears provides for this by traversing the object hierarchy, to
find a method that can handle your request.

To make a sub-controller, all you need to do is make your
sub-controller inherit from the object class.  However there's a
SubController class ``Controller`` in your project's lib.base
(HelloWorld/helloworld/lib/base.py) for you to use if you want a
central place to add helper methods or other functionality to your
SubControllers:

.. code-block:: python

    from lib.base import BaseController
    from tg import redirect

    class MovieController(BaseController):
        @expose()
        def index(self):
            redirect('list/')

        @expose()
        def list(self):
            return 'hello'

    class RootController(BaseController):
        movie = MovieController()

With these in place, you can follow the link:

* http://localhost:8080/movie/
* http://localhost:8080/movie/index

and you will be redirected to:

* http://localhost:8080/movie/list/

Unlike turbogears 1, going to http://localhost:8080/movie **will not**
redirect you to http://localhost:8080/movie/list.  This is due to some
interesting bit about the way WSGI works.  But it's also the right
thing to do from the perspective of URL joins.  Because you didn't
have a trailing slash, there's no way to know you meant to be in the
movie directory, so redirection to relative URLs will be based on the
last / in the URL.  In this case the root of the site.


It's easy enough to get around this, all you have to do is write your
redirect like this:

.. code-block:: python

    redirect('/movie/list/')

Which provides the redirect method with an absolute path, and takes
you exactly where you wanted to go, no matter where you came from.

Passing Parameters To The Controller
---------------------------------------

Now that you have the basic routing dispatch understood, you may be
wondering how parameters are passed into the controller methods.
After all, a framework would not be of much use unless it could accept
data streams from the user.

TurboGears uses introspection to assign values to the arguments in
your controller methods.  This happens using the same duck-typing you
may be familiar with if you are a frequent python programmer.  Here is
the basic approach:

 * The dispatcher gobbles up as much of the URL as it can to find the
     correct controller method associated with your request.
 * The remaining url items are then mapped to the parameters in the method.
 * If there are still remaining parameters they are mapped to \*args in the method signature.
 * If there are named parameters, (as in a form request, or a GET request with parameters), they are mapped to the
     args which match their names, and if there are leftovers, they are placed in \**kw.

Here is an example controller and a chart outlining the way urls are mapped to it's methods:

.. code-block:: python

    class WikiController(TGController):

        def index(self):
            """returns a list of wiki pages"""
            ...

        def _default(self, *args):
            """returns one wikipage"""
            ...

        def create(self, title, text, author='anonymous', **kw):
            wikipage = Page(title=tile, text=text, author=author, tags=str(kw))
            DBSession.add(wikipage)

        def update(self, title, **kw):
            wikipage = DBSession.query(Page).get(title)
            for key, value in kw:
                setattr(wikipage, key, value)

        def delete(self, title):
            wikipage = DBSession.query(Page).get(title)
            DBSession.delete(wikipage)

+----------------------------------------------------+------------+-------------------------------------------------+
| URL                                                | Method     | Argument Assignments                            |
+====================================================+============+=================================================+
| /                                                  | index      |                                                 |
+----------------------------------------------------+------------+-------------------------------------------------+
| /NewPage                                           | _default   | args : ['NewPage']                              |
+----------------------------------------------------+------------+-------------------------------------------------+
| /create/NewPage?text=More Information              | create     | text: 'More Information'                        |
+                                                    |            +-------------------------------------------------+
|                                                    |            | title: 'NewPage'                                |
+----------------------------------------------------+------------+-------------------------------------------------+
| /update/NewPage?author=Lenny                       | update     | kw: {'author':'Lenny'}                          |
+                                                    |            +-------------------------------------------------+
|                                                    |            | title: 'NewPage'                                |
+----------------------------------------------------+------------+-------------------------------------------------+
| /delete/NewPage                                    | delete     | title :'NewPage'                                |
+----------------------------------------------------+------------+-------------------------------------------------+

The parameters that are turned into arguments arrive in string format.
It is a good idea to use Python's type casting capabilities to change
the arguments into the types the rest of your program expects.  For
instance, if you pass an integer 'id' into your function you might use
id = int(id) to cast it into an int before usage.  Another way to
accomplish this feat is to use the @validate decorator, which is
explained in :ref:`Validation`

Ignore Unused Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default TurboGears2 will complain about parameters that the controller
method was not expecting. If this is causing any issue as you need to share
between all the urls a parameter that it is used by your javascript framework
or for any other reason, you can use ``ignore_parameters`` option to have
TurboGears2 ignore them. Just add the list of parameters to ignore in
*config/app_cfg.py*::

    base_config.ignore_parameters = ['timestamp', 'param_name']

You will still be able to access them from the ``tg.request`` object if you
need them for any reason.
