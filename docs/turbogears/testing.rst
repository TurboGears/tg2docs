.. _testing:

=======================
Testing with TurboGears
=======================

The TurboGears quickstart command creates a working pytest test suite for every
new application. The generated tests use WebTest to exercise your WSGI
application and pytest to collect and run the tests.

If you want to try the examples on this page with a fresh project, create one
with authentication and SQLAlchemy support::

    $ gearbox quickstart -a -s testapp
    $ cd testapp

The generated package name will be ``testapp``. If you choose a different
project or package name, replace ``testapp`` in the examples below with that
name.

Running Tests
=============

Install the application together with its testing dependencies from the project
root::

    $ pip install -e ".[testing]"

A newly quickstarted TurboGears 2.5 project declares the testing dependencies in
``pyproject.toml`` under ``[project.optional-dependencies]``::

    testing = [
      "WebTest >= 1.2.3",
      "pytest",
      "coverage",
      "gearbox"
    ]

To run the test suite, execute::

    $ pytest

You should get output similar to::

    ============================= test session starts ==============================
    platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
    rootdir: /path/to/testapp
    configfile: pyproject.toml
    collected 20 items

    testapp/tests/functional/test_authentication.py ...                    [ 15%]
    testapp/tests/functional/test_root.py .......                          [ 50%]
    testapp/tests/models/test_auth.py ..........                           [100%]

    ======================= 20 passed, 14 warnings in 0.75s ========================

The exact number of tests depends on the options you passed to ``gearbox
quickstart``. For example, applications without authentication or database
support generate fewer tests.

Test Collection
---------------

When running ``pytest``, pytest searches for tests in files named
``test_*.py`` or ``*_test.py``. The quickstart creates a ``tests`` package
inside your application package and places functional tests under
``tests/functional`` and model tests under ``tests/models``.

The generated tests are ordinary pytest tests. They keep the traditional
TurboGears ``TestController`` and ``ModelTest`` base classes, but use pytest's
xUnit-style hooks such as ``setup_method`` and ``teardown_method`` instead of
``setUp`` and ``tearDown``.

Writing Tests
=============

When quickstarting an application you will notice that there is a tests package
inside it. This package contains helpers that load your application from
``test.ini`` instead of ``development.ini`` and create a WebTest ``TestApp`` for
functional tests.

The ``TestApp`` is available inside controller test classes as ``self.app``. It
has methods that emulate HTTP requests, such as ``.get``, ``.post`` and
``.put``, and can inspect both HTML and JSON responses.

Take note that ``test.ini`` inherits from ``development.ini`` and just
overwrites some options. For example, SQLAlchemy applications use
``sqlalchemy.url = sqlite:///:memory:`` by default during tests. This creates an
in-memory database for the test suite instead of requiring a real database.

All application tests that call a web page should inherit from
``tests.TestController``. For each test method it:

    * Loads the TurboGears application from ``test.ini``.
    * Provides ``self.app`` as a WebTest ``TestApp`` instance.
    * Creates and initializes the database by running ``setup-app``.
    * Removes the SQLAlchemy session and drops the test database afterwards.

For a sample test, see the generated ``tests/functional/test_root.py``::

    from testapp.tests import TestController


    class TestRootController(TestController):
        """Tests for the method in the root controller."""

        def test_index(self):
            """The front page is working properly"""
            response = self.app.get('/')
            msg = 'TurboGears 2 is rapid web application development toolkit '\
                  'designed to make your life easier.'
            assert msg in response

        def test_environ(self):
            """Displaying the wsgi environ works"""
            response = self.app.get('/environ.html')
            assert 'The keys in the environment are:' in response

Simulating Authentication Requests
----------------------------------

To simulate authentication you can pass an ``extra_environ`` parameter to
``.get``, ``.post`` and the other WebTest request methods. The
``extra_environ`` dictionary adds WSGI environ values that are available in
``tg.request.environ``. TurboGears uses ``REMOTE_USER`` to identify the current
user in the generated tests.

For example, if you want to behave like you are logged in as the editor user,
you can write::

    def test_secc_with_editor(self):
        environ = {'REMOTE_USER': 'editor'}
        self.app.get('/secc', extra_environ=environ, status=403)

The previous test checks that when the user is logged in as *editor*, the
``/secc`` URL returns a *403* error instead of the *401* returned when the user
is not logged in at all.

