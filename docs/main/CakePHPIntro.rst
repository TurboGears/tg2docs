Intro to TurboGears for CakePHP developers
==========================================

:Status: RoughDoc

.. contents:: Table of Contents
   :depth: 2


This document serves as an intro to TurboGears for those migrating from CakePHP (and possibly other PHP frameworks). We will assume some familiarity with the Python language, and will try to stick to outlining the core differences between the *frameworks* rather than the languages (quite beyond the scope of this document).


A 30,000 feet comparison
------------------------

Of course, the largest difference between CakePHP and TurboGears is the core language. However, from a technical standpoint, both are quite similar: Both are open source, both have an active community, and both provide a rich component set.

+----------------+----------+----------+---------+-------------------------+---------+---------------+-------------+
| Framework      | Language | License  | Started | Deployment Options      | MVC     | MVC Push/Pull | i18n & l10n |
+================+==========+==========+=========+=========================+=========+===============+=============+
| **CakePHP**    | PHP      | MIT      | 2005    | Apache, FastCGI,        | Yes     | Push          | Yes         |
|                |          |          |         | etc.                    |         |               |             |
+----------------+----------+----------+---------+-------------------------+---------+---------------+-------------+
| **TurboGears** | Python   | MIT/LGPL | 2005    | paster, Apache          | Yes     | Push          | Yes         |
|                |          |          |         | (mod_wsgi or mod_proxy) |         |               |             |
+----------------+----------+----------+---------+-------------------------+---------+---------------+-------------+


Feature and component wise, both frameworks provide advanced functionality such as a rich ORM, a tight security framework, and an easy to use forms creation & validation framework:

