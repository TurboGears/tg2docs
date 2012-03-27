.. _sqla_master_slave:

========================================
SQLAlchemy Master Slave Load Balancing
========================================

Since version 2.2 TurboGears has basic support for Master/Slave load balancing
and provides a set of utilities to use it.

TurboGears permits to declare a master server and any number of slave servers, all the
writes will automatically redirected to the master node, while the other calls will
be dispatched randomly to the slave nodes.

All the queries executed outside of TurboGears controllers will run only on the
master node, those include the queries performed by the authentication stack to
initially look up an already logged in user, its groups and permissions.

Enabling Master Slave Balancing
=================================

To enable Master Slave load Balancing you just need to edit your `model/__init__.py`
making the ``sessionmaker`` use the TurboGears BalancedSession:

.. code-block:: python

    from tg.configuration.sqla.balanced_session import BalancedSession

    maker = sessionmaker(autoflush=True, autocommit=False,
                         class_=BalancedSession,
                         extension=ZopeTransactionExtension())

Doing this by itself will suffice to make load balancing work, but still
as there is only the standard database configuration the ``BalancedSession``
will just be redirecting all the queries to the only available serve.

Configuring Balanced Nodes
==============================

To let load balancing work we must specify at least a master and slave server
inside our application configuration. The master server can be specified
using the `sqlalchemy.master` set of options, while any number of slaves
can be configured using the `sqlalchemy.slaves` options:

.. code-block:: ini

    sqlalchemy.master.url = mysql://username:password@masterhost:port/databasename
    sqlalchemy.master.pool_recycle = 3600

    sqlalchemy.slaves.slave1.url = mysql://username:password@slavehost:port/databasename
    sqlalchemy.slaves.slave1.pool_recycle = 3600

The master node can be configured also to be a slave, this is usually the
case when we want the master to also handle some read queries.

Driving the balancer
========================

TurboGears provides a set of utilities to let you change the default behavior
of the load balancer. Those include the **@with_engine(engine_name)** decorator
and the **DBSession().using_engine(engine_name)** context.

The with_engine decorator
---------------------------

The ``with_engine`` decorator permits to force a controller method to
run on a specific node. It is a great tool for ensuring that some
actions take place on the master node, like controllers that edit
content.

.. code-block:: python

    from tg import with_engine

    @expose('myproj.templates.about')
    @with_engine('master')
    def about(self):
        DBSession.query(model.User).all()
        return dict(page='about')

The previous query will be executed on the master node, if the **@with_engine**
decorator is removed it will get execute on any random slave.

The ``with_engine`` decorator can also be used to force turbogears
to use the master node when some parameters are passed by url:

.. code-block:: python

    @expose('myproj.templates.index')
    @with_engine(master_params=['m'])
    def index(self):
        DBSession.query(model.User).all()
        return dict(page='index')

In this case calling *http://localhost:8080/index* will result in queries
performed on a slave node, while calling *http://localhost:8080/index?m=1* will
force the queries to be executed on the master node.

Pay attention that the **m=1** parameter can actually have any value, it just
has to be there. This is especially useful when redirecting after an action
that just created a new item to a page that has to show the new item. Using
a parameter specified in *master_params* we can force TurboGears to fetch
the items from the master node so to avoid odd results due to data propagation
delay.

Keeping master_params around
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default parameters specified in ``with_engine`` master_params will be
popped from the controller params. This is to avoid messing with validators
or controller code that doesn't expect the parameter to exist.

If the controller actually needs to access the parameter a dictionary can be
passed to @with_engine instead of a list. The dictionary keys will be
the parameters, while the value will be if to pop it from the
parameters or not.

.. code-block:: python

    @expose('myproj.templates.index')
    @with_engine(master_params={'m':False})
    def index(self, m=None):
        DBSession.query(model.User).all()
        return dict(page='index', m=m)

Forcing Single Queries on a node
----------------------------------

Single queries can be forced to execute on a specific node using the
``using_engine`` method of the ``BalancedSession``. This method
returns a context manager, until queries are executed inside this
context they are run on the constrained engine:

.. code-block:: python

    with DBSession().using_engine('master'):
        DBSession.query(model.User).all()
        DBSession.query(model.Permission).all()
    DBSession.query(model.Group).all()

In the previous example the Users and the Permissions will be
fetched from the master node, while the Groups will be fetched
from a random slave node.

Debugging Balancing
=========================

Setting the root logger of your application to *DEBUG* will let
you see which node has been choose by the ``BalancedSession``
to perform a specific query.


