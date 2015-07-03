.. _testing:

=======================
Testing with TurboGears
=======================

TurboGears quickstart command already provides a fully working test suite for your
newly quickstarted app.

Running Tests
=============

The only required dependency to run the testsuite is the ``nose`` package, which
can be installed with::

    $ pip install nose

Other dependencies used by your tests will automatically be installed when the
test suite is run through the ``install_requires`` and ``testpkgs`` variables in ``setup.py``,
so if your application requires any dependency specific for testing just make sure is
listed there.

To actually run the test suite you can run::

    $ python setup.py nosetests

This will install all the required dependencies and will run the tests.
You should get an output similar to::

    Wrong password keeps user_name in login form ... ok
    Anonymous users are forced to login ... ok
    Logouts must work correctly ... ok
    Voluntary logins must work correctly ... ok
    The data display demo works with HTML ... ok
    The data display demo works with JSON ... ok
    Displaying the wsgi environ works ... ok
    The front page is working properly ... ok
    Anonymous users must not access the secure controller ... ok
    The editor cannot access the secure controller ... ok
    The manager can access the secure controller ... ok
    plain.tests.functional.test_root.TestWithContextController.test_i18n ... ok
    Model objects can be created ... ok
    Model objects can be queried ... ok
    Model objects can be created ... ok
    Model objects can be queried ... ok
    Model objects can be created ... ok
    Users should be fetcheable by their email addresses ... ok
    User objects should have no permission by default. ... ok
    The obj constructor must set the email right ... ok
    The obj constructor must set the user name right ... ok
    Model objects can be queried ... ok

    ----------------------------------------------------------------------
    Ran 22 tests in 11.931s

    OK

Those are the default tests that TurboGears generated for you.

Tests Collection
----------------

When running the ``nosetests`` command nose will look for any ``tests``
directory inside your application package.

Nose itself will look in all files whose name starts with test_[something].py for all the classes
which name starts with Test[Something] and will consider them as Test Cases,
for each method inside the test case whose name starts with test_[something]
they will be treated as Test Units.

Writing Tests
=============

When quickstarting an application you will notice that there is a tests package inside it.
This package is provided by TurboGears itself and contains the fixture already creates a ``TestApp``
instance for you and loads configuration from ``test.ini`` instead of ``development.ini``.

The ``TestApp`` which is available inside *Test Cases* as ``self.app`` is an object with methods
that emulate HTTP requests: ``.get``, ``.post``, ``.put`` and so on and is able to understand
both **html** and **json** responses.

Take note that ``test.ini`` actually inherits from development.ini and just overwrites some options.
For example for tests by default a ``sqlalchemy.url = sqlite:///:memory:`` is used which forces
SQLAlchemy to use an in memory database instead of a real one, so that it is created
and discarded when the test suite is run withouth requiring you to use a real database.

All your application tests that call a web page should inherit from ``tests.TestController``
which ensure:

    * For each test unit the database is created and initialized by calling setup-app.
    * For each test unit the ``self.app`` object is provided which is a ``TestApp``
      instance of your TurboGears2 application loaded from ``test.ini``.
    * After each test unit the database is deleted.
    * After each test unit the SQLAlchemy session is cleared.

For a sample test see ``tests/functional/test_root``::

    from nose.tools import ok_
    from testapp.tests import TestController


    class TestRootController(TestController):
        """Tests for the method in the root controller."""

        def test_index(self):
            response = self.app.get('/')
            msg = 'TurboGears 2 is rapid web application development toolkit '\
                  'designed to make your life easier.'
            ok_(msg in response)

        def test_environ(self):
            response = self.app.get('/environ.html')
            ok_('The keys in the environment are:' in response)

Simulating Authentication Requests
----------------------------------

To simulate authentication you can just pass to the ``.get``, ``.post`` and so on methods an
``extra_environ`` parameter (which is used to add WSGI environ values available
in ``tg.request.environ``) named ``REMOTE_USER``.

For example if you want to behave like you are logged as the editor user you just pass::

    def test_secc_with_editor(self):
        environ = {'REMOTE_USER': 'editor'}
        self.app.get('/secc', extra_environ=environ, status=403)

