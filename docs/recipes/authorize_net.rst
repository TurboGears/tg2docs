================================================
 Credit Card Authorizations Using authorize.net
================================================

.. code-block:: python

    # FancyValidator to process the Credit Card using the authorize package
    class ProcessCard(validators.FancyValidator):
        def _to_python(self, value, state):
    
           # --snip authorize package stuff--
    
            result_dict = aim.transaction(
                # --snip--
                )
    
            if result_dict['code'] == '1':
                # success
                return value
            else:
                # failure
                raise validators.Invalid(
                    result_dict['reason_text'],
                    value, state)
    
    class AuthnetForm(TableForm):
        submit_text='Purchase'
    
        validator = validators.Schema(
            chained_validators = [
                validators.CreditCardValidator('ccType','ccNumber'),
                validators.CreditCardSecurityCode('ccType','ccCode'),
                ProcessCard()
            ]
        )
    
        children=[
            TextField('name', validator=validators.String(not_empty=True)),
            # --snip--
            Spacer(),
            SingleSelectField('ccType', options=[('visa', 'Visa'),
    	    ('mastercard', 'Master Card'), ('discover', 'Discover'),
    	    ('amex', 'American Express')],
    	    validator=validators.NotEmpty),
            CalendarDatePicker('ccExpires', date_format="%m/%Y", validator=validators.NotEmpty),
            TextField('ccNumber', label_text='Card #', validator=validators.NotEmpty),
            TextField('ccCode', label_text='CVV Code', validator=validators.NotEmpty),
            Spacer()
        ]
    
    authnet_form = AuthnetForm('authnet_form')
    
    class AuthnetController(BaseController):
        @expose('vynetwork.templates.authnet.index')
        def index(self, **kw):
            if getattr(tmpl_context, 'form_errors', None):
                if tmpl_context.form_errors.get('_the_form', None):
                    flash(tmpl_context.form_errors['_the_form'], 'error')
            return dict(page='home', kw=kw, form=authnet_form)
    
        @validate(authnet_form, error_handler=index)
        @expose()
        def process(self, **kw):
            return 'Thank you!' 

