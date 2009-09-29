.. _movie-tutorial:

A Movie Database (Models, Views, Controllers)
=============================================

This tutorial introduces:

 * how to define data-models in TurboGears using SQLAlchemy
 * how to interact with your data-models from Python code (controllers)
 * how to modify HTML (Genshi) template views 
 * how to use automatically generated forms to allow users to update your models
 
We will assume you are familiar with the following:

 * The `Model-View-Controller`_ abstraction
 * Basic operations of Relational Databases
 * Basic HTML, CSS and Python
 
.. _Model-View-Controller: http://en.wikipedia.org/wiki/Model-view-controller

You will want to follow along with this tutorial within a TurboGears virtualenv.
On a Linux machine with virtualenv already installed, this is accomplished with::

    virtualenv --no-site-packages movies 
    cd movies
    source bin/activate 
    easy_install tg.devtools

Complete instructions for setting up TurboGears, VirtualEnv and the like 
are available on the :ref:`Download and Install <DownloadInstall>` page.

Getting Started
---------------

We will use the TurboGears "quickstart" command, which will create a generic 
TurboGears project which we can proceed to edit::
  
    paster quickstart movies

We will want to accept most of the defaults.  We will want to have authentication 
in this project, so answer yes when asked about that.

SQLAlchemy Models
-----------------

SQLAlchemy is the default storage layer used by TurboGears 2.0 and above.
SQLAlchemy is a powerful database abstraction layer that lets you begin your 
project using a simple "declarative" form that looks much like other ORMs, 
but allows you to access a more general and powerful abstraction of "Mapper" 
should you need that functionality in the future.
  
If you browse into the new "movies" directory, you will find a sub-directory 
also named "movies".  This directory is your importable package, and within 
it you will find a number of sub-packages, including one named "model".  We 
are going to create our application's data-model here.

We'll create a new file "movie.py" in our "model" directory with this content::

    from sqlalchemy import *
    from sqlalchemy.orm import mapper, relation, backref
    from sqlalchemy.types import Integer, Unicode, Boolean

    from movies.model import DeclarativeBase, metadata, DBSession
    
    __all__ = [ 'Movie' ]

    class Movie(DeclarativeBase):

        __tablename__ = 'movie'

        id = Column(Integer, primary_key=True)
        title = Column(Unicode, nullable=False)
        description = Column(Unicode, nullable=True)
        year = Column(Integer, nullable=True)
        genre_id = Column(Integer,ForeignKey('genre.id'), nullable=True)
        genre = relation('Genre',foreign_keys=genre_id )
        reviewed = Column(Boolean, nullable=False, default=False )
        def __repr__(self):
            return "<Movie('%s','%s', '%s')>" % (
                self.title, self.year, self.description
            )
    class Genre(DeclarativeBase):
        __tablename__ = 'genre'
        id = Column(Integer,primary_key=True)
        title = Column(Unicode,nullable=False,unique=True)

There's a lot going on here, so let's break it down a bit.  The first few 
imports are giving us access to functionality from the SQLAlchemy package.
The sqlalchemy.orm import is letting us access the "declarative" ORM 
mechanisms in SQLAlchemy, while the other two imports are from the generic 
interfaces.

The line::

    from movies.model import DeclarativeBase, metadata, DBSession

is more interesting.  We are actually importing fixtures here from the 
__init__.py module in the same directory as the file we are creating.
These objects are effectively "globals" which all of our application 
code will use to access the database connections, structures etceteras.

One thing to note for your own code: you should never name your 
model modules the same name as your top-level modules ("movies" in our 
case), as the import here would fail as it got confused as to from where to 
import the fixtures.

The DeclarativeBase class is an ORM mechanism from SQLAlchemy which 
allows for declaring tables and their ORM mappers via a simple class 
definition.  Lower-level and more advanced SQLAlchemy usage also allows 
for separately defined tables and mappers.

Now we'll make "Movie" available directly in the movies.model namespace by 
importing it in the model/__init__.py module.  We do this at the bottom of 
the module so that the DBSession, DeclarativeBase and the similar instances 
are already available when we do the import::

    from movies.model.movie import *

