.. _validation:

=====================
Parameters Validation
=====================

When using TurboGears, your controller methods get their arguments
built from the various GET, POST, and URL mechanisms provided by
TurboGears. The only downside is that all the arguments will be
strings and you'd like them converted to their normal Python datatype:
numbers to ``int``, dates to ``datetime``, etc.

This conversion functionality is provided by the `FormEncode`_ package
and is applied to your methods using the :class:`.validate`
decorator. FormEncode provides both validation and conversion as a
single step, reasoning that you frequently need to validate something
before you can convert it or that you'll need to convert something
before you can really validate it.

The ``@validate()`` decorator can evaluate both widget-based forms and
the standard form arguments so they are not dependent on widgets at
all.

Furthermore, the ``@validate()`` decorator is not really required at
all.  It just provides a convenience so that you can assume that you
have the right kind of data inside your controller methods. This helps
separate validation logic from application logic about what to do with
valid data.

If you don't put a ``@validate()`` decorator on your method, you'll
simply have to do the string conversion in your controller.

Validating Parameters
=====================

When not using forms, the story gets a bit more complex. Basically,
you need to specify which validator goes with which argument using in
the :class:`validate` decorator. Here's a simple example:

.. code-block:: python

    from tg import request, validate, expose, TGController
    from tg import validation

    class RootController(TGController):
        @expose('json')
        @validate({"a":validation.Convert(int), "b":validation.RequireValue()})
        def two_validators(self, a=None, b=None, *args):
            validation_status = tg.request.validation

            errors = [{key, value} in validation_status.errors.iteritems()]
            values =  validation_status.values
            return dict(a=a, b=b, errors=str(errors), values=str(values))

The dictionary passed to validators maps the incoming field names to
the appropriate FormEncode validators, ``Int`` in this example.

In case of a validation error TurboGears will provide the errors
and values inside ``tg.request.validation``.

.. note::

    FormEncode provides a number of useful pre-made validators for you to
    use: they are available in the :mod:`formencode.validators` module.

    FormEncode can be used with TurboGears via the tgext.formencode extension.


Validation Process Information
------------------------------

TurboGears provides some information on the currently running validation
process while it is handling the validation error.

Whenever an error handling is in process some properties are available in
the ``tg.request.validation`` to provide overview of the validation error:

    - ``tg.request.validation.values`` The submitted values before validation
    - ``tg.request.validation.errors`` The errors that triggered the error handling
    - ``tg.request.validation.exception`` The validation exception that triggered the error handling
    - ``tg.request.validation.error_handler`` The error handler that is being executed

The Error Handler
=================

In many cases you don't need the granularity provided by ``tg.request.validation``
and probably in case of an error you just want to send the user somewhere else
(maybe to reinsert the data he provided).

This can be achieved by using the ``error_handler`` argument of :class:`.validate`.
The provided function or controller method will be called to generate
a response for the user in case of an error instead of continuing with the current
action:

.. code-block:: python

    from tg import request, validate, expose, TGController
    from tg import validation

    class RootController(TGController):
        @expose()
        def onerror(self, **kwargs):
            return 'An error occurred: %s' % request.validation.errors

        @expose()
        @validate({"a":validation.Convert(int), "b":validation.RequireValue()},
                  error_handler=onerror)
        def two_validators(self, a=None, b=None, *args):
            return 'Values: %s, %s, %s' % (a, b, args)

Heading to ``/two_validators`` without providing a value for ``a`` will lead
to an ``"An error occurred"`` message as the ``onerror`` method is executed
instead of continuing with ``two_validators``.

.. note:: The method in question will be called, with the unvalidated data as
          its parameters, so it's usually best to accept ``**kwargs``.
          And error validation messages will be stored in ``tg.request.validation``.


Validating Forms
================

For manually written forms you can use ``@validate`` on the action that
processes the submitted data and add the errors in your template from
``tg.request.validation``.

TurboGears also provides a more convenient way to create forms,
validate submitted data and display error messages,
those can be managed through :ref:`tw2forms` which work together
with validation by :ref:`tw2_forms_validation`

Any widget based form can then be passed to the ``@validate`` which
will automatically validate the submitted data against that form.

Validators
==========

TurboGears applications will usually rely on three kind of validators:

    * :class:`.Convert` and :class:`RequireValue` which is builtin into TurboGears 
      and can be used for simple conversions like integers, floats and so on...
    * :mod:`tw2.core.validation` which provide ToscaWidgets validators for **Forms**
    * :mod:`formencode.validators` validators which can be used **Standalone** or with a **Form**

