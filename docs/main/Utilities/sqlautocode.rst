.. _sqlautocode:

AutoGenerating Model Code with SQLAutocode
==========================================

:Status: Official

.. contents:: Table of Contents
   :depth: 2


SQLAlchemy is an extremely powerful tool, but unless you
already know how to create table and model code, getting
started can be a bit daunting.  Luckily, sqlautocode was created
to help you get started.  First things first, we need to get
this puppy installed.::

   easy_install sqlutocode
   
We can take a look at the help options in an overview manner:

  $ sqlautocode --help
    Usage: autocode.py <database_url> [options, ]
    Generates Python source code for a given database schema.

    Example: ./autocode.py postgres://user:password@myhost/database -o out.py

    Options:
      -h, --help            show this help message and exit
      -o OUTPUT, --output=OUTPUT
                        Write to file (default is stdout)
      --force               Overwrite Write to file (default is stdout)
      -s SCHEMA, --schema=SCHEMA
                            Optional, reflect a non-default schema
      -t TABLES, --tables=TABLES
                            Optional, only reflect this comma-separated list of
                            tables. Wildcarding with '*' is supported, e.g:
                            --tables account_*,orders,order_items,*_audit
      -b TABLE_PREFIX, --table-prefix=TABLE_PREFIX
                            Prefix for generated SQLAlchemy Table object names
      -a TABLE_SUFFIX, --table-suffix=TABLE_SUFFIX
                            Suffix for generated SQLAlchemy Table object names
      -i, --noindexes, --noindex
                            Do not emit index information
      -g, --generic-types   Emit generic ANSI column types instead of database-
                            specific.
      --encoding=ENCODING   Encoding for output, default utf8
      -e, --example         Generate code with examples how to access data
      -3, --z3c             Generate code for use with z3c.sqlalchemy
      -d, --declarative     Generate declarative SA code
      -n, --interactive     Generate Interactive example in your code.

Well, we won't examine every option here (z3c!?), but it is good to know
what is available before we get started.  Some people prefer to define their
own tables so that they can do custom mappings. Just in case you want to try 
this tutorial out, here is a link to an `sqlite database`_ that you can use.

.. _`sqlite database`: ../../_static/tutorials/sqlautocode/moviedemo.db

Reflecting your database tables
--------------------------------------------------

The first thing we will examine is how one goes about generating table code
for a given database.  This is often preferable when you have sophisticated mappings
that you want to do.

wherever you have saved your database, you can type::

   $ sqlautocode sqlite:///movidemo.db -o tables.py

This will create a tables.py with all of the necessary table definitions.  Here's an excerpt::

    directors =  Table('directors', metadata,
        Column(u'director_id', Integer(), primary_key=1, nullable=False),
                Column(u'name', String(length=100, convert_unicode=False, assert_unicode=None), primary_key=0, nullable=False),
        )
    
    genres =  Table('genres', metadata,
        Column(u'genre_id', Integer(), primary_key=1, nullable=False),
                Column(u'name', String(length=100, convert_unicode=False, assert_unicode=None), primary_key=0),
                Column(u'description', String(length=200, convert_unicode=False, assert_unicode=None), primary_key=0),
        )
    
    movie_directors =  Table('movie_directors', metadata,
        Column(u'movie_id', Integer(), primary_key=1, nullable=False),
                Column(u'director_id', Integer(), primary_key=1, nullable=False),
        ForeignKeyConstraint([u'director_id'], [u'directors.director_id'], name=None),
                ForeignKeyConstraint([u'movie_id'], [u'movies.movie_id'], name=None),
        )
    
    movies =  Table('movies', metadata,
        Column(u'movie_id', Integer(), primary_key=1, nullable=False),
                Column(u'title', String(length=100, convert_unicode=False, assert_unicode=None), primary_key=0, nullable=False),
                Column(u'description', Text(length=None, convert_unicode=False, assert_unicode=None), primary_key=0),
                Column(u'genre_id', Integer(), primary_key=0),
                Column(u'release_date', Date(), primary_key=0),
        ForeignKeyConstraint([u'genre_id'], [u'genres.genre_id'], name=None),
        )

This is a great start if you are already familiar with how SA works, and want to provide your
own model or mappings.  Since the tables are produced in alphabetical order, this is also
affective for reflecting your schema on a regular basis and merging in the changes as your 
database changes if you do not have control over the database schema.  

Reflecting the Database Declaratively
-------------------------------------------------------
Most people getting started with TurboGears or SQLAlchemy for that matter, will probably want
to use the `declarative`_ style of SQLAlchemy model definition.  sqlautocode supports this with the
-d option::

  sqlautocode -d -o model.py sqlite:///devdata.db


