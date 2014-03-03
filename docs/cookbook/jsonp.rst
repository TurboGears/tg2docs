======================================
Using JSONP
======================================

Since version 2.3.2 TurboGears provides built-in support for JSONP rendering.

JSONP works much like JSON output, but instead of providing JSON response it provides
an ``application/javascript`` response with a call to a javascript function providing
all the values returned by the controller as function arguments.

To enable JSONP rendering you must first append it to the list of required engines
inside your application ``config/app_cfg.py``::

    base_config.renderers.append('jsonp')

Then you can declare a JSONP controller by exposing it as::

    @expose('jsonp')
    def jp(self, **kwargs):
        return dict(hello='World')

When accessing ``/jp?callback=callme`` you should see::

    callme({"hello": "World"});

If you omit the ``callback`` parameter an error will be returned as
it is required to know the callback name when using JSONP.

Custom callback parameter
------------------------------------

By default TurboGears will expect the callback name to be provided
in a ``callback`` parameter. This parameter has to be accepted by your
controller (otherwise you can use ``**kwargs`` like the previous examples).

If you need to use a different name for the callback parameter just provide
it in the ``render_params`` of your exposition::

    @expose('jsonp', render_params={'callback_param': 'call'})
    def jp(self, **kwargs):
        return dict(hello='World')

Then instead of opening ``/jp?callback=callme`` to get the JSONP response
you will need to open ``/jp?call=callme`` as stated by the ``callback_param``
option provided in the render_params.

Exposing both JSON and JSONP
------------------------------------

If you want to expose a controller as both JSON and JSONP, just provide
both expositions. You can then use TurboGears request extensions support
to choose which response you need::

    @expose('json')
    @expose('jsonp')
    def jp(self, **kwargs):
        return dict(hello='World')

To get the JSON response simply open ``/jp.json`` while to get the
JSONP response go to ``/jp.js?callback=callme``. If no extension is provided
the first exposition will be returned (in this case JSON).


