.. _building_docs:

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
setup to help work with the latest documentation efforts.


Prerequisite
------------

We assume you have the following basic pieces in place: 

* python >= 2.5
* virtualenv
* easy_install

Please see a BasicInstall_ if you do not have these.

We also use mercurial_, which is a fast, lightweight source control 
management system.   
You can download it from the link in this file, or if you have ubuntu:

    sudo apt-get install mercurial

Setup
-----

We recommend using a virtualenv for documentation development.
Setup could be done without a virtualenv, but we don't recommend it.

First, we setup the virtualenv and install the Turbogears 2.1 development 
branch, after first downloading it using mercurial.   Below, we chose to 
use the name "tgdocs" for our virtualenv directory, and used a subdirectory
under that "src" for our work directory.   You could use different names if
you must.

.. code-block:: bash

    virtualenv --no-site-packages  tgdocs
    cd tgdocs
    source bin/activate
    mkdir src
    cd src
    hg clone http://bitbucket.org/mramm/tg-21/
    cd tg-21
    python setup.py develop
    cd ..

.. note::   Under windows, you use the "activate.bat" script to activate
    your virtualenv.  See BasicInstall_ if you need help with that.

We need several additional packages to support documentation development:

sqlalchemy 
   database support - not sure why tg-21 doesn't install this by default
python_memcached
   this is requirement for the way we generate docs, provides memcache module
mercurial
   make sure this module is installed in your virtualenv.  Needed, if you are starting from a fresh virtualenv.
tgext.geo
   we generate docs from some related packages, again tg-21 install did not install this by default

Here is the command to download these packages.   Again, I'm assuming you are 
still in the virtualenv.

   easy_install sqlalchemy python_memcached mercurial tgext.geo

.. note::  tgext.geo may complain about not being able to install one of its dependencies: MapFish.   This is not critical for building the docs, but if this continues to be a problem you can install it with "easy_install -i http://dev.camptocamp.com/packages/mapfish/1.1/index --allow-hosts=dev.camptocamp.com mapfish==1.1".

After this, you should be able to verify your tg2.1 installation with
 
   paster tginfo


We also need Sphinx_ which enables us to generate html from the rst files.  
However, the documentation uses newer features of sphinx only found in 
the development branch, right now.   So, we get the source using mercurial. 

.. code-block:: bash

    hg clone https://bitbucket.org/birkenfeld/sphinx-06/
    cd sphinx-06
    python setup.py develop
    cd ..


Finally, we are ready to set up the documentation.   
If you feel ready and willing to assist with the documentation efforts,
I hope you have contacted mpedersen via IRC (see above).   In order to help 
with the documentation, you get a bitbucket_ account, and create a fork of 
mpedersen's base documentation repository.  This way, mpedersen can more 
easily merge your changes in with the new documenation.

.. note::  you may set up the documentation without creating your
    own fork of mpedersen's repository, but if you've made it this far, 
    why not go all the way and contribute back to the effort?   

mpedersen wrote a nice :ref:`bitbucket_tutorial`, which has screen shots and
further explanation on how to fork and get and post updates with bitbucket.  We
try to provide the basic information here, but you can work through that
tutorial for additional details.

You need an account on bitbucket_ in order to fork a repository.  
It is a painless process, which can be done by following the link.  
Once you are logged in at bitbucket, go to the mpedersen repository, 
and click 'fork':

    http://bitbucket.org/pedersen/tg_2_1_docs

I recommend adding an extension to your fork like '-yourname', substituting
yourname, of course.   Then you can get your repository with:

.. code-block:: bash

    hg clone http://bitbucket.org/laurin/tg_2_1_docs-yourname/
    cd tg_2_1_docs-yourname/docs
    make html

.. note::  don't forget to substitute '-yourname' for what you used.   
    You will probably get a lot of warnings, but hopefully no errors.  
    The new html documentation should be in the _build/html directory.

.. note::  On Windows, you typically don't have a "make" command available
    to you.   Here are the commands you'd use instead.   
    The first command only needs to be run once - to create the 
    destination directories.   You may also want to read about one person's 
    WindowsInstall_.

.. code-block:: bash

    mkdir _build\html _build\doctrees
    sphinx-build -b html -d _build\doctrees   . _build\html


    
If you want to grab mpedersen's latest changes, later within your work directory

    hg pull -u http://bitbucket.org/pedersen/tg_2_1_docs/


To merge in your changes.   Is this right???

.. code-block:: bash

    hg merge
    hg commit
    hg push

.. note::  push required a login to bitbucket.   You may also find you need to 
    commit any local changes you've made first (it gives a "not updating" 
    warning if this is the case).

The above commands update *your* repository.   In order to get your changes
into the "main" repository that mpedersen maintains, you need to initiate
a "pull request" as detailed in his :ref:`bitbucket_tutorial`.

Thanks very much for considering helping out with the turbogears documentation
efforts!



.. _mercurial: http://mercurial.selenic.com/wiki/Download
.. _sphinx: http://sphinx.pocoo.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _bitbucket: http://bitbucket.org/account/signup/
.. _BasicInstall: http://pylonsbook.com/en/1.0/deployment.html#setting-up-a-virtual-python-environment
.. _WindowsInstall: http://www.blog.pythonlibrary.org/?p=230


.. todo:: perhaps a better basic install for python, virtualenv, easy_setup
.. todo:: review whether my discussion of hg, bitbucket and repositories makes
    sense, and whether mpdedersen's bitbucket tutorial covers all it needs to.
    (note:   I think they make basic sense, but...   I'm not an expert)
.. todo:: review and edit, in general...
    big edit issue:  this now seems like too much for a readme, and I've 
    started using rst type commands.   Perhaps the commands should be broken 
    off into a tutorial, and provide a link to the tutorial.   
    I still recommend highlighting some of the volunteer opportunities.  
.. todo::  working towards no warnings.    found memcache install above is NOT 
    good, and also need to install tgext.geo - however, one of dependencies 
    for tgext.geo has problems...  error: Could not find suitable distribution
    for Requirement.parse('MapFish>=1.1')


