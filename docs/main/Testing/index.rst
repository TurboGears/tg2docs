.. _testing_tg_apps:

===============================
Testing TurboGears Applications
===============================


.. _why:

Why is writing tests so essential?
----------------------------------

If you're already convinced about the merits of test-driven development,
you can `skip this section`_. But maybe you're still wondering whether it's
worthwile spending time writing tests instead of actually coding your
application. We usually tend to not even have time enough for writing
the code and making it work, and we're testing the functionality anyway
while we are coding, right? Will it not unnecessarily slow down your whole
development process?

The reality is, as you will see very soon when you start writing automated
tests, that you will not only be writing better software, but developing the
software will even become less expensive and faster. How so? Well, you may
have experienced it already: While it is quite simple to fix bugs during the
design and implementation phase, once your software will be released and
in production, the time needed for fixing bugs will drastically increase.
This is because with every change you make to fix one bug, you may break
other code and introduce new bugs. You will have to check the functionality
manually over and over again. However, if you have automated tests, you will
notice such problems immediately when running your test suite.

Besides these obvious benefits of automated tests, they inevitably generate
other positive side effects. For example, if you want to automate your testing,
you have to write code in a way that is testable. Such code automatically
tends to have a much better quality, because it is usually less complex and
better structured, therefore more robust and easier to understand and maintain.
Tests often reveal problems with edge cases that you wouldn't have thought
about before writing or executing the tests. As another side benefit, the
test suite can partially replace written documentation with use case examples
and detailed specification of how the code should actually work.

If you have a carefully written test suite in place, it will also encourage
you to refactor your code to make it less complex or more performant. Without
such a test suite, you would be reluctant to make such changes because of the
old saying "never touch a running system." But the automated tests will assure
that you won't break anything during the refactoring, and in the end, the code
will become even better.

If you do not write automated tests, you will inevitably spend much more time
debugging and manually testing your system. And you will never be sure that
your last change didn't break anything. Your development will be driven by
fear of failure and stagnate, while with automated tests, you can always be
confident about your code and you are encouraged to improve it even more.