And that's it.  We can now setup our app and then run the following paster 
command (from the directory where development.ini is, the level below 
our virtualenv directory)::

    python setup.py develop
    paster setup-app development.ini 

which by default would create an SQLite file in the local directory which 
would have a "model" table.

Types
-----

SQLAlchemy provides a number of built-in types which it automatically maps to
underlying database types.  If you want the latest and greatest listing just
type:

.. code-block: python

  >>> from sqlalchemy import types
  >>> dir(types)

The main types are:

================ ========
 type            value    
================ ========
 types.Binary    binary   
 types.Boolean   boolean  
 types.Integer   integer  
 types.Numeric   number   
 types.String    string   
 types.Unicode   unicode
 types.Date      date     
 types.Time      time     
 types.DateTime  datetime 
================ ========

There are also properties that apply to all column objects, which you
might want to set up front.

Properties
----------

============  ==========
 property     value      
============  ==========
 primary_key  True/False 
 nullable     True/False 
 unique       True/False 
 index        True/False
============  ==========

Pretty much these do exactly what you would expect them to do, set a field to
be a primary key or set it to accept null values, unique, indexed, etceteras.
By default fields are none of the above.

Working with the Model
----------------------

We can interact with our model directly from the Python interpreter 
by starting up a paster shell::

    paster shell development.ini 

where we can now import our model::

    >>> from movies.model import *
    >>> import transaction
    >>> drac = Movie( title = 'Dracula', year=1931, description = 'Vampire Movie' )
    >>> print drac
    >>> DBSession.add( drac )
    >>> transaction.commit( )

when running inside TurboGears request handlers, the call to 
transaction.commit is normally handled by middleware which commits 
if a method returns "normally" (including redirects) and rolls 
back if the method raises an uncaught exception.

Aside: If you are an old SQLAlchemy hand, you may be wondering what 
"transaction.commit()" is, as in SQLAlchemy you would normally use 
DBSession.commit() to commit your current transaction.  TurboGears 2.x
uses a middleware component ``repoze.tm`` which allows for multi-database 
commits.  A side-effect of this usage is that use of DBSession.commit() 
is no longer possible.

Browse/Edit with Admin GUI
--------------------------

Your quickstart project will have installed an optional administrative 
GUI (named Catwalk).  This interface can be enhanced with the dojo 
javascript library to give it more useful controls::

    easy_install tw.dojo 

You can start TurboGears' development web server and browse to the 
admin page here:

    http://localhost:8080/admin 

You can customize the administrative GUI considerably as discussed 
in :ref:`tgext-admin`.

Working with the Model in a Controller
--------------------------------------

With our administrative GUI, we could create some Movie and Genre records,
set up some Users to manage permissions and the like, but none of that 
would ever be visible to the user.  We're going to define a simple view 
on the home-page of our site that shows the set of Movies we've defined 
in a simple HTML table.

The site's "index" page is generated by the "exposed" index method on 
the "root" controller.  This is defined in the file::

    movies/movies/controllers/root.py 

in our quick-started application.  We're going to alter this index method 
to load a collection of our SQLAlchemy-generated Movie records and provide 
them to be rendered by the index template.

To make the various parts of the model available, we'll add the following 
to the imports of the root.py module::

    from movies.model import *

which gives us access to DBSession, Movie and Genre.  We then alter our 
index method to look like this::

    @expose('movies.templates.index')
    def index(self):
        """Handle the front-page."""
        movies = DBSession.query( Movie ).order_by( Movie.title )
        return dict(
            page='index',
            movies = movies,
        )