.. _declarative: http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html

This will generate a file that you can use directly in your TurboGears application.  Here is
an excerpt from the model.py that sqlautocode generates::

    movie_directors = Table(u'movie_directors', metadata,
        Column(u'movie_id', Integer(), ForeignKey('movies.movie_id'), primary_key=True, nullable=False),
        Column(u'director_id', Integer(), ForeignKey('directors.director_id'), primary_key=True, nullable=False),

    class Directors(DeclarativeBase):
        __tablename__ = 'directors'
    
        #column definitions
        director_id = Column(u'director_id', Integer(), primary_key=True, nullable=False)
        name = Column(u'name', String(length=100, convert_unicode=False, assert_unicode=None), nullable=False)
    
        #relation definitions
        movies = relation('Movies', secondary=movie_directors)
    
    class Genres(DeclarativeBase):
        __tablename__ = 'genres'
    
        #column definitions
        description = Column(u'description', String(length=200, convert_unicode=False, assert_unicode=None))
        genre_id = Column(u'genre_id', Integer(), primary_key=True, nullable=False)
        name = Column(u'name', String(length=100, convert_unicode=False, assert_unicode=None))
    
        #relation definitions
        movies = relation('Movies')
    
    class Movies(DeclarativeBase):
        __tablename__ = 'movies'
    
        #column definitions
        description = Column(u'description', Text(length=None, convert_unicode=False, assert_unicode=None))
        genre_id = Column(u'genre_id', Integer(), ForeignKey('genres.genre_id'))
        movie_id = Column(u'movie_id', Integer(), primary_key=True, nullable=False)
        release_date = Column(u'release_date', Date())
        title = Column(u'title', String(length=100, convert_unicode=False, assert_unicode=None), nullable=False)
    
        #relation definitions
        genres = relation('Genres')
        directors = relation('Directors', secondary=movie_directors)



The great thing about this code is that since it is generated, you have the ability to modify
it before use.  Notice that it created only tables for those items which are join tables
and therefore do not need their own explicit objects for access.  Also, note that sqlautocode
does not generate backrefs, because all references are provided as forward references.
If you execute model.py, it will create a connection to the database and then exit, 
but there are more compelling things you can do with sqlautocode.

Providing an Interactive Prompt
---------------------------------------------
Declarative generation will actually give you an interactive prompt if you set the -n option.  This
code relies on `ipython` to give you an auto-completing prompt with history, shell tools, and a whole
host of other goodies.  To install it, type::

   easy_install python

Now, regenerate your database with the -n option::

    sqlautocode -d -n -o model.py sqlite:///moviedemo.db

Your model.py file will now have code that you can use to directly access the database.
Here is a short session generated from the example using the database provided::
        
        In [1]: session.query(Directors).all()
        Out[1]: 
        [<__main__.Directors object at 0x155bb30>,
         <__main__.Directors object at 0x155bbb0>,
         <__main__.Directors object at 0x155bb70>,
         <__main__.Directors object at 0x155bc90>,
         <__main__.Directors object at 0x155bcf0>]
        
        In [2]: [director.name for director in session.query(Directors).all()]
        Out[2]: 
        [u'Robert Zemeckis',
         u'David Fincher',
         u'Andy Wachowski',
         u'Larry Wachowski',

The interactive prompt is a great way to demo the power of SQLAlchemy to people who
have never seen it.  And since the output of sqlautocode is just python code, you can modify
the output script to import all sorts of interesting libraries with which to visualize the provided data.

.. _`ipython`: http://www.ipython.org

Injecting the Generated Schema Into your TurboGears Application
-----------------------------------------------------------------

Now that you have a model.py file, you can put this directly in your TG project.  If you have a quickstarted
application, find model/auth.py.  Remove all of the table and declarative definitions, and replace them
with the table and declarative definitions inside the model.py file.  Do not copy over the metadata definition,
or the interactive prompt code if you are copying from the model.  It is very likely that this functionality
will be provided in the quickstart template, or as a paster command in the future, negating the
need for such copying.

A Note on Schemas
-----------------------------
If you use a postgres database, you might use schemas to organize your database's structure.
You can provide sqlautocode schemas for table generation.  Simply add -s <schema_name> to
the list of options.  If you are using the declarative  output, you can do likewise, but if your
database structure has interconnections between schemas, you can provide them as a comma-separated
list: -s <schema1>,<schema2>


