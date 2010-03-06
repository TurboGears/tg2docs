.. _deploy_db:

Deploy a Production Database
=============================

Most production sites will use a dedicated database server rather than
relying on the in-process SQLite engine.  Dedicated servers are generally
better able to handle multiple simultaneous clients, are more robust,
and can be split onto dedicated machines to increase performance.

The subject of installing, managing and configuring database servers
is *far* outside the scope of this document.  There are many books,
courses, and diplomas available on DB administration.  This document's
purpose is to serve as a quick-reference that lets you get started
quickly with setting up common database servers for use with
TurboGears.

.. warning::

   Keep in mind, a database server is a server process running on your
   network.  As such, you should treat it as a potential source of
   security failures.  You need to keep your DB server up-to-date and
   use strong passwords for all accounts, *even* if you only expose the
   DB on a "trusted" port.

.. _deploy_postgresql:

PostgreSQL
-----------

PostgreSQL is a mature, robust, efficient ACID database server.  It
is available for all major platforms, and has GUI administrative tools
(though almost all "serious" users use the robust command-line tools).

PostgreSQL is very well packaged on most Linux distributions, generally
the packages will automatically create a default `database cluster`
so that all you need to do is to create a user and a database, then
configure your application to use that database:

.. code-block:: bash

    $ sudo aptitude install postgresql
    $ sudo -u postgres createuser
    # interactive questions here, including password
    # your user doesn't need any particular permissions
    $ sudo -u postgres createdb --owner=username databasename

at this point you have a database server and a user account that can
access (just) the one database you've created.  If you want, you can
test the database using the command-line psql client from PostgreSQL:

.. code-block:: bash

    $ psql -U username -h localhost databasename
    (realtime-tut)$ psql -U username -h localhost databasename
    Password for user username:
    Welcome to psql 8.3.8, the PostgreSQL interactive terminal.

    Type:  \copyright for distribution terms
           \h for help with SQL commands
           \? for help with psql commands
           \g or terminate with semicolon to execute query
           \q to quit

    SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)

    databasename=>\q

You can type SQL statements (followed by a ; and a return) to execute
them immediately against your database.

.. warning::

    Keep in mind, it is *easy* to lose data if you issue the wrong
    command in psql!  This is a raw connection to the database and
    you are logged in as the owner of the database.

Once you are satisfied that your database is defined and accessible,
you alter your production.ini file.  The SQLAlchemy URL should point
at the database you've created:

.. code-block:: ini

    # sqlalchemy.url = sqlite:///%(here)s/devdata.db
    sqlalchemy.url = postgres://username:password@hostname:port/databasename

.. warning::

   Your corporate policies may preclude developers having access
   to the username/passwords of production sites. In this case, do *not*
   check the production.ini file into your development repository, instead
   check it into your configuration-management database (e.g. etckeeper),
   and restrict the file's read permissions as appropriate to allow only the
   server process to read it.

You need to add a PostgreSQL database driver to  your VirtualEnv to
be able to access the server:

.. code-block:: bash

    (tg2env)$ easy_install psycopg2

Now you can initialize your application's database:

.. code-block:: bash

    (tg2env)$ paster setup-app production.ini
    (tg2env)$ paster serve production.ini

Obviously this is only scratching the surface of PostgreSQL installation
and maintenance.  For further information:

* `The PostgreSQL Docs`_ -- PostgreSQL is extremely well documented, most of the
  time any question you are likely to have has already been answered in the
  official documentation.

.. _`The PostgreSQL Docs`: http://www.postgresql.org/docs/8.4/interactive/index.html

.. todo:: Document setup of MySQL
.. todo:: Document setup of MongoDB
.. todo:: Document setup of Oracle (low priority)
.. todo:: Document setup of MSSQL (low priority)

What's Next?
-------------

* :ref:`deploy_standard` -- if you are deploying your application, you likely want
  to continue working through the standard deployment pattern
