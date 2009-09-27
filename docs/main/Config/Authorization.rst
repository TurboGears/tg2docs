.. _authconfig:

Authorization/Authentication Config Settings
==============================================

:Status: Official

.. contents:: Table of Contents
   :depth: 2


Often times your database schema will not match the
TG Quickstart schema, or you may have to Authenticate
in a manner different from just authorizing with the
database.  These settings help make it easier to alter
these settings.

Basic Config Settings
-----------------------

It's very easy for you to customize authentication and identification settings
in :mod:`repoze.who` from ``{yourproject}.config.app_cfg.sa_auth``. The 
available directives are all optional:

* ``form_plugin``: An instance of your custom :mod:`repoze.who` challenger.
* ``form_identifies`` (bool): Whether your custom challenger should also be
  used as an identifier (e.g., an instance of 
  :mod:`repoze.who.plugins.form.RedirectingFormPlugin`).
* You may also customize the parameters sent to
  :class:`repoze.who.middleware.PluggableAuthenticationMiddleware`. For example,
  to set an additional :mod:`repoze.who` authenticator, you may use something
  like this in ``{yourproject}.config.app_cfg``::
  
      # ...
      from repoze.who.plugins.htpasswd import HTPasswdPlugin, crypt_check
      # ...
      htpasswd_auth = HTPasswdPlugin('/path/to/users.htpasswd', crypt_check)
      app_cfg.sa_auth.authenticators = [('htpasswd_auth', htpasswd_auth)]
      # ...

Customizing the model structure assumed by the quickstart
---------------------------------------------------------

Your auth-related model doesn't `have to` be like the default one, where the
class for your users, groups and permissions are, respectively, ``User``,
``Group`` and ``Permission``, and your users' user name is available in
``User.user_name``. What if you prefer ``Member`` and ``Team`` instead of
``User`` and ``Group``, respectively? Or what if you prefer ``Group.members``
instead of ``Group.users``? Read on!

Changing class names
~~~~~~~~~~~~~~~~~~~~

Changing the name of an auth-related class (``User``, ``Group`` or ``Permission``)
is a rather simple task. Just rename it in your model, and then make sure to
update ``{yourproject}.config.app_cfg`` accordingly.

For example, if you renamed ``User`` to ``Member``, ``{yourproject}.config.app_cfg``
should look like this::

    # ...
    from yourproject import model
    # ...
    base_config.sa_auth.user_class = model.Member
    # ...

Changing attribute names
~~~~~~~~~~~~~~~~~~~~~~~~

You can also change the name of the attributes assumed by
:mod:`repoze.what` in your auth-related classes, such as renaming
``User.groups`` by ``User.memberships``.

Changing such values is what :mod:`repoze.what` calls "translating".
You may set the translations for the attributes of the models
:mod:`repoze.what` deals with in ``{yourproject}.config.app_cfg``. For
example, if you want to replace ``Group.users`` by ``Group.members``, you may
set the following translation in that file::

    base_config.sa_auth.translations.users = 'members'

These are the translations you may set in ``base_config.sa_auth.translations``:
    * ``user_name``: The translation for the attribute in ``User.user_name``.
    * ``users``: The translation for the attribute in ``Group.users``.
    * ``group_name``: The translation for the attribute in ``Group.group_name``.
    * ``groups``: The translation for the attribute in ``User.groups`` and
      ``Permission.groups``.
    * ``permission_name``: The translation for the attribute in
      ``Permission.permission_name``.
    * ``permissions``: The translation for the attribute in ``User.permissions``
      and ``Group.permissions``.
    * ``validate_password``: The translation for the method in
      ``User.validate_password``.

``AppConfig`` Method Overrides
-------------------------------

.. automethod:: tg.configuration.AppConfig.add_auth_middleware
.. automethod:: tg.configuration.AppConfig.setup_sa_auth_backend

