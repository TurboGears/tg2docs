.. _database_migration:

Database Schema Migrations
==============================

Since version 2.1.1 TurboGears has integrated migrations support
for each new quickstarted project.

TurboGears 2 relies on the `sqlalchemy-migrate`_ project to
automate database schema migration.

.. _sqlalchemy-migrate: http://code.google.com/p/sqlalchemy-migrate/

Getting Started
-----------------

TurboGears provides a ``gearbox migrate`` command to manage schema migration.
You can run ``gearbox migrate db_version`` to see the current version
of your schema::

    $ gearbox migrate -c development.ini db_version
    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'

    0

This is possible because when ``gearbox setup-app`` is ran
a ``migrate_version`` table is created in your database. 
This table will keep the current version
of your schema to track when applying migrations is required.

If you examine your database, you should be able to see schema version tracking
table and check what it is the current version of your schema::

    sqlite> .headers on
    sqlite> select * from migrate_version;
    repository_id|repository_path|version
    migration|migration|0

This is exactly like running the ``gearbox migrate db_version`` command, both
should tell you the same database version. In this case as we just created
the project the reported version is 0.

Note that the ``repository_id`` column should uniquely identify your
project's set of migrations.  Should you happen to deploy multiple
projects in one database, you will be able to manage multiple schema
versions by changing the ``repository_id`` variable in the
``migration/migrate.cfg`` of each project to a different value.


Integrating Migrations in the Development Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the database under version control and a repository for schema
change scripts, you are ready to begin regular development.  We will
now walk through the process of creating, testing, and applying a
change script for your current database schema.  Repeat these steps as
your data model evolves to keep your databases in sync with your
model.


Creating migrations
---------------------------------

The ``gearbox migrate script`` command will create an empty change script for you,
automatically naming it and placing it in your repository::

    $ gearbox migrate script 'Initial Schema'

The command will return by just printing the migrations repository where it is
going to create the new script::

    $ gearbox migrate script 'Initial Schema
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

    $ gearbox migrate test
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

Applying migrations
------------------------

The script is now ready to be deployed::

    $ gearbox migrate upgrade

If your database is already at the most recent revision, the command
will produce no output.  If migrations are applied, you will see 
output similar to the following::

    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'

    0 -> 1... 
    done

Keeping your websetup on sync
---------------------------------

Each time you create a new migration you should consider keeping your
websetup in sync with it. For example if you create a new table inside
a migration when you will run ``gearbox setup-app`` on a new database
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
-----------------------------

There are some cases in which downgrading your schema might be required.
In those cases you can perform the ``gearbox migrade downgrade`` command::

    $ gearbox migrate downgrade 0
    Migrations repository 'migration',
    database url 'sqlite:////private/tmp/migr/devdata.db'
    
    1 -> 0... 
    done
