.. _login_cleaner:

Adding a custom login cleaner
=============================

The default authentication mechanism checks the login user name, exactly
as it was entered by the user in the login form, against the user names
stored in the database. However, sometimes you may want to "sanitize"
the login names that have been entered by the users before comparing them
with the user names stored in the database. For instance, if you know you
have only lower case user names in the database, you may want to automatically
change the entered login name to lower case, so that it will not matter
if a user enters the name capitalized or has the caps lock key active when
typing. Or, if you are using user logins that are numbers, you may want
to remove leading zeros or any whitespace grouping the numbers into blocks.

You can realize such a "login cleaner" either by  using a modified repoze.who
form plugin or by wrapping your application in a special WSGI middleware.
Using the repoze.who plugin system may be more simple and obvious in this
case, but the middleware approach can also be used for other purposes not
related to authentication, so we will show both ways of doing it.

In our example, we assume the login names are numbers, and we want to
remove leading zeros and whitespace as well as any non-ascii characters
that may raise errors when decoding the string for comparison with the
login names in the database.


Solution 1, using a modified repoze.who form plugin
---------------------------------------------------

Save this module as lib/login_cleaner.py inside your TurboGears application::

    from repoze.who.plugins.friendlyform import FriendlyFormPlugin

    __all__ = ['LoginCleanerPlugin']

    class LoginCleanerFormPlugin(FriendlyFormPlugin):
        """Modified repoze.who FriendlyFormPlugin plugin with login clean-up."""

        def identify(self, environ):
            """Remove interim zeros and iterim whitespace in the login name."""
            identity = super(LoginCleanerFormPlugin, self).identify(environ)
            if identity:
                login = identity['login']
                if login:
                    # remove all non-ascii chars and whitespace
                    login = ''.join(c for c in login if 32 < ord(c) < 128)
                    # remove leading zeros if login is a number
                    if login.isdigit():
                        login = login.lstrip('0')
                    identity['login'] = login
            return identity

In config/app_cfg.py, add this::

    from myapp.lib.login_cleaner import LoginCleanerFormPlugin

    # Set up our modified form plugin for getting the credentials:
    base_config.sa_auth.form_plugin = LoginCleanerFormPlugin(
        login_form_url="/login", login_handler_path="/login_handler",
        logout_handler_path="/logout_handler", rememberer_name="cookie",
        post_login_url=base_config.sa_auth.post_login_url,
        post_logout_url=base_config.sa_auth.post_logout_url, charset='utf-8')

Solution 2, using a custom WSGI middleware
------------------------------------------

Save this module as lib/login_cleaner.py inside your TurboGears application::

    from webob import Request

    __all__ = ['LoginCleanerMiddleware']

    class LoginCleanerMiddleware(object):
        """WSGI middleware for login clean-up."""

        def __init__(self, app,
                login_handler_path='/login_handler', charset='utf-8'):
            self.app = app
            self.login_handler_path = login_handler_path
            self.charset = charset

        def __call__(self, environ, start_response):
            app = self.app
            path_info = environ['PATH_INFO']
            if path_info == self.login_handler_path:
                request = Request(environ, charset=self.charset)
                login = request.POST.get('login')
                if login:
                    # remove all non-ascii chars and whitespace
                    login = ''.join(c for c in login if 32 < ord(c) < 128)
                    # remove leading zeros if login is a number
                    if login.isdigit():
                        login = login.lstrip('0')
                    request.POST['login'] = login
            return app(environ, start_response)

In config/app_cfg.py, add this::

    from myapp.lib.login_cleaner import LoginCleanerMiddleware

    def make_app(global_conf, full_stack=True, **app_conf):
        app = make_base_app(global_conf, full_stack=True, **app_conf)

        # wrap the application with our custom middleware for login clean-up:
        app = LoginCleanerMiddleware(app, login_handler_path=app_conf.get(
            'sa_auth.login_handler', '/login_handler'))

        return app
