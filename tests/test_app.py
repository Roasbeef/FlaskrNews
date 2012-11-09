"""
Tests can be run from the commandline using GAE v1.4.3's testbed functionality,
and by running the following command:

    python test.py

"""

import unittest
import warnings
from google.appengine.ext import testbed

# Ignore UserWarnings cause by jinja2 using pkg_resources.py
warnings.simplefilter('ignore')

# And just write your unittests like normal below.

import flask
from app import create_app


class LibsImportTest(unittest.TestCase):

    def setUp(self):
        import libs.flask
        self.path = libs.flask.__path__

    def test_regular_path_without_libs(self):
        flask_path = flask.__path__
        assert flask_path == self.path


class AppTest(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        app = create_app()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        self.testbed.deactivate()

    def test_index_page(self):
        rv = self.app.get('/')
        assert "I'm in yo app-engine" in rv.data

    def test_flask_default_redirecting(self):
        rv = self.app.get('/todo')
        assert 'Redirecting...' in rv.data
        assert rv.status_code == 301

    def test_todo_page(self):
        rv = self.app.get('/todo/')
        assert 'some todos' in rv.data

    def test_add_todo_and_redirect(self):
        rv = self.app.post('/todo/add', data=dict(todo='tests'))
        assert 'Redirecting...' in rv.data

    def test_qunit_page(self):
        rv = self.app.get('/qunit/')
        assert 'QUnit Tests' in rv.data

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        assert rv.status_code == 404


if __name__ == '__main__':
    unittest.main()
