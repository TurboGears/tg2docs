****************************************************************
Authentication in TurboGears 2 applications
****************************************************************

This document describes how :mod:`repoze.who` is integrated into TurboGears
and how you make get started with it. For more information, you may want
to check :mod:`repoze.who`'s website.

:mod:`repoze.who` is a powerful and extensible ``authentication`` package for
arbitrary WSGI applications. By default TurboGears2 configures it to log using
a form and retrieving the user informations through the user_name field of the
User class. This is made possible by the ``authenticator plugin`` that TurboGears2
uses by default which is ``repoze.who.plugins.sa.SQLAlchemyAuthenticatorPlugin``.

How it works in TurboGears
============================

The authentication layer it's a WSGI middleware which is able to authenticate
the user through the method you want (e.g., LDAP or HTTP authentication),
"remember" the user in future requests and log the user out.

You can customize the interaction with the user through four kinds of
`plugins`, sorted by the order in which they are run on each request:

* An ``identifier plugin``, with no action required on the user's side, is able
  to tell whether it's possible to authenticate the user (e.g., if it finds
  HTTP Authentication headers in the HTTP request). If so, it will extract the
  data required for the authentication (e.g., username and password, or a
  session cookie). There may be many identifiers and :mod:`repoze.who` will run
  each of them until one finds the required data to authenticate the user.
* If at least one of the identifiers could find data necessary to authenticate
  the current user, then an ``authenticator plugin`` will try to use the
  extracted data to authenticate the user. There may be many authenticators
  and :mod:`repoze.who` will run each of them until one authenticates the user.
* When the user tries to access a protected area or the login page, a
  ``challenger plugin`` will come up to request an action from the user (e.g.,
  enter a user name and password and then submit the form). The user's response
  will start another request on the application, which should be caught by
  an `identifier` to extract the login data and then such data will be used
  by the `authenticator`.
* For authenticated users, :mod:`repoze.who` provides the ability to load
  related data (e.g., real name, email) in the WSGI environment so that it can
  be easily used in the application. Such a functionality is provided by
  so-called ``metadata provider plugins``. There may be many metadata providers
  and :mod:`repoze.who` will run them all.

When :mod:`repoze.who` needs to store data about the authenticated user in the
WSGI environment, it uses its ``repoze.who.identity`` key, which can be
accessed using the code below::

    from tg import request

    # The authenticated user's data kept by repoze.who:
    identity = request.environ.get('repoze.who.identity')

Such a value is a dictionary and is often called "the identity dict". It will
only be defined if the current user has been authenticated.


There is a short-cut to the code above in the WSGI ``request``, which will
be defined in ``{yourproject}.lib.base.BaseController`` if you enabled
authentication and authorization when you created the project.

For example, to check whether the user has been authenticated you may
use:

.. code-block:: python

    # ...
    from tg import request
    # ...
    if request.identity:
        flash('You are authenticated!')

 ``request.identity`` will equal to ``None`` if the user has not been
 authenticated.

 Likewise, this short-cut is also set in the template context as
 ``tg.identity``.

The username will be available in ``identity['repoze.who.userid']``
(or ``request.identity['repoze.who.userid']``, depending on the method you
select).

The FastFormPlugin
----------------------

By default, TurboGears |version| configures :mod:`repoze.who` to use
:class:`tg.configuration.auth.fastform.FastFormPlugin` as the first
identifier and challenger -- using ``/login`` as the relative URL that will
display the login form, ``/login_handler`` as the relative URL where the
form will be sent and ``/logout_handler`` as the relative URL where the
user will be logged out. The so-called rememberer of such identifier will
be an instance of :class:`repoze.who.plugins.cookie.AuthTktCookiePlugin`.

All these settings can be customized through the ``config.app_cfg.base_config.sa_auth``
options in your project. Identifiers, Authenticators and Challengers can be overridden
providing a different list for each of them as::

    base_config.sa_auth['identifiers'] = [('myidentifier', myidentifier)]

