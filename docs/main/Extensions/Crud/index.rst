.. _tgext.crud.controller:


TurboGears Automatic CRUD Generation
=====================================

Overview
--------

This is a simple extension that provides a basic controller class that
can be extended to meet the needs of the developer.  The intention is
to provide a fast path to data management by allowing the user to
define forms and override the data interaction with custom
manipulations once the view logic is in place.  The name of this
extensible class is CrudRestController.

What is CRUD?
~~~~~~~~~~~~~

CRUD is a set of functions to manipulate the data in a database:
create, read, update, delete.

Um, REST?
~~~~~~~~~

REST is a methodology for mapping resource manipulation to meaningful
URL.  For instance if we wanted to edit a user with the ID 3, the URL
might look like: /users/3/edit.  For a brief discussion on REST, take
a look at `the microformats entry
<http://microformats.org/wiki/rest/urls>`_.

Before We Get Started
---------------------

Here is the model definition we will be using for this tutorial::

    from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
    from sqlalchemy.orm import relation
    
    from moviedemo.model import DeclarativeBase
    
    class Genre(DeclarativeBase):
        __tablename__ = "genres"
        genre_id = Column(Integer, primary_key=True)
        name = Column(String(100))
    
    class Movie(DeclarativeBase):
        __tablename__ = "movies"
        movie_id = Column(Integer, primary_key=True)
        title = Column(String(100), nullable=False)
        description = Column(Text, nullable=True)
        genre_id = Column(Integer, ForeignKey('genres.genre_id'))
        genre = relation('Genre', backref='movies')
        release_date = Column(Date, nullable=True)

Putting The CRUD Into REST
--------------------------

EasyCrudRestController
~~~~~~~~~~~~~~~~~~~~~~~~~

The first thing we want to do is instantiate a ``EasyCrudRestController``.
We import the controller from the extension, and then provide it with a
model class that it will use for its data manipulation.  For this
example we will utilize the Movie class.::

    from tgext.crud import EasyCrudRestController
    from moviedemo.model import DBSession, Movie

    class MovieController(EasyCrudRestController):
        model = Movie
    
    class RootController(BaseController):
        movies = MovieController(DBSession)

That will provide a simple and working CRUD controller already configured
with some simple views to list, create, edit and delete objects of
type Movie.

Customizing EasyCrudRestController
+++++++++++++++++++++++++++++++++++++

The ``EasyCrudRestController`` provides some quick customization tools.
Having been thought to quickly prototype parts of your web applications
the EasyCrudRestController permits both to tune forms options and to
add utility methods on the fly::

    class TicketCrudController(EasyCrudRestController):
        model = Ticket

        __form_options__ = {
            '__hide_fields__':['_id', 'status', 'sprint'],
            '__field_order__':['title', 'description'],
            '__field_widget_types__':{'description':TextArea}
        }

        __table_options__ = { # see Sprox TableBase and Sprox TableFiller
            '__limit_fields__': ['title', 'desc'],
            '__add_fields__': {'computed': None},
            'computed': lambda filler, row: row.some_field * 2
        }

        __setters__ = {
                'done':('status', 'done'),
                'todo':('status', 'new'),
                'revert':('sprint', lambda ticket:ticket.sprint.project.backlog),
                'sprint':('sprint', lambda ticket:ticket.sprint.project.last_sprint),
        }

The ``__form_options__`` dictionary will permit to tune the forms configuration.
The specified options will be applied to both the form used to create new entities
and to edit the existing ones.
To have a look at the available options refer to
`Sprox FormBase <http://sprox.org/modules/sprox.formbase.html#module-sprox.formbase>`_

The ``__table_options__`` dictionary will permit to tune the forms configuration.
To have a look at the available options refer to
`Sprox TableBase <http://sprox.org/modules/sprox.tablebase.html#sprox.tablebase.TableBase>`_,
`Sprox TableFiller <http://sprox.org/modules/sprox.fillerbase.html?highlight=tablefiller#sprox.fillerbase.TableFiller>`_,
and their parents as well.

The ``__setters__`` option provides a way to add new simple methods on the fly
to the controller. The key of the provided dictionary is the name of the method, while
the value is a tuple where the first argument is the attribute of the object
that has to be changed. The second argument is the value that has to be set, if the
second argument is a callable it will be called passing the object to edit as the
argument.

In the previous example calling http://localhost:8080/tickets/5/done will set the
ticket 5 status to done.

Creating our own CrudRestController
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``EasyCrudRestController`` provides a preconfigured ``CrudRestController``
but often you will need to deeply customize it for your needs. To do that
we can start over with a clean controller and start customizing it::

    from tgext.crud import CrudRestController
    from moviedemo.model import DBSession, Movie

    class MovieController(CrudRestController):
        model = Movie
    
    class RootController(BaseController):
        movies = MovieController(DBSession)

Well that won't actually get you anywhere, in fact, it will do nothing
at all.  We need to provide CrudRestController with a set of widgets
and datafillers so that it knows how to handle your REST requests.
First, lets get all of the Movies to display in a table.

