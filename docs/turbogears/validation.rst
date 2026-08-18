.. _validation:

=====================
Parameters Validation
=====================

Controller arguments arrive from the request as strings. TurboGears validation
is the layer that converts those strings to Python values, checks that required
values were submitted, and decides what response should be returned when
validation fails.

In TurboGears 2.5.1 this support is built in. The common cases are handled by:

* Python type hints on controller arguments, activated with ``@validate()``.
* :class:`tg.validation.Convert`, for explicit conversion callables.
* :class:`tg.validation.RequireValue`, for required string-like values that do
  not need conversion.
* Custom validators that provide a ``to_python`` method.

For a complete reference of validation configuration options, see
:ref:`Validation <config-options>`.

FormEncode is no longer part of TurboGears itself. If an application still wants
to use FormEncode validators or schemas, install and enable the
``tgext.formencode`` extension; see :ref:`validation_extensions`.

Validating Parameters with Type Hints
=====================================

For controller methods that only need simple conversions, annotate the arguments
and add ``@validate()``. When no explicit validators are passed, TurboGears
builds validators from the function signature.

.. code-block:: python

    from tg import TGController, expose, validate
    from tg.controllers.util import validation_errors_response


    class RootController(TGController):
        @expose('json')
        @validate(error_handler=validation_errors_response)
        def movie(self, movie_id: int, featured: bool = False, rating: float = 0.0):
            return dict(movie_id=movie_id, featured=featured, rating=rating)

A request to ``/movie?movie_id=7&featured=true&rating=8.5`` calls the method
with ``movie_id`` as an ``int``, ``featured`` as a ``bool`` and ``rating`` as a
``float``.

Arguments without defaults are also required by the controller dispatcher. If
the request omits one, the request can fail during dispatch with ``404 Not
Found`` before the validation error handler runs. Arguments with defaults are
optional; if the request omits them, the default value is passed to the
controller. Use an explicit validator on an argument with a default when a
missing query parameter should be reported through validation instead of
dispatch. Boolean annotations use TurboGears' boolean parser, so values such as
``true``, ``false``, ``yes``, ``no``, ``1`` and ``0`` are accepted.

Type hints are used as conversion callables. Runtime types such as ``int``,
``float``, ``str`` and ``bool`` are good fits for automatic validation. For
custom parsing, use an explicit validator.

Explicit Native Validators
==========================

For fields that need a custom conversion function or custom error message, pass
a dictionary to :class:`tg.decorators.validate`. The dictionary maps request
parameter names to validators.

.. code-block:: python

    from tg import TGController, expose, request, validate
    from tg.validation import Convert, RequireValue


    class RootController(TGController):
        @expose('json')
        @validate({
            'quantity': Convert(int, msg='Quantity must be a number'),
            'title': RequireValue(msg='Title is required'),
        })
        def save(self, quantity=None, title=None):
            validation_status = request.validation
            return dict(
                quantity=quantity,
                title=title,
                errors={
                    key: str(value)
                    for key, value in validation_status.errors.items()
                },
                values=validation_status.values,
            )

``Convert`` accepts any callable that takes one value and returns the converted
value. If the callable raises an exception, TurboGears treats validation as
failed and uses the validator's ``msg`` as the error message. Missing values
are errors unless you provide a ``default`` -- including an explicit
``default=None``, which makes the field optional and passes ``None`` to the
action when the value is missing:

.. code-block:: python

    @expose('json')
    @validate({'page': Convert(int, default=1),
               'tag': Convert(str, default=None)})
    def list_items(self, page=1, tag=None):
        return dict(page=page, tag=tag)

``Convert`` also has a deterministic representation with no memory addresses,
which is safe to log or include in diagnostics. The ``default=<required>``
marker distinguishes "no default supplied" from an explicit ``default=None``::

    >>> repr(Convert(int))
    Convert(func=builtins.int, msg='Invalid', default=<required>)
    >>> repr(Convert(int, default=None))
    Convert(func=builtins.int, msg='Invalid', default=None)

