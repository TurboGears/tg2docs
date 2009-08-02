Using multiple databases in TurboGears
======================================

:Status: RoughDoc

.. contents:: Table of Contents
   :depth: 2

.. todo:: This tutorial was originally written for TG v2.0, and should be reviewed by a TG developer to make sure it is consistent with v2.1 updates

The goal of this tutorial is to configure TurboGears to use multiple databases. In this tutorial we will simply set up two different databases engines that will use db session handlers of DBSession and DBSession2, db metadata names of metadata and metadata2, and DeclarativeBase objects of DeclarativeBase and DeclarativeBase2.

Define your database urls in the [app:main] section of your .ini file(s)
------------------------------------------------------------------------

The first thing you will need to do is edit your .ini file to specify multiple url options for the sqlalchemy configuration.

In myapp/development.ini (or production.ini, or whatever.ini you are using), comment out the original sqlalchemy.url assignment and add the multiple config options::

    #sqlalchemy.url = sqlite:///%(here)s/devdata.db
    sqlalchemy.first.url = sqlite:///%(here)s/database_1.db
    sqlalchemy.second.url = sqlite:///%(here)s/database_2.db


Change the way your app loads the database engines
--------------------------------------------------

Now we need to instruct the app to load the multiple databases correctly. This requires telling base_config (in app_cfg.py) to load our own custom AppConfig with the proper multi-db assignments and a call to the model's init_model method (more on that in the next step).

In myapp/config/app_cfg.py::

    # make sure these imports are added to the top
    from tg.configuration import AppConfig, config
    from pylons import config as pylons_config
    from myapp.model import init_model

    # add this before base_config =
    class MultiDBAppConfig(AppConfig):
        def setup_sqlalchemy(self):
            """Setup SQLAlchemy database engine(s)"""
            from sqlalchemy import engine_from_config
            engine1 = engine_from_config(pylons_config, 'sqlalchemy.first.')
            engine2 = engine_from_config(pylons_config, 'sqlalchemy.second.')
            # engine1 should be assigned to sa_engine as well as your first engine's name
            config['pylons.app_globals'].sa_engine = engine1
            config['pylons.app_globals'].sa_engine_first = engine1
            config['pylons.app_globals'].sa_engine_second = engine2
            # Pass the engines to init_model, to be able to introspect tables
            init_model(engine1, engine2)

    #base_config = AppConfig()
    base_config = MultiDBAppConfig()

Update your model's __init__ to handle multiple sessions and metadata
---------------------------------------------------------------------

Switching the model's init from a single-db config to a multi-db simply means we have to duplicate our DBSession and metata assignments, and then update the init_model method to assign/configure each engine correctly.

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


Tell your models which engine to use
------------------------------------

Now that the configuration has all been taken care of, you can instruct your models to inherit from either the first or second DeclarativeBase depending on which DB engine you want it to use.

For example, in myapp/model/spam.py (uses engine1)::

    from sqlalchemy import Table, ForeignKey, Column
    from sqlalchemy.types import Integer, Unicode, Boolean
    from myapp.model import DeclarativeBase

    class Spam(DeclarativeBase):
        __tablename__ = 'spam'

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

If you needed to use the DBSession here (or in your controllers), you would use DBSession for the 1st engine and DBSession2 for the 2nd (see the previous and next sections).

Optional: Create and populate each database in websetup.py
----------------------------------------------------------

If you want your setup_app method to populate each database with data, simply use the appropriate metadata/DBSession objects as you would in a single-db setup.

In myapp/websetup.py::

    def setup_app(command, conf, vars):
        """Place any commands to setup myapp here"""
        load_environment(conf.global_conf, conf.local_conf)
        # Load the models
        from myapp import model
        print "Creating tables for engine1"
        model.metadata.create_all()
        print "Creating tables for engine2"
        model.metadata2.create_all()

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

