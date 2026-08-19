.. _sqla_master_slave:

===========================================
SQLAlchemy Master and Read-Replica Routing
===========================================

TurboGears 2.5 includes ``BalancedSession``, a SQLAlchemy session class that
can route request-time reads to configured read replicas and route session
flushes to a master database. The database replication, failover, health
checking, and replication-lag policy remain outside TurboGears.

The configuration names the primary database ``master`` and the read replicas
``slaves``. These names are part of the TurboGears API, even when the database
team uses ``primary`` and ``replica`` for the same roles.

Prerequisites
=============

This recipe applies to a full-stack TurboGears application with SQLAlchemy
enabled. The application must use ``BalancedSession`` as the class for its
scoped SQLAlchemy session. A configuration containing master and replica URLs
is not sufficient by itself.

If the generated ``model/__init__.py`` contains a normal ``sessionmaker``,
replace the session setup with the following current SQLAlchemy-compatible
form. Keep the application's existing model imports and ``init_model``
function.

.. code-block:: python

    import zope.sqlalchemy
    from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

    from tg.configuration.sqla.balanced_session import BalancedSession

    DBSession = scoped_session(sessionmaker(class_=BalancedSession))
    zope.sqlalchemy.register(DBSession)

    DeclarativeBase = declarative_base()
    metadata = DeclarativeBase.metadata

``zope.sqlalchemy.register`` connects the scoped session to TurboGears'
transaction manager. Do not add the obsolete ``autocommit`` argument or the
old ``ZopeTransactionExtension`` session extension.

Configure the master and replicas
==================================

Set at least one master URL and one replica URL in the ``[app:main]`` section
of the application's INI file. Use the connection URL and credentials supplied
by the deployment environment; the example contains placeholders rather than
real credentials.

.. code-block:: ini

    use_sqlalchemy = true

    sqlalchemy.master.url = postgresql+psycopg://USER:PASSWORD@PRIMARY_HOST/DATABASE
    sqlalchemy.slaves.replica1.url = postgresql+psycopg://USER:PASSWORD@REPLICA_HOST/DATABASE

The ``sqlalchemy.slaves.<name>.url`` form creates a replica named ``<name>``.
The name must not be ``master``. Other SQLAlchemy engine options can use the
same prefixes, for example ``sqlalchemy.master.pool_recycle`` and
``sqlalchemy.slaves.replica1.pool_recycle``.

When ``sqlalchemy.master.url`` is present, TurboGears creates the master engine,
creates one engine for every configured ``sqlalchemy.slaves.<name>`` entry, and
requires at least one replica. The regular ``sqlalchemy.url`` setting is used
for a non-balanced application and is not needed for this configuration.

How routing works
=================

``BalancedSession.get_bind`` applies these rules:

* Unless an explicit engine constraint is active, a session flush uses the
  master engine.
* During a request, an unconstrained non-flush operation uses a randomly chosen
  configured replica.
* An explicit engine constraint takes precedence over the default routing.
* Outside a TurboGears request, or when balancing is not configured, the
  application's normal SQLAlchemy engine is used. In a balanced application
  that engine is the master.

The implementation classifies a flush, not the intent of every SQL statement.
Use an explicit master constraint for write paths that do not go through the
session's normal flush operation. Replica selection also does not provide a
read-after-write consistency guarantee; route a read to the master when its
result must include a just-committed write.

Force an entire controller action to the master
================================================

Use ``with_engine`` when every SQLAlchemy operation in a controller action must
use a particular configured engine. The decorator affects the current
TurboGears request only.

.. code-block:: python

    from sqlalchemy import select
    from tg import expose, with_engine

    from myapp.model import DBSession, User


    class AccountController:
        @expose()
        @with_engine("master")
        def current(self, user_id):
            user = DBSession.scalar(select(User).where(User.id == user_id))
            return {"user": user}

Use the exact configured replica name when deliberately selecting one:
``@with_engine("replica1")``. Prefer the master for actions that combine a
write with a consistency-sensitive read instead of depending on replica
propagation timing.

Force selected reads with a request parameter
==============================================

``master_params`` selects the master when a named controller parameter is
present and truthy. A list means that matching parameters are removed before
the controller is called. A dictionary controls whether each parameter is
removed.

.. code-block:: python

    @expose()
    @with_engine(master_params={"after_write": False})
    def detail(self, user_id, after_write=None):
        user = DBSession.scalar(select(User).where(User.id == user_id))
        return {"user": user, "after_write": after_write}

With this example, a truthy ``after_write`` value forces the master and remains
available to ``detail`` because its dictionary value is ``False``. A false or
missing value leaves the operation eligible for replica routing.

Force individual operations
============================

For code that is not a controller action, use the session's
``using_engine`` context manager. This is also useful for a small section of a
controller that must use the master while other reads may use replicas.

.. code-block:: python

    from sqlalchemy import select

    from myapp.model import DBSession, User


    with DBSession().using_engine("master"):
        users = DBSession.scalars(select(User).order_by(User.id)).all()

The constraint is restored when the context exits. Use the context around the
whole consistency-sensitive unit of work; changing the constraint does not
turn a replica into a master and does not change the database's transaction
semantics.

Sessions, transactions, and background work
============================================

TurboGears removes the configured SQLAlchemy session at the end of each web
request. Do not retain ``DBSession``'s request-local session object for use by a
later request or background task.

The full-stack configurator enables its transaction manager by default. With
``zope.sqlalchemy.register(DBSession)``, a successful request commits the
transaction and a failed request rolls it back. A SQLAlchemy transaction can
also retain the connection selected for that transaction, so replica routing
must not be treated as a per-statement consistency policy. Start a
master-constrained unit of work when the operation requires master visibility.

Code running outside a TurboGears request does not receive a request-local
``with_engine`` constraint and falls back to the master. Background jobs that
need a different explicit choice should use ``DBSession().using_engine(...)``.

Operational limits and diagnostics
==================================

TurboGears chooses replicas randomly from the configured names. The current
``BalancedSession`` does not perform replica health checks, failover, lag
measurement, or load-aware selection. Configure those concerns in the
infrastructure that provides the database endpoints.

To inspect engine choices during development, enable ``DEBUG`` logging for
``tg.configuration.sqla.balanced_session``. The session logs whether it chose
the master, a replica, or an explicitly forced engine.