Checking HTML Responses
-----------------------

WebTest can parse HTML responses with Beautiful Soup. A generated test includes
an example of accessing the parsed response::

    def test_index(self):
        response = self.app.get('/')
        links = response.html.find_all('a')
        assert links, "Mummy, there are no links here!"

If you prefer jQuery-like DOM traversal, install ``pyquery`` and use the
``response.pyquery`` helper::

    def test_hello_world(self):
        res = self.app.get('/')
        assert res.pyquery('h1').text() == 'Hello World'
        assert res.pyquery('title').text() == 'Hello to You'

For ``pyquery`` documentation, see https://pyquery.readthedocs.io/.

Submitting Forms
----------------

The WebTest ``TestApp`` can also fill and submit forms. This can be used to test
features that require submission of form values::

    class TestFormApp(TestController):
        """Tests an app that contains a simple HTML form with:

            <form id="form1" action="/submit" method="POST">
                <input type="text" name="value"/>
            </form>

           That submits to:

            @expose('json')
            def submit(self, value=None, **kwargs):
                return dict(value=value)
        """

        def test_form_submission(self):
            page = self.app.get('/')

            form = page.forms['form1']
            form['value'] = 'prova'

            res = form.submit()
            assert res.json['value'] == 'prova', res

The form itself is identified by its **id**, so ``page.forms['form1']`` works
because the form has ``id="form1"``.

.. _testing_outside_controllers:

Testing Outside Controllers
---------------------------

There might be cases when you are required to test something outside a
controller, which is common with validators or utility methods.

In those cases you can inherit from ``tests.TestController`` as usual, but you
probably will not use ``self.app`` unless you need a request in place during
your test.

This might be the case if your utility function or class uses TurboGears
features that depend on a request like ``tg.url``, ``tg.i18n.ugettext`` and so
on.

Since version ``2.3.6`` the :class:`.test_context` context is available. When
used with a ``with`` statement, the whole body of the ``with`` will run with a
fake TurboGears context, much like the one you get when using ``/_test_vars``::

    from tg.util.webtest import test_context

    with test_context(self.app):
        hello = ugettext('hello')
        assert hello == 'hello', hello

On ``2.3.5`` the same behaviour could be achieved using the special
``/_test_vars`` URL, which initializes a fake TurboGears context that will be
used until removed::

    from testapp.tests import TestController


    class TestWithContextController(TestController):
        def test_i18n(self):
            self.app.get('/_test_vars')  # Initialize a fake request

            hello = ugettext('hello')
            assert hello == 'hello', hello

Make sure you reset the request context after using ``/_test_vars``. Otherwise
you might end up with a messy environment because you have left behind globally
registered objects. It is a good practice to perform another request to reset
the global object status at the end of the test method::

    from testapp.tests import TestController


    class TestWithContextController(TestController):
        def teardown_method(self, method):
            self.app.get('/_del_test_vars', status=404)  # Reset fake request
            super().teardown_method(method)

        def test_i18n(self):
            self.app.get('/_test_vars')  # Initialize a fake request

            hello = ugettext('hello')
            assert hello == 'hello', hello

Coverage
========

Coverage is the process of identifying all the paths of execution that the test
suite is not checking. Aiming at 100% code coverage means that your tests pass
through all branches in your code and all the code you wrote has been run at
least once.

Note that coverage can guarantee that you checked code you wrote, but it cannot
measure code that should have been written and was not. Missing error handling
will not be detected by coverage, but coverage is a reliable tool to ensure that
existing code has been checked at least once.

A newly quickstarted project includes ``coverage`` in its testing dependencies.
To run pytest under coverage, pass your package name as the coverage source::

    $ coverage run --source=testapp -m pytest
    $ coverage report --show-missing

Replace ``testapp`` with your application's package name. You should get output
similar to::

    Name                              Stmts   Miss  Cover   Missing
    ---------------------------------------------------------------
    testapp/controllers/root.py          60      7    88%   47, 67, 73, 80, 86, 99-100
    testapp/model/auth.py                67      7    90%   70, 73, 94, 97, 115, 179, 182
    ---------------------------------------------------------------
    TOTAL                              443     34    92%

You can also save the coverage configuration in a ``.coveragerc`` file::

    [run]
    source = testapp

    [report]
    show_missing = true
    fail_under = 90

With this configuration, running ``coverage report`` will fail if total coverage
is below 90%.
