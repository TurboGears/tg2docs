"""Setup the ToscaSample application"""
import logging

import transaction
from tg import config

from toscasample.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup toscasample here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from toscasample import model
    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)


    transaction.commit()
    print "Successfully setup"
