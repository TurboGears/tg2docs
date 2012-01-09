================================================
Whetting the Appetite: Make a Wiki in 20 Minutes
================================================

.. archive:: wiki20
   :root: Wiki-20

How does TurboGears2 help you get development done quickly? We'll show
you by developing a simple wiki application that should take you no
more than 20 minutes to complete. We're going to do this without
explaining the steps in detail (that is what this book is for, after
all). As a result, you'll see how easily you can make your own web
applications once you are up to speed on what TurboGears2 offers.

If you're not familiar with the concept of a wiki you might want to
check out `the Wikipedia entry <http://en.wikipedia.org/wiki/Wiki>`_.
Basically, a wiki is an easily-editable collaborative web content
system that makes it trivial to link to pages and create new pages.
Like other wiki systems, we are going to use CamelCase words to
designate links to pages.

If you have trouble with this tutorial ask for help on the `TurboGears
discussion list`_, or on the IRC channel #turbogears.  We're a
friendly bunch and, depending what time of day you post, you'll get
your answer in a few minutes to a few hours. If you search the mailing
list or the web in general you'll probably get your answer even
faster. **Please don't post your problem reports as comments on this
or any of the following pages of the tutorial**. Comments are for
suggestions for improvement of the docs, not for seeking support.

If you want to see the final version you can download a copy of the
`wiki code`_.

Setup
=====

.. highlight:: bash

To go through this tutorial, you'll need:

#.  Python_ 2.4, 2.5, 2.6 or 2.7.  Note that Mac OSX 10.5 (Leopard)
    comes with Python 2.5 pre-installed.

#.  virtualenv_. Not that on many Linux based systems you will need to
    install a Python development package for this to work, such as
    python-devel or python-dev. In addition, virtualenv is available
    via most package managers, so can be installed that way.

#.  A web browser.

#.  Your favorite editor.

#.  Two command line windows
    (you only *need* one, but two is nicer).

