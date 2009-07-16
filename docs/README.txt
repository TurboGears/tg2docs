Documentation Generation Guide
==================================

Setting up for Documentation Development
----------------------------------------

Here we explain how to download the development documentation, and setup
your environment to compile it.

The docs are written in reStructuredText_ (.rst files), a simple markup 
language often used to document python projects.   
We use Sphinx_ to generate html from the rst files.

Since this documentation is for the 2.1 development branch of Turbogears,
we also need to download the source in order to generate documentation from 
the modules.

If you are interested in helping with the new turbogears docs, we recommend 
you touch base with mpedersen on the IRC channel #turbogears.  He appreciates
any help you can give, and can help you get setup so he can more easily
incorporate your modifications.   Below is the recommended 
setup work best with the latest documentation efforts.


Prerequisite
------------

We assume you have the following basic pieces in place: 

* python >= 2.5
* virtualenv
* easy_install

Please see a BasicInstall_ if you do not have these.

We also use mercurial_, which is a fast, lightweight source control management system.   You cand download it from the link above, or if you have ubuntu:

    sudo apt-get install mercurial

Setup
-----

We recommend using a virtualenv for documentation development.
Setup could be done without a virtualenv, but we don't recommend it.

First, we setup the virtualenv and install the Turbogears 2.1 development branch, after first downloading it using mercurial.   

Note:  you could of course use a different name than 'tgdocs', for your virtualenv, or a different directory than "src" for your work directory.
 
    virtualenv 
    virtualenv --no-site-packages  tgdocs
    cd tgdocs
    source bin/activate
    mkdir src
    cd src
    hg clone http://bitbucket.org/mramm/tg-21/
    cd tg-21
    python setup.py develop
    cd ..

We need several additional packages to support documentation development:

sqlalchemy 
   database support - not sure why tg-21 doesn't install this by default
pysvn
   required for the Wiki20 doc which pulls source code from svn
memcache
   I believe this is needed for the documentation on caching

Here is the command to download these packages.   Again, I'm assuming you are still in the virtualenv.

   easy_install sqlalchemy pysvn memcache

After this, you should be able to verify your tg2.1 installation with
 
   paster tginfo


We also need Sphinx_ which enables us to generate html from the rst files.  However, the documentation uses newer features of sphinx only found in the development branch, so far.   So, we get the source using mercurial. 

    hg clone https://bitbucket.org/birkenfeld/sphinx-06/
    cd sphinx-06
    python setup.py develop
    cd ..


Finally, we are ready to setup the documentation.   
If you feel ready and willing to assist with the documentation efforts,
I hope you have contacted mpedersen via IRC (see above).   In order to help 
with the documentation, you get a bitbucket_ account, and create a fork of 
mpedersen's base documentation repository.  This way, mpedersen can more 
easily merge your changes in with the new documenation.

Note:  you may set up the documentation without creating your
own fork of mpedersen's repository, as detailed below.  
But if you've made it this far, why not go all the way and 
contribute back to the effort?   

:ref:`main/bitbucket_tutorial`
You can read more about forking a project on bitbucket, and merging your changes back in

You need an account on bitbucket_ in order to fork a repository.  
It is a painless process, which can be done by following the link.  
you are logged in at bitbucket, go to the mpedersen repository, and click 'fork':
    http://bitbucket.org/pedersen/tg_2_1_docs

I recommend adding an extension to your fork like '-yourname', substituting
yourname, of course.   Then you can get your repository with:

    hg clone http://bitbucket.org/laurin/tg_2_1_docs-yourname/
    cd tg_2_1_docs-yourname
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

.. _mercurial: http://mercurial.selenic.com/wiki/Download
.. _sphinx: http://sphinx.pocoo.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _bitbucket: http://bitbucket.org/account/signup/
.. _BasicInstall: http://pylonsbook.com/en/1.0/deployment.html#setting-up-a-virtual-python-environment


.. todo:: perhaps a better basic install for python, virtualenv, easy_setup


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


