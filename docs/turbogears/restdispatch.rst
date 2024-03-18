.. _restdispatch:

============================
RESTful Requests Dispatching
============================

If you are developing an application where you want to expose your
database using a stateless API, :class:`tg.RestController`
might be for you.  If you want to serve resources with multiple
formats, and handle embedded resource lookup, you might find
RestController useful.  If you want to provide simple URLs which are
consistent across all of the data shared and manipulated in your
application, RestController is probably worth a look.


Unlike `TGController <objectdispatch>`_, RestController provides a mechanism to access the
request's method, not just the URL.  If you are not familiar with how
HTTP requests work, think for a minute about the difference between
sending a form with GET and POST.  Primarily, developers use POST to
send data to modify the database.  They use GET to retrieve data.
These are HTTP methods.

Standard HTTP verbiage includes: GET, POST, PUT, and DELETE.
RestController supports these, and also adds a few shortcuts for URL
dispatch that makes displaying the data as forms and lists a little
easier for the user.  The API docs describe each of the supported
controller functions in brief, so use that if you already understand
REST and need a quick way to start using it, this document will be
your guide. It is intended to provide a step-by-step example of how to
implement REST using RestController.

To explain how RESTful works with TurboGears we are going to define
a simple webservice that exposes a list of movies. WebServices are
usually an ideal candidate for RESTful dispatch and so provide
a simple and clean showcase of the feature.

Here is the Model used to develop this chapter:

.. code-block:: python

    from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table
    from sqlalchemy.orm import relation

    from moviedemo.model import DeclarativeBase, metadata

    movie_directors_table = Table('movie_directors', metadata,
                                  Column('movie_id', Integer, ForeignKey('movies.movie_id'), primary_key = True),
                                  Column('director_id', Integer, ForeignKey('directors.director_id'), primary_key = True))

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

    class Director(DeclarativeBase):
        __tablename__ = "directors"

        director_id = Column(Integer, primary_key=True)
        title = Column(String(100), nullable=False)
        movies = relation(Movie, secondary=movie_directors_table, backref="directors")

I am isolating Movies, Genres, and Directors for the purpose of
understanding how objects might relate to one another in a RESTful
context.  For purposes of this demonstration, Movies can only have one
Genre, but may be related to one or more Directors.  Directors may be
related to one or more Movies.

Listing Resources
---------------------------

Lets provide a simple listing of the movies in our database.

Our controller class is going to look like this:

.. code-block:: python

    from tg import RestController
    from tg.decorators import with_trailing_slash

    class MovieController(RestController):

        @expose('json')
        def get_all(self):
            movies = DBSession.query(Movie).all()
            return dict(movies=movies)

Supposing our MovieController is mounted with the name ``movies`` inside
our ``RootController`` going to http://localhost:8080/movies will provide
the list of our movies encoded in json format.

If you ware looking for a way to fill some sample movies, just jump to
http://localhost:8080/admin and create any data you need to make sure
your controller is working as expected.

Creating New Items
----------------------------

We use the `post` method to define how we go about saving our movie to
the database. This method gets called whenever the http://localhost:8080/movies
url is accessed using a POST request:

.. code-block:: python

    from datetime import datetime

    class MovieRestController(RestController):

        @expose('json')
        def post(self, title, description, directors=None, genre_id=None, release_date=None):
            if genre_id is not None:
                genre_id = int(genre_id)

            if directors is not None:
                if not isinstance(directors, list):
                    directors = [directors]
                directors = [DBSession.query(Director).get(director) for director in directors]
            else:
                directors = []

            if release_date is not None:
                release_date = datetime.strptime(release_date, "%m/%d/%y")

            movie = Movie(title=title, description=description, release_date=release_date,
                          directors=directors, genre_id=genre_id)
            DBSession.add(movie)
            DBSession.flush()

            return dict(movie=movie)

If the insertion is successful we are going to receive back the newly created
movie with its movie_id. The ``DBSession.flush()`` call is explicitly there
to make SQLAlchemy get a movie_id for the newly inserted movie.

This will not be the case if the user enters some weird date
format for "release_date" or doesn't provide a title or description.

One way to counteract this problem is by writing a validator when the parameters
don't respect the expected format.

If you don't know how to test this controller, check for browser extension
to make POST requests. Most browser have one, for Google Chrome you can try
`PostMan <https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm?hl=en>`_
which does a good job.

Validating The User's Input
+++++++++++++++++++++++++++

Before we add our record to the database, it is probably a good idea
to validate the data so we can prompt the user if there are mistakes.
RestController uses the same machinery that TGControllers use for
validation. We use FormEncode's validators to test that our fields are
not empty, and that the release_date has correct formatting:

.. code-block:: python

    import datetime
    from tg import request, validate
    from tg.validation import Convert, RequireValue

    @validate({
        'title': RequireValue(),
        "description": RequireValue(),
        "genre_id": Convert(int),
        "release_date": Convert(lambda v: datetime.datetime.strptime(v, "%Y-%m-%d"))
    })
    @expose('json')
    def post(self, **kw):
        if request.validation.errors:
            return dict(errors=dict([(field, str(e)) for field, e in request.validation.errors.items()]))

        #...proceed like before...