``RequireValue`` is useful when the incoming value should stay a string but must
not be empty.

Validation Errors
=================

When validation fails, TurboGears records details on ``tg.request.validation``.
During error handling these attributes are available:

* ``tg.request.validation.values`` -- the submitted values before validation.
* ``tg.request.validation.errors`` -- the field errors that triggered error
  handling.
* ``tg.request.validation.exception`` -- the validation exception.
* ``tg.request.validation.error_handler`` -- the error handler currently being
  executed.

If no error handler is configured, TurboGears uses the original controller
action as the error handler. The action is called with the unvalidated request
values, while ``tg.request.validation`` contains the validation errors. This is
useful for actions that redisplay their own form, but it also means invalid
input is not automatically rejected.

For JSON APIs, a common choice is
:func:`tg.controllers.util.validation_errors_response`, which returns a
``422 Unprocessable Content`` response containing the validation errors as
JSON (``{"errors": ..., "values": ...}``).

.. code-block:: python

    from tg import TGController, expose, validate
    from tg.controllers.util import validation_errors_response


    class ApiController(TGController):
        @expose('json')
        @validate(error_handler=validation_errors_response)
        def item(self, item_id: int):
            return dict(item_id=item_id)

A request such as ``/item?item_id=not-a-number`` returns a JSON error response
instead of entering the controller action.

The Error Handler
=================

For HTML forms and other user-facing pages, you usually want to redisplay a page
or redirect the user when validation fails. Pass an ``error_handler`` to
``@validate`` when validation failures should be handled by a different action.

.. code-block:: python

    from tg import TGController, expose, request, validate
    from tg.validation import Convert, RequireValue


    class RootController(TGController):
        @expose()
        def onerror(self, **kwargs):
            return 'An error occurred: %s' % request.validation.errors

        @expose()
        @validate({
            'quantity': Convert(int, msg='Quantity must be a number'),
            'title': RequireValue(msg='Title is required'),
        }, error_handler=onerror)
        def save(self, quantity=None, title=None):
            return 'Saved %s copies of %s' % (quantity, title)

The error handler is called with the unvalidated request parameters, so it is
usually best for handlers to accept ``**kwargs``. Validation messages remain
available through ``tg.request.validation`` while the handler runs.

Validating Forms
================

For manually written forms, put ``@validate`` on the action that processes the
submitted data and read validation errors from ``tg.request.validation`` in the
handler or template.

TurboGears can also validate widget-based forms. In TurboGears 2.5, install
and enable ``tgext.tw2`` before relying on ToscaWidgets2 forms; the extension
adds the TW2 middleware and registers TW2 validation errors with TurboGears.
When using ToscaWidgets2, pass the form class to ``@validate`` and provide an
error handler that redisplays the form:

.. code-block:: python

    import tw2.core as twc
    import tw2.forms as twf
    from tg import expose, validate


    class MovieForm(twf.Form):
        class child(twf.TableLayout):
            title = twf.TextField(validator=twc.Required)

        action = '/save_movie'

    @expose('myapp.templates.index')
    def index(self, **kw):
        return dict(form=MovieForm)

    @expose()
    @validate(MovieForm, error_handler=index)
    def save_movie(self, *args, **kw):
        return str(kw)

See :ref:`tw2_forms_validation` for ``tgext.tw2`` setup and a larger
ToscaWidgets2 form example.

Writing Custom Validators
=========================

A native TurboGears field validator is any object with a ``to_python`` method.
The method receives the submitted value and returns the converted value. Raise
:class:`tg.validation.TGValidationError` when validation fails.

.. code-block:: python

    from tg.validation import TGValidationError


    class PositiveInt:
        def to_python(self, value, state=None):
            try:
                value = int(value)
            except (TypeError, ValueError):
                raise TGValidationError('Integer expected', value)

            if value <= 0:
                raise TGValidationError('Positive integer expected', value)

            return value

