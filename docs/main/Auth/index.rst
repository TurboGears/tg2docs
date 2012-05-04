.. _auth_and_auth:

Authentication and Authorization in TurboGears 2
================================================

:Status: Official

This documents describes how to implement authentication and authorization in
TG 2 applications.

.. contents:: Table of Contents
    :depth: 2

Overview
--------

``Authentication`` is the act verifying that somebody is really who she claims
to be, which is normally done using credentials (e.g., when you need to access
your email, you provide the email address and your password, or if you want
to check your bank account, you'll probably have to provide you Id number and
your card's PIN). In other words, finding `who` you are.

``Authorization``, on the other hand, is the act of granting access to given
resources depending on whether you have permission to use them. For example,
allowing registered members to leave comments on a blog, or allowing your
friends to see your pictures while others cannot.
In other words, finding `what` you may do.

TurboGears 2 applications may take advantage of a robust, extendable, pluggable
and easy-to-use system for authentication and authorization suitable for nearly
all situations in fact, you may extend it to suit your needs if it doesn't,
which should be really simple in most situations. Such a system is made up of
independent components, well integrated into TurboGears:

  * :mod:`repoze.who`, a framework for ``authentication`` in WSGI applications.
    You normally don't have to care about it because by default TurboGears |version|
    applications ship all the code to set it up (as long as you had selected
    such an option when you created the project), but if you need something
    more advanced you are at the right place.

You may store your users' credentials where you want (e.g., in a database, an
LDAP server, an .htaccess file) and also store your authorization settings
in any type of source (e.g., in a database, Ini file) -- if the back-end you
need is not available, you may create it yourself (which is usually very easy).
And don't worry if you need to change the back-end afterwards: You would not
need to touch your code! Except, of course, the snippet that tells where the
data may be found.


The three pillars: Users, groups and permissions
------------------------------------------------

TurboGears uses a common pattern based on the ``users`` (authenticated
or anonymous) of your web application, the ``groups`` they belong to and the
``permissions`` granted to such groups. But you can extend it to check for many
other conditions (such as checking that the user comes from a given country,
based on her IP address, for example).

The authentication framework (:mod:`repoze.who`) only deals with the source(s)
that handle your users' credentials. It will look for a way to match
your username and password to some user on your database and check if he can
login. While the TurboGears authorization layer fetches the actual user
that logged in, its groups and permissions and permits to check for them.

Getting started, quickly
------------------------

To use authentication and authorization in a new project,
just answer "yes" during the `paster quickstart` process when it
asks you if you want authorization::

  Do you need authentication and authorization in this project? [yes]

You'll then get authentication and authorization code added for you, including
the SQLAlchemy-powered model definitions in ``{yourpackage}.model.auth``
and the relevant settings in ``{yourpackage}.config.app_cfg``. It also defines
the default users, groups and permissions in ``{yourpackage}.websetup``, which
you may want to customize.

Before trying to login and try authorization with the rows defined in
``{yourpackage}.websetup``, you have to create the database; run the following
command from your project's root directory::

    paster setup-app development.ini

Beyond the quickstart
---------------------

If you need more power than that provided by the quickstart, or if you just
want to customize some things, you may want to read the following pages:

.. toctree::
    :maxdepth: 1

    Authentication
    Authorization
    Customization
    LoginCleaner
    whoini
    OpenID