Since the benefits of autmated tests are so overwhelming, they are not
considered an annoying duty you carried out after writing your code, but some
developers even start writing code by writing the corresponding test ("test
first development" or "test driven development"). This approach sounds
illogical at first, but it has several advantages, besides making sure that
every function in the code is accompanied by an automated test. In the end,
you will find out that test driven programming makes writing tests fun and you
will start wondering how you ever had written programs without writing tests.


.. _`skip this section`:
.. _testing_with_nose:

Unit testing with "Nose"
------------------------

The foundation of all automated testing is the so-called "unit testing".
As the name says, a "unit test" will only test one unit of your code at
a time, i.e. the smallest testable parts of your application. In our case,
this is usually a Python method or function. One of the basic principles
of unit testing is that each test should be independent from the others.

The Python standard library provides the `unittest`_ framework that helps
you to write unit tests based on these principles. Alternatively, you can
also write tests using the `doctest`_ module in the Python standard library.
This allows you to embed your tests in the docstrings of your code, nicely
utilizing the mentioned overlap between writing tests and documentation.

A popular Python tool that extends the basic unittest framework is `nose`_.
It makes writing unit tests even easier by providing more and simpler ways
of collecting the tests, running the tests and setting up the so-called
"test fixtures". The `nose` framework also provides a plugin mechanism
for adding in further test-related tools such as the "coverage" module
allowing you to measure exact code coverage of your application.

`Nose` is used as the base for testing TurboGears applications as well as
TurboGears itself, and therefore will be automatically installed together
with TurboGears. You can run the tests with the ``nosetests`` command.
Let's try this with a quickstarted TurboGears application:

.. code-block:: bash

    $ paster quickstart --noinput myapp
    $ cd myapp
    $ python setup.py develop
    $ paster setup-app development.ini
    $ nosetests

    ....................
    ----------------------------------------------------------------------
    Ran 20 tests in 3.000s

    OK

As you see, the quickstarted application already comes with 20 tests which
you can use as the starting point for building the complete test suite for
your application, and which should all pass unless you changed anything to
your application. `Nose` is able to find these tests due to certain naming
conventions. So you don't need to manually specify where your tests are when
writing and executing the tests. This is one of the many features that makes
testing with `nose` so comfortable. By the way, `nose` will also be used when
running the ``test`` command of setuptools, i.e. you can also run the tests
with ``python setup.py test`` or ``python setup.py nosetests``. However,
the ``nosetests`` command is simpler to type and you can pass it a lot of
useful command-line options. For instance, the option ``-v`` (for "verbose")
will display more information about the individual tests `nose` has collected:

.. code-block:: bash

    $ nosetests -v

    Anonymous users are forced to login ... ... ok
    Logouts must work correctly ... ok
    Voluntary logins must work correctly ... ok
    The data display demo works with HTML ... ok
    The data display demo works with JSON ... ok
    Displaying the wsgi environ works ... ok
    The front page is working properly ... ok
    Anonymous users must not access the secure controller ... ok
    The editor cannot access the secure controller ... ok
    The manager can access the secure controller ... ok
    Model objects can be created ... ok
    Model objects can be queried ... ok
    that Model objects can be created ... ok
    Model objects can be queried ... ok
    Model objects can be created ... ok
    Users should be fetcheable by their email addresses ... ok
    User objects should have no permission by default ... ok
    The obj constructor must set the email right ... ok
    The obj constructor must set the user name right ... ok
    Model objects can be queried ... ok

    ----------------------------------------------------------------------
    Ran 20 tests in 3.000s

    OK

You will find all of these tests in the package ``tests`` inside your
TurboGears application. This package has been divided into two subpackages,
``functional`` and ``models``. The ``models`` package contains unit tests
for your `model classes`_. The ``functional`` package contains tests for the
controllers_ of your application. Since they test the whole application stack,
they are actually not unit tests, but so-called "functional tests"
or "integration tests". Let's have a look at the example tests in these
packages in more detail.


.. _model:
.. _`model classes`:

Testing your model classes
--------------------------

The ``model`` package inside your test package comes with a simple base class
for testing your SQLAlchemy model classes, called ``ModelTest``. Unit tests
allow setting up a so-called "test fixture" with a ``setUp()`` method, often
accompanied by a ``tearDown()`` method for cleaning up the fixture after use.
The ``ModelTest`` class uses this mechanism for creating a model object
and writing it to the database. The example test class for the ``User``
model class, using ``ModelTest`` as its base class, looks like this::

    class TestUser(ModelTest):
        """Unit test case for the ``User`` model."""

        klass = model.User
        attrs = dict(
            user_name = u"ignucius",
            email_address = u"ignucius@example.org"
            )

        def test_obj_creation_username(self):
            """The obj constructor must set the user name right"""
            eq_(self.obj.user_name, u"ignucius")

        def test_obj_creation_email(self):
            """The obj constructor must set the email right"""
            eq_(self.obj.email_address, u"ignucius@example.org")

        def test_no_permissions_by_default(self):
            """User objects should have no permission by default."""
            eq_(len(self.obj.permissions), 0)

        def test_getting_by_email(self):
            """Users should be fetcheable by their email addresses"""
            him = model.User.by_email_address(u"ignucius@example.org")
            eq_(him, self.obj)

You will find this code in the ``test_auth`` module, because the ``User`` class
is defined in the ``model.auth`` module of your application. For clarity, the
names of the test files should correspond to the name of the files they are
testing. As you see, you need to specify the name of the model class with the
``klass`` attribute, and you can also specify the attributes for initializing
the model object in ``attrs``. You don't need to add tests for creating and
querying users from the database, as these tests are already inherited from the
base class ``MOdelTest``. The object that is created by the ``setUp()`` method
is stored in the ``obj`` member. The ``eq_`` function used in the four test
method has been imported from ``nose.tools`` and is just a shorthand for the
``assert`` statement that is actually at the core of every unit test.
So the first test method is equivalent to::

        def test_obj_creation_username(self):
            """The obj constructor must set the user name right"""
            assert self.obj.user_name == u"ignucius"

The ``nose.tools`` package contains some more of such convenience functions
and decorators. A more useful one is the ``raises`` decorator for checking
whether your test method raises a certain (expected) exception.

Let's assume we want to add a property ``top_level_domain`` to our ``User``
class that returns the top level domain of the user's email address. As
already mentioned, it is a good idea to write the unit test *before* writing
the actual code. So we add the following method to our ``TestUser`` class::

        def test_top_level_domain_property(self):
            """The top level domain must be returned as a property"""
            eq_(self.obj.top_level_domain, 'org')

You see how simple it is to add a uni test, and that this test also documents
that we do not want the returned value to start with a dot. Let's run our
test suite. If you don't want to run the full test suite, you can specify
the tests to run as arguments on the command line, like this:

.. code-block:: bash

    $ nosetests myapp.tests.models.test_auth

    ..........E
    ======================================================================
    ERROR: The top level domain must be returned as a property
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
        eq_(self.obj.top_level_domain, 'org')
    AttributeError: 'User' object has no attribute 'top_level_domain'

    ----------------------------------------------------------------------
    Ran 11 tests in 0.063s

    FAILED (errors=1)

As expected, the test failed, because we haven't added any code to the
User class yet. However, it is important to verify that the test is actually
picked up by `nose` and that it really fails if the tested functionality is
not implemented. Let's now add our ``top_level_domain`` property to the
``User`` class which can be found in the file ``myapp/model/auth.py``::

    @property
    def top_level_domain(self):
        """Return the top level domain of the user's email address."""
        return self.email_address.rsplit('.', 1)[-1]

We re-run our test suite to check that this code is working properly:

.. code-block:: bash

    $ nosetests

    .....................
    ----------------------------------------------------------------------
    Ran 21 tests in 3.125s

    OK

Et voilà, we know that our new property is working. You soon will start to
love these little dots indicating that your tests are passing...


.. _controllers:

Testing your controllers
------------------------

As already mentioned, you will find the tests for the example controller
methods of your quickstarted application in the ``tests.functional``
package. There are actually two test modules, ``test_authentication``
for testing the user login provided by the authentication sub-system,
and ``test_root`` for testing the actual functionality of the root controller.

Again, the quickstarted test package provides a base class ``TestController``
for all of these tests. In its ``setUp()`` method, it creates an instance
of your application which is then stored in the ``app`` attribute and run.
By default, this application instance has authentication disabled. The idea
behind this is that you test authentication separately from the actual
functionality of the controller, and independently of which kind of
authentication you have configured. Here is the test for the front page
provided by the root controller of your quickstarted application::

    class TestRootController(TestController):
        """Tests for the method in the root controller."""

        def test_index(self):
            """The front page is working properly"""
            response = self.app.get('/')
            msg = 'TurboGears 2 is rapid web application development toolkit '\
                  'designed to make your life easier.'
            # You can look for specific strings:
            assert_true(msg in response)

In ``self.app`` you actually get a wrapper around the WSGI application, which
is provided by the WebTest_ utility. This wrapper provides a convenient
interface for testing WSGI applications like those created with TurboGears.
What is so nice about this approach is that you don't need to run a web
server for the functional tests, which makes testing much speedier. WebTest
simply simulates the full request-response cycle for you.

As you see in the first line of the ``test_index()`` method, you can send a
request to your imaginary webserver using the ``get()`` method. As the method
name indicates, this is a ``GET`` request. For a POST request, you would use
the ``post()`` method. You can also add headers as argument ot the ``get()``
or ``post()`` method. As return value, you will get a response object. This
response object has the usual attributes such as ``status`` , ``headers``,
``body``, and ``request`` plus some additional functionality for testing.
For instance, as you see in the example above, ``msg in response`` allows
you to check that the string ``msg`` is found in the response body. The
``assert_true`` function is imported from ``nose.tools`` again and simply
checks that the given expression is true.

Some of the example methods of the root controller require authorization.
There is also the ``secc`` subcontroller which is set up so that only
users with "manage" permission, such as the "manager", can access it in
a quickstarted application. The following test verifies this by trying
to access the ``secc`` controller as user "editor"::

    def test_secc_with_editor(self):
        """The editor cannot access the secure controller"""
        environ = {'REMOTE_USER': 'editor'}
        self.app.get('/secc', extra_environ=environ, status=403)

As you can see here, you can pass extra environment variables and an expected
HTTP status code (in this case 403, i.e. "forbidden") to the ``get()`` method
of the test application. We still need to check that we *can* access the
``secc`` controller when we log in as "manager"::

    def test_secc_with_manager(self):
        """The manager can access the secure controller"""
        environ = {'REMOTE_USER': 'manager'}
        resp = self.app.get('/secc', extra_environ=environ, status=200)
        assert 'Secure Controller here' in resp.body, resp.body

In this case, the response should have the HTTP status code 200 (i.e. "ok").
The text "Secure Controller here" is displayed to the user by the index
method method of the secure controller using a flash message. You don't
need to worry that the flash mechanism is using a cookie in the background;
the testing framework handles all of this transparently for you.

In the case that the assert statement fails, it prints the response body as
an error message. This helps you to fix spelling errors in your expected text.
You can also print the values of all the objects in failed assert statements
by running ``nosetests`` with the ``-d`` option. Another way of inspecting
the values of objects involved in your test is simply adding print statements
to your test methods. Note that ``nose`` very conveniently will only display
the output of failing tests. Even interactive debugging of your tests is
possible with the ``--pdb`` and ``--pdb-failures`` options of `nose`.

You can set up the configuration used for your test suite in the ``test.ini``
configuration file. Note that by default, an in-memory database will be used,
but most of the other settings will be the same as in your development
environment, because by default the ``test.ini`` file has the following entry::

    [app:main]
    sqlalchemy.url = sqlite:///:memory:
    use = config:development.ini


.. _measuring_coverage:

Measuring code coverage
-----------------------

Your goal should be to have a test suite covering 100% of your application
code. How can you make sure this is the case, and there are no untested areas?
Luckily, with `coverage.py`_ you have a useful tool for measuring code coverage
of any Python program. You need to install it first, which is as simple as:

.. code-block:: bash

    $ easy_install coverage

You can instruct `nose` to run the coverage tool on your test suite and print
a coverage report, using the following options:

.. code-block:: bash

    $ nosetests --with-coverage --cover-package=myapp

    Name                       Stmts   Exec  Cover   Missing
    -----------------------------------------------------------
    myapp                          1      1   100%
    myapp.config                   1      1   100%
    myapp.config.app_cfg          22     22   100%
    myapp.config.environment       4      4   100%
    myapp.config.middleware        8      8   100%
    myapp.controllers              1      1   100%
    myapp.controllers.error        9      9   100%
    myapp.controllers.root        51     44    86%   47, 63, 69, ...
    myapp.controllers.secure      13     12    92%   31
    myapp.lib                      1      1   100%
    myapp.lib.app_globals          5      5   100%
    myapp.lib.base                13     13   100%
    myapp.lib.helpers              2      2   100%
    myapp.model                   11     11   100%
    myapp.model.auth              79     69    87%   17-18, 83, 86, ...
    myapp.templates                1      1   100%
    myapp.websetup                11     11   100%
    myapp.websetup.bootstrap      38     32    84%   49-54
    myapp.websetup.schema          9      9   100%
    -----------------------------------------------------------
    TOTAL                        280    256    91%
    -----------------------------------------------------------
    Ran 21 tests in 5.359s

This is already quite a good coverage. Let's try to improve the coverage
of the root controller. The report shows that line 47 of the
``controllers.root`` module is missing, and if you open the file with an
editor, you will find that this is the controller method for the "about" page.
You can add the following test method to the ``TestRootController`` class
in the ``tests.functional.test_root`` module to fix this::

        def test_about(self):
            """The about page can be displayed"""
            response = self.app.get('/about.html')
            assert_true('<h2>Architectural basics'
                ' of a quickstart TG2 site.</h2>' in response)

The report also shows that lines 83 and 86 of the ``model.auth`` module are
not covered, and you will find that these are ``__repr__()`` and ``unicode()``
methods of the ``Group`` class. You can fix this by adding two test methods
to the ``TestGroup`` class in the ``tests.models.test_auth`` module::

        def test_obj_repr(self):
            """The obj has a proper string representation"""
            eq_(repr(self.obj), "<Group: name=test_group>")

        def test_obj_unicode(self):
            """The obj can be converted to a unicode string"""
            eq_(unicode(self.obj), u"test_group")

If you now print a coverage report again, you will notice that the coverage
has increased from 91% to 92%.


.. _more:

Want to learn more?
-------------------

If you want to learn more about testing TurboGears applications,
we recommend studying the following online ressources:

  * The `Testing chapter of the Pylons book`_
  * The documentation of the `nose`_ testing framework
  * `Testing Applications with WebTest`_
  * `Test utilites for repoze.who-powered applications`_
  * The documentation of the `unittest`_ and `doctest`_ packages
    in the Python standard library
  * The documentation of the `coverage.py`_ tool
  * `Introduction to Test Driven Design`_
  * The Python testing tools mailing list (`testing_in_python`_)

.. _`coverage.py`: http://nedbatchelder.com/code/coverage/
.. _`doctest`: http://docs.python.org/library/doctest.html
.. _`nose`: http://somethingaboutorange.com/mrl/projects/nose/
.. _`unittest`: http://docs.python.org/library/unittest.html
.. _`webtest`: http://pythonpaste.org/webtest/

.. _`Introduction to Test Driven Design`: http://www.agiledata.org/essays/tdd.html
.. _`Test utilites for repoze.who-powered applications`: http://code.gustavonarea.net/repoze.who-testutil/
.. _`Testing Applications with WebTest`: http://pythonpaste.org/webtest/
.. _`Testing chapter of the Pylons book`: http://pylonsbook.com/en/1.1/testing.html

.. _`testing_in_python`: http://lists.idyll.org/listinfo/testing-in-python
