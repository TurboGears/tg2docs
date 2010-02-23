"""Main Controller"""

from toscasample.lib.base import BaseController
from tg import expose, flash, require, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_

from webhelpers import paginate
from tg.decorators import paginate as paginatedeco

from tg import tmpl_context, validate

from toscasample.controllers.error import ErrorController
from toscasample.model import DBSession, Movie
from toscasample.widgets.movie_form_6 import create_movie_form


class RootController(BaseController):
    error = ErrorController()

    @expose()
    def index(self):
        redirect("list")

    @expose("toscasample.templates.movie_list")
    def list(self, page=1):
        """List and paginate all movies in the database"""
        movies = DBSession.query(Movie)
        currentPage = paginate.Page(movies, page, items_per_page=5)
        return dict(movies=currentPage.items, page='ToscaSample Movie list', 
                    currentPage=currentPage)
    
    @expose("toscasample.templates.movie_list_deco")
    @paginatedeco("movies", items_per_page=5)
    def decolist(self):
        """List and paginate all movies in the database using the
        paginate() decorator."""
        movies = DBSession.query(Movie)
        return dict(movies=movies, page='ToscaSample Movie list')

    @expose('toscasample.templates.new_form')
    def new(self, **kw):
        """Show form to add new movie data record."""
        tmpl_context.form = create_movie_form
        return dict(modelname='Movie',
            page='ToscaSample New Movie')


    @validate(create_movie_form, error_handler=new)
    @expose()
    def create(self, **kw):
        """Create a movie object and save it to the database."""
        movie = Movie()
        movie.title = kw['title']
        movie.year = kw['year']
        movie.release_date = kw['release_date']
        movie.description = kw['description']
        movie.genre = kw['genre']
        DBSession.add(movie)
        flash("Movie was successfully created.")
        redirect("list")
