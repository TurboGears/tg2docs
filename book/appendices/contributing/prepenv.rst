======================================
Preparing Your Development Environment
======================================

Installing and Using Git
========================

Please refer to the `Git`_ site for directions on how to install a
current version of Git on your system. Note that we do not recommend
using a version less than 1.5 for working with Git. Versions earlier
than that seemed overly complex to use.

The best way to use a version control system (and especially a
distributed version control system like `Git`_) is a subject that
could span several books.

Instead of going through all of the detail of the many ways to use
`Git`_, we refer you to the `Git documentation`_ site for a long list
of tutorials, online documentation, and books (both paper and ebook)
for you to read that will teach you the many options you can use with
`Git`_.

.. _Git: http://www.git-scm.com/
.. _Git documentation: http://www.git-scm.com/documentation

Create A virtualenv
===================

As stated in :ref:`whyvirtualenv`, a virtualenv is extremely recommended
for development work. Make a new blank virtualenv and activate
it. This way, you will have all of your work isolated, preventing
conflicts with anything else on which you might be working.

Do not do any easy_install's of any sort. We will cover that in the next step.

Installing TurboGears2
======================

On the TurboGears2_ project pages at SourceForge_, we have a total of
four repositories that we use.

`TG2.x Core`_
    This is the actual core of TurboGears2. Unless you are working on
    modifying a template or one of the Paster_ based tools, or even
    the documentation, this is the repository you want.

`TG2.x Devtools`_
    This repository is the add-on tools. It gets updated when you wish
    to make a change to help an application developer (as opposed to
    an application installer). It contains all the stock TurboGears2
    templates, and references the Paster_ toolchain to provide an HTTP
    server, along with other :doc:`command line <../commandline>`
    tools.

`TG2.x Docs`_
    This repository contains two versions of the documentation. The
    first version (located in the docs directory) is the older docs,
    and is gradually being phased out. The newer version (located
    under the book directory) contains this file (and others) and is
    gradually being brought on par with the old, and will eventually
    replace the older version entirely.

`Tg2 Tutorials`_
     This repository contains all of the sample code. Hiring Pond (see
     :doc:`../../part1/hiringpond`) will live here as well once the code
     really gets underway.


The best way to prepare your development environment is to take the
following steps:

#. Clone the first three repositories (`TG2.x Core`_,
   `TG2.x Devtools`_, and `TG2.x Docs`_).

#. Enter the top level directory for your TG2.x Core clone, and run
   ``python setup.py develop``

#. Enter the top level directory for your TG2.x Devtools clone, and
   run ``python setup.py develop``

#. Enter the ``book`` directory for your TG2.x Docs clone, and
   run ``python setup.py develop``

After you've done all this, you have a working copy of the code
sitting in your system. You can explore the code and begin working
through any of the `sf.net tickets`_ you wish, or even on your own new
features that have not yet been submitted.

Note that, for all repositories, work is to be done off of the
``development`` branch. Either work directly on that branch, or do the
work on a branch made from the ``development`` branch. The ``master``
branch is reserved for released code.

When working on your feature or ticket, make certain to add the test
cases. Without them, the code will not be accepted.

.. _TurboGears2: http://sourceforge.net/p/turbogears2/home/
.. _SourceForge: http://www.sourceforge.net/
.. _Paster: http://www.pythonpaste.org/
.. _TG2.x Core: http://sourceforge.net/p/turbogears2/tg2/
.. _TG2.x Devtools: http://sourceforge.net/p/turbogears2/tg2devtools/
.. _TG2.x Docs: http://sourceforge.net/p/turbogears2/tg2docs/
.. _Tg2 Tutorials: http://sourceforge.net/p/turbogears2/tg2tut/
.. _sf.net tickets: http://sourceforge.net/p/turbogears2/tickets/
