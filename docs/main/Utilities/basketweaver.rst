.. _basketweaver:

Generating your own Private Python Package Index
====================================================

:Status: Official

.. contents:: Table of Contents
   :depth: 2


Perhaps you have an application that you need to deploy
in a number of places in your organization, but you cannot
deploy to `pypi`_ because the code is proprietary.  Basketweaver
was a tool that allows you to set up a static file index
which you can share with Apache, NGinx, even Cachefly if 
you have a large distribution base and need a CDN for your files.
Here's how you can take your application, and turn it into
an index you can install from.

Collecting Dependencies using compoze
--------------------------------------
If your current site-packages is adequate serve to create an index, 
you can pull them down using the compoze tool.  First, we need to
install it:: 
   
   easy_install http://dist.repoze.org/legacy/compoze-0.2.tar.gz

Now we can fetch all the packages we need using Compoze::
  
    compoze  --fetch-site-packages --path=mytgapp_index

Now, compoze will not pull any local packages, so if you have
things that are not part of `pypi`_ you are going to need to copy
eggs for them in to the mytgapp_index directory.  For more information
on creating your own eggs please see :ref:`tgeggdeployment`.

Using Basketweaver to create the Index
---------------------------------------
easy_install requires .html files in a certain format in
order to pull down dependencies.  Basketweaver will take
a directory of eggs and do just that.  First, let's install
it::

    easy_install basketweaver

Now, lets move into our mytgapp_index dir and create the index:

    cd mytgapp_index
    makeindex *

If you list the "index" directory inside, you will see folders
for all dependent packages.  Basketweaver will also have created
an index.html for you.

Serving with Apache
---------------------

Now, copy your top-level index folder to wherever you
serve Apache files from.

Other Personal PyPI alternatives
---------------------------------

`EggBasket`_ is a TurboGears 1.0 application that provides similar
services, with a web frontend.

.. _`EggBasket`: http://www.chrisarndt.de/projects/eggbasket/

Installing from your index
---------------------------

simple. add -i http://path/to/private/index 

And `Bob's Your Uncle`_.

.. _`Bob's your Uncle`: http://en.wikipedia.org/wiki/Bob%27s_your_uncle
.. _`pypi`: http://pypi.python.org


