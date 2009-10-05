.. _using-who.ini:

Using who.ini
=============

Once you have disabled your quickstart configuration 
(see :ref:`disabling-auth`), you may find yourself wanting to 
use the `who.ini` configuration mechanism referenced in 
most `repoze.who` documentation.  This section describes how 
to create a `who.ini`-based configuration that looks much 
like the quickstart configuration you just disabled.

Since `repoze.who` is WSGI middleware, you will need to alter 
your project's `project.config.middleware.py` file to create 
your middleware from your .ini file::

    from repoze.who.config import make_middleware_with_config as make_who_with_config
    ...
        # Wrap your base TurboGears 2 application with custom middleware here
        app = make_who_with_config(
            app, 
            global_conf, 
            app_conf.get('who.config_file','who.ini'), 
            app_conf.get('who.log_file','stdout'),
            app_conf.get('who.log_level','debug')
        )

and add the following to your config file's app:main section::

    who.config_file = %(here)s/who.ini
    who.log_level = debug
    who.log_file = stdout

at this point, you are using the standard `repoze.who` configuration mechanism,
so should be able to follow most `repoze.who` documentation to complete your 
configurations.

Quickstart via `who.ini`
------------------------

If you would like to start off your customizations with something similar 
to the `repoze.who.quickstart` mechanism, you can use standard mechanisms 
to set up most of the machinery that the quickstart provides.  Here is a 
sample `who.ini` that provides much of the quickstart behaviour::

    # Sample of a who.ini file from which to begin configuring
    # this looks a lot like the "quickstart" application's setup,
    # minus the translation capability...

    [plugin:auth_tkt]
    # Cookie-based session identification storage
    use = repoze.who.plugins.auth_tkt:make_plugin
    secret = 'this secret is not really very SECRET!'

    [plugin:friendlyform]
    # Redirecting form which does login via a "post"
    # from a regular /login form 
    use = repoze.who.plugins.friendlyform:FriendlyFormPlugin
    login_form_url= /login
    login_handler_path = /login_handler
    logout_handler_path = /logout_handler
    rememberer_name = auth_tkt
    post_login_url = 
    post_logout_url = 

    [plugin:sqlauth]
    # An SQLAlchemy authorization plugin
    use = customwho.lib.auth:auth_plugin

    # Now the configuration starts wiring together the pieces
    [general]
    request_classifier = repoze.who.classifiers:default_request_classifier
    challenge_decider = repoze.who.classifiers:default_challenge_decider

    [identifiers]
    # We can decide who the user is trying to identify as using either 
    # a fresh form-post, or the session identifier cookie
    plugins =
        friendlyform;browser
        auth_tkt

    [authenticators]
    plugins =
        sqlauth

    [challengers]
    plugins =
        friendlyform;browser

    [mdproviders]
    # Metadata providers are the things that actually look up a user's credentials
    # here we have a plugin that provides "user" information (md_plugin) and another,
    # which acts as an adapter to the first, to provide group/permission information.
    plugins =
        customwho.lib.auth:md_plugin
        customwho.lib.auth:md_group_plugin

Note that "customwho" is the project name here.  Also note that the `who.ini`
file references a custom Python module `customwho.lib.auth` which is where
we set up our `repoze.who` plugins in the normal manner for `repoze.who`::

    """Example of a simplistic, importable authenticator plugin

    Intended to work like a quick-started SQLAlchemy plugin"""
    from repoze.who.plugins.sa import (
        SQLAlchemyAuthenticatorPlugin,
        SQLAlchemyUserMDPlugin,
    )
    from repoze.what.plugins.sql import configure_sql_adapters
    from repoze.what.middleware import AuthorizationMetadata

    from customwho import model
    auth_plugin = SQLAlchemyAuthenticatorPlugin(model.User, model.DBSession)
    md_plugin = SQLAlchemyUserMDPlugin(model.User, model.DBSession )
    _source_adapters = configure_sql_adapters(
        model.User,
        model.Group,
        model.Permission,
        model.DBSession,
    )
    md_group_plugin = AuthorizationMetadata(
        {'sqlauth': _source_adapters['group']},
        {'sqlauth': _source_adapters['permission']},
    )

This module creates a number of plugins which the `who.ini` file references.
It is also possible to configure plugins to accept parameters from the 
`who.ini` configuration file (by specifying a plugin: section and providing 
the parameters).

Next Steps
----------

 * :ref:`openid` -- describes how to use a Repoze.who plugin to authenticate
   users via the OpenID mechanism

References
----------

 * `Pylons Repoze.who Cookbook`_ -- describes how the `repoze.who` middleware
   fitted into a Pylons application (TurboGears 2.x is a Pylons application)

.. _`Pylons Repoze.who Cookbook`: http://wiki.pylonshq.com/display/pylonscookbook/Authentication+and+Authorization+with+%60repoze.who%60
