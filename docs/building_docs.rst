.. _building_docs:

Documentation Generation Guide
==============================

Setting up for Documentation Development
----------------------------------------

Here we explain how to download the development documentation, and setup
your environment to compile it.

The docs are written in reStructuredText_ (.rst files), a simple markup
language often used to document python projects.   We use Sphinx_ to generate
html from the rst files.

Since this documentation is for the 2.1 development branch of Turbogears,
we also need to download the source in order to generate documentation from
the modules.

If you are interested in helping with the turbogears docs, we recommend you
touch base with mpedersen on the IRC channel #turbogears.  He appreciates any
help you can give, and can help you get setup so he can more easily incorporate
your modifications.   Below is the recommended setup to help work with the
latest documentation efforts.


Prerequisite
------------

We assume you have the following basic pieces in place:

* Python >= 2.5
* virtualenv
* easy_install

Please see BasicInstall_ if you do not have these.

We also use Mercurial_, which is a fast, lightweight source control management
system. You can download it from the link in this file, or if you have
ubuntu:

.. code-block:: bash

    sudo apt-get install mercurial

Setup
-----

We recommend using a virtualenv for documentation development. While you
can work without the virtualenv, we do not recommend it, do not support,
and do not document the methods to do so.

First, we setup the virtualenv and install the Turbogears 2.1 development
branch, after first downloading it using Mercurial_.   I include a step
for installing Mercurial, which you can skip if you already have it.

Below, we chose to use the name "tgdocs" for our virtualenv directory, and
used a subdirectory under that "src" for our work directory.
You could use different names if you must.

.. code-block:: bash

    virtualenv --no-site-packages  tgdocs
    cd tgdocs
    source bin/activate
    easy_install mercurial
    mkdir src
    cd src
    hg clone http://bitbucket.org/turbogears/tg-dev/
    cd tg-dev
    python setup.py develop
    cd ..
    hg clone http://bitbucket.org/turbogears/tgdevtools-dev/
    cd tgdevtools-dev
    python setup.py develop
    cd ..

.. note::   Under Windows, you use "Scripts\\activate.bat" to activate
    your virtualenv.  See BasicInstall_ if you need help with that.
    Also, in order to install Mercurial from source, you will need MinGW
    and ``set LIBRARY_PATH=C:\Programme\Python25\libs`` in activate.bat.
    Installing gettext and make from GnuWin32 will also be useful for
    compiling Mercurial and building the TurboGears docs.

We need several additional packages to support documentation development:

mapfish
   tgext.geo relies on MapFish, so we install it.
python_memcached
   This is requirement for the way we generate docs, provides memcache module
sphinx
   Sphinx_ is the tool used to generate html from the rst files.
sqlalchemy
   This is required for the documentation to avoid generating warnings when
   it is built.
tgext.geo
   We generate docs from some related packages, this is not installed by default

Here is the command to download these packages.  Again, I'm assuming you are
still in the virtualenv.

.. code-block:: bash


   easy_install sqlalchemy python_memcached tgext.geo mapfish sphinx

After this, you should be able to verify your TurboGears |version| installation with

.. code-block:: bash

   paster tginfo


Finally, we are ready to set up the documentation.   If you feel ready and
willing to assist with the documentation efforts, I hope you have contacted
mpedersen via IRC (see above).   In order to help with the documentation,
you get a bitbucket_ account, and create a fork of mpedersen's base
documentation repository.  This way, mpedersen can more easily merge your
changes in with the new documenation.

.. note::  you may set up the documentation without creating your
    own fork of mpedersen's repository, but if you've made it this far,
    why not go all the way and contribute back to the effort?

mpedersen wrote a nice :ref:`bitbucket_tutorial`, which has screen shots and
further explanation on how to fork and get and post updates with bitbucket.  We
try to provide the basic information here, but you can work through that
tutorial for additional details.

You need an account on bitbucket_ in order to fork a repository.  It
is a painless process, which can be done by following the link to the
bitbucket_ home page.  Once you are logged in at bitbucket, go to the
`mpedersen repository`_, and click 'fork'.

I recommend adding an extension to your fork like '-yourname', substituting
yourname, of course.   Then you can get your repository with:

.. code-block:: bash

    hg clone http://bitbucket.org/yourname/tg_2_1_docs-yourname/
    cd tg_2_1_docs-yourname/docs
    make html

.. note::  don't forget to substitute '-yourname' for what you used.
    The new html documentation should be in the _build/html directory.

.. note::  On Windows, if you haven't installed a "make" command
    (e.g. from GnuWin32),  use the following commands to build manually.
    The first command only needs to be run once - to create the
    destination directories.   You may also want to read about one person's
    WindowsInstall_.

    	.. code-block:: bash

	    mkdir _build\html _build\doctrees
	    sphinx-build -b html -d _build\doctrees. _build\html


If you want to grab mpedersen's latest changes, later within your work directory

    hg pull -u `mpedersen repository`_


To merge in your changes:

.. code-block:: bash

    hg commit
    hg push

.. note::  push requires a login to bitbucket.   You may also find you need to
    commit any local changes you've made first (it gives a "not updating"
    warning if this is the case).

The above commands update *your* repository.   In order to get your changes
into the "main" repository that mpedersen maintains, you need to initiate
a "pull request".   You can read more about using bitbucket in this tutorial:
:ref:`bitbucket_tutorial`.

Status
---------
You can check on the current status of todo items by typing ::

	hg locate -0 | xargs -0 grep 'todo::'|wc -l

at the command prompt in the highest level directory of the doc repository.

Thank you very much for helping out with the turbogears documentation
efforts!

.. _Mercurial: http://mercurial.selenic.com/wiki/Download
.. _sphinx: http://sphinx.pocoo.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _bitbucket: http://bitbucket.org/account/signup/
.. _BasicInstall: http://pylonsbook.com/en/1.0/deployment.html#setting-up-a-virtual-python-environment
.. _WindowsInstall: http://www.blog.pythonlibrary.org/?p=230
.. _`mpedersen repository`: http://bitbucket.org/pedersen/tg_2_1_docs

