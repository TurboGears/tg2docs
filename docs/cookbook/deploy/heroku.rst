heroku
++++++

This recipe assumes that you have a TurboGears app setup using a Paste INI file,
inside a package called 'myapp'. If you are deploying a custom TurboGears application
in minimal mode you might have to tune the following instructions.

Step 0: Install heroku
======================

Install the heroku gem `per their instructions
<http://devcenter.heroku.com/articles/quickstart>`_.

Step 1: Add files needed for heroku
===================================

You will need to add the following files with the contents as shown to the
root of your project directory (the directory containing the setup.py).

``requirements.txt``:

You can autogenerate this file by running:

.. code-block:: bash

    $ pip freeze > requirements.txt

You will have probably have a line in your requirements file that has your project name in it.
It might look like either of the following two lines depending on how you setup your project.
If either of these lines exist, **delete them**.

.. code-block:: text

    projectname=0.1dev
         or
    -e git+git@xxxx:<git username>/xxxxx.git....#egg=projectname

Now that you have properly frozen your application dependencies it is required to add
the webserver you want to use to actually serve your application requests.

This tutorial uses the *Waitress* webserver, so we need to add it to the dependencies
declared in the ``requirements.txt``

.. code-block:: bash

    $ echo "waitress" >> requirements.txt

Step 2: Editing Configuration File
====================================

As heroku passes some configuration options in ENVIRON variables, it is necessary
for our application to read them from the Heroku environment. Those are typically
the ``PORT`` where your application server has to listen, the ``URL`` of your
database and so on...

First of all we need to copy the ``development.ini`` to a ``production.ini`` file
we are going to use for the heroku deployment:

.. code-block:: bash

    $ cp development.ini production.ini

The only options you are required to change are the one related to the server.
So your ``[server:main]`` section should look like:

.. code-block:: ini

    [server:main]
    use = egg:waitress#main
    host = 0.0.0.0
    get port = heroku_port

Then probably want to disable the ``debug`` inside the ``[DEFAULT]`` section.

Step 3: Starting the application
====================================

``Procfile``:

Generate this by running:

.. code-block:: bash

    $ echo "web: ./run" > Procfile

``run``:

Create ``run`` with the following:

.. code-block:: text

    #!/bin/bash
    python setup.py develop
    gearbox serve --debug -c production.ini heroku_port=$PORT

.. note::

    Make sure to ``chmod +x run`` before continuing.
    The 'develop' step is necessary because the current package must be
    installed before paste can load it from the INI file.

.. note::

    This assumes the INI file to use is ``production.ini``, change as
    necessary. The server section of the INI will be ignored as the server
    needs to listen on the port supplied in the OS environ.

Step 4: Setup git repo and heroku app
=====================================

Navigate to your project directory (directory with setup.py) if not already there.
If you project is already under git version control, skip to the 'Initialize the heroku stack' section.

Inside your projects directory, if this project is not tracked under git it is recommended that you first create a good .gitignore file (you can skip this step). You can get the recommended python one by running:

.. code-block:: bash

    $ wget -O .gitignore https://raw.github.com/github/gitignore/master/TurboGears2.gitignore


Once that is done, run:

.. code-block:: bash

    $ git init
    $ git add .
    $ git commit -m "initial commit"

Step 5: Initialize the heroku stack
===================================

.. code-block:: bash

    $ heroku create

Step 6: Deploy
==============

To deploy a new version, push it to heroku:

.. code-block:: bash

    $ git push heroku master

Make sure to start one worker:

.. code-block:: bash

    $ heroku scale web=1

Check to see if your app is running

.. code-block:: bash

    $ heroku ps

Take a look at the logs to debug any errors if necessary:

.. code-block:: bash

    $ heroku logs -t

