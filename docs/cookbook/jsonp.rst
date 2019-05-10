.. _tg-json:

======================================
JSON and JSONP Rendering
======================================

JSON Renderer
=============

TurboGears always provided builtin support for JSON Rendering, this is provided by the
:class:`.JSONRenderer` and the :func:`.json.encode` function.

The first is what empowers the ``@expose('json')`` feature while the second is an
utility function you can call whenever encoding to json is needed. Both rely on
on :class:`tg.jsonify.JSONEncoder` which is able to handle more types than the standard
one provided by the python ``json`` module and can be extended to support more types.

Using it is as simple as::

    @expose('json')
    def jp(self, **kwargs):
        return dict(hello='World')

Which, when calling ``/jp`` would result in::

    {"hello": "World"}

Customizing JSON Encoder
------------------------

While you can create your own encoder, turbogears has a default instance of :class:`.JSONEncoder`
which is used for all encoding performed by the framework itself. Behavior of this encoder
can be driven by providing a ``__json__`` method inside objects for which you want to
customize encoding and can be configured using through following options:

    * ``json.isodates`` -> Whenever to encode dates in ISO8601 or not, the default is ``False``
    * ``json.custom_encoders`` -> Dictionary of ``type: function`` mappings which can specify
      custom encoders for specific types. Custom encoders are functions that are called
      to get a basic object the json encoder knows how to handle.

For example to configure a custom encoder for dates your project ``app_cfg.py`` would look
like::

    from datetime import date

    def dmy_encoded_date(d):
        return d.strftime('%d/%m/%Y')

    base_config['json.custom_encoders'] = {date: dmy_encoded_date}

That would cause all ``datetime.date`` instances to be encoded using ``dmy_encode_date`` function.

If the encoded object provides a ``__json__`` method this is considered the **custom encoder**
for the object itself and it is called to get a basic type the json encoder knows how to handle
(usually a ``dict``).

.. note::

    ``json.custom_encoders`` take precedence over ``__json__``, this is made so that
    users can override behavior for third party objects that already provide a ``__json__``
    method.

Per method customization
------------------------

The same options available inside the ``json.`` configuration namespace are available
as ``render_params`` for the :class:`.expose` decorator. So if you want to turn
on/off iso formatted dates for a single method you can do that using::

    from datetime import datetime

    @expose('json', render_params=dict(isodates=True))
    def now(self, **kwargs):
        return dict(now=datetime.utcnow())

JSONP Renderer
==============

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
-------------------------

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
----------------------------

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