Sprox
~~~~~

`Sprox <http://sprox.org>`_ is a library that can help you to generate
forms and filler data.  It utilizes metadata extracted from the
database definitions to provide things like form fields, drop downs,
and column header data for view widgets.  Sprox is also customizable,
so we can go in and modify the way we want our data displayed once we
get going with it.  Here we define a table widget using Sprox's
:class:`sprox.tablebase.TableBase` class for our movie table.::

    from sprox.tablebase import TableBase
    
    class MovieTable(TableBase):
        __model__ = Movie
        __omit_fields__ = ['genre_id']
    movie_table = MovieTable(DBSession)

Filling Our Table With Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

So, now we have our movie_table, but it's not going to do us much good
without data to fill it.  Sprox provides a
:class:`sprox.fillerbase.TableFiller` class which will retrieve the
relevant data from the database and package it in a dictionary for
consumption.  This is useful if you are creating JSON_.  Basically,
you can provide CrudRestController with any object that has a
get_value function and it will work because of duck typing.  Just make
certain that your get_value function returns the right data type for
the widget you are filling.  Here is what the filler would look like
instantiated.::

    from sprox.fillerbase import TableFiller

    class MovieTableFiller(TableFiller):
        __model__ = Movie
    movie_table_filler = MovieTableFiller(DBSession)

We add movie_id to the limited fields so that the "__actions__" field
can provide proper links to this primary key.

Putting It All Together
~~~~~~~~~~~~~~~~~~~~~~~

Let's modify our CrudRestController to utilize our new table.  The new
RootController would look like this::

    from tgext.crud import CrudRestController
    from moviedemo.model import DBSession, Movie
    from sprox.tablebase import TableBase
    from sprox.fillerbase import TableFiller
    
    class MovieTable(TableBase):
        __model__ = Movie
    movie_table = MovieTable(DBSession)

    class MovieTableFiller(TableFiller):
        __model__ = Movie
    movie_table_filler = MovieTableFiller(DBSession)
    
    class MovieController(CrudRestController):
        model = Movie
        table = movie_table
        table_filler = movie_table_filler
    
    class RootController(BaseController):
        movie = MovieController(DBSession)

You can now visit /movies/ and it will display a list of movies.

.. image:: images/table.png


Forms
-----

One of the nice thing about Sprox table definitions is that they
provide you with a set of RESTful links.  CrudRestController provides
methods for these pages, but you must provide the widgets for the
forms.  Specifically, we are talking about the edit and new forms.
Here is one way you might create a form to add a new record to the
database using :class:`sprox.formbase.AddRecordForm`::

    class MovieAddForm(AddRecordForm):
        __model__ = Movie
        __omit_fields__ = ['genre_id', 'movie_id']
    movie_add_form = MovieAddForm(DBSession)

Adding this to your movie controller would look make it now look
something like this::

    class MovieController(CrudRestController):
        model = Movie
        table = movie_table
        table_filler = movie_table_filler
        new_form = movie_add_form

You can now visit /movies/new and get a page that looks like this.

.. image:: images/new_form.png

Edit Form
~~~~~~~~~

Now we just need to map a form to the edit function so that we can
close the loop on our controller.  The reason we need separate forms
for Add and Edit is due to validation.  Sprox will check the database
for uniqueness on a "new" form.  On an edit form, this is not required
since we are updating, not creating.::

    from sprox.formbase import EditableForm
    
    class MovieEditForm(EditableForm):
        __model__ = Movie
        __omit_fields__ = ['genre_id', 'movie_id']
    movie_edit_form = MovieEditForm(DBSession)
    


The biggest difference between this form and that of the "new" form is
that we have to get data from the database to fill in the form.  Here
is how we use :class:`sprox.formbase.EditFormFiller` to do that::

    from sprox.fillerbase import EditFormFiller
    
    class MovieEditFiller(EditFormFiller):
        __model__ = Movie
    movie_edit_filler = MovieEditFiller(DBSession)

Now it is a simple as adding our filler and form definitions to the
``MovieController`` and close the loop on our presentation.  Here is
what the form looks like when we go to edit it.

.. image:: images/edit_form.png


Declarative
-----------

If you are interested in brevity, the crud controller may be created
in a more declarative manner like this::

    from tgext.crud import CrudRestController
    from sprox.tablebase import TableBase
    from sprox.formbase import EditableForm, AddRecordForm
    from sprox.fillerbase import TableFiller, EditFormFiller
        
    class DeclarativeMovieController(CrudRestController):
        model = Movie
        
        class new_form_type(AddRecordForm):
            __model__ = Movie
            __omit_fields__ = ['genre_id', 'movie_id']
    
        class edit_form_type(EditableForm):
            __model__ = Movie
            __omit_fields__ = ['genre_id', 'movie_id']
    
        class edit_filler_type(EditFormFiller):
            __model__ = Movie
    
        class table_type(TableBase):
            __model__ = Movie
            __omit_fields__ = ['genre_id', 'movie_id']
    
        class table_filler_type(TableFiller):
            __model__ = Movie

