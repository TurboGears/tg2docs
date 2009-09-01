Profiling Your App
==================

:Status: Work in progress

.. contents:: Table of Contents
    :depth: 2


TurboGears does not come with a built-in profiler, but an easy to use
WSGI application profiler is just an easy_install away!


Installing repoze.profile
-------------------------

First, install it with easy_install::

  easy_install -i http://dist.repoze.org/simple repoze.profile

Next add it to your WSGI stack in middleware.py in the config folder::

  from repoze.profile.profiler import AccumulatingProfileMiddleware

  def make_app(global_conf, full_stack=True, **app_conf):
       app = make_base_app(global_conf, full_stack=True, **app_conf)

       # Wrap your base TurboGears 2 application with custom middleware here
       app = AccumulatingProfileMiddleware(
               app,
               log_filename='/tmp/proj.log',
               cachegrind_filename='/tmp/cachegrind.out.bar',
               discard_first_request=True,
               flush_at_shutdown=True,
               path='/__profile__'
       )
       
       return app

Gathering Profile Data
----------------------

Just fire up a browser (or functional test-runner like twill, ab
(apache bench), or whatever).  The repoze.profile middleware will
profile everything above it in the WSGI stack.


Viewing Profile Data
--------------------

There's a built in web based view of your profile data. It should now
be available at the location /__profile__ in your app. For explanation
of the various columns shown on this page refer to python profiler
docs `http://docs.python.org/library/profile.html`.

Some distros package the profiler separately. Make sure to install  the python-profiler package as well.

Reference:

http://blog.repoze.org/repozeprofile-0_2-released.html
