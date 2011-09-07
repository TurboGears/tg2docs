.. _ming_and_model:

Working With Ming And MongoDB
===========================================

MongoDB_ is a high-performance schemaless database that allows you
to store and retrieve JSON-like documents. MongoDB_ stores these
documents in collections, which are analogous to SQL tables.
Because MongoDB_ is schemaless, there are no guarantees given
to the database client of the format of the data that may be
returned from a query; you can put any kind of document into
a collection that you want.

While this dynamic behavior is handy in a rapid development
environment where you might delete and re-create the database
many times a day, it starts to be a problem when you need to
make guarantees of the type of data in a collection
(because you code depends on it).

Ming_ allows you to specify the schema for your data
in Python code and then develop in confidence,
knowing the format of data you get from a query.


TurboGears Integration
----------------------

TurboGears Ming integration is entirely pushed into the
generated quickstart template since version 2.1.3

To generate a Ming based project you just need to
pass the ``--ming`` option to the quickstart command.
For more informations refer to the :ref:`quickstarting` section.

TurboGears will rely on the unit of work pattern of Ming
flushing the session for you at the end of each request.
This will happen only if everything went fine.
In case of an exception the session won't be flushed
and any change performed throught the ORM layer won't
happen avoiding an incosistent environment due to
half made changes.

.. note:: Note that if you perform any change outside the
          ming unit of work or if you flush the session
          yourself you might still end with an inconsistent
          environment.

Getting Started
---------------

If you don't know how Ming_ works at all, please take a few
minutes to read over these tutorials:

* `ORM Tutorial`_ -- which covers the ORM parts
* `Intro to Ming`_ -- which covers a more general intro

Your quickstarted project will have a subpackage called `model`, made
up of the following files:

* `__init__.py`: This is where the database access is set up. Your
  collections should be imported into this module, and you're highly
  encouraged to define them in a separate module - `entities`, for
  example.
* `session.py`: This file defines the session of your database
  connection. By default TurboGears will use a Session object
  with multithreading support. You will usually need to import
  this each time you have to declare a ``MappedClass`` to
  specify the session that has to be used to perform queries.
* `auth.py`: This file will be created if you enabled authentication
  and authorization in the quickstart. It defines two collections
  :mod:`repoze.what.quickstart` relies on: `User` (for the registered
  members in your website and the groups they belong to) and `Permission`
  (a permission granted to one or more groups).

Defining Your Own Collections
---------------------------------

By default TurboGears configures Ming_ in Declarative mode.
This is similar to the SQLAlchemy declarative support and needs
each model to inherit from the ``MappedClass`` class.

The tables defined by the quickstart in `model/auth.py` are based on
the declarative method, so you may want to check it out to see how
columns are defined for these tables.
For more information, you may read the `ORM Tutorial`_.

Once you have defined your collections in a separate module in the `model`
package, they should be imported from `model/__init__.py`. So the end
of this file would look like this:

.. code-block:: python

  # Import your model modules here.
  from auth import User, Permission
  # Say you defined these three classes in the 'movies'
  # module of your 'model' package.
  from movies import Movie, Actor, Director

Indexing Support
----------------------------

TurboGears supports also automatic indexing of MongoDB_ fields.
If you want to guarantee that a field is unique or indexed you
just have to specify the ``unique_indexes`` or ``indexes`` variables
for the ``__mongometa__`` attribute of the mapped class.

.. code-block:: python

    class Permission(MappedClass):
        class __mongometa__:
            session = DBSession
            name = 'tg_permission'
            unique_indexes = [('permission_name',),]

TurboGears will ensure indexes for your each time the application
is started, this is performed inside the ``init_model`` function.

Adding More Data to Groups
----------------------------

By default the Ming support will come with models for ``User``
and ``Permission`` while the groups will be handled as a list
of group names inside the users and permissions. This reduces
the number of requests that have to be done to the the database
each time the user visits a page to detect its permissions and groups
resulting in a performance improvement.

If you want to add metadata to the groups you can use the same
solution that TurboGears Ming support uses for the permissions.
Create a ``Group`` MappedClass and put it in relation with the ``User``
the same way the ``permissions`` property of the ``User`` does for the
``Permission``.

.. code-block:: python

    class Group(MappedClass):
        class __mongometa__:
            session = DBSession
            name = 'tg_group'
            unique_indexes = [('group_name',),]

        _id = FieldProperty(s.ObjectId)
        group_name = FieldProperty(s.String)
        description = FieldProperty(s.String)

    class User(MappedClass):
        [...]

        @property
        def groups_info(self):
            return Group.query.find(dict(group_name={'$in':self.groups})).all()

.. _Intro to Ming: http://merciless.sourceforge.net/tour.html
.. _ORM Tutorial: http://merciless.sourceforge.net/orm.html
.. _MongoDB: http://www.mongodb.org
.. _Ming: http://merciless.sourceforge.net/tour.html
