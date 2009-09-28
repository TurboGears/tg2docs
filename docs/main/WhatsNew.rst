.. _whatsnew:

What's New In TurboGears 2
==========================

The most significant change in TurboGears 2 is the decision to work
very, very closely with Pylons.  We've basically built a copy of the
TurboGears 1.x API on top of Pylons/paste which allows our two
communities to work together on everything from internationalization
to database connection pooling.

Another significant change is that we've removed the tg-admin wrapper
and started explicitly using paster for administrative commands to
match what Pylons was doing.  We've re-implemented the old tg-admin
commands as paster commands; for example, "tg-admin quickstart" is
replaced by "paster quickstart".

The "Why" Of TurboGears 2
-------------------------

Lots of questions have been asked about why we've decided to create
TurboGears 2 the way we did, so let's try to answer them as best we
can.

Why So Many Changes?
~~~~~~~~~~~~~~~~~~~~

Well, there are a lot of changes, but perhaps not as many as it looks
like from the description.  We were able to keep the controller API
very similar to TurboGears 1, and Genshi copied the Kid API, so while
we chose new components, we didn't really change the way Controllers
and Templates look very much at all.  Sure, there are some minor
changes here and there, but one member of the TurboGears 2 training
class at PyCon said "I didn't notice a lot that was new in terms of
how you put a TurboGears application together."

Why Not Just Merge With Pylons?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Well, Pylons is committed to being officially template engine
agnostic, ORM agnostic, etc.  On the other hand TurboGears is
committed to providing a "Full-Stack" for web development.  So, the
two communities have different, but compatible priorities.  If you
think about it Pylons provides a great set of tools for building a
full-stack framework, and people had been asking for a full-stack
Pylons implementation for a long time.  And TurboGears 2 provides
that.

There are a lot of benefits to having a full-stack.  You can build
form helpers which do all sorts of interesting things (introspect
model objects to make web-based forms, automatically display form
errors, etc) because you can make some assumptions about what tools
will be available and what will be used.  In particular, you can start
building pluggable website components much more easily, because you
are building on a known set of tools.

Why Not Use CherryPy 3?
~~~~~~~~~~~~~~~~~~~~~~~

This is something we really struggled with.  CherryPy 3 is a huge
improvement over CherryPy 2, providing a much richer programming
experience, and huge performance gains.  But TurboGears 1 was very
tightly coupled to the config system of CherryPy 2, which was entirely
rewritten in CherrPy 3.  We tried to make a backwards compatible TG
based on CherryPy 3, but discovered that it was significantly more
difficult than we had expected.

At the same time there was a push to make TurboGears 2 more WSGI
based, and to take advantage of things like Routes middleware, and to
generally take advantage of the Pylons/WSGI revolution.  We discovered
that Pylons had a lot of the same code as TurboGears (both of us had
Buffet implementations, both of us had SQLObject wrappers that did the
same thing, etc)

Why Genshi?
~~~~~~~~~~~

Well, Genshi is an intentional re-implementation of Kid, with an
almost identical API.  But internally it's simpler, faster, and
provides better error messages.  The inclusion of a couple of new
features -- includes and full x-path support -- also make it
significantly more flexible.

Genshi has also developed a larger, more active community than Kid,
and is being used in lots of places outside of TurboGears so, unlike
Kid, it's not at all likely to have to be taken over and maintained by
the TG core developers.

Why SQLAlchemy?
~~~~~~~~~~~~~~~

SQLAlchemy is arguably the best ORM available for Python.  Some have even proclaimed
it the best ORM in any language.  The fact is, writing your own ORM is hard, and
if we were to spend time doing that, we'd have no time to glue together everything
that makes TG great.  Previously, TurboGears used SQLObject, which implements
the `ActiveRecord`_ pattern, whereas SQLAlchemy utilizes the Data Mapper Pattern.
We feel that the `Data Mapper`_ Pattern is more flexible for the longevity of a project,
in that it gives you direct access to the Table Objects, allowing you to map
the Related Objects around it.  For those who want everything summed up in a 
single mapping class, SQLAlchemy provides a Declarative form of Object definition
which implements ActiveRecord, while still giving you access to your tables.

Design decisions aside, SA has an active `community`_, and has a well-maintained 
codebase that is also well `documented`_.  This makes it a perfect choice for
us because while we love giving you documentation, there is no way we
could provide the detail required to do Object Relational Mapping justice.

.. _`ActiveRecord`: http://en.wikipedia.org/wiki/Active_record_pattern
.. _`Data Mapper`: http://www.martinfowler.com/eaaCatalog/dataMapper.html
.. _`community`: http://groups.google.com/group/sqlalchemy
.. _`documented`: http://www.sqlalchemy.org/docs/

New Features Of TurboGears 2:
-----------------------------

  * Cache system
  * Error report: interactive tracebacks through the web, custom error pages, and email alerts
  * API Document generator through Sphinx
  * could pass status code to flash message
  * support crud interface generator

Compatibility
-------------

Areas of compatibility:

  * Like TurboGears 1.1, TurboGears 2 supports Python 2.4 and above.
  * TurboGears 1.x and TurboGears 2.x can both be installed on the
    same machine.  They are different packages with different
    namespaces.  Right now there are no dependency conflicts.  But
    using virtualenv is highly recommended to eliminate the
    possibility of future dependency conflicts.
  * Object dispatch is implemented in TurboGears 2.x, so you can use
    arguments and keywords in functions the same way you did in
    TurboGears 1.x.
  * Expose and error handling decorators are implemented in TurboGears 2.x,
    you can use decorators just like TurboGears 1.x.


Differences:
  * CherryPy filters will not work in TurboGears 2.x.  You can write
    middleware to do what filters did in CherryPy2
  * The @expose decorator has a slightly updated syntax for content
    type declaration
  * All template engines now have search paths to find the templates.
    The default template directory is on the search path so using dotted
    notation in @expose decorators has been deprecated.

    .. todo:: Difficulty: Easy. has dotted notation for templates in @expose really been deprecated?
  * Object dispatch does not support dots in URLs the way TurboGears 1
    did.
  * CherryPy request and response objects are replaced with WebOb
    request and response objects.

Command Changes
---------------

Use paster command instead of the old tg-admin command.

For example you now type ``paster quickstart`` rather than ``tg-admin
quickstart`` to start a project.

Here's a full list of the old command line tools and their new
equivalents

  * ``tg-admin quickstart`` ---> ``paster quickstart``
  * ``tg-admin info`` ---> ``paster tginfo``
  * ``tg-admin toolbox`` --> ``paster toolbox``
  * ``tg-admin shell`` --> ``paster shell``
  * ``tg-admin sql create`` --> ``paster setup-app development.ini``

Project Layout Changes
----------------------

Both controllers.py and model.py have been replaced by the controllers
and model folders.  In other words they are now Python packages, in
just the way they were in TurboGears 1 if you used the '--template
tgbig' option with quickstart.

  * your root controller is not in ``controllers.py`` -> it has moved to ``controllers/root.py``
  * ``model.py`` -> ``model/__init__.py``
  * ``myproject_dev.cfg`` -> ``development.ini`` **With a whole new structure based on paste.deploy**
  * ``app.cfg`` -->  ``config/environment.py`` and to a lesser extent ``config/middleware.py``


New Imports
-----------

  * import turbogears -> import tg
  * turbogears.config.get('sqlalchemy.dburi') -> pylons.config['sqlalchemy.url']
  * pylons.tmpl_context provides a request local place to stick stuff
  * pylons.request  provides the rough equivalent of cherrypy.request
  * pylons.response provides the equivalent of cherrypy.response