SQLAlchemy query operations are an involved subject (see the 
`SQLAlchemy Object Relational Tutorial`_ for an in-depth exploration of it.  
Here we are querying all Movie instances and sorting them by their ``title``
field.                                                         

We could actually run our application now, and other than a tiny slowdown 
of the front-page load, we would not be able to see any change in the 
application.  The controller has provided information, but we need to alter 
the view to make that information visible.

Altering a View
---------------

To make our collection of Movies visible, we are going to change the index 
template for our application.  The ``expose`` decorator on the index method 
gives the dotted-format module name of the (Genshi) template which is going 
to be used to render the page.  Here it is movies.templates.index, so we 
will open the file movies/movies/templates/index.html to edit it.

We are going to replace most of this file, so here we show the entire file,
rather than just the edits we would make to it:

.. code-block:: html

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
                          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:py="http://genshi.edgewall.org/"
          xmlns:xi="http://www.w3.org/2001/XInclude">

      <xi:include href="master.html" />

    <head>
      <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
      <title>Movie-base Tutorial</title>
    </head>

    <body>
      <div id="movie-index">
        <h2>Movie-base Tutorial</h2>
        <table class="movie-listing">
            <thead>
                <tr><th>Title</th><th>Year</th><th>Genre</th><th>Description</th></tr>
            </thead>
            <tbody>
                <tr py:for="movie in movies">
                    <th class="movie-title">${movie.title}</th>
                    <td class="movie-year">${movie.year}</td>
                    <td class="genre-title"><span py:if="movie.genre" py:strip="">${movie.genre.title}</span></td>
                    <td class="movie-description">${movie.description}</td>
                </tr>
            </tbody>
        </table>
      </div>
      <div class="clearingdiv" />
    </body>
    </html>

Genshi is an ``attribute language`` system which requires rigorous XML correctness.
If you leave off a closing-tag or forget to put quotes around an attribute value 
you will get Genshi templating errors.  Luckily Genshi tends to be relatively good 
at pointing out where the error is, though occasionally you'll have to think a bit 
to figure out which particular tag isn't closed, for instance.

TurboGears actually supports a number of templating languages, including :ref:`Genshi <genshi>`, :ref:`Jinja <jinja>` and :ref:`Mako <mako>`. 
The differences between them tend to be subtle enough that new users don't
generally need to worry about choosing an alternate templating system.

Aside: Adding some Style
------------------------

You may have noticed that our view/template set a lot of "class" and "id"
values.  This is to make it easy to select the various components from within 
CSS stylesheets.  Your quick-started project already includes a CSS stylesheet 
in the master.html template.  The template included is in:

    movies/movies/public/css/style.css

we can open this file and add the following CSS directives to have our 
table of movies be a little easier to read::

    #movie-index .movie-listing {
        width: 100%;
        background-color: lightgray;
    }
    #movie-index .movie-listing tr {
        background-color: white;
    }

CSS takes a significant amount of work to master, particularly with regard to 
the intricacies of legacy browser support.  We'll assume you will learn CSS 
yourself and leave it as showing you where to put the results of your learning.

Automatic Forms for User Interaction (Sprox)
--------------------------------------------

As you might have guessed by the Admin UI, TurboGears is able to ``introspect``
your database model in order to provide common ``CRUD`` (Create, Update, Destroy)
forms.  We'll use this capability, which is provided by the `Sprox`_ library
to create a simple form our users can use to add new movies to our database::

    from sprox.formbase import AddRecordForm
    from tg import tmpl_context
    class AddMovie(AddRecordForm):
        __model__ = Movie
    add_movie_form = AddMovie(DBSession)
    
we can then pass this form to our template in the ``index`` method of 
our root controller::

    @expose('movies.templates.index')
    def index(self, **named):
        """Handle the front-page."""
        movies = DBSession.query( Movie ).order_by( Movie.title )
        tmpl_context.add_movie_form = add_movie_form
        return dict(
            page='index',
            movies = movies,
        )

Why are we using ``tmpl_context``?  Why don't we just pass our 
widget into the template as a parameter?  The reason is is that 
TurboGears controllers often do double duty as both web-page 
renderers and JSON handlers.  By putting "view-specific" code 
into the tmpl_context and "model-data" into the result dictionary,
we can more readily support the JSON queries.

The tmpl_context
        
Now we call our widget from within our ``index`` template:

.. code-block:: html

    <h2>New Movie</h2>
    ${tmpl_context.add_movie_form( action='add_movie') }

