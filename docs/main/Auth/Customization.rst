Customizing authentication and authorization
============================================

:Status: Official

Here you will learn how to customize the way TurboGears configures
authentication and thus :mod:`repoze.who` indirectly for you.

This is all done from ``{yourproject}.config.app_cfg.base_config.sa_auth``.

Customizing authentication settings
-----------------------------------

It's very easy for you to customize authentication and identification settings
in :mod:`repoze.who` from ``{yourproject}.config.app_cfg.base_config.sa_auth``.

Customizing how user informations, groups and permissions are retrieved
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TurboGears provides an easy shortcut to customize how your authorization
data is retrieved without having to face the complexity of the underlying
authentication layer. This is performed by the ``TGAuthMetadata`` object
which is configured in your project ``config.app_cfg.base_config``.

This object provides three methods which have to return respectively the
user, its groups and its permissions. You can freely change them as you wish
as they are part of your own application behavior.

Adavanced Customizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. _disabling-auth:

Disabling authentication and authorization
------------------------------------------

If you need more flexibility than that provided by the quickstart, or you are
not going to use :mod:`repoze.who`, you should prevent TurboGears from dealing
with authentication/authorization by removing (or commenting) the following
line from ``{yourproject}.config.app_cfg``::

    base_config.auth_backend = '{whatever you find here}'

Then you may also want to delete those settings like ``base_config.sa_auth.*``
-- they'll be ignored.

Next Steps
----------

* :ref:`openid` -- describes how to use a `repoze.who` plugin to
  authenticate users via the OpenID mechanism
