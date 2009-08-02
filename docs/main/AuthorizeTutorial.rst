Using Authorize.net in a TurboGears Form
===========================================

.. contents:: Table of Contents
   :depth: 2

The goal of this tutorial is to get a tw.forms form to go through two layers of validation before passing:

   1) Use the validation packages provided by tw.forms and formencode
   2) If the first layer of validation passes, try to run the authorize.net charge using the authorize package. If this returns a response code of 1 (approved) then all validation has passed. Otherwise, invalidate the form and flash the authorize.net error.

The authorize package
---------------------

The authorize package handles authorize.net requests, and can be found `here <http://www.adroll.com/labs>`_ or by typing: ``easy_install authorize``

Defining the validator
----------------------

First we will need to define our ProcessCard() class which will be the chained FancyValidator for processing the card::

    import tw.forms as twf
    from authorize import aim as aim_api

    # FancyValidator to process the Credit Card using the authorize package
    class ProcessCard(twf.validators.FancyValidator):
        def _to_python(self, value, state):
            # Setup the aim Api object.
            aim = aim_api.Api(AUTHNET_LOGIN, AUTHNET_KEY, is_test=False)

            # Create a transaction against a credit card
            result_dict = aim.transaction(
                amount=u"16.00",
                card_num=unicode(value['card_number']),
                exp_date=unicode(value['card_expiry']),
                # ...and others...
                )

            if result_dict['code'] == '1':
                # success
                return value
            else:
                # failure
                raise twf.validators.Invalid(result_dict['reason_text'], value, state)

Defining the form
-----------------

Next we'll define our form class that will end up being passed to the view::

    from tw.api import WidgetsList

    class AuthnetForm(twf.TableForm):
        submit_text='Process Card'

        # specify chained validators
        validator = twf.validators.Schema(
            chained_validators = [
                twf.validators.CreditCardValidator('card_type','card_number'),
                twf.validators.CreditCardSecurityCode('card_type','card_cvv'),
                # you could also add an expiry validator, but authnet will handle this for you
                ProcessCard()
            ]
        )

        # specify form fields
        class fields(WidgetsList):
            name = twf.TextField(validator=twf.validators.String(not_empty=True))
            # ...and others like address, city, state, zip...
            spacer = twf.Spacer(suppress_label=True)
            card_type = twf.SingleSelectField(options=[('visa', 'Visa'),
                                                       ('mastercard', 'Master Card'),
                                                       ('discover', 'Discover'),
                                                       ('amex', 'American Express')], validator=twf.validators.NotEmpty)
            card_expiry = twf.CalendarDatePicker(date_format="%m/%Y", validator=twf.validators.NotEmpty)
            card_number = twf.TextField(label_text='Card #', validator=twf.validators.NotEmpty)
            card_cvv = twf.TextField(label_text='CVV Code', validator=twf.validators.NotEmpty)

Using it in a controller
------------------------

Now all you have to do is set up your controller class methods to use the form::

    # Assign a name to the form
    authnet_form = AuthnetForm('authnet_form', action='/authnet/process/')

    class AuthnetController(BaseController):
        @expose('authnet.templates.index')
        def index(self, **kw):
            if '_the_form' in tmpl_context.form_errors:
                # if we have top-level form errors, use flash() to display them
                flash(tmpl_context.form_errors['_the_form'], 'error')
            # Use ${form()} to print the form in your template
            return dict(form=authnet_form)
        
        
        @validate(authnet_form, error_handler=index)
        @expose()
        def process(self, **kw):
            # if validation passes, this method will run (specified by form action)
            return 'Card was successfully charged!'
