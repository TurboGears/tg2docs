.. _multidatabase:

Using both SQLAlchemy and MongoDB
=================================

TurboGears since version 2.3.8 allows to enable both Ming and SQLAlchemy into
the same project. This can be achieved by specifying both the ``use_ming=True``
and ``use_sqlalchemy=True`` options in configuration.

By Default the *SQLAlchemy* session is considered the primary and is installed as
``config['DBSession']`` unless it's explicitly set in configuration. When a new
project is created, the quickstart will automatically set this according to the
``--ming`` or ``--sqlalchemy`` option, so you usually are ensured that the primary
database is the one you quickstarted the project with.

Both databases will call ``model.init_model`` with their engine, according to the
engine type you can take proper action and return the right database session.

To configure both Ming and SQLAlchemy sessions your ``model/__init__.py``
will probably look like::

    from sqlalchemy.engine import Engine

    # SQLAlchemy Configuration
    from zope.sqlalchemy import ZopeTransactionExtension
    from sqlalchemy.orm import scoped_session, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    maker = sessionmaker(autoflush=True, autocommit=False,
                         extension=ZopeTransactionExtension())
    DBSession = scoped_session(maker)
    DeclarativeBase = declarative_base()
    metadata = DeclarativeBase.metadata

    # Ming Configuration
    from ming import Session
    from ming.orm import ThreadLocalORMSession

    mingsession = Session()
    ODMSession = ThreadLocalORMSession(mingsession)

    def init_model(engine):
        if isinstance(engine, Engine):
            # SQLAlchemy
            DBSession.configure(bind=engine)
            return DBSession
        else:
            # Ming
            mingsession.bind = engine
            return ODMSession

The returned session will be available as ``config['MingSession']`` and ``config['SQLASession']``
according to the initialized engine. You just have to ensure your models use the right session.

Using Multiple Databases In TurboGears
======================================

:Status: RoughDoc

.. contents:: Table of Contents
   :depth: 2

The goal of this tutorial is to configure TurboGears to use multiple
databases. In this tutorial we will simply set up two different
databases engines that will use db session handlers of DBSession and
DBSession2, db metadata names of metadata and metadata2, and
DeclarativeBase objects of DeclarativeBase and DeclarativeBase2.

.. note::

   When using multiple databases you won't be able to create relations
   (foreign keys) between tables on two different databases.

.. note::

   Most plugins and extensions will take for granted that you have
   a single database connection, and might not work properly when multiple
   databases are used.

Define your database urls in the [app:main] section of your .ini file(s)
------------------------------------------------------------------------

The first thing you will need to do is edit your .ini file to specify
multiple url options for the sqlalchemy configuration.

In myapp/development.ini (or production.ini, or whatever.ini you are
using), comment out the original ``sqlalchemy.url`` assignment and add the
multiple config options::

    # We need two different connection URLs for the two engines,
    # so we comment the default one to avoid unexpected usages.
    # sqlalchemy.url = sqlite:///%(here)s/devdata.db

    sqlalchemy.first.url = sqlite:///%(here)s/database_1.db
    sqlalchemy.second.url = sqlite:///%(here)s/database_2.db

Change The Way Your App Loads The Database Engines
--------------------------------------------------

Now we need to instruct the app configurator to load the multiple databases
correctly. This requires telling the configurator (in app_cfg.py) to use
our own custom SQLAlchemy component with the proper multi-db assignments and a
call to the model's init_model method (more on that in the next step).

In myapp/config/app_cfg.py::

    from tg.configurator.components.sqlalchemy import SQLAlchemyConfigurationComponent
    class CustomSQLAComponent(SQLAlchemyConfigurationComponent):
        def setup_sqlalchemy(self, conf, app):
            from sqlalchemy import engine_from_config
            engine1 = engine_from_config(conf, 'sqlalchemy.first.')
            engine2 = engine_from_config(conf, 'sqlalchemy.second.')

            # We will consider engine1 the "default" engine
            conf['tg.app_globals'].sa_engine = engine1
            conf['tg.app_globals'].sa_engine2 = engine2

            # Pass the engines to init_model, to be able to introspect tables
            model.init_model(engine1, engine2)
            conf['SQLASession'] = conf['DBSession'] = model.DBSession
            conf['SQLASession2'] = conf['DBSession2'] = model.DBSession2

        def add_middleware(self, conf, app):
            # We need to ensure that both sessions are closed at the end of a request.
            from tg.support.middlewares import DBSessionRemoverMiddleware
            dbsession = conf.get('SQLASession')
            app = DBSessionRemoverMiddleware(dbsession, app)
            dbsession2 = conf.get('SQLASession2')
            app = DBSessionRemoverMiddleware(dbsession2, app)
            return app

    # Here is where the standard configurator is created.
    base_config = FullStackApplicationConfigurator()

    # And here we replace the default SQLAlchemy component
    # with our custom one.
    base_config.replace('sqlalchemy', CustomSQLAComponent)

Update Your Model's __init__ To Handle Multiple Sessions And Metadata
---------------------------------------------------------------------

Switching the model's init from a single-db config to a multi-db
simply means we have to duplicate our DBSession and metata
assignments, and then update the init_model method to assign/configure
each engine correctly.