While in many cases ``Convert`` will suffice, the ``FormEncode`` library provides a pretty
complete set of validators:

    * Attribute
    * Bool
    * CIDR
    * ConfirmType
    * Constant
    * CreditCardExpires
    * CreditCardSecurityCode
    * CreditCardValidator
    * DateConverter
    * DateTime
    * DateValidator
    * DictConverter
    * Email
    * Empty
    * False
    * FancyValidator
    * FieldStorageUploadConverter
    * FieldsMatch
    * FileUploadKeeper
    * FormValidator
    * IDeclarative
    * IPhoneNumberValidator
    * ISchema
    * IValidator
    * Identity
    * IndexListConverter
    * Int
    * Interface
    * Invalid
    * MACAddress
    * MaxLength
    * MinLength
    * NoDefault
    * NotEmpty
    * Number
    * OneOf
    * PhoneNumber
    * PlainText
    * PostalCode
    * Regex
    * RequireIfMissing
    * RequireIfPresent
    * Set
    * SignedString
    * StateProvince
    * String
    * StringBool
    * StringBoolean
    * StripField
    * TimeConverter
    * True
    * URL
    * UnicodeString
    * Validator
    * Wrapper

For the absolute most up-to date list of available validators, check
the `FormEncode validators`_ module. You can also create your own
validators or build on existing validators by inheriting from one of
the defaults.

See the FormEncode documentation for how this is done.

.. _`FormEncode validators`: https://formencode.readthedocs.io/en/latest/modules/validators.html

You can also compose ``compound`` validators with logical operations,
the FormEncode compound module provides `All` (all must pass), 
`Any` (any one must pass) and `Pipe` (all must pass with the results of 
each validator passed to the next item in the Pipe).  You can use these 
like so::

    from formencode.compound import All
    ...
    the_validator=All(
        validators.NotEmpty(),
        validators.UnicodeString(),
    )

Writing Custom Validators
-------------------------

If you can't or don't want to rely on the FormEncode library you can write
your own validators.

Validators are simply objects that provide a ``to_python`` method
which returns the converted value or raise :py:class:`tg.validation.TGValidationError`

For example a validator that converts a paramter to an integer would look like:

.. code-block:: python

    from tg.validation import TGValidationError

    class IntValidator(object):
        def to_python(self, value, state=None):
            try:
                return int(value)
            except:
                raise TGValidationError('Integer expected')

Then it is possible to pass an instance of IntValidator to the TurboGears ``@validate``
decorator.

Schema Validators
-----------------

Sometimes you need more power and flexibility than you can get from
validating individual form fields.  Fortunately FormEncode provides
just the thing for us -- Schema validators.

If you want to do multiple-field validation, reuse validators or just
clean up your code, validation ``formencode.Schema``s are the way to go. 
You create a validation schema by inheriting from
:class:`formencode.schema.Schema` and pass the newly created ``Schema``
as the ``validators`` argument instead of passing a dictionary.

Create a schema:

.. code-block:: python

    class PwdSchema(schema.Schema):
        pwd1 = validators.String(not_empty=True)
        pwd2 = validators.String(not_empty=True)
        chained_validators = [validators.FieldsMatch('pwd1', 'pwd2')]

Then you can use that schema in @validate rather than a dictionary of
validators::

    @expose()    
    @validate(validators=PwdSchema())
    def password(self, pwd1, pwd2):
        if tg.request.validation.errors:
            return "There was an error"
        else:
            return "Password ok!"

Besides noticing our brilliant security strategy, please notice the
``chained_validators`` part of the schema that guarantees a pair of
matching fields.

Again, for information about ``Invalid`` exception objects, creating
your own validators, schema and FormEncode in general, refer to the
`FormEncode Validator`_ documentation and don't be afraid to check the
``Formencode.validators`` source. It's often clearer than the 
documentation.

Note that Schema validation is rigorous by default, in particular, you 
must declare *every* field you are going to pass into your controller 
or you will get validation errors.  To avoid this, add::

    class MySchema( schema.Schema ):
        allow_extra_fields=True

to your schema declaration.

.. _`FormEncode Validator`: http://www.formencode.org/en/latest/Validator.html

.. _FormEncode: http://formencode.org/

