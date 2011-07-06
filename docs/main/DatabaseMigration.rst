.. _database_migration:

Database Schema Migrations
==============================

Since version 2.1.1 TurboGears has integrated migrations support
for each new quickstarted project. For previous versions or to
manually manage migrations please refer to :ref:`manual_database_migration`

TurboGears 2 relies on the `sqlalchemy-migrate`_ project to
automate database schema migration.

.. _sqlalchemy-migrate: http://code.google.com/p/sqlalchemy-migrate/

Prerequisites
-------------

This document assumes that you have an existing **TurboGears >= 2.1.1** project
that uses the built-in support for SQLAlchemy.  If you
are not yet at that stage, you may want to review the following:

* :ref:`quickstarting`
* :ref:`sqlalchemy_and_model`

Additionally, it is assumed that you have reached a point in the
development life cycle where a change must be made to your current data
model. This could mean adding a column to an existing table, adding a
table, removing a table, or any number of other database schema
changes.

The examples in this document will be based on the :ref:`wiki20`, but
the information applies to any TurboGears 2 project.

Getting Started
---------------

TurboGears provides a ``paster migrate`` command to manage schema migration.
You can run ``paster migrate db_version`` to see the current version
of your schema::

    $ paster migrate -c development.ini db_version
    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'

    0

This is possible because when ``paster setup-app development.ini`` is ran 
a ``migrate_version`` table is created in your database. 
This table will keep the current version
of your schema to track when applying migrations is required.

If you examine your database, you should be able to see schema version tracking
table and check what it is the current version of your schema::

    sqlite> .headers on
    sqlite> select * from migrate_version;
    repository_id|repository_path|version
    migration|migration|0

This is exactly like running the ``paster migrate db_version`` command, both
should tell you the same database version. In this case as we just created
the project the reported version is 0.

Note that the ``repository_id`` column should uniquely identify your
project's set of migrations.  Should you happen to deploy multiple
projects in one database, you will be able to manage multiple schema
versions by changing the ``repository_id`` variable in the
``migration/migrate.cfg`` of each project to a different value.


Integrating Migrations in the Development Process
----------------------------------------------------------

With the database under version control and a repository for schema
change scripts, you are ready to begin regular development.  We will
now walk through the process of creating, testing, and applying a
change script for your current database schema.  Repeat these steps as
your data model evolves to keep your databases in sync with your
model.


Create Your First Change Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``paster migrate script`` command will create an empty change script for you,
automatically naming it and placing it in your repository::

    $ paster migrate script 'Initial Schema'

The command will return by just printing the migrations repository where it is
going to create the new script::

    $ paster migrate script 'Initial Schema
    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'

    $ ls migration/versions
    001_Initial_Schema.py __init__.py

Edit the Script
~~~~~~~~~~~~~~~

Each change script provides an ``upgrade`` and ``downgrade`` method, and
we implement those methods by creating and dropping the ``pages_table``
respectively::

    from sqlalchemy import *
    from migrate import *

    metadata = MetaData()
    pages_table = Table("pages", metadata,
                        Column("id", Integer, primary_key=True),
                        Column("pagename", Text, unique=True),
                        Column("data", Text)
                        )


    def upgrade(migrate_engine):
        # Upgrade operations go here. Don't create your own engine; use the engine
        # named 'migrate_engine' imported from migrate.
        metadata.bind = migrate_engine
        pages_table.create()

    def downgrade(migrate_engine):
        # Operations to reverse the above upgrade go here.
        metadata.bind = migrate_engine
        pages_table.drop()

Test the Script
~~~~~~~~~~~~~~~

Anyone who has experienced a failed schema upgrade on a production
database knows how uniquely uncomfortable that situation can be.
Although testing a new change script is optional, it is clearly a good
idea.  After you execute the following test command, you will ideally be
successful::

    $ paster migrate test
    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'
    
    Upgrading...
    done
    Downgrading...
    done
    Success

If you receive an error while testing your script, one of two issues
is probably the cause:

* There is a bug in the script
* You are testing a script that conflicts with the schema as it currently exists.

If there is a bug in your change script, you can fix the bug and rerun
the test.

Deploy the Script
~~~~~~~~~~~~~~~~~

The script is now ready to be deployed::

    $ paster migrate upgrade

If your database is already at the most recent revision, the command
will produce no output.  If migrations are applied, you will see 
output similar to the following::

    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'

    0 -> 1... 
    done

Keeping your websetup on sync
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each time you create a new migration you should consider keeping your
websetup in sync with it. For example if you create a new table inside
a migration when you will run ``paster setup-app`` on a new database
it will already have the new table as you probably declared it in your
model too but the migrations version will be 0. So trying to run any
migration will probably crash due to the existing table.

To prevent this your ``websetup`` script should always initialize the
database in the same state where it would be after applying all the
available migrations. To ensure this you will have to add at the end
of the ``websetup/bootstrap.py`` script a pool of commands to set the
schema version to the last one::

    from migrate.versioning.schema import ControlledSchema
    schema = ControlledSchema(config['pylons.app_globals'].sa_engine, 'migration')
    print 'Setting database version to %s' % schema.repository.latest
    schema.update_repository_table(0, schema.repository.latest)

Downgrading your schema
~~~~~~~~~~~~~~~~~~~~~~~~~~

There are some cases in which downgrading your schema might be required.
In those cases you can perform the ``paster migrade downgrade`` command::

    $ paster migrate downgrade 0
    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'
    
    1 -> 0... 
    done

Additional Information and Help
-------------------------------

* The `sqlalchemy-migrate documentation`_.
* The `TurboGears SQLAlchemy documentation`_.

Many of the sqlalchemy-migrate developers are on the SQLAlchemy
mailing list.  Problems integrating sqlalchemy-migrate into a
TurboGears project should be sent to the `TurboGears mailing list`_.

.. _`sqlalchemy-migrate documentation`: http://code.google.com/p/sqlalchemy-migrate/w/list
.. _`TurboGears SQLAlchemy documentation`: http://turbogears.org/2.1/docs/main/SQLAlchemy.html
.. _`TurboGears mailing list`: http://groups.google.com/group/turbogears
