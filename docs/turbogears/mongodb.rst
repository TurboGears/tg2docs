.. _mongodb_ming:

=============
Using MongoDB
=============

TurboGears supports MongoDB_ out of the box by using the Ming_ ORM.
Ming_ was made to look like SQLAlchemy, so if you are proficient with
SQLAlchemy and MongoDB it should be easy for you to get used to the Ming_
query language. This also makes easy to port a TurboGears SQLAlchemy based
application to MongoDB.

QuickStarting with MongoDB
==========================

To create a project using MongoDB_ you just need to pass the ``--ming``
option to the ``gearbox quickstart`` command.

.. code-block:: bash

    $ gearbox quickstart --ming myproj

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

    ming.url = mongodb://localhost:27017/myproject

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
=================

If you don't know how Ming_ works at all, please take a few
minutes to read over the Ming_ documentation as this documentation
will only cover Ming integration with TurboGears.

Your quickstarted project will have a subpackage called `model`, made
up of the following files:

* `__init__.py`: This is where the database access is set up. Your
  collections should be imported into this module, and you're highly
  encouraged to define them in a separate module - `entities`, for
  example.
* `session.py`: This file defines the session of your database
  connection. By default TurboGears will use a Session object
  with multi-threading support. You will usually need to import
  this each time you have to declare a ``MappedClass`` to
  specify the session that has to be used to perform queries.
* `auth.py`: This file will be created if you enabled authentication
  and authorization in the quickstart. It defines three collections
  :mod:`repoze.who` relies on: ``User`` (for the registered
  members in your website and the groups they belong to), ``Group``
  (for groups of users) and ``Permission`` (a permission granted
  to one or more groups).

Defining Your Own Collections
=============================

By default TurboGears configures Ming_ in Declarative mode.
This is similar to the SQLAlchemy declarative support and needs
each model to inherit from the ``MappedClass`` class.

The tables defined by the quickstart in `model/auth.py` are based on
the declarative method, so you may want to check it out to see how
columns are defined for these tables.

To see how to define your models refer to Ming UserGuide_

Once you have defined your collections in a separate module in the ``model``
package, they should be imported from ``model/__init__.py``. So the end
of this file would look like this:

.. code-block:: python

  # Import your model modules here.
  from auth import User, Permission
  # Say you defined these three classes in the 'movies'
  # module of your 'model' package.
  from movies import Movie, Actor, Director

Indexing Support
----------------

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

Indexes are covered in detail in Ming Indexing_ Documentation.

Handling Relationships
======================

Ming comes with support to one-to-many, many-to-one and many-to-many
Relations_ they provide an easy to use access to related objects.
The fact that this relation is read only isn't a real issue as the
related objects will have a ``ForeignIdProperty`` which can be changed
to add or remove objects to the relation.

TurboGears comes with a bunc of Many-to-Many relations already defined
so you can see them in action in the ``Permission`` and ``Group`` classes:

.. code-block:: python

    class Group(MappedClass):
        """
        Group definition.
        """
        class __mongometa__:
            session = DBSession
            name = 'tg_group'
            unique_indexes = [('group_name',),]

        _id = FieldProperty(s.ObjectId)
        group_name = FieldProperty(s.String)
        display_name = FieldProperty(s.String)

        permissions = RelationProperty('Permission')

    class Permission(MappedClass):
        """
        Permission definition.
        """
        class __mongometa__:
            session = DBSession
            name = 'tg_permission'
            unique_indexes = [('permission_name',),]

        _id = FieldProperty(s.ObjectId)
        permission_name = FieldProperty(s.String)
        description = FieldProperty(s.String)

        _groups = ForeignIdProperty(Group, uselist=True)
        groups = RelationProperty(Group)

You can see the ``permissions`` and ``groups`` properties that provide
the interface to the relation and the ``_groups`` property that stores
ids of groups related to each Permission in a mongodb array.

In this case each user will have one or more groups stored with their group_name
inside the `Permission._groups` array. Accessing `Permission.groups` will provide a list
of the groups the user is part of.

For a complete coverage of Relationships with Ming refer to Ming Relations_ guide.

Custom Properties
=================

There are cases when you will want to adapt a value from the database
before loading and storing it. A simple example of this case is the
password field, this will probably be encrypted with some kind of
algorithm which has to be applied before saving the field itself.

To handle those cases TurboGears Ming allows subclassing field property
to declare CustomProperties_. This provides a way to hook two functions
which have to be called before storing and retrieving the value to adapt it
through Python Descriptors Protocol:

.. code-block:: python

    class PasswordProperty(FieldProperty):
        @classmethod
        def _hash_password(cls, password):
            salt = sha256()
            salt.update(os.urandom(60))
            salt = salt.hexdigest()

            hash = sha256()
            # Make sure password is a str because we cannot hash unicode objects
            hash.update((password + salt).encode('utf-8'))
            hash = hash.hexdigest()

            password = salt + hash

            # Make sure the hashed password is a unicode object at the end of the
            # process because SQLAlchemy _wants_ unicode objects for Unicode cols
            password = password.decode('utf-8')

            return password

        def __set__(self, instance, value):
            value = self._hash_password(value)
            return FieldProperty.__set__(self, instance, value)

In the previous example the password property automatically hashed
each time a new value is assigned to the property. That is performed
by ``PasswordProperty.__set__`` which calls ``_hash_password`` before
calling ``FieldProperty.__set__`` which actually saves the password.

For additional details on working with custom properties refer to
CustomProperties_ Ming Documentation.


.. _Relations: http://merciless.sourceforge.net/userguide.html#relating-classes
.. _MongoDB: http://www.mongodb.org
.. _Ming: http://merciless.sourceforge.net/
.. _UserGuide: http://merciless.sourceforge.net/userguide.html#mapped-classes-and-documents
.. _Indexing: http://merciless.sourceforge.net/mongodb_indexes.html
.. _CustomProperties: http://merciless.sourceforge.net/custom_properties.html