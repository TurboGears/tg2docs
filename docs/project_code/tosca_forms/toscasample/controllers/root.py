"""Main Controller"""

from toscasample.lib.base import BaseController
from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from toscasample.controllers.error import ErrorController

##{import}
from tg import tmpl_context, redirect, validate
from toscasample.model import metadata, DBSession, Movie
from toscasample.widgets.movie_form_7 import create_movie_form
##

##{picture_import}

import shutil
import os
from pkg_resources import resource_filename

public_dirname = os.path.join(os.path.abspath(resource_filename('toscasample', 'public')))
movies_dirname = os.path.join(public_dirname, 'movies')

##
class RootController(BaseController):
    error = ErrorController()

    @expose()
    def index(self):
        redirect("list")

    ##{list}
    @expose("toscasample.templates.movie_list")
    def list(self):
        """List all movies in the database"""
        return dict(movies=DBSession.query(Movie),
            page='ToscaSample Movie list')
    ##

    ##{new}
    @expose('toscasample.templates.new_form')
    def new(self, **kw):
        """Show form to add new movie data record."""
        tmpl_context.form = create_movie_form
        return dict(modelname='Movie', value=kw)
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

    
    ##{create_with_picture}
    @validate(create_movie_form, error_handler=new)
    @expose()
    def create(self, **kw):
        movie = Movie()
        movie.title = kw['title']
        movie.year = kw['year']
        movie.release_date = kw['release_date']
        movie.description = kw['description']
        movie.genre = kw['genre']
        
        #save the filename to the database
        movie.picture_filename = kw['picture_filename'].filename
        DBSession.add(movie)
        DBSession.flush()

        #write the picture file to the public directory
        movie_path = os.path.join(movies_dirname, str(movie.id))
        try:
            os.makedirs(movie_path)
        except OSError:
            #ignore if the folder already exists
            pass
            
        movie_path = os.path.join(movie_path, movie.picture_filename)
        f = file(movie_path, "w")
        f.write(kw['picture_filename'].value)
        f.close()
        
        flash("Movie was successfully created.")
        redirect("list")
