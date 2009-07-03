Documentation Generation Guide
==================================

DOC Generation
--------------

Make sure that you have followed the instructions in top-level ``INSTALL.txt``
file to install TurboGears 2.

Prerequisite
------------

You also need to install Sphinx_ to generate the TurboGears documentation from
docs.turbogears.org::

    $ easy_install Sphinx

And pysvn module is required for the Wiki20 doc which pulls source code from svn.

    http://pysvn.tigris.org/project_downloads.html

Source package is here:

    http://pysvn.barrys-emacs.org/source_kits/pysvn-1.6.1.tar.gz

This may require that you have the includes for SVN.

To generate the docs you will also need:

  - Mercurial installed
  - memcache or cmemcache installed (http://gijsbert.org/downloads/cmemcache/cmemcache-0.95.tar.bz2)

Generate Doc
-------------

For the following, change to the ``docs`` directory below the top-level
TurboGears 2 source directory.

Finally, run ``make <builder>`` to generate docs::

    $ make html

Sphinx v0.6.2 Issues
--------------------

After Sphinx v0.5.2, Sphinx has issues generating the documentation. The
fix is to retrieve the latest 0.6 version from Mercurial, and install that
version. That version can actually generate the docs just fine.

It can be retrieved here: https://bitbucket.org/birkenfeld/sphinx-06/

.. _sphinx: http://sphinx.pocoo.org/
.. _sourceforge: http://sourceforge.net/project/showfiles.php?group_id=32455
.. _reStructuredText: http://docutils.sourceforge.net/rst.html

