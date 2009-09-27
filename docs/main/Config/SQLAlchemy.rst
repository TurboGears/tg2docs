.. _saconfig:

Template rendering config settings
==================================

.. currentmodule:: tg.configuration

:Status: Official

.. contents:: Table of Contents
   :depth: 2


Though the majority of folks will use TurboGears with SQLAlchemy, there
are those who have interest in running the full stack of TG with a non-relational
database like mongodb or couchdb.  There are a few settings that allow this,
the most pertinent is: use_sqlalchemy:

``base_config.use_sqlalchemy`` -- Set to False to turn off sqlalchemy support

TurboGears takes advantage of repoze's transaction manager software.  Basically,
the transaction manager wraps each of your controller methods, and should a method
fail, the transaction will roll back.  if you utilize the transaction manager, then
the result of a successful method call results in a commit to the database.  If
the contoller method does not utilize the database, there is no database interaction
performed.  What this means is that you never have to worry about committing, or
rolling back when controller code fails, TG handles this for you automatically.

``base_config.use_transaction_manager`` -- Set to False to turn off the
Transaction Manager and handle transactions yourself.


``AppConfig`` Method Overrides
-------------------------------

.. automethod:: tg.configuration.AppConfig.setup_sqlalchemy
.. automethod:: tg.configuration.AppConfig.add_tm_middleware
