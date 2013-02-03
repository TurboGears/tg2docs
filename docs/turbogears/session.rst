.. _session:

Web Session Usage
=================

:Status: Work in progress

Why Use Sessions?
-----------------

Sessions are a common way to keep simple browsing data attached to a
user's browser. This is generally used to store simple data that does
not need to be persisted in a database.

Sessions in TurboGears can be backed by the filesystem, memcache, the
database, or by hashed cookie values.  By default, cookies are used
for storing the session data, which is only good for storing very
little amounts of data in the session since all data will be sent
back and forth within the cookie. If you are storing lots of data in
the session, :ref:`Memcache <memcache>` is recommended.

.. warning::

    Using cookies for storing the whole session's content exposes
    your application to possible exploits if the attacker gets to
    know the secret key which is used for the encryption of the
    cookies. Considering this, it is probably better to use the
    filesystem storage if you don't want to set up memcache.

.. note::

    When using the filesystem backed storage, you must be aware of
    the fact, that beaker does **not** clean up the session files
    at all. You have to make sure to clean up the data directory on
    a regular basis yourself.
    Refer to the `Beaker documentation`_ for more details.

.. _Beaker documentation: http://beaker.readthedocs.org/en/latest/sessions.html#removing-expired-old-sessions

How To Use Sessions?
--------------------

If you just quickstarted a TurboGears 2 application, the session
system is pre-configured and ready to be used.

By default we are using the Beaker session system. This system is
configured to use hashed cookies for session storage.

Each time a client connects, the session middleware (Beaker) will
inspect the cookie using the cookie name we have defined in the
configuration file.

If the cookie is not found it will be set in the browser. On all
subsequent visits, the middleware will find the cookie and make use of
it.

When using the cookie based backend, all data that you put into the
session will be pickled, hashed and encrypted by the middleware 
when sending the response to the browser and vice-versa when
reading the request.

In the other backends, the cookie only contains a large random key
that was set at the first visit and has been associated behind the
scenes to a file in the file system cache. This key is then used to
lookup and retrieve the session data from the proper datastore.

OK, enough with theory! Let's get to some real life (sort of)
examples.  Open up your root controller and add the following import
at the top the file:

.. code-block:: python

    from tg import session

What you get is a Session instance that is always request-local, in
other words, it's the session for this particular user.  The session
can be manipulated in much the same way as a standard python
dictionary.

Here is how you search for a key in the session:

.. code-block:: python

    if session.get('mysuperkey', None):
        # do something intelligent
        pass

and here is how to set a key in the session:

.. code-block:: python

    session['mysuperkey'] = 'some python data I need to store'
    session.save()

You should note that you need to explicitly save the session in order for your
keys to be stored in the session.

You can delete all user session with the `delete()` method of the
session object:

.. code-block:: python

    session.delete()

Even though it's not customary to delete all user sessions on a production
environment, you will typically do it for cleaning up after
usability or functional tests.

Avoid automatic session extension
-----------------------------------

TurboGears by default automatically extends session life time
at every request if a session is already available. You can
avoid this behavior by changing your application configuration

.. code-block:: python

    beaker.session.tg_avoid_touch = true

This will also prevent TurboGears from causing an automatic
session save at every request.
