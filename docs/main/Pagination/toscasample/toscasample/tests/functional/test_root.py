
"""Test suite for the root controller"""

from toscasample.tests import TestController
from nose.tools import assert_true


class TestRootController(TestController):

    def test_index(self):
        response = self.app.get('/', status=302)

    def test_list(self):
        response = self.app.get('/list')
        assert_true('Movie List' in response)
        assert_true('Add a Movie' in response)

    def test_new(self):
        response = self.app.get('/new')
        assert_true('New Movie' in response)
        assert_true('<form id="create_movie_form"' in response)
