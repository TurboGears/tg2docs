SQLAlchemy Models (Creating a Movie Database)
=============================================

This tutorial introduces the use of the SQLAlchemy Object Relational Mapper (ORM).
SQLAlchemy is a powerful database abstraction layer that lets you start off 
with a simple "declarative" form that looks much like other ORMs, but allows 
you to access a more general and powerful abstraction of "Mapper" should 
you need that functionality in the future.

We will assume you are familiar with the following:

 * The `Model-View-Controller`_ abstraction

 * Basic operations of Relational Databases
 
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
  
If you browse into the new "movies" directory, you will find a sub-directory 
also named "movies".  This directory is your importable package, and within 
it you will find a number of sub-packages, including one named "model".  We 
are going to create our application's data-model here.

We'll create a new file "movie.py" in our "model" directory with this content::

    from sqlalchemy import *
    from sqlalchemy.orm import mapper, relation, backref
    from sqlalchemy.types import Integer, Unicode

    from movies.model import DeclarativeBase, metadata, DBSession
    
    __all__ = [ 'Movie' ]

    class Movie(DeclarativeBase):

        __tablename__ = 'movie'

        id = Column(Integer, primary_key=True)
        title = Column(Unicode, nullable=False)
        description = Column(Unicode, nullable=True)
        year = Column(Integer, nullable=True)
        release_date = Column(Date, nullable=True)
        genre_id = Column(Integer,ForeignKey('genre.id'), nullable=True)
        genre = relation('Genre',foreign_keys=genre_id )
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

SQLAlchemy References
---------------------

 * `SQLAlchemy Documentation`_:
 
   * `Object Relational Mapper`_
   * `SQLAlchemy Expressions`_
   
 * The zope.sqlalchemy transaction module (TODO: documentation)

.. _`SQLAlchemy Documentation`: http://www.sqlalchemy.org/docs/05/
.. _`Object Relational Mapper`: http://www.sqlalchemy.org/docs/05/ormtutorial.html
.. _`SQLAlchemy Expressions`: http://www.sqlalchemy.org/docs/05/sqlexpression.html

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

which gives us access to DBSession, Model and Genre.  We then alter our 
index method to look like this::

    @expose('movies.templates.index')
    def index(self):
        """Handle the front-page."""
        movies = DBSession.query( Movie ).order_by( Movie.title )
        return dict(
            page='index',
            movies = movies,
        )

SQLAlchemy query operations are an involved subject (see the References 
for the SQLAlchemy ORM tutorial for an in-depth exploration of it.  Here 
we are querying all Movie instances and sorting them by their 
"title" field.

We could actually run our application now, and other than a tiny slowdown 
of the front-page load, we would not be able to see any change in the 
application.  The controller has provided information, but we need to alter 
the view to make that information visible.

Altering a View
---------------

To make our collection of Movies visible, we are going to change the index 
template for our application.  The "expose" decorator on the index method 
gives the dotted-format module name of the (Genshi) template which is going 
to be used to render the page.  Here it is movies.templates.index, so we 
will open the file movies/movies/templates/index.html to edit it.

We are going to replace most of this file, so here we show the entire file,
rather than just the edits we would make to it::

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
                    <td class="genre-title">${movie.genre.title}</td>
                    <td class="movie-description">${movie.description}</td>
                </tr>
            </tbody>
        </table>
      </div>
      <div class="clearingdiv" />
    </body>
    </html>

Genshi is an "attribute language" system which requires rigorous XML correctness.
If you leave off a closing-tag or forget to put quotes around an attribute value 
you will get Genshi templating errors.  Luckily Genshi tends to be relatively good 
at pointing out where the error is, though occasionally you'll have to think a bit 
to figure out which particular tag isn't closed, for instance.

:ref:`genshi`

TurboGears actually supports a number of other templating languages, including 
:ref:`kid` and :ref:`mako`.  The differences between them tend to be subtle 
enough that new users don't generally need to worry about choosing an alternate
templating system.

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

Next Steps
----------

 * :ref:`form-basics` -- overview of how to create/handle forms 
 * :ref:`writing_controllers` -- explores the process of writing controller methods in depth, including discussions of how to handle not-found pages, how to set up URL hierarchies via object dispatch and the like.
 * :ref:`getting-to-know` -- documents describing TurboGears' approach and mechanics,
    you should read these after you have completed a few tutorials.