In myapp/model/__init__.py::

   # after the first maker/DBSession assignment, add a 2nd one
   maker2 = sessionmaker(autoflush=True, autocommit=False,
                      extension=ZopeTransactionExtension())
   DBSession2 = scoped_session(maker2)

   # after the first DeclarativeBase assignment, add a 2nd one
   DeclarativeBase2 = declarative_base()

   # uncomment the metadata2 line and assign it to DeclarativeBase2.metadata
   metadata2 = DeclarativeBase2.metadata



   # finally, modify the init_model method to allow both engines to be passed (see previous step)
   # and assign the sessions and metadata to each engine
   def init_model(engine1, engine2):
     """Call me before using any of the tables or classes in the model."""

      #    DBSession.configure(bind=engine)
      DBSession.configure(bind=engine1)
      DBSession2.configure(bind=engine2)

      metadata.bind = engine1
      metadata2.bind = engine2


Tell Your Models Which Engine To Use
------------------------------------

Now that the configuration has all been taken care of, you can
instruct your models to inherit from either the first or second
DeclarativeBase depending on which DB engine you want it to use.

For example, in myapp/model/spam.py (uses engine1)::

    from sqlalchemy import Table, ForeignKey, Column
    from sqlalchemy.types import Integer, Unicode, Boolean
    from myapp.model import DeclarativeBase

    class Spam(DeclarativeBase):
        __tablename__ = 'spam'

        def __init__(self, id, variety):
            self.id = id
            self.variety = variety

        id = Column(Integer, autoincrement=True, primary_key=True)
        variety = Column(Unicode(50), nullable=False)

And then in myapp/model/eggs.py (uses engine2)::

    from sqlalchemy import Table, ForeignKey, Column
    from sqlalchemy.types import Integer, Unicode, Boolean
    from myapp.model import DeclarativeBase2

    class Eggs(DeclarativeBase2):
        __tablename__ = 'eggs'

        def __init__(self, id, pkg_qty):
            self.id = id
            self.pkg_qty = pkg_qty

        id = Column(Integer, autoincrement=True, primary_key=True)
        pkg_qty = Column(Integer, default=12)

If you needed to use the DBSession here (or in your controllers), you
would use DBSession for the 1st engine and DBSession2 for the 2nd (see
the previous and next sections).

Create And Populate Each Database In Websetup
---------------------------------------------

If you want your setup_app method to populate each database with data,
simply use the appropriate metadata/DBSession objects as you would in
a single-db setup.

In myapp/websetup/schema.py::

   def setup_schema(command, conf, vars):
       from tgmultidb import model
       print("Creating tables")
       model.metadata.create_all(bind=config['tg.app_globals'].sa_engine)
       model.metadata2.create_all(bind=config['tg.app_globals'].sa_engine2)
       transaction.commit()

In myapp/websetup/bootstrap.py::

   def setup_app(command, conf, vars):
      from sqlalchemy.exc import IntegrityError
      try:
        # populate spam table
        spam = [model.Spam(1, u'Classic'), model.Spam(2, u'Golden Honey Grail')]
        # DBSession is bound to the spam table
        model.DBSession.add_all(spam)

        # populate eggs table
        eggs = [model.Eggs(1, 12), model.Eggs(2, 6)]
        # DBSession2 is bound to the eggs table
        model.DBSession2.add_all(eggs)

        model.DBSession.flush()
        model.DBSession2.flush()
        transaction.commit()
        print "Successfully setup"
      except IntegrityError:
         print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
         import traceback
         print(traceback.format_exc())
         transaction.abort()
         print('Continuing with bootstrapping...')

Additional Support
------------------

There are some additional features that TurboGears2 provides out of
the box for single databases that might require change when multiple
DBs are involved.

Authentication
~~~~~~~~~~~~~~

Your User/Group/Permission and support tables usually need to
be all in the same database. In case this database is not the
one managed by primary ``DeclarativeBase`` and primary ``DBSession``
you need to provide to ``base_config.sa_auth.dbsession`` the
right session.

Admin
~~~~~

The default turbogears admin is mounted to handle all the models
through ``DBSession``. If you moved any mode to ``DBSession2`` you
will have to accordingly configure two admins::

   class RootController(BaseController):
       admin = AdminController([model.Spam], DBSession, config_type=TGAdminConfig)
       admin2 = AdminController([model.Eggs], DBSession2, config_type=TGAdminConfig)

Migrations
~~~~~~~~~~

Code in myapp/websetup/schema.py that initializes the migrations
will have to be duplicated to allow migrations for both DB1 and DB2::

    print('Initializing Primary Migrations')
    import alembic.config
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "migration1")
    alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.first.url'])
    import alembic.command
    alembic.command.stamp(alembic_cfg, "head")

    print('Initializing Secondary Migrations')
    import alembic.config
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "migration2")
    alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.second.url'])
    import alembic.command
    alembic.command.stamp(alembic_cfg, "head")

You will need also to provide two different migration repositories for the two
db. The easiest way is usually to take the ``migration`` directory and rename
it to ``migration1`` and ``migration2``, then make sure to update references
to ``sqlchemy.`` inside the two directories ``migration1/env.py`` and ``migration2/env.py``
so that they point to ``sqlalchemy.first.`` and ``sqlalchemy.second.``.

You can then choose for which database run the migrations by providing the
``--location`` option to ``gearbox migrate`` command::

   $ gearbox migrate -l migration1 db_version
   198f81ba8170 (head)
   $ gearbox migrate -l migration2 db_version
   350269a5537c (head)


