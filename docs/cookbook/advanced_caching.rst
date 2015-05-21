Advanced Caching Recipes
========================

Caching Template and Controller
-------------------------------

A simple form of joint controller+template caching can be achieved by using both :class:`.cached` decorator
and ``tg_cache`` parameter as described in :ref:`caching`.

While it is more common having to perform some kind of minimal computation in controller to decide
which cache key to use and rely on the template caching only, the caching system can be leveraged to turn
the whole request in a direct cache hit based on the request parameters.

This can be achieved by relying on the :class:`.cached` decorator and using :func:`.render_template` to
actually render the template during controller execution and caching it together with the controller itself::

    from tg import cached, render_template

    @cached()
    @expose(content_type='text/html')
    def cached_func(self, what='about'):
        return render_template(dict(page=what, time=time.time()),
                               'genshi', 'myproj.templates.cached_func')

.. note::

    While ``@cached`` caches the controller itself, any hook or validation associated to the
    controller will still be executed. This might be what you want (for example when tracking
    page views through an hook) or it might not, depending on your needs you might want to move
    hooks and validation inside the controller itself to ensure they are cached.

.. _caching_auth:

Caching Authentication
----------------------

Authentication in TurboGears is provided by ``repoze.who`` through the ``ApplicationAuthMetadata`` class
as described in :ref:`authentication`.

``ApplicationAuthMetadata`` provides two major steps in authentication:

    * One is authenticating the user itself for the first time (done by ``ApplicationAuthMetadata.authenticate``) which
      is in charge of returning the ``user_name`` that uniquely identifies the user (or any other unique identifier)
      that is then received by the other methods to lookup the actual user data.
    * The second step, which is the metadata provisioning, is performed on each request and receives the previously
      identified user as returned by the authentication step. This is performed by ``get_user``, ``get_groups`` and
      ``get_permissions`` which are in charge of returning the three aforementioned information regarding the user.

It's easy to see that this second step is usually the one that has most weight over the request throughput as
it involves three different queries to the database. Usually we cannot rely on the TurboGears caching for those
methods as they happen before the TurboGears cache is ready, but fortunately we can still cache it by writing an
:class:`.ApplicationWrapper` that performs the work in place of the metadata provisioning functions.

First action is to change our ``ApplicationAuthMetadata`` to actually avoid fetching any data::

    from tg.util import Bunch

    class ApplicationAuthMetadata(TGAuthMetadata):
        def __init__(self, sa_auth):
            self.sa_auth = sa_auth

        def authenticate(self, environ, identity):
            ... # authenticate implementation

        def get_user(self, identity, userid):
            return Bunch(user_name=userid)

        def get_groups(self, identity, userid):
            return []

        def get_permissions(self, identity, userid):
            return []

    base_config.sa_auth.authmetadata = ApplicationAuthMetadata(base_config.sa_auth)

This will actually do nothing and just return a fake user for requests when they perform the metadata
provisioning during authentication.

The real metadata provisioning will be performed by an ad-hoc ApplicationWrapper that can access the
cache::

    from tg.appwrappers.base import ApplicationWrapper

    class AuthMetadataApplicationWraper(ApplicationWrapper):
        def __init__(self, next_handler, config):
            super(AuthMetadataApplicationWraper, self).__init__(next_handler, config)
            self.sa_auth = config['sa_auth']

        def get_auth_metadata(self, userid):
            user = self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(user_name=userid).first()
            return {
                'user': user,
                'groups': [g.group_name for g in user.groups],
                'permissions': [p.permission_name for p in user.permissions]
            }

        def __call__(self, controller, environ, context):
            identity = environ.get('repoze.who.identity')
            if identity is not None:
                userid = identity['repoze.who.userid']
                auth_cache = context.cache.get_cache('auth')
                auth_metadata = auth_cache.get_value(key=userid,
                                                     createfunc=lambda: self.get_auth_metadata(userid),
                                                     expiretime=3600)

                auth_metadata['user'] = self.sa_auth.dbsession.merge(auth_metadata['user'], load=False)

                identity.update(auth_metadata)
                environ['repoze.what.credentials'].update(identity)

            return self.next_handler(controller, environ, context)

    base_config.register_wrapper(AuthMetadataApplicationWraper)

This is usually enough to cache authentication requests in an environment where user data, permissions
and groups change rarely. A better cache management, invalidating the user cache whenever the user itself
or its permission change, is required for more volatile scenarios.

