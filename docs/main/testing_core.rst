.. _testing_core:

Setting up the TurboGears Test Environment and Testing
========================================================

Initial Environment Setup
---------------------------


Please follow the instructions on the install_ page to get your
environment started.  Pay special attention to the virtualenv
setup.  You want to do your TG development within a clean environment
that will not interfere with any existing projects you may have.

.. _install: DownloadInstall.html#installing-the-development-version-of-turbogears-2

Package Installation
--------------------
Because Turbogears allows the user to swap out so many different moving parts,
we need to be able to prove that we can support these components regularly
in order to provide a robust experience for our users.

Right now TG testing depends on lxml because of chameleon.genshi, a very fast
implementation of genshi that uses the lxml driver.  This driver is written
in C, and therfore requires some linkage to work properly.  Lot's of folks
have problems getting this to work, but if you try this, it will often work::

    $ STATIC_DEPS=true; easy_install lxml
    
You can then install chameleon.genshi successfully::
    
    $ easy_install chameleon.genshi

Tests do have more dependencies than simply using TurboGears because
they use all the opional module and also some test specific utilities.
In order to install all of these, make sure that you have TurboGears2
registered with Setuptools, either by installing it or by seting it up
in development mode (`setup.py develop`) then ask Setuptools to
install the test dependencies:

    $ easy_install 'TurboGears2[core-testing]'
    

Testing
-------

Automated unit tests are essential to make the future growth of the
project as error free as possible.

TurboGears 2 uses Nose_, which makes testing easy. You can run the
tests in each of the source directories just by running `nosetests`.
For example, to run the test on the TG2 server:

.. code-block:: bash

  (tg2dev)$ cd tg2
  (tg2dev)$ nosetests

.. _Nose: http://somethingaboutorange.com/mrl/projects/nose/

Default options for `nosetests` can often be found in the
`[nosetests]` section of `setup.cfg` and additional options can be
passed on the command line.  See the Nose_ documentation for details.

With any luck, your tests will run and produce something like the following output::

   ----------------------------------------------------------------------
    Ran 245 tests in 2.457s

    OK

As you can see, the tests really take very little time to run, so it makes sense
to run the tests any time you want to contribute code in order to make certain it
does not break any existing functionality.

Coverage
----------

Adequate code coverage is a goal for the TurboGears project, as it is probably
the minimum you could do to make sure your code is well tested.  Code coverage
testing is built into nose and easy to use.  To test TurboGears and see the code
coverage output simply type::

    $ nosetests --with-coverage --cover-package=tg
    
The end your output will look something like this::

    TOTAL                                 1554   1407    90%   
    ----------------------------------------------------------------------
    Ran 245 tests in 3.659s

    OK

TurboGears does not currently have 100% coverage, and we realize this is an issue.
We'd love some help in this area, so if you have some time and want to learn
more about the internals of TurboGears, pick a few untested lines of code and
figure out how to supply sufficient tests to cover that code.  