The previous test will check that when user is logged as *editor* a *403* error is returned
from the ``/secc`` url instead of the *401* which is returned when user is not logged at all.

Checking HTML Responses
-----------------------

Within the tests it is also possible to check complex HTML structures if the ``pyquery`` module
is installed.

To install ``pyquery`` just add it to your ``testpkgs`` in ``setup.py`` so that it will be
automatically installed when running the test suite.

**PyQuery** is a python module that works like jQuery and permits easy traversing of the DOM::

    from testapp.tests import TestController


    class TestHelloWorldApp(TestController):
        """Tests an app that returns a simple HTML response with:

            <html>
                <head>
                    <title>Hello to You</title>
                </head>
                <body>
                    <h1>Hello World</h1>
                </body>
            </html>
        """

        def test_hello_world(self):
            res = self.app.get('/')
            assert res.pyquery('h1').text() == 'Hello World'

        def test_title(self):
            res = self.app.get('/')
            assert res.pyquery('title').text() == 'Hello to You'

For ``pyquery`` documentation please rely on https://pythonhosted.org/pyquery/

Submitting Forms
----------------

The ``TestApp`` permits also to easily fill and submit forms,
this can be used to test features that require submission of form values::

    from testapp.tests import TestController


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

The *form* itself is identified by its **id**, so the ``page.forms['form1']`` works as
the form has ``id="form1"``.

Testing Outside Controllers
---------------------------

There might be cases when you are required to test something outside a controller,
this is common with validators or utility methods.

In those cases you can inherit from ``tests.TestController`` as usual, and you
will probably won't use the ``self.app`` object. Unless you are required to have a
request in place during your test.

This might be the case if your utility function or class uses TurboGears features that
depend on a request like ``tg.url``, ``tg.i18n.ugettext`` and so on...

Since version ``2.3.6`` the :class:`.test_context` context is available, when used
together with a ``with`` statement, the whole body of the ``with`` will run with
a fake TurboGears context, much like the one you get when using ``/_test_vars``::

    from tg.util.webtest import test_context

    with test_context(self.app):
        hello = ugettext('hello')
        assert hello == 'hello', hello

On ``2.3.5`` the same behaviour could be achieved using the special ``/_test_vars``
url which initializes a fake TurboGears context which will be used until removed::

    from testapp.tests import TestController


    class TestWithContextController(TestController):
        def test_i18n(self):
            self.app.get('/_test_vars')  # Initialize a fake request

            hello = ugettext('hello')
            assert hello == 'hello', hello

Make sure you reset the request context after using ``/_test_vars`` otherwise
you might end up with a messy environment as you have left behind the globally
registered objects. It is a good practice to perform another another request to
properly reset the global object status at the end of the test unit::

    from testapp.tests import TestController


    class TestWithContextController(TestController):
        def tearDown(self):
            self.app.get('/_del_test_vars', status=404)  # Reset fake request
            super(TestWithContextController, self).tearDown()

        def test_i18n(self):
            self.app.get('/_test_vars')  # Initialize a fake request

            hello = ugettext('hello')
            assert hello == 'hello', hello

Coverage
========

Coverage is the process of identifying all the paths of execution that the Test Suite is not
checking. Aiming at 100% code coverage means that we are sure that our tests pass through all
branches in our code and all the code we wrote has been run at least once.

Note that Coverage is able to guarantee that we checked everything we wrote, it is not able
to measure code that we should have written but didn't.
Missing errors handling won't be detected in coverage but it is a fairly reliable tool to ensure
that everything your wrote has been checked at least once.

By default coverage reporting is disabled in turbogears test suite, but it can easily be turned
on by changing ``with-coverage`` option in ``setup.cfg``::

    [nosetests]
    verbosity = 2
    detailed-errors = 1
    with-coverage = true  # CHANGED TO true TO ENABLE COVERAGE
    cover-erase = true
    cover-package = plain

When coverage is enabled, after the tests results, you will get the coverage report::

    ..
    Name      Stmts   Miss  Cover   Missing
    ---------------------------------------
    _opnums      13      8    38%   2-3, 6-9, 12, 16-17
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    OK

