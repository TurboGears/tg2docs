.. ldapauth:


Using LDAP for user authentication and authorization
====================================================

:Status: RoughDoc

.. contents:: Table of Contents
   :depth: 1

This recipe shows how to configure TurboGears to use an LDAP
directory for user authentication and authorization.


Requirements
------------

We will use the `who_ldap` plugin for `repoze.who` for this purpose,
since it supports both Python 2 and Python 3.

You can find the `documentation for who_ldap
<https://pypi.python.org/pypi/who_ldap/>`_ on PyPi.
From there, you can also install `who_ldap`, just run::

    pip install who_ldap

You should also add this requirement to your project's `setup.py` file::

    install_requires=[
        ...,
        "who_ldap",
        ]

Note that `who_ldap` itself requires the `ldap3` package
(formerly known as python3-ldap), which is a pure Python implementation
of an LDAP v3 client. See the `documentation for ldap3
<https://ldap3.readthedocs.org/en/latest/>`_ for details.


Configuration
-------------

Here is an example configuration that you can put into the
`config/app_cfg.py` file of your project::

    # Configure the base SQLALchemy setup:
    base_config.use_sqlalchemy = False

    # Configure the authentication backend:

    # YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP
    base_config.sa_auth.cookie_secret = 'secret'

    base_config.auth_backend = 'ldapauth'

    from who_ldap import (LDAPSearchAuthenticatorPlugin,
                          LDAPAttributesPlugin, LDAPGroupsPlugin)

    # Tell TurboGears how to connect to the LDAP directory

    ldap_url = 'ldaps://ad.snake-oil-company.com'
    ldap_base_dn = 'ou=users,dc=ad,dc=snake-oil-company,dc=com'
    ldap_bind_dn = 'cn=bind,cn=users,dc=ad,dc=snake-oil-company,dc=com'
    ldap_bind_pass = 'silverbullet'

    # Authenticate users by searching in LDAP

    ldap_auth = LDAPSearchAuthenticatorPlugin(
        url=ldap_url, base_dn=ldap_base_dn,
        bind_dn=ldap_bind_dn, bind_pass=ldap_bind_pass,
        returned_id='login',
        # the LDAP attribute that holds the user name:
        naming_attribute='sAMAccountName',
        start_tls=True)

    base_config.sa_auth.authenticators = [('ldapauth', ldap_auth)]

    # Retrieve user metadata from LDAP

    ldap_user_provider = LDAPAttributesPlugin(
        url=ldap_url, bind_dn=ldap_bind_dn, bind_pass=ldap_bind_pass,
        name='user',
        # map from LDAP attributes to TurboGears user attributes:
        attributes='givenName=first_name,sn=last_name,mail=email_address',
        flatten=True, start_tls=True)

    # Retrieve user groups from LDAP

    ldap_groups_provider = LDAPGroupsPlugin(
        url=ldap_url, base_dn=ldap_base_dn,
        bind_dn=ldap_bind_dn, bind_pass=ldap_bind_pass,
        filterstr='(&(objectClass=group)(member=%(dn)s))',
        name='groups',
        start_tls=True)

    base_config.sa_auth.mdproviders = [
        ('ldapuser', ldap_user_provider),
        ('ldapgroups', ldap_groups_provider)]

    from tg.configuration.auth import TGAuthMetadata

    class ApplicationAuthMetadata(TGAuthMetadata):
        """Tell TurboGears how to retrieve the data for your user"""

        # map from LDAP group names to TurboGears group names
        group_map = {'operators': 'managers'}

        # set of permissions for all mapped groups
        permissions_for_groups = {'managers': {'manage'}}

        def __init__(self, sa_auth):
            self.sa_auth = sa_auth

        def get_user(self, identity, userid):
            user = identity.get('user')
            if user:
                name ='{first_name} {last_name}'.format(**user).strip()
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


    base_config.sa_auth.authmetadata = ApplicationAuthMetadata(
        base_config.sa_auth)

    # Override this if you would like to provide a different who plugin for
    # managing login and logout of your application:

    base_config.sa_auth.form_plugin = None

    # Page where you want users to be redirected to on login:

    base_config.sa_auth.post_login_url = '/post_login'

    # Page where you want users to be redirected to on logout:

    base_config.sa_auth.post_logout_url = '/post_logout'

You will need to change the connection parameters to point to your
user base in your LDAP directory and login with a bind user and
password that is authorized to search over the directory.

You may also need to change some of the other parameters according
to your requirements. The configuration for retrieving user metadata
and user groups is optional if you want to use LDAP solely for
authentication and not for authorization.
