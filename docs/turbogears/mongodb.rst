.. _mongodb_ming:

===================
Using MongoDB
===================

TurboGears supports MongoDB_ out of the box by using the Ming_ ORM.
Ming_ was made to look like SQLAlchemy, so if you are proficient with
SQLAlchemy and MongoDB it should be easy for you to get used to the Ming_
query language. This also makes easy to port a TurboGears SQLAlchemy based
application to MongoDB.

QuickStarting with MongoDB
===============================

To create a project using MongoDB_ you just need to pass the ``--ming``
option to the ``gearbox quickstart`` command.

.. code-block:: bash

    $ gearbox quickstart --ming

The quickstarted project will provide an authentication and authorization
layer like the one that is provided for the SQLAlchemy version. This
means that you will have the same users and groups you had on the standard
quickstarted project and also that all the predicates to check for authorization
should work like before.

The main difference is that you won't be able to use the application
without having a running MongoDB_ database on the local machine.

By default the application will try to connect to a server on port
*27017* on local machine using a database that has the same name
of your package.

This can be changed by editing the development.ini file::

    ming.url = mongodb://localhost:27017/
    ming.db = myproject

Now that everything is in place to start using MongoDB_ as your
database server you just need to proceed the usual way by filling
your database.

.. code-block:: bash

      $ gearbox setup-app

The quickstart command from above will create the authentication
collections and setup a default user/password for you::

      user: manager
      password: managepass

Working With Ming
=====================

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
=================================

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

Handling Relationships
==============================

Ming comes with support to one-to-many and many-to-one Relations_
they provide an easy to use access to related objects. The fact
that this relation is read only isn't a real issue as the related
objects will have a ``ForeignIdProperty`` which can be changed
to add or remove objects to the relation.

As MongoDB provides too many ways to express a many-to-many
relationship, those kind of relations are instead left on their own.
TurboGears anyway provides a tool to make easier to access and
modify those relationships.

``tgming.ProgrammaticRelationProperty`` provides easy access to
those relationships exposing them as a list while leaving to the
developer the flexibility to implement the relationship as it
best suites the model.

A good example of how the ProgrammaticRelationProperty works
is the ``User`` to ``Group`` relationship:

.. code-block:: python

    from tgming import ProgrammaticRelationProperty

    class Group(MappedClass):
        class __mongometa__:
            session = DBSession
            name = 'tg_group'

        group_name = FieldProperty(s.String)

    class User(MappedClass):
        class __mongometa__:
            session = DBSession
            name = 'tg_user'

        _groups = FieldProperty(s.Array(str))

        def _get_groups(self):
            return Group.query.find(dict(group_name={'$in':self._groups})).all()
        def _set_groups(self, groups):
            self._groups = [group.group_name for group in groups]
        groups = ProgrammaticRelationProperty(Group, _get_groups, _set_groups)

In this case each user will have one or more groups stored with their group_name
inside the `User._groups` array. Accessing `User.groups` will provide a list
of the groups the user is part of. This list is retrieved using `User._get_groups`
and can be set with `User._set_groups`.

Using Synonyms
========================

There are cases when you will want to adapt a value from the database
before loading and storing it. A simple example of this case is the
password field, this will probably be encrypted with some kind of
algorithm which has to be applied before saving the field itself.

To handle those cases TurboGears provides the ``tgming.SynonymProperty``
accessor. This provides a way to hook two functions which have to be
called before storing and retrieving the value to adapt it.

.. code-block:: python

    from tgming import SynonymProperty

    class User(MappedClass):
        class __mongometa__:
            session = DBSession
            name = 'tg_user'

        _password = FieldProperty(s.String)

        def _set_password(self, password):
            self._password = self._hash_password(password)
        def _get_password(self):
            return self._password
        password = SynonymProperty(_get_password, _set_password)

In the previous example the password property is stored encrypted inside the
`User._password` field but it is accessed using the `User.password` property
which encrypts it automatically before setting it.


.. _Relations: http://merciless.sourceforge.net/orm.html#relating-classes
.. _Intro to Ming: http://merciless.sourceforge.net/tour.html
.. _ORM Tutorial: http://merciless.sourceforge.net/orm.html
.. _MongoDB: http://www.mongodb.org
.. _Ming: http://merciless.sourceforge.net/tour.html