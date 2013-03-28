.. _pagination-quickstart:

Pagination Quickstart For Turbogears2
=====================================

:Status: Work in progress

Prerequisites
-------------

We start from an existing projects name *paginatesample* supposing a model that looks like:

.. code-block:: python

    class Movie(DeclarativeBase):
        __tablename__ = 'movie'

        id = Column(Integer, primary_key=True)
        title = Column(String(100), nullable=False)
        description = Column(Text, nullable=True)
        year = Column(Integer, nullable=True)
        genre = Column(Integer, nullable=True)
        release_date = Column(Date, nullable=True)

        def __str__(self):
            if self.year:
                return '"%s" (%d)' % (self.title, self.year)
            else:
                return '"%s"' % self.title

Populating The Database
^^^^^^^^^^^^^^^^^^^^^^^

To have some sample data to work with, let's populate the database
with some movies. Add these lines to ``websetup.py`` (above
transaction.commit())::

	    movieDatas = [["Into the Wild", 2007],
	                  ["The Big Lebowsky", 1998],
	                  ["Pulp Fiction", 1994],
	                  ["Dead Man", 1995],
	                  ["Night on Earth", 1991],
	                  ["Genova", 2008],
	                  ["Snatch", 2000]]

	    movies = []
	    for data in movieDatas:
	        movie = Movie()
	        movie.title = data[0]
	        movie.year = data[1]
	        model.DBSession.add(movie)


After you set up your application and restart the server you should now have
seven movies listed.

.. code-block:: bash

	paster setup-app development.ini
	paster serve --reload development.ini



Basic Pagination
----------------

With a model and some data set up, add ``webhelpers.paginate`` to your
controller, and create an instance of ``paginate.Page`` that you pass
to the template.

Import paginate in your ``controllers/root.py`` and modify the
``list()`` method to look like this::

	    from webhelpers import paginate

	    @expose("paginatesample.templates.movie_list")
	    def list(self, page=1):
	        """List and paginate all movies in the database"""
	        movies = DBSession.query(Movie)
	        currentPage = paginate.Page(movies, page, items_per_page=5)
	        return dict(movies=currentPage.items, page='paginatesample Movie list', currentPage=currentPage)

This creates and passes a ``paginate.Page`` object to our template, so
we can use it there to access a ``pager()``.

The subset of items that should be displayed for the current page we
get from ``currentPage.items`` and display them in the template like
we normally would.


Now the pagination can be displayed in the template like this:

.. highlight:: html+genshi

Template code in ``templates/movie_list.html``::

	<p class="pagelist">${currentPage.pager()}</p>

.. highlight:: python



Now we add some padding to the pagelist and make it centered.

Create a file pagination.css in your public/css/ directory with the
following contents and include it in style.css:

.. highlight:: css

CSS in ``public/css/style.css``::

	@import url("pagination.css");

CSS in ``public/css/pagination.css``::

	.pagelist strong {
		padding: 5px;
	}

	p.pagelist {
		text-align: center;
	}

Your movie listing should now look something like this:

.. image:: tg2pagination_fig1.png


Paginate Decorator
------------------

TurboGears provides a convenient `paginate()` decorator that you can
combine with `expose()`.  To use it, you simply have to pass it the
name of a collection to paginate.  In ``controller/root.py``::

    from tg.decorators import paginate as paginatedeco
    @expose("paginatesample.templates.movie_list_deco")
    @paginatedeco("movies", items_per_page=5)
    def decolist(self):
        """List and paginate all movies in the database using the
        paginate() decorator."""
        movies = DBSession.query(Movie)
        return dict(movies=movies, page='paginatesample Movie list')

.. highlight:: python

In your template, you can now use the collection direction since it
will be trimed to only contain the current page.  You will also have
have a basic page navigation with
`${tmpl_context.paginators.movies.pager()}`::

    <ol>
       <li py:for="movie in movies" py:content="movie">Movie title and year</li>
    </ol>

    <p class="pagelist">
      ${tmpl_context.paginators.movies.pager()}
    </p>

.. highlight:: html+genshi


Advanced Pagination
-------------------

More Formatting
^^^^^^^^^^^^^^^

Demonstrating some more formating arguments::

	${currentPage.pager(format='~3~', page_param='page', show_if_single_page=True)}


See
:mod:`webhelpers.paginate`
for more details.

Adding Parameters to Links
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can pass any number of arguments to the *pager* function and they will be used to create
the links to the other pages.

For example with the following code::

    ${currentPage.pager(param1='hi', param2='man')}

the resulting links will be:

- */list?page=1&param1=hi&param2=man*
- */list?page=2&param1=hi&param2=man*

and so on...

By default the url used to generate links will be the same of the page
where the paginated data will be visible, this can be changed by passing
the **link** argument to the *pager* function::

    ${currentPage.pager(link='/otherlink', param1='hi', param2='man')}

and the resulting link will be generated by using the provided url:

- /otherlink?page=1&param1=hi&param2=man


Adding Previous And Next Links
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's add previous and next links:

.. highlight:: html+genshi

Modify the pagelist in ``templates/movie_list.html`` to look like
this::

	<p class="pagelist">
		<a class="prevPage" href="/list?page=${currentPage.previous_page}">&lt;&lt;&lt;</a>
		${currentPage.pager(format='~3~', page_param='page', show_if_single_page=True)}
		<a class="nextPage" href="/list?page=${currentPage.next_page}">&gt;&gt;&gt;</a>
	</p>

Functional, but not very pretty:

.. image:: tg2pagination_fig2.png



Adding Some Arrow Images
^^^^^^^^^^^^^^^^^^^^^^^^

Let's add some images:

 .. image:: icons/arrow-left.png
   :height: 32

 .. image:: icons/arrow-right.png
   :height: 32


.. note ::

	These images are public domain - feel free to use them any way
	you like.  Different sizes and the source \*.psd are included
	in the project file.)


.. highlight:: html+genshi

Change the pagelist code in ``templates/movie_list.html``::

	<p class="pagelist">
		<a class="prevPage" href="/list?page=${currentPage.previous_page}">&nbsp;</a>
		${currentPage.pager(format='~3~', page_param='page', show_if_single_page=True)}
		<a class="nextPage" href="/list?page=${currentPage.next_page}">&nbsp;</a>
	</p>

.. highlight:: css

Add this to the CSS in ``public/css/pagination.css``::

	a.prevPage {
		background: url("/images/icons/png/32x32/arrow-left.png") no-repeat;
		padding-left: 18px;
		padding-right: 18px;
		padding-top: 12px;
		padding-bottom: 15px;
		text-decoration: none;
		}

	.nextPage {
		background: url("/images/icons/png/32x32/arrow-right.png") no-repeat;
		padding-left: 18px;
		padding-right: 18px;
		padding-top: 12px;
		padding-bottom: 15px;
		text-decoration: none;
		}

And this is what the end result looks like:

.. image:: tg2pagination_fig3.png