Note that the validation errors are stored in request.validation.
This is done by the TG dispatch on a failed validation.

Getting one Item
----------------------------

Using the get_one() method, we can display one item from the database
to the user.:

.. code-block:: python

    @expose('json')
    def get_one(self, movie_id):
        movie = DBSession.get(Movie, movie_id)
        return dict(movie=movie)

Updating an Existing Item
----------------------------

PUT is the method used for updating an existing record using REST.  We
can validate in the same manner as before:

.. code-block:: python

    @validate({
        'title': RequireValue(),
        "description": RequireValue(),
        "genre_id": Convert(int),
        "release_date": Convert(lambda v: datetime.datetime.strptime(v, "%Y-%m-%d"))
    })
    @expose('json')
    def put(self, movie_id, title, description, directors, genre_id, release_date, **kw):
        if request.validation.errors:
            return dict(errors=dict([(field, str(e)) for field, e in request.validation.errors.items()]))

        movie = DBSession.query(Movie).get(movie_id)
        if not movie:
            return dict(errors={'movie':'Movie not found'})

        genre_id = int(genre_id)
        if not isinstance(directors, list):
            directors = [directors]
        directors = [DBSession.query(Director).get(director) for director in directors]

        movie.genre_id = genre_id
        movie.title=title
        movie.description = description
        movie.directors = directors
        movie.release_date = release_date

        return dict(movie=movie)

Deleting An Item From Our Resource
--------------------------------------

The work-horse of delete is attached to the post_delete method.  Here
we actually remove the record from the database, and then redirect
back to the listing page:

.. code-block:: python

    @expose('json')
    def post_delete(self, movie_id, **kw):
        movie = DBSession.query(Movie).get(movie_id)
        if not movie:
            return dict(errors={'movie':'Movie not found'})

        DBSession.delete(movie)
        return dict(movie=movie.movie_id)


Nesting Resources With RestControllers
----------------------------------------------------

RestControllers expect nesting as any TG controller would, but it uses
a different method of dispatch than regular TG Controllers.  This is
necessary when you need resources that are related to other resources.
This can be a matter of perspective, or a hard-link which filters the
results of the sub controller.  For our example, we will use a nested
controller to display all of the directors associated with a Movie.

The challenge for design of your RESTful interface is determining how
to associate parts of the URL to the resource definition, and defining
which parts of the URL are part of the dispatch.  

To do this, RestController introspects the get_one method to determine 
how many bits of the URL to nip off and makes them available inside the 
``request.controller_state.routing_args`` dictionary.

This is because you may have one or more identifiers to determine an object; 
for instance you might use lat/lon to define a location.  
Since our MovieController defines a get_one which takes a movie_id as
a parameter, we have no work to do there.

All we have to do now is define our MovieDirectorController, and
provide linkage into the MovieController to provide this
functionality:

.. code-block:: python

    from tg import request

    class MovieDirectorController(RestController):
        @expose('json')
        def get_all(self):
            movie_id = request.controller_state.routing_args.get('movie_id')
            movie = DBSession.query(Movie).get(movie_id)
            return dict(movie=movie, directors=movie.directors)

    class MovieRestController(RestController):
        directors = MovieDirectorController()

        @expose('json')
        def get_one(self, movie_id):
            movie = DBSession.query(Movie).get(movie_id)
            return dict(movie=movie)

This example only defines the get_all function, I leave the other
RESTful verbiage as an exercise for you to do.

One trick that I will explain, is how to use ``_before`` to get
the related Movie object within all of your MovieDirectorController
methods with a single define.

Here is what the Controller looks like with ``_before`` added in:

.. code-block:: python

    from tg import tmpl_context, request

    class MovieDirectorController(RestController):

        def _before(self, *args, **kw):
            movie_id = request.controller_state.routing_args.get('movie_id')
            tmpl_context.movie = DBSession.query(Movie).get(movie_id)

        @with_trailing_slash
        @expose('json')
        def get_all(self):
            return dict(movie=tmpl_context.movie, directors=tmpl_context.movie.directors)

Non-RESTful Methods
--------------------

Let's face it, REST is cool, but sometimes it doesn't meet our needs
or time constraints.  A good example of this is a case where you want
an autocomplete dropdown in your "edit" form, but the resource that
would provide the Json for this dropdown has not been fleshed out yet.
as a hack, you might add a field_dropdown() method in your controller
which sends back the json required to feed your form.  RestController
allows methods named outside of the boundaries of the default methods
supported.  In other words, it's just fine to include a method in your
RestController that does not fit the REST HTML verbiage specification.

Supporting TGController's Inside RestController
+++++++++++++++++++++++++++++++++++++++++++++++++++

Just as RestController supports obscure names for methods, it can
handle nested TGController classes as well.  When dispatch encounters
a URL which maps to a non-RestController, it switches back to the
normal TG dispatch.  Simply said, you may include regular classes for
dispatch within your RestController definition.


