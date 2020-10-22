.. _testing:

=======================
Testing with TurboGears
=======================

.. warning::
  Starting from turbogears 2.5 newly quickstarted projects make use of pytest instead of nose.
  If you already quickstarted and want to stay on nose you can check the `old documentation`_
  Or if you just have the default tests you might try to replace the tests directory with one got from a new quickstart with the same options of your project

TurboGears quickstart command already provides a fully working test suite for your
newly quickstarted app.

.. _old documentation: https://turbogears.readthedocs.io/en/tg2.4.3/turbogears/testing.html

Running Tests
=============

Tests dependencies can be installed through::

    $ pip install -e ".[testing]"

To actually run the test suite you can run::

    $ pytest

You should get an output similar to::

  ================================= test session starts ==================================
  platform linux -- Python 3.8.6, pytest-6.1.1, py-1.9.0, pluggy-0.13.1
  Using --randomly-seed=221764868
  rootdir: /mnt/esterno/axant/tg2devtools/newapp, configfile: setup.cfg
  plugins: cov-2.10.1, randomly-3.4.1
  collected 32 items                                                                     

  newapp/tests/models/test_auth.py ...........                                     [ 34%]
  newapp/tests/functional/test_authentication.py ......                            [ 53%]
  newapp/tests/functional/test_root.py ...............                             [100%]

  ----------- coverage: platform linux, python 3.8.6-final-0 -----------
  Name    Stmts   Miss  Cover   Missing
  -------------------------------------
  -------------------------------------
  TOTAL     496      0   100%

  24 files skipped due to complete coverage.

  ============================ 32 passed, 1 warning in 6.16s =============================

The default tests that TurboGears generated for you depends on the options of your quickstart.
It will always run with 100% code coverage.

Tests Suite Structure
---------------------

When running the ``pytest`` command nose will look for any ``tests``
directory inside your application package.

The ``pytest-randomly`` plugin is automatically used to run tests in a different order on each run

Inside the tests directory there is a file called ``conftest.py`` and a directory called ``_conftest``
Turbogears default fixtures are in that directory.
You can add your own in separate files and import them in the conftest file.
Those Fixtures are automatically available in all tests

Writing Tests
=============

Available Fixtures
------------------

There are ``app`` and ``_app`` fixtures.
``app`` is the default test application, it is like calling ``_app`` without arguments.
``_app`` returns a webtest object you can use it to make requests to your app; you can see `webtest documentation`_
``_app`` also takes ``name``, ``reconfig`` and ``setup_app`` paramters:

- ``name``: is the name of the wsgi app you are testing, it must be in the ``test.ini`` file. it is a way of configuring the app
- ``reconfig``: dictionary used to change the configuration of the app on the fly for the given test
- ``setup_app``: init the database, the same as running ``gearbox setup-app -c test.ini``

Take note that ``test.ini`` actually inherits from development.ini and just overwrites some options.
For example for tests by default a ``sqlalchemy.url = sqlite:///:memory:`` is used which forces
SQLAlchemy to use an in memory database instead of a real one, so that it is created
and discarded when the test suite is run withouth requiring you to use a real database.

Also note that:

* After each test unit the database is deleted.
* After each test unit the SQLAlchemy/Ming session is cleared.

For a sample test see ``tests/functional/test_root``::

  @pytest.mark.parametrize('url,user,status', (
      ('/secc', None, 401),
      ('/secc', 'manager', 200),
      ('/secc', 'editor', 403),
      ('/secc/some_where', 'manager', 200),
      ('/secc/some_where', 'editor', 403),
  ))
  def test_secc_access(app, env, url, user, status):
      app.get(url, extra_environ=env(user), status=status)

In this example we also make use of the ``env`` fixture, it is a shorthand to ``{'REMOTE_USER': user}``
The extra_environ is documeted here_ and the environ itself is documented in PEP333_

There is also a ``obj`` fixture that can be useful to test database objects::

  obj(model.User, dict(user_name="ignucius", email_address="ignucius@example.org"))

.. _webtest documentation: https://docs.pylonsproject.org/projects/webtest/en/latest/
.. _here: https://docs.pylonsproject.org/projects/webtest/en/latest/testapp.html?highlight=extra_environ#modifying-the-environment-simulating-authentication
.. _PEP333: https://www.python.org/dev/peps/pep-0333/#environ-variables

Checking HTML Responses
-----------------------

Within the tests it is also possible to check complex HTML structures if the ``pyquery`` module
is installed.

To install ``pyquery`` just add it to your ``testpkgs`` in ``setup.py`` so that it will be
automatically installed when running the test suite.

**PyQuery** is a python module that works like jQuery and permits easy traversing of the DOM::

    def test_hello_world_and_title(app):
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
        res = self.app.get('/')
        assert res.pyquery('h1').text() == 'Hello World'
        assert res.pyquery('title').text() == 'Hello to You'

For ``pyquery`` documentation `see here`_

.. _see here: https://pythonhosted.org/pyquery/

Testing Outside Controllers
---------------------------

There might be cases when you are required to test something outside a controller,
this is common with validators or utility methods.

You will probably won't use the ``app`` object. Unless you are required to have a
request in place during your test.

This might be the case if your utility function or class uses TurboGears features that
depend on a request like ``tg.url``, ``tg.i18n.ugettext`` and so on...

Notes about older TurboGears versions
-------------------------------------

Since version ``2.3.6`` the :class:`.test_context` context is available, when used
in a context manager, the whole body of the ``with`` will run with
a fake TurboGears context, much like the one you get when using ``/_test_vars``::

    from tg.util.webtest import test_context

    with test_context(self.app):
        hello = ugettext('hello')
        assert hello == 'hello', hello

On ``2.3.5`` the same behaviour could be achieved using the special ``/_test_vars``
url which initializes a fake TurboGears context which will be used until removed::

  def test_i18n(self):
      self.app.get('/_test_vars')  # Initialize a fake request

      hello = ugettext('hello')
      assert hello == 'hello', hello

Make sure you reset the request context after using ``/_test_vars`` otherwise
you might end up with a messy environment as you have left behind the globally
registered objects. It is a good practice to perform another another request to
properly reset the global object status at the end of the test unit::

  self.app.get('/_del_test_vars', status=404)  # Reset fake request

Coverage
========

Coverage is the process of identifying all the paths of execution that the Test Suite is not
checking. Aiming at 100% code coverage means that we are sure that our tests pass through all
branches in our code and all the code we wrote has been run at least once.

Note that Coverage is able to guarantee that we checked everything we wrote, it is not able
to measure code that we should have written but didn't.
Missing errors handling won't be detected in coverage but it is a fairly reliable tool to ensure
that everything your wrote has been checked at least once.

By default coverage reporting is enabled in turbogears test suite, but it can easily be turned
off by changing ``addopts`` option in ``setup.cfg`` to disable ``pytest-cov`` plugin::

  [tool:pytest]
  #addopts = --cov=.

To make the test suite fail if coverage drops below 100% you can uncomment this line in ``.coveragerc``::

  fail_under = 100

Also ``tests`` directory coverage reporting is enabled by default, you can turn it off in ``omit`` values of coveragerc but is not suggested (eg you could overwrite a test by redefining it)
