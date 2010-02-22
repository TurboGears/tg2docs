"""Main Controller"""

from toscasample.lib.base import BaseController
from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from toscasample.controllers.error import ErrorController

##{import}
from tg import tmpl_context, redirect, validate
from toscasample.model import metadata, DBSession, Movie
from toscasample.widgets.movie_form_6 import create_movie_form
##

from webhelpers import paginate

class RootController(BaseController):
    error = ErrorController()

    @expose()
    def index(self):
        redirect("list")

    ##{list}
    @expose("toscasample.templates.movie_list")
    def list(self, page=1):
        """List and paginate all movies in the database"""
        movies = DBSession.query(Movie)
        currentPage = paginate.Page(movies, page, items_per_page=5)
        return dict(movies=currentPage.items, page='ToscaSample Movie list', currentPage=currentPage)
    ##

    ##{new}
    @expose('toscasample.templates.new_form')
    def new(self, **kw):
        """Show form to add new movie data record."""
        tmpl_context.form = create_movie_form
        return dict(modelname='Movie',
            page='ToscaSample New Movie')
    ##

    ##{create}
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
    ##
