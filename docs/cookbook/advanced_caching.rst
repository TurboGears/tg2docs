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
                               'kajiki', 'myproj.templates.cached_func')

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
    * The second step, which is the metadata provisioning, is performed by :class:`.IdentityApplicationWrapper`
      and receives the previously identified user as returned by the authentication step.
      This is performed by ``get_user``, ``get_groups`` and ``get_permissions`` which are in charge of returning
      the three aforementioned information regarding the user.

It's easy to see that this second step is usually the one that has most weight over the request throughput as
it involves three different queries to the database.

We can easily change the ``ApplicationAuthMetadata`` in our code to rely on the cache to fetch user data instead
of loading it back from database::

    from tg import cache

    class ApplicationAuthMetadata(TGAuthMetadata):
        def __init__(self, sa_auth):
            self.sa_auth = sa_auth

        def authenticate(self, environ, identity):
            # This should be your current authenticate implementation
            ...

        def get_user(self, identity, userid):
            identity.update(self._get_cached_auth_metadata(userid))
            return identity['user']

        def get_groups(self, identity, userid):
            return identity['groups'] or []

        def get_permissions(self, identity, userid):
            return identity['permissions'] or []

        def _get_cached_auth_metadata(self, userid):
            """Retrieves the user details from the cache when available"""
            auth_cache = cache.get_cache('auth')
            auth_metadata = auth_cache.get_value(key=userid,
                                                 createfunc=lambda: self._retrieve_auth_metadata(userid),
                                                 expiretime=3600)

            auth_metadata['user'] = self.sa_auth.dbsession.merge(auth_metadata['user'], load=False)
            return auth_metadata

        def _retrieve_auth_metadata(self, userid):
            """Retrieves user details from the database"""
            user = self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(user_name=userid).first()
            return {
                'user': user,
                'groups': user and [g.group_name for g in user.groups],
                'permissions': user and [p.permission_name for p in user.permissions]
            }

This is usually enough to cache authentication requests in an environment where user data, permissions
and groups change rarely. A better cache management, invalidating the user cache whenever the user itself
or its permission change, is required for more volatile scenarios.

