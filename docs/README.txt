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


.. todo:: no INSTALL.txt for tg2


---------------
my steps...

# made sure I had the following installed:
#   virtualenv
#   mercurial
#   pysvn, and memcache were already installed 
# started with a fresh virtualenv, getting tg 2.1 first

    virtualenv --no-site-packages  tgdocs
    cd tgdocs
    source bin/activate
    mkdir src
    cd src
    hg clone http://bitbucket.org/mramm/tg-21/
    cd tg-21
    python setup.py develop

Note:  downloaded a bunch of dependencies, tried to confirm install with

    paster tginfo

Note: it complained about sqlalchemy, so...

    easy_install sqlalchemy

paster tginfo now looked good

Starting getting docs setup

    easy_install Sphinx

# downloaded more dependencies
#  I had previously create bitbucket account, and created my
#   fork, tg_2_1_docs_lek    from:
#  from:    http://bitbucket.org/pedersen/tg_2_1_docs/

used previous fork

    hg clone http://bitbucket.org/laurin/tg_2_1_docs_lek/
    cd tg_2_1_docs_lek
    hg pull -u http://bitbucket.org/pedersen/tg_2_1_docs/

# told me:
#   not updating, since new heads added
#   (run 'hg heads' to see heads, 'hg merge' to merge)
# tried both hg heads and hg merge, told me it merged

    hg merge
    hg commit
    hg push

Note:  push required login

Note:  sphinx 0.6.2 and 0.5.2 did NOT sucessfully build, so we are using sphinx development version

# first go back to top level "src" directory

    cd ../..
    hg clone https://bitbucket.org/birkenfeld/sphinx-06/
    cd sphinx-06
    python setup.py develop
    cd ../tg_2_1_docs_lek/docs
    make html

Success!



some notes below on sphinx problems
# started testing docs (already in dir tg_2_1_docs_lek)
cd docs  
make html
# sphinx complained.   decided to downgrade
easy_install "sphinx==0.5.2"
# trying again
make html
# gave "minor" warning about tg2.1 branch?
#    AttributeError: type object 'TGController' has no attribute '__before__'
# ... but seemed to create some docs
# tried to look at them in browser, and found _build/html empty!  ack.
# got same type of error with "clean" pedersen/tg_2_1_docs
# looking at   /tmp/sphinx-err-n2A748.log
#put problem on pastebin:  http://www.pastebin.org/1942
# trying with development sphinx, back to my "top level"
cd ../..
hg clone https://bitbucket.org/birkenfeld/sphinx-06/
cd sphinx-06
python setup.py develop
cd ../tg_2_1_docs_lek/docs
make html
# success!   (with quite a few warnings)