Use it like any other explicit validator. Add an error handler when invalid
values should be rejected instead of passed to the original action with details
in ``tg.request.validation``:

.. code-block:: python

    from tg import expose, validate
    from tg.controllers.util import validation_errors_response

    @expose('json')
    @validate({'count': PositiveInt()}, error_handler=validation_errors_response)
    def repeat(self, count=None):
        return dict(count=count)

.. _validation_extensions:

Validation Extensions
=====================

TurboGears validation can be extended by registering additional validator types
and validation exceptions with the application configurator. The main example is
``tgext.formencode``, which restores FormEncode integration for applications
that still depend on FormEncode validators, schemas or variable decoding.

Using tgext.formencode
----------------------

Install the extension alongside your application::

    $ pip install tgext.formencode

For a packaged application, also add ``tgext.formencode`` to your project
requirements. Then enable it in your application's ``config/app_cfg.py`` before
the WSGI application is created:

.. code-block:: python

    from tg import FullStackApplicationConfigurator
    import tgext.formencode

    base_config = FullStackApplicationConfigurator()
    tgext.formencode.plugme(base_config)

Once enabled, FormEncode ``Invalid`` exceptions are treated as validation
errors and FormEncode schemas can be passed to ``@validate``.

.. note::

    ``tgext.formencode`` also plugs into TurboGears i18n so FormEncode error
    messages can be translated. FormEncode does not ship translation catalogs
    for every locale, including English. With ``tgext.formencode`` 0.1.1, a
    quickstarted application that has request-language detection enabled might
    log trapped ``LanguageError`` exceptions such as ``No translation file found
    for domain: 'FormEncode'`` even though validation responses still work.

    If your application does not need request-language detection, disable it in
    ``config/app_cfg.py`` before creating the WSGI application::

        base_config.update_blueprint({'i18n.enabled': False})

    If your application does use i18n, configure it to use languages for which
    FormEncode provides catalogs, or expect untranslated FormEncode messages
    until the extension falls back cleanly for missing catalogs.

Individual FormEncode Validators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from formencode import validators
    from tg import TGController, expose, validate
    from tg.controllers.util import validation_errors_response


    class RootController(TGController):
        @expose('json')
        @validate({
            'email': validators.Email(not_empty=True),
        }, error_handler=validation_errors_response)
        def subscribe(self, email=None):
            return dict(email=email)

FormEncode Schemas
~~~~~~~~~~~~~~~~~~

Use a schema when multiple fields must be validated together.

.. code-block:: python

    from formencode import Schema, validators
    from tg import TGController, expose, validate
    from tg.controllers.util import validation_errors_response


    class PasswordSchema(Schema):
        allow_extra_fields = True
        filter_extra_fields = True

        password = validators.String(not_empty=True)
        confirm_password = validators.String(not_empty=True)
        chained_validators = [
            validators.FieldsMatch('password', 'confirm_password')
        ]


    class RootController(TGController):
        @expose('json')
        @validate(PasswordSchema(), error_handler=validation_errors_response)
        def change_password(self, password=None, confirm_password=None):
            return dict(changed=True)

FormEncode schemas are strict by default: fields that are not declared by the
schema can produce validation errors. Set ``allow_extra_fields`` or
``filter_extra_fields`` on the schema when your controller receives additional
parameters.

Variable Decoding
~~~~~~~~~~~~~~~~~

``tgext.formencode`` also provides the traditional FormEncode variable decoding
decorator. It expands variable-encoded request parameters before validation:

.. code-block:: python

    from tg import TGController, expose
    from tgext.formencode import variable_decode


    class RootController(TGController):
        @expose('json')
        @variable_decode
        def tags(self, **kw):
            return kw

For example, parameters such as ``tag-0=python&tag-1=turbogears`` add a
``tag`` list to the controller parameters while leaving the original parameters
in place.
