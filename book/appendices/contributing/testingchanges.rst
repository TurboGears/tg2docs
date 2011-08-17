====================
Testing Your Changes
====================

After doing your development work, before sending to the main
repositories (or sending in a pull request), you must make sure that
your code does not break anything.

This process is actually rather painless. The first time you do it,
you need to run ``python setup.py nosetests`` from the top of your
working tree. This will download any missing packages that are
required for testing, and then run the tests.

After that first time, you may use ``nosetests``, and all of the tests
will be run.

In either case, you will be told about any failures. If you have any,
either fix the code or (if the test case is wrong) fix the test. Then
re-run the tests.

If you are interested, you can also see the current status of the
tests, and how much of the core code is actually being tested. Run
this command::

     $ nosetests --with-coverage --cover-package=tg

You will now see which lines are being tested, which ones are not, and
have a thorough report on the status of the testing coverage.