You don't have to use :mod:`repoze.who` directly either, unless you decide not
to use it the way TurboGears configures it.

Customizing authentication and authorization
============================================

It's very easy for you to customize authentication and identification settings
in :mod:`repoze.who` from ``{yourproject}.config.app_cfg.base_config.sa_auth``.

Customizing how user informations, groups and permissions are retrieved
--------------------------------------------------------------------------

TurboGears provides an easy shortcut to customize how your authorization
data is retrieved without having to face the complexity of the underlying
authentication layer. This is performed by the ``TGAuthMetadata`` object
which is configured in your project ``config.app_cfg.base_config``.

This object provides three methods which have to return respectively the
user, its groups and its permissions. You can freely change them as you wish
as they are part of your own application behavior.

Advanced Customizations
---------------------------

For more advanced customizations or to use repoze plugins to implement
different forms of authentication you can freely customize the whole
authentication layer using through the ``{yourproject}.config.app_cfg.base_config.sa_auth``
options.

The available directives are all optional:

* ``form_plugin``: This is a replacement for the FriendlyForm plugin and will be
    always used as a challenger. If ``form_identifies`` option is True it will
    also be appended to the list of identifiers.
* ``ìdentifiers``: A custom list of :mod:`repoze.who` identifiers.
    By default it contains the ``form_plugin`` and the ``AuthTktCookiePlugin``.
* ``challengers``: A custom list of :mod:`repoze.who` challengers.
    The ``form_plugin`` is always appended to this list, so if you have
    only one challenger you will want to change the ``form_plugin`` instead
    of overridding this list.
* ``authmetadata``: This is the object that TG will use to fetch authorization metadata.
    Changing the authmetadata object you will be able to change how TurboGears
    fetches your user data, groups and permissions. Using authmetada a new
    :mod:`repoze.who` metadata provider is created.
* ``mdproviders``: This is a list of :mod:`repoze.who` metadata providers.
    If ``authmetadata`` is not None a metadata provider based on it will always
    be appended to the mdproviders.

Customizing the model structure assumed by the quickstart
---------------------------------------------------------

Your auth-related model doesn't `have to` be like the default one, where the
class for your users, groups and permissions are, respectively, ``User``,
``Group`` and ``Permission``, and your users' user name is available in
``User.user_name``. What if you prefer ``Member`` and ``Team`` instead of
``User`` and ``Group``, respectively?

First of all we need to inform the authentication layer that our user is stored
in a different class. This makes :mod:`repoze.who` know where to look for the user
to check its password::

    # what is the class you want to use to search for users in the database
    base_config.sa_auth.user_class = model.Member

Then we have to tell out ``authmetadata`` how to retrieve the user, its groups
and permissions::

    from tg.configuration.auth import TGAuthMetadata

    #This tells to TurboGears how to retrieve the data for your user
    class ApplicationAuthMetadata(TGAuthMetadata):
        def __init__(self, sa_auth):
            self.sa_auth = sa_auth

        def authenticate(self, environ, identity):
            user = self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(user_name=identity['login']).first()
            if user and user.validate_password(identity['password']):
                return identity['login']

        def get_user(self, identity, userid):
            return self.sa_auth.user_class.query.get(user_name=userid)

        def get_groups(self, identity, userid):
            return [team.team_name for team in identity['user'].teams]

        def get_permissions(self, identity, userid):
            return [p.permission_name for p in identity['user'].permissions]

    base_config.sa_auth.authmetadata = ApplicationAuthMetadata(base_config.sa_auth)

Now our application is able to fetch the user from the ``Member`` table and
its groups from the ``Team`` table. Using ``TGAuthMetadata`` makes also possible
to introduce a caching layer to avoid performing too many queries to fetch
the authentication data for each request.

BasicAuth Example
-----------------------------

The following is an example of an advanced authentication stack customization
to use browser basic authentication instead of form based authentication.

