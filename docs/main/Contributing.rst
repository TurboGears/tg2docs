Contributing to TurboGears 2
============================

If you want to help out, we want to help you help out! The goal of this document is to help you get started and answer any questions you might have. The `Project Philosophy`_ document has a more high-level view, whereas this document is nuts-and-bolts. The `TurboGears team`_ page lists who is responsible for what (a little outdated don't trust it much).

.. _Project Philosophy: TG2Philosophy.html
.. _TurboGears team: http://docs.turbogears.org/TurboGearsTeam

Installing 
------------
This is covered in the main `Installation Documentation`_

.. _Installation Documentation : DownloadInstall.html#installing-the-development-version-of-turbogears-2

Source Layout
-------------

TurboGears 2 is composed of two core packages.

* tg package is TurboGears 2 core. 
* tg.devtools is a set of tools used for developing turbogears applications but not needed for running them.
  
Coding style
------------

Since it's hard to argue with someone who's already written a code style document, TurboGears 2 follows `PEP 8`_ conventions. The only rule we are do not enforce is the 80 characters per line, as templates and other web related files simply don't fit into 80 chars in a natural way.

To ensure that files in the TurboGears source code repository have proper line-endings, you must configure your Subversion client. Please see the `patching guidelines`_ for details.

.. _PEP 8: http://www.python.org/peps/pep-0008.html

Testing
-------

Automated unit tests are essential to make the future growth of the project as error free as possible.

TurboGears 2 uses Nose_, which makes testing easy. You can run the tests in each of the source directories just by running `nosetests`.  For example, to run the test on the TG2 server:

.. code-block:: bash

  (tg2dev)$ cd tg2
  (tg2dev)$ nosetests

.. _Nose: http://somethingaboutorange.com/mrl/projects/nose/

Default options for `nosetests` can often be found in the `[nosetests]` section of `setup.cfg` and additional options can be passed on the command line.  See the Nose_ documentation for details.

For TG2 projects all testing default are configured in it's tests package for maximun user configurability.

Documenting Changes
-------------------

The `TurboGears Trac`_ is mostly used for tracking upcoming changes and tasks required before release of a new version. The changelog_ provides the human readable list of changes.

.. _changelog: http://trac.turbogears.org/wiki/2.0/changelog

Updating the changelog right before a release just slows down the release. Please **update the changelog as you make changes**, and this is **especially** critical for **backwards incompatibilities**.

How to Submit a Patch
---------------------

Please make sure that you read and follow the `patching guidelines`_.

.. _patching guidelines: http://docs.turbogears.org/patching_guidelines

Documentation
-------------

As mentioned in the `Project Philosophy`_ document, a feature doesn't truly exist until it's documented. Tests can serve as good documentation, because you at least know that they're accurate. But, it's also nice to have some information in English.

There are two kinds of docs, and both have their useful place:

**API reference**

These are generated with sphinx and normally include both TG docs and the sphinx sources of all upstream packages (that use sphinx)

**Manual**

    The TurboGears 2 documentation is online at
    http://turbogears.org/2.0/docs/

Please document your own work. It doesn't have to be Shakespeare, but the editors don't enjoy writing documentation any more than you do (we'd rather be coding) and it's much easier to edit an existing doc than it is to figure out your code and write something from scratch.

Contributing Documentation
----------------------------

Please see the TG1 `guidelines for contributing documentation`_ for pointers on documentation format and style.

.. _guidelines for contributing documentation: http://docs.turbogears.org/DocHelp

Check out a copy of the `documentation tree`_, edit the reStructured Text source files, and submit patches via tickets on the `TurboGears Trac`_ setting the ticket's type to "Documentation" or an email to `turbogears-docs`_, we'll prefer patches for changes that modify old documents and a single file with the new document if it's entirely new.

.. _documentation tree: http://svn.turbogears.org/docs/
.. _TurboGears Trac: http://trac.turbogears.org/
.. _turbogears-docs: http://groups.google.com/group/turbogears-docs

If you want to work on the docs sources and build the documentation tree you will also need:

     * Sphinx_
     * `pysvn`_

.. _Sphinx: http://sphinx.pocoo.org/
.. _pysvn: http://pysvn.tigris.org/project_downloads.html

Assuming that you're going to work in a virtualenv called `tg2dev`,
activate the virtualenv:

.. code-block:: bash

  $ cd tg2dev
  $ source bin/activate

`(tg2dev)` will be prefixed to your prompt to indicate that the
`tg2dev` virtualenv is activated.

Check out the latest version of the docs sources from the subversion
repositories:

.. code-block:: bash

  (tg2dev)$ svn co http://svn.turbogears.org/docs

Build the documentation tree with:

.. code-block:: bash

  (tg2dev)$ cd docs/2.0/docs
  (tg2dev)$ make html

You can view the docs by pointing your browser at the file::

  docs/2.0/docs/_build/html/index.html


