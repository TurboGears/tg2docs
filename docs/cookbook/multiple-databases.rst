.. _multidatabase:

Using Multiple SQLAlchemy Databases
===================================

TurboGears can use more than one SQLAlchemy engine in the same application.
Each engine needs its own scoped session, declarative base, and metadata. Model
classes inherit from the base for the database that stores their tables.

This guide assumes a current TurboGears 2.5 application created with the
SQLAlchemy option, for example::

    gearbox quickstart --sqlalchemy myapp

The standard SQLAlchemy configuration component configures one engine and one
session. The application below replaces that component with a small component
that configures two engines and removes both sessions at the end of each
request.

.. note::

   The two databases are independent. SQLAlchemy cannot enforce a foreign key
   between tables stored in different databases, and a query cannot transparently
   join tables through two separate engines. Keep related tables in the same
   database, or coordinate cross-database work explicitly in application code.

.. note::

   A request can use both sessions, but two engines do not make a cross-database
   write one atomic database transaction. Define the failure and retry behavior
   for operations that update both databases.

Configure the database URLs
---------------------------

The application configuration uses separate prefixes for the two engines. Keep
``sqlalchemy.url`` as an alias for the first database because the standard
``gearbox migrate`` command reads that key. The running application uses the
``first`` and ``second`` keys instead::

    [app:main]
    # Used by the migration command for the first database only.
    sqlalchemy.url = sqlite:///%(here)s/database_1.db

    sqlalchemy.first.url = sqlite:///%(here)s/database_1.db
    sqlalchemy.second.url = sqlite:///%(here)s/database_2.db
    sqlalchemy.first.echo = false
    sqlalchemy.second.echo = false

For a server database, replace each SQLite URL with that database's SQLAlchemy
URL. Do not commit credentials in an INI file; use the deployment's secret
configuration mechanism instead.

Create one session and metadata set per database
------------------------------------------------

Replace the generated SQLAlchemy setup in ``myapp/model/__init__.py`` with two
session/metadata sets. Register both scoped sessions with ``zope.sqlalchemy``
so TurboGears' transaction manager can participate in their transactions::

    """The application's SQLAlchemy model objects."""

    import zope.sqlalchemy
    from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

    maker = sessionmaker(autoflush=True)
    DBSession = scoped_session(maker)
    zope.sqlalchemy.register(DBSession)
    DeclarativeBase = declarative_base()
    metadata = DeclarativeBase.metadata

    maker2 = sessionmaker(autoflush=True)
    DBSession2 = scoped_session(maker2)
    zope.sqlalchemy.register(DBSession2)
    DeclarativeBase2 = declarative_base()
    metadata2 = DeclarativeBase2.metadata


    def init_model(engine1, engine2):
        """Bind each scoped session to its database engine."""
        DBSession.configure(bind=engine1)
        DBSession2.configure(bind=engine2)
        return DBSession, DBSession2


    # Import mapped classes after the bases and sessions exist.
    from myapp.model.spam import Spam
    from myapp.model.eggs import Eggs

    __all__ = (
        "DBSession", "DBSession2", "DeclarativeBase", "DeclarativeBase2",
        "metadata", "metadata2", "Spam", "Eggs",
    )

The generated model module may also contain authentication models. Keep those
models and import them from the base/session used by the database containing
the authentication tables.

Configure both engines
----------------------

In ``myapp/config/app_cfg.py``, subclass the current SQLAlchemy configuration
component. Its ``setup_sqlalchemy`` and ``add_middleware`` methods are the
extension points used below; ``FullStackApplicationConfigurator.replace``
replaces the built-in component without changing the rest of the application
configuration::

    from sqlalchemy import engine_from_config
    from tg import FullStackApplicationConfigurator
    from tg.configurator.components.sqlalchemy import (
        SQLAlchemyConfigurationComponent,
    )
    from tg.support.middlewares import DBSessionRemoverMiddleware

    from myapp import model


    class MultipleSQLAlchemyConfigurationComponent(
        SQLAlchemyConfigurationComponent
    ):
        """Configure two SQLAlchemy engines and their scoped sessions."""

        def setup_sqlalchemy(self, conf, app):
            engine1 = engine_from_config(conf, "sqlalchemy.first.")
            engine2 = engine_from_config(conf, "sqlalchemy.second.")

            conf["tg.app_globals"].sa_engine = engine1
            conf["tg.app_globals"].sa_engine2 = engine2

            session1, session2 = model.init_model(engine1, engine2)
            conf["SQLASession"] = session1
            conf["DBSession"] = session1
            conf["SQLASession2"] = session2
            conf["DBSession2"] = session2

        def add_middleware(self, conf, app):
            app = DBSessionRemoverMiddleware(conf["SQLASession"], app)
            return DBSessionRemoverMiddleware(conf["SQLASession2"], app)


    base_config = FullStackApplicationConfigurator()
    base_config.replace(
        "sqlalchemy", MultipleSQLAlchemyConfigurationComponent
    )