Crud Operations
---------------

We have really been focusing on the View portion of our controller.
This is because CrudRestController performs all of the applicable
creates, updates, and deletes on your target object for you.  This
default functionality is provided by
:class:`sprox.saormprovider.SAORMProvider`.  This can of course be
overridden.


Overriding Crud Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

CrudRestController extends RestController, which means that any
methods available through RestController are also available to CRC.

+-----------------+----------------------------------------------------------+--------------------------------------------+
| Method          | Description                                              | Example Method(s) / URL(s)                 |
+=================+==========================================================+============================================+
| get_all         | Display the table widget and its data                    | GET /movies/                               |
+-----------------+----------------------------------------------------------+--------------------------------------------+
| new             | Display new_form                                         | GET /movies/new                            |
+-----------------+----------------------------------------------------------+--------------------------------------------+
| edit            | Display edit_form and the containing record's data       | GET /movies/1/edit                         |
+-----------------+----------------------------------------------------------+--------------------------------------------+
| post            | Create a new record                                      | POST /movies/                              |
+-----------------+----------------------------------------------------------+--------------------------------------------+
| put             | Update an existing record                                | POST /movies/1?_method=PUT                 |
|                 |                                                          +--------------------------------------------+
|                 |                                                          | PUT /movies/1                              |
+-----------------+----------------------------------------------------------+--------------------------------------------+
| post_delete     | Delete an existing record                                | POST /movies/1?_method=DELETE              |
|                 |                                                          +--------------------------------------------+
|                 |                                                          | DELETE /movies/1                           |
+-----------------+----------------------------------------------------------+--------------------------------------------+
| get_delete      | Delete Confirmation page                                 | Get  /movies/1/delete                      |
+-----------------+----------------------------------------------------------+--------------------------------------------+

If you are familiar with RestController you may notice that get_one is
missing.  There are plans to add this functionality in the near
future.  Also, you may note the ?_method on some of the URLs.  This is
basically a hack because existing browsers do not support the PUT and
DELETE methods.  Just note that if you decide to incorporate a TW in
your edit_form description you must provide a
``HiddenField('_method')`` in the definition.

Adding Functionality
~~~~~~~~~~~~~~~~~~~~

REST provides consistency across Controller classes and makes it easy
to override the functionality of a given RESTful method.  For
instance, you may want to get an email any time someone adds a movie.
Here is what your new controller code would look like::

    class MovieController(CrudRestController):

        # (...)

        @expose(inherit=True)
        def post(self, **kw):
            email_info()
            return super(MovieController, self).post(**kw)

You might notice that the function has the @expose decorator.  This is
required because the expose decoration occurs at the class-level, so
that means that when you override the class method, the expose is
eliminated.  We add it back to the method by adding @expose with the
``inherit`` parameter to inherit the behavior from the parent method.

For more details you can refer to the
:ref:`TGController Subclassing <tgcontrollers-subclassing>` documentation.

Overriding Templates
~~~~~~~~~~~~~~~~~~~~

To override the template for a given method, you would simple
re-define that method, providing an expose to your own template, while
simply returning the value of the super class's method.::

    class MovieController(CrudRestController):

        # (...)

        @expose('movie_demo.templates.my_get_all_template', inherit=True)
        def get_all(self, *args, **kw):
            return super(MovieController, self).get_all(*args, **kw)
            
Removing Functionality
~~~~~~~~~~~~~~~~~~~~~~

You can also block-out capabilities of the RestController you do not
wish implemented.  Simply define the function that you want to block,
but do not expose it. Here is how we "delete" the delete
functionality.::

    class MovieController(CrudRestController):
    
        # (...)
        
        def post_delete(self, *args, **kw):
            """This is not allowed."""
            pass

Menu Items
----------

The default templates for :mod:`tgext.crud` make it very easy to add a
menu with links to other resources.  Simply provide a dictionary of
names and their representing model classes and it will display these
links on the left hand side.  Here is how you would provide links for
your entire model.::
        
    import inspect
    from sqlalchemy.orm import class_mapper
    
    models = {}
    for m in dir(model):
        m = getattr(model, m)
        if not inspect.isclass(m):
            continue
        try:
            mapper = class_mapper(m)
            models[m.__name__.lower()] = m
        except:
            pass
    
    class RootController(BaseController):
        movie = MovieController(DBSession, menu_items=models)

Which results in a new listing page like this.

.. image:: images/menu_items.png


CRC: The Sweet Spot
-------------------

CrudRestController represents sort of a sweet-spot with respect to
functionality.  It doesn't do everything for you, but it can save you
a bunch of work, especially when you are prototyping an application.
If you need more flexibility, you should take a look at
RestController, which provides no form/crud functionality.  If you are
really looking for something that makes all of the forms for you, but
can be configured, take a look at the `Turbogears Admin System
<http://pypi.python.org/pypi/tgext.admin>`_.

.. _JSON: http://www.json.org/
.. _AJAX: http://en.wikipedia.org/wiki/Ajax_%28programming%29