Declaring a Custom Authentication Backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First required step is to declare that we are going to use a custom
authentication backend::

    base_config.auth_backend = 'htpasswd'

When this is valued to ``ming`` or ``sqlalchemy`` TurboGears will configure
a default authentication stack based on users stored on the according database,
if ``auth_backend`` is ``None`` the whole stack will be disabled.

Then we must remove all the simple authentication options, deleting all the
``basic_config.sa_auth`` from ``app_cfg.py`` is usually enough. Leaving
unexpected options behind (options our authentication stack doesn't use)
might lead to a crash on application startup.

Using HTPasswd file for users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next step is storing our users inside an ``htpasswd`` file,
this can be achieved by using the ``HTPasswdPlugin`` authenticator::

    from repoze.who.plugins.htpasswd import HTPasswdPlugin, plain_check
    base_config.sa_auth.authenticators = [('htpasswd', HTPasswdPlugin('./htpasswd', plain_check))]

This will make TurboGears load users from an htpasswd file inside the directory
we are starting the application from. The ``plain_check`` function is the
one used to decode password stored inside the htpasswd file. In this case
passwords are expected to be in plain text in the form::

    manager:managepass

Challenging and Identifying users with BasicAuth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that we are correctly able to authenticate users from an htpasswd
file, we need to use BasicAuth for identifying returning users::

    from repoze.who.plugins.basicauth import BasicAuthPlugin

    base_auth = BasicAuthPlugin('MyTGApp')
    base_config.sa_auth.identifiers = [('basicauth', base_auth)]

This will correctly identify users that are already logged using
BasicAuth, but we are still sending users to login form to
perform the actual login.

As BasicAuth requires the login to be performed through the browser
we must disable the login form and set the basic auth
plugin as a challenger::

    # Disable the login form, it won't work anyway as the credentials
    # for basic auth must be provided through the browser itself
    base_config.sa_auth.form_identifies = False

    # Use BasicAuth plugin to ask user for credentials, this will replace
    # the whole login form.
    base_config.sa_auth.challengers = [('basicauth', base_auth)]

Providing User Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The previous steps are focused on providing a working authentication layer,
but we will need to also identify the authenticated user so that
also ``request.identity`` and the authorization layer can work as
expected.

This is achieved through the ``authmetadata`` option, which tells
TurboGears how to retrieve the user and it's informations. In this
case as we don't have a database of users we will just provide a
simple user with only ``display_name`` and ``user_name`` so that
most things can work. For ``manager`` user we will also provide the
``managers`` group so that user can access the TurboGears admin::

    from tg.configuration.auth import TGAuthMetadata

    class ApplicationAuthMetadata(TGAuthMetadata):
        def __init__(self, sa_auth):
            self.sa_auth = sa_auth

        def get_user(self, identity, userid):
            # As we use htpasswd for authentication
            # we cannot lookup the user in a database,
            # so just return a fake user object
            from tg.util import Bunch
            return Bunch(display_name=userid, user_name=userid)

        def get_groups(self, identity, userid):
            # If the user is manager we give him the
            # managers group, otherwise no groups
            if userid == 'manager':
                return ['managers']
            else:
                return []

        def get_permissions(self, identity, userid):
            return []

    base_config.sa_auth.authmetadata = ApplicationAuthMetadata(base_config.sa_auth)

Removing Login Form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As the whole authentication is now performed through BasicAuth
the login form is now unused, so probably want to remove the login form related
urls which are now unused:

    - /login
    - /post_login
    - /post_logout


.. _disabling-auth:

Disabling authentication and authorization
============================================

If you need more flexibility than that provided by the quickstart, or you are
not going to use :mod:`repoze.who`, you should prevent TurboGears from dealing
with authentication/authorization by removing (or commenting) the following
line from ``{yourproject}.config.app_cfg``::

    base_config.auth_backend = '{whatever you find here}'

Then you may also want to delete those settings like ``base_config.sa_auth.*``
-- they'll be ignored.