+-------------------------+-----------------------------+-------------------------------------------+
| Feature/Component       | CakePHP                     | TurboGears                                |
+=========================+=============================+===========================================+
| ORM:                    | Active Record Pattern       | ``SQLAlchemy`` (Data Mapper Pattern)      |
+-------------------------+-----------------------------+-------------------------------------------+
| Testing Framework:      | Based on SimpleTest         | ``nose``                                  |
+-------------------------+-----------------------------+-------------------------------------------+
| Security Framework:     | Security component          | ``repoze.who`` & ``repoze.what``          |
+-------------------------+-----------------------------+-------------------------------------------+
| Forms Framework:        | Form helper                 | ``tw.forms`` & ``formencode``             |
+-------------------------+-----------------------------+-------------------------------------------+
| Caching Framework:      | Yes                         | ``beaker``                                |
+-------------------------+-----------------------------+-------------------------------------------+
| DB Migration Framework: | SchemaShell                 | ``sqlalchemy-migrate``                    |
+-------------------------+-----------------------------+-------------------------------------------+
| Template Framework:     | PHP files                   | Multiple [#]_                             |
+-------------------------+-----------------------------+-------------------------------------------+
| Ajax:                   | Prototype & script.aculo.us | ``toscawidgets`` or roll your own [#]_    |
+-------------------------+-----------------------------+-------------------------------------------+


.. [#] TurboGears supports Genshi (default), Mako, and Jinja2 out of the box. See the `alternate templates <Templates/Alternative.html>`_ page for more information.
.. [#] TurboGears is JavaScript/Ajax agnostic and therefore approaches Ajax and DHTML differently than a framework tied to only one JS library. For more information see the `ToscaWidgets <ToscaWidgets/ToscaWidgets.html>`_ section.


Project Folders
---------------

+------------------------+-------------------------------------------+
| CakePHP                | TurboGears                                |
+========================+===========================================+
| app/config             | myapp/config                              |
+------------------------+-------------------------------------------+
| app/controllers        | myapp/controllers                         |
+------------------------+-------------------------------------------+
| app/locale             | myapp/i18n                                |
+------------------------+-------------------------------------------+
| app/models             | myapp/model                               |
+------------------------+-------------------------------------------+
| app/plugins            | myapp/lib                                 |
+------------------------+-------------------------------------------+
| app/tmp                | data                                      |
+------------------------+-------------------------------------------+
| app/vendors            | n/a -- use ``easy_install packagename``   |
+------------------------+-------------------------------------------+
| app/views              | myapp/templates                           |
+------------------------+-------------------------------------------+
| app/webroot            | myapp/public                              |
+------------------------+-------------------------------------------+

See `this image <../_static/tg2_files.jpg>`_ for more information.


Routes
------

By default TurboGears is setup with one default route which goes to your RootController. This means you typically don't have to think about routes at all, and gives you great design flexibility.

However, advanced routing is available if needed. See `this page <RoutesIntegration.html>`_ for more information.


Controller
----------

In CakePHP (and many other PHP web frameworks) you are expected to have a separate controller file & class for each ``:controller`` route. The methods of the controller class become the ``:action`` routes, with the method arguments being the ``:id``.

In TurboGears, the philosiphy is similar with a bit of added flexability. As was mentioned in the previous section, the default routing in TurboGears is to the RootController class in ``myapp/controllers/root.py``. From RootController, you are free to define "sub-controllers" and methods however you like. A typical setup might look like this:

In ``myapp/controllers/root.py``::

    # initial imports edited out
    
    # this import loads our "sub-controller"
    from myapp.controllers.about import AboutController
    
    class RootController(BaseController):
        # the line below instructs the "about" route (http://www.example.com/about/) to
        # load the index method of the AboutController
        about = AboutController()
        
        # the next few lines handle the loading of the "root" route (http://www.example.com/)
        @expose('myapp.templates.index') # loads the index template
        def index(self):                 # defines the "index" action
            return dict(page='index')    # the 'page' variable is available in our template
        
        # you could just as easily specify another "controller" route (like we did with 'about')
        # by defining another method in this controller (becomes http://www.example.com/contact/)
        @expose()                        # no template needed (returning a string)
        def contact(self):
            return 'email@example.com'   # simply prints email@example.com


This is what the ``AboutController`` file might look like:

In ``myapp/controllers/about.py``::

    class AboutController(BaseController):
        # the index action (http://www.example.com/about/)
        @expose('myapp.templates.about')
        def index(self):
            return dict(page='about')


$components, $helpers, and $uses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Although these attributes play a major part in CakePHP classes, TurboGears has no need for this type of class attribute definition. To use a "component" or "helper" package in your class you would simply ``import packagename``. For your models you would simply ``from myapp.model import ModelClassName``.

Controller Methods
^^^^^^^^^^^^^^^^^^

CakePHP has a few special controller methods that deal with things like passing objects to a template, rendering templates, etc. Below is a list of these methods, and TurboGears' equivalent:

+------------------------+-------------------------------------------------+
| CakePHP                | TurboGears                                      |
+========================+=================================================+
| set()                  | ``tmpl_context`` or passed in ``return dict()`` |
+------------------------+-------------------------------------------------+
| render()               | ``@expose(myapp.path.to.templatefile)``         |
+------------------------+-------------------------------------------------+
| redirect()             | ``from tg import redirect``                     |
+------------------------+-------------------------------------------------+
| flash()                | ``from tg import flash``                        |
+------------------------+-------------------------------------------------+


Components
----------

The "batteries included" nature of Python (and therefore TurboGears) means that you have a lot of packages available right at your fingertips. Aside from familiarizing yourself with Python's standard library, it is also a good idea to become acquainted with `TurboGears' module library <../modindex.html>`_.


A Comparison of Components
^^^^^^^^^^^^^^^^^^^^^^^^^^

+------------------------+--------------------------------------------------------+
| CakePHP [#]_           | TurboGears                                             |
+========================+========================================================+
| ACL, Auth  & Security  | ``repoze.who`` and ``repoze.what``                     |
+------------------------+--------------------------------------------------------+
| Cookie                 | ``from tg import response``, ``response.set_cookie()`` |
|                        | & ``from tg import request``, ``request.cookies``      |
+------------------------+--------------------------------------------------------+
| Email                  | ``TurboMail`` [#]_                                     |
+------------------------+--------------------------------------------------------+
| RequestHandler         | ``request.environ`` (dictionary)                       |
+------------------------+--------------------------------------------------------+
| Session                | ``from tg import session``                             |
+------------------------+--------------------------------------------------------+

.. [#] http://book.cakephp.org/view/170/Core-Components
.. [#] http://www.python-turbomail.org/


Models & Behaviors
------------------

TurboGears uses a high-performance enterprise-level SQL toolkit and ORM named `SQLAlchemy <./SQLAlchemy.html>`_.


Views
-----

Whereas PHP itself acts as CakePHP's template language, TurboGears has `a number of templating languages available <./Templates/Alternative.html>`_. The most popular choices are `Genshi <http://genshi.edgewall.org/>`_ (a pure XML-based template language) and `Mako <http://www.makotemplates.org/>`_ (non-XML, but much faster than Genshi).

As we saw earlier in TG's equivalent `Controller Methods`_, data is typically passed from the controller to the view by using the special ``tmpl_context`` object, or by defining dictionary values in the controller method's ``return``.

Helpers
-------

Helpers are managed in the ``mypackage/lib/helpers.py`` file and are typically accessed in your template through the ``h`` object. TurboGears ships with several built-in helpers (see `the webhelpers page <../modules/thirdparty/webhelpers.html>`_), but Python's modular nature makes it very easy to add helpers to your project. Usually all you have to do is ``easy_install packagename`` and then at the top of your ``helpers.py`` file put ``import packagename as mynewhelper``. You can then access your new helper in your view by using ``h.mynewhelper``.


A Comparison of Helpers
^^^^^^^^^^^^^^^^^^^^^^^

As we just mentioned, TurboGears makes it very easy to "plug & play" helpers. Below is a list of CakePHP's built-in helpers, with the TurboGears equivalent that is typically used:

+------------------------+-------------------------------------------+
| CakePHP [#]_           | TurboGears                                |
+========================+===========================================+
| Ajax                   | ``toscawidgets`` or roll your own [2]_    |
+------------------------+-------------------------------------------+
| Cache                  | ``beaker``                                |
+------------------------+-------------------------------------------+
| Form                   | ``tw.forms`` and/or ``sprox``             |
+------------------------+-------------------------------------------+
| HTML                   | ``webhelpers.html``                       |
+------------------------+-------------------------------------------+
| JavaScript             | ``webhelpers.html``                       |
+------------------------+-------------------------------------------+
| Number                 | ``webhelpers.number``                     |
+------------------------+-------------------------------------------+
| Paginator              | ``webhelpers.paginate``                   |
+------------------------+-------------------------------------------+
| RSS                    | ``webhelpers.feedgenerator``              |
+------------------------+-------------------------------------------+
| Session                | ``tg.session``                            |
+------------------------+-------------------------------------------+
| Text                   | ``webhelpers.text``                       |
+------------------------+-------------------------------------------+
| Time                   | ``webhelpers.date``                       |
+------------------------+-------------------------------------------+
| XML                    | ``ElementTree`` or ``lxml``               |
+------------------------+-------------------------------------------+

.. [#] http://book.cakephp.org/view/181/Core-Helpers


Scaffolding
-----------

Apart from a `project quickstart <./QuickStart.html>`_, TurboGears tries to avoid generating code for you. We are of the opinion that it is easier to build pages from the ground up than to tweak code that is generated from a framework's "best-guess" about your project.

Having said that, there are a couple of modules and extensions that can help you start interacting with your models right away:

* `Sprox <http://sprox.org/>`_
* `tgext.crud <./Extensions/Crud/index.html>`_
* `tgext.admin <./Extensions/Admin/index.html>`_



Pros and Cons
-------------

**CakePHP**

*Pros*
    * PHP hosting environments are a dime a dozen
    * The "views" are regular PHP files (no need to learn a new template syntax)
    * The built-in ``$ajax`` helper class provides a convenient wrapper for Prototype/Scriptaculous

*Cons*
    * The built-in DHTML & Ajax is tied to one JavaScript/Ajax library
    * CakePHP is typically *much* slower than TurboGears [6]_
 
 
**TurboGears**

*Pros*
    * SQLAlchemy
    * JavaScript library independent with multiple widget options
    * Multiple templating options (XML based and non-XML based)
    * TurboGears is typically *much* faster than CakePHP [6]_

*Cons*
    * Might need root access to set up a "production" environment (see `deployment options <./Deployment.html>`_)

.. [#] http://blog.curiasolutions.com/?p=172
 