we pass an ``action`` parameter to the form to tell it what controller method 
(url) it should use to process the results of submitting the form.  We'll create 
the controller on our root controller::

    @expose( )
    @validate( 
        form=add_movie_form,
        error_handler=index,
    )
    def add_movie( self, title, description, year, genre, **named ):
        """Create a new movie record"""
        new = Movie(
            title = title,
            description = description,
            year = year,
            reviewed = False,
            genre_id = genre,
        )
        DBSession.add( new )
        flash( '''Added movie: %s'''%( title, ))
        redirect( './index' )

We do not use a template in our ``expose`` call here, as we are not going 
to return an HTML page from this method.  The ``validate`` decorator uses 
the Sprox widget/form's automatically generated validator to convert the 
incoming form values into Python objects and check for required fields.
If there are errors, the error_handler controller method will be called.
In this case, as is common, we use the same view which presented the 
problematic form, as most widgets (including Sprox' widgets) are designed 
to display error messages when errors occur.

Note the use of DBSession.add() on the new instance.  Without this, the 
record would not be registered with the transactional machinery, and would 
simply disappear when the request completed.

Customizing the Sprox Form
--------------------------

At this point we can view our site and see the movie-adding form just 
below the list of Movies.  We can enter new values in the form and we will 
create new Movie records.  However, the form is not particularly elegant 
looking, as the use of "Unicode" values (without size limits) for the 
title has convinced Sprox to use ungainly TextArea control instead of more 
compact TextField controls.  We also have a number of extraneous controls 
for ids, and the "reviewed" flag is visible to the user.

To clean the form up somewhat, we will refine the set of fields in the form
by omitting the unwanted fields and declaring the widget-type to use for the 
title field.  The resulting add_movie_form looks like this::

    from sprox.formbase import AddRecordForm
    from tw.forms import TextField,CalendarDatePicker
    class AddMovie(AddRecordForm):
        __model__ = Movie
        __omit_fields__ = [
            'id', 'genre_id', 'reviewed'
        ]
        title = TextField
    add_movie_form = AddMovie(DBSession)

Last but not least, we alter our index page to no longer display any movies 
which have not yet been reviewed by our admins (using the admin controller),
which is done by adding a ``filter`` clause to the SQLAlchemy query::

    movies = DBSession.query( Movie ).filter(
        Movie.reviewed == True
    ).order_by( Movie.title )

`Sprox`_ allows you to rapidly prototype applications under TurboGears, and
provides considerable customization (documented on their web-site).  
As you refine your application you may replace many of the 
Sprox-provided forms with custom forms created using the underlying 
``ToscaWidgets`` framework, or potentially even forms directly coded 
into your templates.  The automatically generated forms can save you 
a significant amount of time until you get there.

.. _`Sprox`: http://www.sprox.org

Next Steps
----------

 * `SQLAlchemy Object Relational Tutorial`_ -- learn how to use SQLAlchemy effectively to model your applications
 * :ref:`simple-widget-form` -- learn how to use ToscaWidgets to create custom forms
 * :ref:`Genshi <genshi>` -- learn the default templating language for views
 * :ref:`tgext.crud.controller` -- learn how to automate CRUD-style editing even more
 * :ref:`tgext-admin` -- learn how to customize the admin UI

References
---------------------

 * `SQLAlchemy Documentation`_:
 
   * `Object Relational Mapper`_
   * `SQLAlchemy Expressions`_

 * `Sprox`_ Website -- includes customization tutorials
   
 * The zope.sqlalchemy transaction module
 
.. _`SQLAlchemy Documentation`: http://www.sqlalchemy.org/docs/05/
.. _`Object Relational Mapper`: http://www.sqlalchemy.org/docs/05/ormtutorial.html
.. _`SQLAlchemy Expressions`: http://www.sqlalchemy.org/docs/05/sqlexpression.html
.. _`SQLAlchemy Object Relational Tutorial`: http://www.sqlalchemy.org/docs/05/ormtutorial.html
