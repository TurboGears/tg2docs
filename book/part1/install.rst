=====================================================
Installing TurboGears2: From Nothing to Serving Pages
=====================================================

We've covered some of this material in the previous chapter
(:doc:`wiki20`), but in this chapter we are going to cover it in more
depth. Here, we explain why we install things the way we do, and why
we recommend you do too.

virtualenv and You: A Perfect Match
===================================

virtualenv_ is an extremely handy tool while doing development of any
sort, or even just testing out a new application. Using it allows you
to have a sandbox in which to work, separate from your system's
Python. This way, you can try out experimental code without worrying
about breaking another application on your system. It also provides
easy ways for you to work on developing the next version of your
application without worrying about a conflicting version already
installed on your system.

It's a tool that you would do well to learn and use. You could even
check out the virtualenvwrapper_ tools by Doug Hellman (though this is
not required, and we will not assume you have them installed
throughout this book, they are still quite nice to have and use).

Installation on Windows
-----------------------

Open a command prompt, and run::

     C:\> easy_install virtualenv

This will install a binary distribution for you, precompiled for
Windows.

Installation on UNIX/Linux/Mac OSX
----------------------------------

For these platforms, there exists a large amount of variation in the
exact process to install virtualenv.

#. Attempt to install via your platform's package manager (for
   example: ``apt-get install python-virtualenv`` or ``yum install
   virtualenv``).

#. Attempt a plain ``easy_install`` via ``easy_install virtualenv``

#. Your platform may need to have the Python header files
   installed. You will need to work with whatever tools come with your
   platform to make this happen (for instance, OSX requires the XCode
   tools to install virtualenv, or on Ubuntu, you can use ``apt-get
   install python-dev``). After doing this, ``easy_install
   virtualenv`` should work.

If none of these methods work, please feel free to ask on the `mailing
list`_ for help, and we'll work through it with you.

virtualenv Notes
----------------

When you use virtualenv, you have many options available to you (use
``virtualenv --help`` to see the full list). We are only going to
cover basic use here.

The first thing you need to know is that virtualenv is going to make a
directory which amounts to a private installation of Python. This
means it will have bin, include, and lib directories. Most commonly,
you will be using the files in the bin directory: specifically,
activate will become your best friend.

The second thing you need to know is that you will *rarely* want to
use the system site-packages directory, and we **never** recommend it
with TurboGears2. As a result, we always recommend turning it off when
using virtualenv. It makes debugging much easier when you know what is
there all the time.

The last thing to note is that you have the option of choosing a
different default Python interpreter for your virtualenv. This will
allow you to test on different Python versions, such as 2.4, 2.5, 2.6,
2.7, or even PyPy_. Normally, this won't matter, but it is helpful to
know that you can switch easily.

Usage of virtualenv
-------------------

To use virtualenv, you run it like so::

   $ virtualenv --no-site-packages -p /usr/bin/python2.7 ${HOME}/tg2env

When done, with these options, you will now have a Python 2.7
virtualenv located at ${HOME]/tg2 that has nothing but what comes with
Python. By changing */usr/bin/python2.7* to point to a different
Python interpreter, you will be able to choose a different version of
Python. By changing *${HOME}/tg2env* to point to a different
directory, you can choose a different location for your new
virtualenv.

For the duration of this book, we will assume that the virtualenv you
are using is located at *${HOME}/tg2env*. Please change the commands
we give to you to match your system if you choose to use a different
directory for your virtualenv.

Once you have a virtualenv, you must activate it. On a UNIX/Linux/Mac
OSX machine, from the command line, you do the following::

    $ source ${HOME}/tg2env/bin/activate

On Windows systems, from the command line, you do the following::

   C:\> \path\to\virtualenv\Script\activate.bat

That's it. From this point onward, any ``easy_install`` commands will
automatically use your virtualenv, as will your setup.py scripts that
will be developed in later chapters.

Installing TurboGears2
======================

TurboGears2 is actually distributed in two separate packages:
TurboGears2 and tg.devtools.

TurboGears2
    This is the actual framework. If you are writing an application
    which utilizes TurboGears2, then this is the package you need to
    add as a dependency in your setup.py file.

tg.devtools
    This package contains tools and dependencies to help you during
    your development process. It includes the Paste HTTP server,
    quickstart templates, and other tools. You will generally *not*
    list this as a dependency in your setup.py file, though you may
    have reason to do so. The application we will be developing for
    this book does not rely on it, and will not list it.

After activating your virtualenv, you only need to run one command::

    $ easy_install tg.devtools

That's it. Once it completes, you now have the TurboGears2 framework
and development tools installed.

Getting Pages Visible in Your Browser
=====================================

You will now need to create an application using what you've
installed. The steps below describe how to create a basic application
for an application named "Tester". It is assumed to be created at *${HOME}/tester*::

    $ cd ${HOME}
    $ paster quickstart
    Enter project name: Tester
    Enter package name [tester]: 
    Would you prefer mako templates? (yes/[no]): no
    Do you need authentication and authorization in this project? ([yes]/no): yes
    $ cd tester
    $ python setup.py develop
    $ paster setup-app development.ini
    $ paster serve development.ini

At this time, the basic application is installed, and you can point
your web browser to http://localhost:8080/ to see the results.

Here's a breakdown of what those steps did::

    $ paster quickstart
    Enter project name: Tester
    Enter package name [tester]: 
    Would you prefer mako templates? (yes/[no]): no
    Do you need authentication and authorization in this project? ([yes]/no): yes

This deployed the quickstart template for a new application named
"Tester". It created a directory named "tester" and wrote the files
there. TurboGears2 supports the usage of Genshi, Mako. and Jinja2
templates. By default, we choose Genshi, and the choice to use Mako
out of the box is provided here. We also turn on authentication and
authorization. This is required for proper SQLAlchemy support (and is
done this way so that Mongo/Cassandra/etc can be better supported
later).::

    $ python setup.py develop

This installs the "tester" application into your virtualenv in a
development mode. This means that you do not have to do a reinstall
every time you make a change. Any changes in the current directory
will be automatically reflected in your virtualenv without you doing
any special steps.::

    $ paster setup-app development.ini

This runs the application's setup routines. It creates database
schemas, and populates default data. You may, of course, add more, bu
that's what happens by default.::

    $ paster serve development.ini

This command brings the web application into a running state, and
allows you to view and test your code. We do not recommend Paster for
normal use, instead suggesting mod_wsgi and the like (see Part IV when
it is ready). For development, though, it will suit your needs very
well.

When you are done with Paster (for whatever reason), use Control-C to
exit. When you are done with development for the day, use
``deactivate`` to return your command prompt to using the system wide
Python installation.

.. todo:: Add link to Part IV when it is written.

To summarize the entire process::

   $ virtualenv --no-site-packages ${HOME}/tg2env
   $ source ${HOME}/tg2env/bin/activate
   $ easy_install tg.devtools
   $ paster quickstart
   $ cd appname
   $ python setup.py develop
   $ paster setup-app development.ini
   $ paster serve development.ini
   Control-C
   $ deactivate

At this point, you are able to use virtualenv, install TurboGears2,
and get the default quickstarted web application up and serving pages.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _mailing list: http://groups.google.com/group/turbogears
.. _PyPy: http://www.pypy.org/
