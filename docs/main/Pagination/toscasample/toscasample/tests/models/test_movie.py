
"""Test suite for the movie model"""

from nose.tools import eq_

from toscasample import model
from toscasample.tests import ModelTest


class TestMovie(ModelTest):
    klass = model.Movie
    attrs = dict(
        title = "Metropolis",
        year = 1927
        )
