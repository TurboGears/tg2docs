.. _database_migration:

Database Schema Migrations
==============================

Since version 2.1.1 TurboGears has integrated migrations support
for each new quickstarted project.

TurboGears 2.3 and newer rely on the `alembic`_ project to
automate database schema migration.

.. _alembic: http://alembic.readthedocs.io/en/latest/

Getting Started
-----------------

TurboGears provides a ``gearbox migrate`` command to manage schema migration.
You can run ``gearbox migrate db_version`` to see the current version
of your schema::

    $ gearbox migrate -c development.ini db_version
    Context impl SQLiteImpl.
    Will assume transactional DDL.
    Current revision for sqlite:////tmp/migr/devdata.db: None

By default the database version is ``None`` until a migration is applied.
The first time a migration is applied the ``migrate_version`` table is
created. This table will keep the current version
of your schema to track when applying migrations is required.

If you examine your database, you should be able to see schema version tracking
table and check what it is the current version of your schema::

    sqlite> .headers on
    sqlite> select * from migrate_version;
    version_num
    4681af2393c8

This is exactly like running the ``gearbox migrate db_version`` command, both
should tell you the same database version.
In this case the reported version is 4681af2393c8.

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

    $ gearbox migrate create 'Initial Schema'

The command will return by just printing the migrations repository where it is
going to create the new script::

    $ gearbox migrate create 'Initial Schema'
        Generating /tmp/migr/migration/versions/2a3f515bad0_initial_schema.py... done

    $ ls migration/versions
    2a3f515bad0_this_is_an_example.py

Edit the Script
~~~~~~~~~~~~~~~

Each change script provides an ``upgrade`` and ``downgrade`` method, and
we implement those methods by creating and dropping the ``account`` table
respectively::

    revision = '2a3f515bad0'
    down_revision = '4681af2393c8'

    from alembic import op
    import sqlalchemy as sa

    def upgrade():
        op.create_table(
            'account',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('description', sa.Unicode(200)),
        )

    def downgrade():
        op.drop_table('account')

Test the Script
~~~~~~~~~~~~~~~

Anyone who has experienced a failed schema upgrade on a production
database knows how uniquely uncomfortable that situation can be.
Although testing a new change script is optional, it is clearly a good
idea.  After you execute the following test command, you will ideally be
successful::

    $ gearbox migrate test
    Context impl SQLiteImpl.
    Will assume transactional DDL.
    Running upgrade 4681af2393c8 -> 2a3f515bad0
    Context impl SQLiteImpl.
    Will assume transactional DDL.
    Running downgrade 2a3f515bad0 -> 4681af2393c8

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

    Context impl SQLiteImpl.
    Will assume transactional DDL.
    Running upgrade 4681af2393c8 -> 2a3f515bad0

Keeping your websetup on sync
---------------------------------

Each time you create a new migration you should consider keeping your
websetup in sync with it. For example if you create a new table inside
a migration when you will run ``gearbox setup-app`` on a new database
it will already have the new table as you probably declared it in your
model too but the migrations version will be ``None``. So trying to run any
migration will probably crash due to the existing tables.

To prevent this your ``websetup`` script should always initialize the
database in the same state where it would be after applying all the
available migrations. To ensure this you will have to add at the end
of the ``websetup/schema.py`` script a pool of commands to set the
schema version to the last one::

    import alembic.config, alembic.command
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "migration")
    alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.url'])
    alembic.command.stamp(alembic_cfg, "head")

Downgrading your schema
-----------------------------

There are some cases in which downgrading your schema might be required.
In those cases you can perform the ``gearbox migrate downgrade`` command::

    $ gearbox migrate downgrade
    Context impl SQLiteImpl.
    Will assume transactional DDL.
    Running downgrade 2a3f515bad0 -> 4681af2393c8