Keep the generated ``use_sqlalchemy`` and ``model`` blueprint settings, and
set the default session to the first database. For example, the relevant part
of the generated configuration is::

    base_config.update_blueprint({
        "use_sqlalchemy": True,
        "model": model,
        "DBSession": model.DBSession,
    })

The inherited component still honors ``use_sqlalchemy``; leave that option
enabled. Do not configure the same sessions through the single-engine component
as well.

Assign model classes to a database
-----------------------------------

A model's declarative base determines which metadata set is created and which
session should be used for queries. For example, ``myapp/model/spam.py`` uses
the first database::

    from sqlalchemy import Column, Integer, Unicode

    from myapp.model import DeclarativeBase


    class Spam(DeclarativeBase):
        __tablename__ = "spam"

        id = Column(Integer, primary_key=True)
        variety = Column(Unicode(50), nullable=False)

``myapp/model/eggs.py`` uses the second database::

    from sqlalchemy import Column, Integer

    from myapp.model import DeclarativeBase2


    class Eggs(DeclarativeBase2):
        __tablename__ = "eggs"

        id = Column(Integer, primary_key=True)
        package_quantity = Column(Integer, nullable=False)

Use the matching session in controllers and other application code. SQLAlchemy
objects remain associated with the session that loaded or created them; pass
identifiers or plain values between database operations rather than moving an
object directly between ``DBSession`` and ``DBSession2``::

    from sqlalchemy import select

    from myapp.model import DBSession, DBSession2, Eggs, Spam


    spam_rows = DBSession.scalars(select(Spam)).all()
    egg_rows = DBSession2.scalars(select(Eggs)).all()

Create both schemas during setup
--------------------------------

Create each metadata set against its corresponding engine in
``myapp/websetup/schema.py``. Passing the engine explicitly avoids relying on
removed or implicit metadata binding::

    from tg import config
    import transaction

    from myapp import model


    def setup_schema(command, conf, vars):
        model.metadata.create_all(bind=config["tg.app_globals"].sa_engine)
        model.metadata2.create_all(bind=config["tg.app_globals"].sa_engine2)
        transaction.commit()

If the application uses Alembic migrations, prefer migrations as the source of
production schema changes. Keep ``create_all`` in setup only when that is the
chosen behavior for a new or disposable database.

Populate each database explicitly
----------------------------------

Use the matching session when bootstrapping rows. TurboGears' transaction
manager can coordinate the registered sessions for the request, but application
code must still handle the possibility that one database operation succeeds and
the other fails::

    import transaction

    from myapp import model


    def bootstrap(command, conf, vars):
        model.DBSession.add(model.Spam(variety="Classic"))
        model.DBSession2.add(model.Eggs(package_quantity=12))
        model.DBSession.flush()
        model.DBSession2.flush()
        transaction.commit()

In a real application, make bootstrap operations safe to rerun and handle
integrity errors according to the application's startup policy.

Authentication and other extensions
-----------------------------------

Authentication tables must use the session configured for the database that
stores users, groups, and permissions. Set the authentication metadata provider
to that session instead of assuming the primary ``DBSession``. For example, a
SQLAlchemy authentication provider backed by the second database must receive
``model.DBSession2`` and the mapped user class from ``DeclarativeBase2``.

Components that assume one ``DBSession`` or one metadata object need explicit
configuration before they can work with both databases. Review admin,
authentication, search, and other extensions individually; do not expose models
from both databases through a component that expects a single session.

Migrations for both databases
-----------------------------

``gearbox migrate`` reads one ``sqlalchemy.url`` and one migration location at
a time. A multiple-database application therefore needs one migration
repository per database, and each repository's ``env.py`` must point at the
metadata for that database.

For example:

* keep ``migration/`` for the first database and leave its generated
  ``target_metadata = model.metadata`` unchanged;
* copy ``migration/`` to ``migration2/``;
* change ``migration2/env.py`` to use
  ``target_metadata = model.metadata2``;
* use a migration config whose ``[app:main]`` section sets
  ``sqlalchemy.url`` to the second database URL.

The first database can use the alias in ``development.ini``::

    gearbox migrate -c development.ini -l migration db_version
    gearbox migrate -c development.ini -l migration upgrade

For the second database, create a separate local or deployment-specific config
file such as ``database2-migrations.ini``. It needs the URL consumed by
Alembic; it does not replace the application's runtime configuration::

    [app:main]
    sqlalchemy.url = sqlite:///database_2.db

Run the second repository with that config::

    gearbox migrate -c database2-migrations.ini -l migration2 db_version
    gearbox migrate -c database2-migrations.ini -l migration2 upgrade

Keep each migration repository's revisions and schema version table separate.
Do not run a revision generated from ``model.metadata`` against the second
database when its models and metadata differ.

The generated ``websetup/schema.py`` stamps one migration repository by default.
If setup creates and stamps both databases, duplicate that stamping logic with
the second repository and its URL, or keep schema creation and migration
application as separate deployment steps. Verify both databases independently
with ``db_version`` after setup.