#.  **Optional:** If you're not aware of it, you may also find the
    `ipython shell`_ to be helpful. It supports attribute tab completion for
    many objects (which can help you find the method you're searching for)
    and can display contextual help if you append a question mark onto the
    end of an object or method. You can do the same in the standard shell
    with the ``dir()`` and ``help()`` functions, but ipython is more
    convenient. ipython has a number of other convenient features, like
    dropping into the debugger on an error; take a look at the `ipython docs`_
    for more information. You can install it with::

        $ easy_install ipython

This tutorial doesn't cover Python at all. Check the `Python
Documentation`_ page for more coverage of Python.

Virtual Environment
===================

The use of a virtual environment is highly recommended. It allows you
to segregate your development work from the system, so you can freely
experiment without worrying about breaking some other package. The use
of it is two steps: Making the directory structure for the virtual
environment, and activating it.

Making the Virtual Environment
------------------------------

This is the same across all platforms. Use the following command::

     $ virtualenv --no-site-packages path/to/virtualenvironment

The "--no-site-packages" ensures that your virtual environment is just
what comes with Python. Using that, you ensure that you have no
unknown conflicts while doing your development.

Activating the Virtual Environment
----------------------------------

On Linux and other UNIX (or UNIX-like) operating systems, use this
command::

   $ source path/to/virtualenvironment/bin/activate

On Windows, use this command::

   C:\> path\to\virtualenvironment\bin\activate
   
On all platforms, when you are done, use the "deactivate" command to
return to using your system wide Python installation.

Installing the Development Tools
================================

Once you have your development environment prepared (using the
instructions for making a virtualenv above), installing TurboGears2
itself is extremely easy. Run this command::

     $ easy_install -i http://tg.gy/current tg.devtools

Wait a few moments as the dependencies are installed and prepared for
you.

Quickstart
==========

TurboGears2 provides a suite of tools for working with projects by
adding several commands to the Python command line tool ``paster``. A
few will be touched upon in this tutorial. (Check the
:doc:`../appendices/commandline` for a full listing.) The first tool
you'll need is ``quickstart``, which initializes a TurboGears project.
Go to a command line window and run the following command::

    $ paster quickstart

You'll be prompted for the name of the project (this is the pretty
name that human beings would appreciate), and the name of the package
(this is the less-pretty name that Python will like).  Here's what our
choices for this tutorial look like::

    $ paster quickstart
    Enter project name: Wiki 20
    Enter package name [wiki20]: 
    Would you prefer mako templates? (yes/[no]): no
    Do you need authentication and authorization in this project? ([yes]/no): yes

    
We recommend you use the names given here: this documentation looks
for files in directories based on these names.

Now ``paster`` will spit out a bunch of stuff::

  Selected and implied templates:
    tg.devtools#turbogears2  TurboGears 2. Standard Quickstart Template

  ...etc...

  reading manifest file 'Wiki_20.egg-info/SOURCES.txt'
  reading manifest template 'MANIFEST.in'
  writing manifest file 'Wiki_20.egg-info/SOURCES.txt'

This creates a few files in a directory tree just below your current
directory.  You will notice that the quickstart created a directory
without spaces for convenience: project name "Wiki 20" resulted in the
directory name "Wiki-20".  Go in there and take a look around::

    $ cd Wiki-20

You need to update the dependencies in the file "setup.py". Currently,
it looks like this:

.. code:: Wiki-20/setup.py
   :revision: a88c887745f6457f8348bac861538665f8496ff5
   :section: setupdeps

You need to add "docutils" to the list. TurboGears2 does not require
docutils, but the wiki we are building does. In addition, if you are
using Python 2.4, you need to add "pysqlite". For this tutorial, we
are using the SQLite_ database, and Python 2.4 does not include
support for it out of the box.

Now to be able to run the project you will need to install it and
its dependencies. This can be quickly achieved by running from
inside the ``Wiki-20`` directory::

    $ python setup.py develop

Then ``paster`` provides a simple mechanism for running a TurboGears
project.  Again from the ``Wiki-20`` directory, run this command::

    $ paster serve --reload development.ini

The ``--reload`` flag means that changes that you make in the project
will automatically cause the server to restart itself. This way you
immediately see the results.

Point your browser to http://localhost:8080 , and you'll see a nice
welcome page. You now have a working project!  And you can access the
project from within the python/ipython shell by typing::

    $ paster shell development.ini

If ipython is installed within your virtual environment, it will be the
default shell.  Right now, we're not going to do much with the shell, but
you may find other tutorials which use it to add data to the database.


Controller And View
===================

If you take a look at the code that ``quickstart`` created, you'll see
everything necessary to get up and running. Here, we'll look at the
two files directly involved in displaying this welcome page.

TurboGears follows the `Model-View-Controller paradigm`_
(a.k.a. "MVC"), as do most modern web frameworks like Rails, Django,
Struts, etc.

**Model**
    For a web application, the "model" refers to the way the data is
    stored. In theory, any object *can* be your model. In practice,
    since we're in a database-driven world, your model will be based
    on a relational database. By default TurboGears 2 uses the
    powerful, flexible, and relatively easy-to-use SQLAlchemy object
    relational mapper to build your model and to talk to your
    database. We'll look at this in a later section.

**View**
    To minimize duplication of effort web frameworks use *templating
    engines* which allow you to create "template" files. These specify
    how a page will always look, with hooks where the templating
    engine can substitute information provided by your web
    application.  TurboGears 2's default templating engine is
    `Genshi`_, although several other engines are supported out of the
    box and can be configured in your `config/app_cfg.py` file (see
    part IV of this book).

    .. todo:: add link to part IV when it is written

**Controller**
    The controller is the way that you tell your web application how
    to respond to events that arrive on the server. In a web
    application, an "event" usually means "visiting a page" or
    "pressing a submit button" and the response to an event usually
    consists of executing some code and displaying a new page.

Controller Code
---------------

.. highlight:: python

`Wiki-20/wiki20/controllers/root.py` (see below) is the code that
causes the welcome page to be produced. After the imports the first
line of code creates our main controller class by inheriting from
TurboGears' ``BaseController``::

    class RootController(BaseController):

The TurboGears 2 controller is a simple object publishing system; you
write controller methods and ``@expose()`` them to the web. In our
case, there's a single controller method called ``index``. As you
might guess, this name is not accidental; this becomes the default
page you'll get if you go to this URL without specifying a particular
destination, just like you'll end up at ``index.html`` on an ordinary
web server if you don't give a specific file name. You'll also go to
this page if you explicitly name it, with
``http://localhost:8080/index``. We'll see other controller methods
later in the tutorial so this naming system will become clear.

The ``@expose()`` decorator tells TurboGears which template to use to
render the page.  Our ``@expose()`` specifies::

    @expose('wiki20.templates.index')

This gives TurboGears the template to use, including the path
information (the ``.html`` extension is implied). We'll look at this
file shortly.

Each controller method returns a dictionary, as you can see at the end
of the ``index`` method. TG takes the key:value pairs in this
dictionary and turns them into local variables that can be used in the
template.

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: a88c887745f6457f8348bac861538665f8496ff5


Displaying The Page
-------------------

`Wiki-20/wiki20/templates/index.html` (see below) is the template
specified by the ``@expose()`` decorator, so it formats what you view
on the welcome screen. Look at the file; you'll see that it's standard
XHTML with some simple namespaced attributes. This makes it very
designer-friendly, and well-behaved design tools will respect all the
`Genshi`_ attributes and tags.  You can even open it directly in your
browser.

Genshi directives are elements and/or attributes in the template that
are usually prefixed with ``py:``. They can affect how the template is
rendered in a number of ways: Genshi provides directives for
conditionals and looping, among others.  We'll see some simple Genshi
directives in the sections on :ref:`Editing pages <editing_pages>` and
:ref:`Adding views <adding_views>`.


.. code:: Wiki-20/wiki20/templates/index.html
   :revision: a88c887745f6457f8348bac861538665f8496ff5

Wiki Model and Database
=======================

``quickstart`` produced a directory for our model in
`Wiki-20/wiki20/model/`. This directory contains an `__init__.py`
file, which makes that directory name into a python module (so you can
use ``import model``).

Since a wiki is basically a linked collection of pages, we'll define a
``Page`` class as the name of our model. Create a new file called
`page.py` in the ``Wiki-20/wiki20/model/`` directory:

.. code:: Wiki-20/wiki20/model/page.py
   :revision: 5a429eb6c366afe80a21523b7bf334f2b57e588e


In order to easily use our model within the application, modify the
`Wiki-20/wiki20/model/__init__.py` file to add ``Page`` to the
module. Add the following line *at the end of the file*:.

.. code-block:: python

    from wiki20.model.page import Page

.. warning::

    It's very important that this line is at the end because
    ``Page`` requires the rest of the model to be initialized
    before it can be imported:

Let's investigate our model a little more.  The ``metadata`` object is
automatically created by the ``paste`` command inside the
``__init__.py`` file. It's a "single point of truth" that keeps all
the information necessary to connect to and use the database. It
includes the location of the database, connection information and the
tables that are in that database. When you pass the metadata object to
the various objects in your project they initialize themselves using
that metadata.

In this case, the metadata object configures itself using the
`development.ini` file, which we'll look at in the next
section.

The SQLAlchemy ``DeclarativeBase`` object defines what a single Python
object looks like in the database, and adds any necessary constraints
(so, for example, even if your database doesn't enforce uniqueness,
SQLAlchemy will attempt to do so). It provides the metadata object
mentioned above, and makes it very easy to define mappings from
objects to tables in your database.

An object defined using the DeclarativeBase has a set of class level
variables (instead of instance level) which define the columns. As you
can see, ``Column`` objects are defined in the same way that you
define them within a database: name, type, and constraints.

Note that it's also possible to start with an existing database, but
that's a more advanced topic that we won't cover in this tutorial.  If you
would like more information on how to do that, check out sqlautocode.

.. todo:: add internal links to sqlautocode when ready.

Database Configuration
----------------------

By default, projects created with ``quickstart`` are configured to use
a very simple SQLite database (however, TurboGears 2 supports most
popular databases). This configuration is controlled by the
`development.ini` file in the root directory (`Wiki-20`, for our
project).

Search down until you find the ``[app:main]`` section in
`development.ini`, and then look for ``sqlalchemy.url``. You should
see this::

    sqlalchemy.url = sqlite:///%(here)s/devdata.db

Turbogears will automatically replace the ``%(here)s`` variable with
the parent directory of this file, so for our example it will produce
``sqlite:///Wiki-20/devdata.db``. You won't see the `devdata.db` file
now because we haven't yet initialized the database.


Initializing The Tables
-----------------------

Before you can use your database, you need to initialize it and add
some data.  There's built in support for this in TurboGears using
``paster setup-app``.  The quickstart template gives you a basic 
template database setup inside the ``websetup/boostrap.py`` file
which by default creates two users, one manager group and one
manage permission:

.. highlight:: python

We need to update the file to create our `FrontPage` data just before
the ``DBSession.flush()`` command by adding::

    page = model.Page("FrontPage", "initial data")
    model.DBSession.add(page)

The resulting boostrap file will look like:

.. code:: Wiki-20/wiki20/websetup/bootstrap.py


If you're familiar with SQLAlchemy this should look pretty standard to
you.  One thing to note is that we use::

    transaction.commit()

Where you're used to seeing ``DBSession.commit()`` we use
``transaction.commit()``.  This calls the transaction manager which
helps us to support cross database transactions, as well as
transactions in non relational databases, but ultimately in the case
of SQLAlchemy it calls ``DBSession.commit()`` just like you might if
you were doing it directly.

Now run the ``paster setup-app`` command:

.. code-block:: bash

    $ paster setup-app development.ini

You'll see output, but you should not see error messages. At this
point your database is created and has some initial data in it, which
you can verify by looking at ``Wiki-20/devdata.db``. The file should
exist and have a nonzero size.

That takes care of the "M" in MVC.  Next is the "C": controllers.


Adding Controllers
==================

.. highlight:: python

Controllers are the code that figures out which page to display, what
data to grab from the model, how to process it, and finally hands off
that processed data to a template.

``quickstart`` has already created some basic controller code for us
at `Wiki-20/wiki20/controllers/root.py`.  Here's what it looks like
now:

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: a88c887745f6457f8348bac861538665f8496ff5

First, we must import the ``Page`` class from our model. At the end of
the ``import`` block, add this line::

    from wiki20.model.page import Page

Now we will change the template used to present the data, by changing
the ``@expose('wiki20.templates.index')`` line to::

    @expose('wiki20.templates.page')

This requires us to create a new template named `page.html` in the
`wiki20/templates` directory; we'll do this in the next section.

Now we must specify which page we want to see.  To do this, add a
parameter to the ``index()`` method. Change the line after the
``@expose`` decorator to::

    def index(self, pagename="FrontPage"):

This tells the ``index()`` method to accept a parameter called
``pagename``, with a default value of ``"FrontPage"``.

Now let's get that page from our data model.  Put this line in the
body of ``index``::

    page = DBSession.query(Page).filter_by(pagename=pagename).one()

This line asks the SQLAlchemy database session object to run a query
for records with a ``pagename`` column equal to the value of the
``pagename`` parameter passed to our controller method.  The
``.one()`` method assures that there is only one returned result;
normally a ``.query`` call returns a list of matching objects. We only
want one page, so we use ``.one()``.

Finally, we need to return a dictionary containing the ``page`` we
just looked up.  When we say::

   return dict(wikipage=page)

The returned ``dict`` will create a template variable called
``wikipage`` that will evaluate to the ``page`` object that we looked
it up.

Here's the whole file after incorporating the above modifications:

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: 133a5a52b778c916cc4441deb44ab99e08e89e46
   
Now our ``index()`` method fetches a record from the database
(creating an instance of our mapped ``Page`` class along the way), and
returns it to the template within a dictionary.

.. _adding_views:

Adding Views (Templates)
========================

.. highlight:: html

``quickstart`` also created some templates for us in the
`Wiki-20/wiki20/templates` directory: `master.html` and `index.html`.
Back in our simple controller, we used ``@expose()`` to hand off a
dictionary of data to a template called ``'wiki20.templates.index'``,
which corresponds to `Wiki-20/wiki20/templates/index.html`.

Take a look at the following line in `index.html`::

    <xi:include href="master.html" />

This tells the ``index`` template to *include* the ``master``
template.  Using includes lets you easily maintain a cohesive look and
feel throughout your site by having each page include a common master
template.

Similarly the lines::

  <xi:include href="header.html" />
  <xi:include href="footer.html" />

Tell Genshi to pull in the headers and footers for the page.

Copy the contents of `index.html` into a new file called `page.html`.
Now modify it for our purposes:

.. code:: Wiki-20/wiki20/templates/page.html
   :revision: e610faabe4758844256dcc946258ad89badf7905
   
This is a basic XHTML page with three substitutions:

1.  In the ``<title>`` tag, we substitute the name of the page, using
    the ``pagename`` value of ``page``.  (Remember, ``wikipage`` is an
    instance of our mapped ``Page`` class, which was passed in a
    dictionary by our controller.)

2.  In the second ``<div>`` element, we substitute the page name again
    with Genshi's ``py:replace``:

    .. code:: Wiki-20/wiki20/templates/page.html
       :revision: e610faabe4758844256dcc946258ad89badf7905
       :section: PageName
   
3.  In the third ``<div>``, we put in the contents of our``wikipage``:

    .. code:: Wiki-20/wiki20/templates/page.html
       :revision: e610faabe4758844256dcc946258ad89badf7905
       :section: PageContent

When you refresh the output web page you should see "initial data"
displayed on the page.

.. note:: py.replace_ replaces the *entire tag* (including start and
  end tags) with the value of the variable provided.

   .. _py.replace: http://genshi.edgewall.org/wiki/Documentation/xml-templates.html#id8

.. admonition:: For the curious...

   Do you wonder what those html comments like ##{B:PageContent} are?
   They do not matter for this tutorial and are only to help the
   documentation (you're soaking in it!) isolate certain lines of code
   to display, like above.

.. _editing_pages:

Editing pages
=============

One of the fundamental features of a wiki is the ability to edit the
page just by clicking "Edit This Page," so we'll create a template for
editing. First, make a copy of `page.html`:

.. code-block:: bash

    cd wiki20/templates
    cp page.html edit.html

We need to replace the content with an editing form and ensure people
know this is an editing page. Here are the changes for ``edit.html``.

.. highlight:: html

#. Change the title in the header to reflect that we are editing the
   page:

   .. code:: Wiki-20/wiki20/templates/edit.html
      :revision: 64df312db3002afd53b04d62319e57d7356ee4c9
      :section: Head

#. Change the div that displays the page:

    .. code:: Wiki-20/wiki20/templates/page.html
       :revision: e610faabe4758844256dcc946258ad89badf7905
       :section: PageContent

   with a div that contains a standard HTML form:

   .. code:: Wiki-20/wiki20/templates/edit.html
      :revision: 64df312db3002afd53b04d62319e57d7356ee4c9
      :section: Form

.. highlight:: python

Now that we have our view, we need to update our controller in order
to display the form and handle the form submission. For displaying the
form, we'll add an ``edit`` method to our controller in
`Wiki-20/wiki20/controllers/root.py`. The new `root.py` file looks
like this:

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: 66831c2877f1bdfb357018be2eaeb3ba83d96387

For now, the new method is identical to the ``index`` method; the only
difference is that the resulting dictionary is handed to the ``edit``
template. To see it work, go to
http://localhost:8080/edit/FrontPage . However, this only works because
FrontPage already exists in our database; if you try to edit a new
page with a different name it will fail, which we'll fix in a later
section.

Don't click that save button yet! We still need to write that method.

Saving Our Edits
================

When we displayed our wiki's edit form in the last section, the form's
``action`` was ``/save``.  So, we need to make a method called
``save`` in the Root class of our controller.

However, we're also going to make another important change. Our
``index`` method is *only* called when you either go to ``/`` or
``/index``. If you change the ``index`` method to the special method
``_default``, then ``_default`` will be automatically called whenever
nothing else matches. ``_default`` will take the rest of the URL and
turn it into positional parameters. This will cause the wiki to become
the default when possible.

Here's our new version of `root.py` which includes both ``default``
and ``save``:

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: 39410f7744de3ac88391d26f1ff3797e8a9dc6b3

Unlike the previous methods we've made, ``save`` just uses a plain
``@expose()`` without any template specified. That's because we're
only redirecting the user back to the viewing page.

Although the ``page.data = data`` statement tells SQLAlchemy that you
intend to store the page data in the database, nothing happens until
the ``DBSession.flush()`` method is called. This is commonly referred
to as the "unit of work" pattern, and it's an important structure for
database developers because it allows SQLAlchemy to combine many
operations into a single database update (or a minimized number of
updates if some changes depend upon earlier changes) and thus be much
more efficient in the database resources used.

SQLAlchemy also provides a ``DBSession.commit()`` method which flushes
and commits any changes you've made in a transaction.  TurboGears 2
provides a flexible transaction management system that automates this
process wrapping each web request in its own transaction and
automatically rolling back that transaction if you get a python
exception, or return an HTTP error code as your response.

You don't have to do anything to use this transaction management
system, it should just work. So, you can now make changes and save the
page we were editing, just like a real wiki.

What About WikiWords?
=====================

Our wiki doesn't yet have a way to link pages. A typical wiki will
automatically create links for *WikiWords* when it finds them
(WikiWords have also been described as WordsSmashedTogether). This
sounds like a job for a regular expression.

Here's the new version of `root.py`, which will be explained
afterwards:

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: 3d7f5ceea10e87e510f97f78bb870275293a1d1d

We need some additional imports, including ``re`` for regular
expressions and a method called ``publish_parts`` from ``docutils``.

A WikiWord is a word that starts with an uppercase letter, has a
collection of lowercase letters and numbers followed by another
uppercase letter and more letters and numbers. The ``wikiwords``
regular expression describes a WikiWord.

In ``_default``, the new lines begin with the use of ``publish_parts``,
which is a utility that takes string input and returns a dictionary of
document parts after performing conversions; in our case, the
conversion is from Restructured Text to HTML.  The input
(``page.data``) is in Restructured Text format, and the output format
(specified by ``writer_name="html"``) is in HTML. Selecting the
``fragment`` part produces the document without the document title,
subtitle, docinfo, header, and footer.

You can configure TurboGears so that it doesn't live at the root of a
site, so you can combine multiple TurboGears apps on a single
server. Using ``tg.url()`` creates relative links, so that your links
will continue to work regardless of how many apps you're running.

The next line rewrites the ``content`` by finding any WikiWords and
substituting hyperlinks for those WikiWords. That way when you click
on a WikiWord, it will take you to that page. The ``r'string'`` means
'raw string', one that turns off escaping, which is mostly used in
regular expression strings to prevent you from having to double escape
slashes. The substitution may look a bit weird, but is more
understandable if you recognize that the ``%s`` gets substituted with
``root``, then the substitution is done which replaces the ``\1`` with
the string matching the regex.

Note that ``_default()`` is now returning a ``dict`` containing an
additional key-value pair: ``content=content``. This will not break
``wiki20.templates.page`` because that page is only looking for
``page`` in the dictionary, however if we want to do something
interesting with the new key-value pair we'll need to edit
``wiki20.templates.page``:

.. code:: Wiki-20/wiki20/templates/page.html
   :revision: 3d7f5ceea10e87e510f97f78bb870275293a1d1d
   :language: html

Since ``content`` comes through as XML, we can strip it off using the
``XML()`` function to produce plain text (try removing the function
call to see what happens).

To test the new version of the system, edit the data in your front
page to include a WikiWord. When the page is displayed, you'll see
that it's now a link.  You probably won't be surprised to find that
clicking that link produces an error.


Hey, Where's The Page?
======================

What if a Wiki page doesn't exist? We'll take a simple approach: if
the page doesn't exist, you get an edit page to use to create it.

In the ``_default`` method, we'll check to see if the page exists. If
it doesn't, we'll redirect to a new ``notfound`` method. We'll add
this method after the ``_default`` method and before the ``edit``
method. Here are the changes we make to the controller:

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: 2f70ae5753f91724424858e07bcd612c9b696a97

The ``_default`` code changes illustrate the "better to beg forgiveness
than ask permission" pattern which is favored by most Pythonistas --
we first try to get the page and then deal with the exception by
redirecting to a method that will make a new page.

We're also leaking a bit of our model into our controller. For a
larger project, we might create a facade in the model, but here we'll
favor simplicity. Notice that we can use the ``redirect()`` to pass
parameters into the destination method.

As for the ``notfound`` method, the first two lines of the method add
a row to the page table. From there, the path is exactly the same it
would be for our ``edit`` method.

With these changes in place, we have a fully functional wiki. Give it
a try!  You should be able to create new pages now.


Adding A Page List
==================

Most wikis have a feature that lets you view an index of the pages. To
add one, we'll start with a new template, `pagelist.html`. We'll copy
`page.html` so that we don't have to write the boilerplate.

.. code-block:: bash

    cd wiki20/templates
    cp page.html pagelist.html

After editing, our `pagelist.html` looks like:

.. code:: Wiki-20/wiki20/templates/pagelist.html
   :revision: 9e9b683642740bc6fc1dfcc45f535829c7881705
   :language: html

The section in bold represents the Genshi code of interest. You can
guess that the ``py:for`` is a python ``for`` loop, modified to fit
into Genshi's XML. It iterates through each of the ``pages`` (which
we'll send in via the controller, using a modification you'll see
next). For each one, ``Page Name Here`` is replaced by ``pagename``,
as is the URL. You can learn more about the `Genshi templating
engine`_ at their site.


We must also modify the controller to implement ``pagelist`` and to
create and pass ``pages`` to our template:

.. code:: Wiki-20/wiki20/controllers/root.py
   :revision: 9e9b683642740bc6fc1dfcc45f535829c7881705
   :language: python

Here, we select all of the ``Page`` objects from the database, and
order them by pagename.

We can also modify `page.html` so that the link to the page list is
available on every page:

.. code:: Wiki-20/wiki20/templates/page.html
   :revision: 9e9b683642740bc6fc1dfcc45f535829c7881705
   :language: html

You can see your pagelist by clicking the link on a page or by going
directly to http://localhost:8080/pagelist .


Further Exploration
===================

Now that you have a working Wiki, there are a number of further places
to explore:

#. You can add JSON support via jQuery

#. You can learn more about the `Genshi templating engine`_.

#. You can learn more about the `SQLAlchemy ORM`_.

.. todo:: Add link to help show how to add jQuery support

If you had any problems with this tutorial, or have ideas on how to
make it better, please let us know on the `mailing list`_! Suggestions
are almost always incorporated.


.. _`mailing list`: http://groups.google.com/group/turbogears
.. _`Genshi templating engine`: http://genshi.edgewall.org/wiki/Documentation/templates.html
.. _`SQLAlchemy ORM`: http://www.sqlalchemy.org/
.. _`wiki code`: ../_static/wiki20.zip
.. _TurboGears discussion list: http://groups.google.com/group/turbogears
.. _Python: http://www.python.org/download/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _ipython shell: http://ipython.scipy.org/
.. _ipython docs: http://ipython.scipy.org/moin/Documentation
.. _Python Documentation: http://www.python.org/doc
.. _SQLite: http://www.sqlite.org/
.. _Model-View-Controller paradigm: http://en.wikipedia.org/wiki/Model-view-controller
.. _plugins available: http://www.turbogears.org/cogbin/
.. _Genshi: http://genshi.edgewall.org/wiki/Documentation/xml-templates.html
