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
are available on the :ref:`Download and Install <downloadinstall>` page.

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

Browse/Edit with Admin GUI
--------------------------

Your quickstart project will have installed an optional administrative 
GUI (named Catwalk).  This interface can be enhanced with the dojo 
javascript library to give it more useful controls::

    easy_install tw.dojo 

You can start TurboGears' development web server and browse to the 
admin page here:

    http://localhost:8080/admin 

You can customize the administrative GUI considerably.

Reference
---------

 * `SQLAlchemy Object Relational Tutorial <http://www.sqlalchemy.org/docs/04/ormtutorial.html>`_
 * Catwalk/Admin GUI Tutorial (.. todo:: cross-reference)
 * The transaction module (.. todo:: documentation)

.. todo:: cross-reference Catwalk/Admin GUI Tutorial

.. todo:: documentation of transaction module

Next Steps
----------

 * Controllers
 * Views (Forms) (ToscaWidgets .. todo:: cross-reference)

.. todo:: cross-reference views with ToscaWidgets
