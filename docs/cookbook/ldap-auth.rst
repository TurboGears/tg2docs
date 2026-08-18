.. ldapauth:


Using LDAP for user authentication and authorization
====================================================

:Applies to: TurboGears 2.5 and ``who_ldap`` 4.0.0

.. contents:: Table of Contents
   :depth: 1

This recipe shows how to configure TurboGears to use an LDAP
directory for user authentication and authorization. It uses
``who_ldap`` for LDAP authentication and metadata, and
:class:`tg.configuration.auth.TGAuthMetadata` to adapt that metadata to
TurboGears' user, group, and permission model.


Requirements
------------

Use the verified `who_ldap 4.0.0 release
<https://pypi.org/project/who_ldap/4.0.0/>`_, which provides ``repoze.who``
plugins for LDAP authentication and metadata. Install it with::

    python -m pip install 'who_ldap==4.0.0'

Add this requirement to your project's ``pyproject.toml``
``[project].dependencies`` list::

    [project]
    dependencies = [
      # keep the dependencies already listed here...
      "who_ldap==4.0.0",
    ]

``who_ldap`` depends on the `ldap3 package
<https://ldap3.readthedocs.io/en/latest/>`_, a Python LDAP v3 client. See the
`who_ldap source documentation <https://github.com/m-martinez/who_ldap>`_
for plugin details.


Configuration
-------------

Here is an example configuration that you can put into the
`config/app_cfg.py` file of your project. The LDAP authenticator validates
credentials; the metadata providers add LDAP data to the identity; and
``TGAuthMetadata`` maps that identity data to TurboGears user, group, and
permission values::

    import os

    # LDAP supplies the user data; no SQLAlchemy user model is required.
    base_config.update_blueprint({
        'use_sqlalchemy': False,
        'sa_auth.enabled': True,
        'sa_auth.cookie_secret': os.environ['TG_COOKIE_SECRET'],
    })

    from who_ldap import (LDAPSearchAuthenticatorPlugin,
                          LDAPAttributesPlugin, LDAPGroupsPlugin)

    # Tell TurboGears how to connect to the LDAP directory

    ldap_url = 'ldaps://ldap.example.com'
    ldap_base_dn = 'ou=users,dc=example,dc=com'
    ldap_bind_dn = 'cn=bind,ou=users,dc=example,dc=com'
    ldap_bind_pass = os.environ['LDAP_BIND_PASSWORD']

    # Authenticate users by searching in LDAP

    ldap_auth = LDAPSearchAuthenticatorPlugin(
        url=ldap_url, base_dn=ldap_base_dn,
        bind_dn=ldap_bind_dn, bind_pass=ldap_bind_pass,
        returned_id='login',
        # the LDAP attribute that holds the user name:
        naming_attribute='sAMAccountName')

    base_config.update_blueprint({
        'sa_auth.authenticators': [('ldapauth', ldap_auth)],
    })

    # Retrieve user metadata from LDAP

    ldap_user_provider = LDAPAttributesPlugin(
        url=ldap_url, bind_dn=ldap_bind_dn, bind_pass=ldap_bind_pass,
        name='user',
        # map from LDAP attributes to TurboGears user attributes:
        attributes='givenName=first_name,sn=last_name,mail=email_address',
        flatten=True)

    # Retrieve user groups from LDAP

    ldap_groups_provider = LDAPGroupsPlugin(
        url=ldap_url, base_dn=ldap_base_dn,
        bind_dn=ldap_bind_dn, bind_pass=ldap_bind_pass,
        filterstr='(&(objectClass=group)(member=%(dn)s))',
        name='groups')

    base_config.update_blueprint({
        'sa_auth.mdproviders': [
            ('ldapuser', ldap_user_provider),
            ('ldapgroups', ldap_groups_provider),
        ],
    })

    from tg.configuration.auth import TGAuthMetadata

    class ApplicationAuthMetadata(TGAuthMetadata):
        """Adapt LDAP identity metadata for TurboGears."""

        # map from LDAP group names to TurboGears group names
        group_map = {'operators': 'managers'}

        # set of permissions for all mapped groups
        permissions_for_groups = {'managers': {'manage'}}

        def get_user(self, identity, userid):
            user = identity.get('user')
            if user:
                name = ' '.join(filter(None, (
                    user.get('first_name'), user.get('last_name'))))
                user.update(user_name=userid, display_name=name)
            return user

        def get_groups(self, identity, userid):
            get_group = self.group_map.get
            return [get_group(g, g) for g in identity.get('groups', [])]

        def get_permissions_for_group(self, group):
            return self.permissions_for_groups.get(group, set())

        def get_permissions(self, identity, userid):
            permissions = set()
            get_permissions = self.get_permissions_for_group
            for group in self.get_groups(identity, userid):
                permissions |= get_permissions(group)
            return permissions


    base_config.update_blueprint({
        'sa_auth.authmetadata': ApplicationAuthMetadata(),
    })

    # Pages where you want users to be redirected after login and logout:

    base_config.update_blueprint({
        'sa_auth.post_login_url': '/post_login',
        'sa_auth.post_logout_url': '/post_logout',
    })

The example uses an ``ldaps://`` URL, so it leaves ``start_tls`` disabled.
If your directory requires StartTLS instead, use an ``ldap://`` URL and set
``start_tls=True`` on each ``who_ldap`` plugin; do not combine StartTLS with
LDAPS. ``who_ldap`` 4.0.0 does not expose ``ldap3`` certificate-validation
settings in these constructors, so this example does not establish strict
certificate verification. Use an LDAP integration path that enables the
required certificate validation before production deployment.

Change the connection parameters to point to your LDAP user base. The bind
account must be authorized to search the directory. Supply
``LDAP_BIND_PASSWORD`` and ``TG_COOKIE_SECRET`` through deployment secret
management rather than committing either value to source control.

The configuration for retrieving user metadata and user groups is optional if
you want to use LDAP solely for authentication and not for authorization.
TurboGears 2.5 calls the adapter in this recipe ``TGAuthMetadata``; it does not
provide a separate ``TGAuthMetadataProvider`` class.
