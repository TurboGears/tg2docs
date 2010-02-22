"""Setup the ToscaSample application"""
import logging

import transaction
from tg import config

from toscasample.config.environment import load_environment

from toscasample.model import Movie

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup toscasample here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from toscasample import model
    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)
    
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

    transaction.commit()
    print "Successfully setup"
