.. _tw2forms:

=================================
Creating and Validating Forms
=================================

TurboGears relies on ToscaWidgets for Forms building and validations.
Since version 2.2 TurboGears uses ToscaWidgets2, this is an introduction
on using ToscaWidgets2 for building and validating forms, a more complete
documentation is available on the
`ToscaWidgets2 Documentation <http://tw2core.readthedocs.org/en/latest/index.html#>`_ itself.

Displaying Forms
======================

To create a form you will have to declare it specifying:

    * the form action (where to submit the form data)
    * the form layout (how the form will be displayed)
    * the form fields

The *action* can be specified as an attribute of the form itself, while the *layout*
must be a class named **child** which has to inherit from ``tw2.forms.BaseLayout``.
Any of ``tw2.forms.TableLayout`` or ``tw2.forms.ListLayout`` will usually do, but you
can easily write your own custom layouts. The form *fields* can then be specified
inside the **child** class.

.. code-block:: python

    import tw2.core as twc
    import tw2.forms as twf

    class MovieForm(twf.Form):
        class child(twf.TableLayout):
            title = twf.TextField()
            director = twf.TextField(value='Default Director')
            genres = twf.CheckBoxList(options=['Action', 'Comedy', 'Romance', 'Sci-fi'])

        action = '/save_movie'

To display the form we can return it from the controller where it must be rendered:

.. code-block:: python

    @expose('tw2test.templates.index')
    def index(self, *args, **kw):
        return dict(page='index', form=MovieForm)

and *display* it inside the template itself.
Any field of the form can be filled using the *value* argument passed to the
display function. The values provided inside this argument will override the
field default ones.

.. code-block:: html+genshi

    <div id="getting_started">
        ${form.display(value=dict(title='default title'))}
    </div>

When submitting the form the **save_movie** controller declared in the *action*
attribute of the form will receive the submitted values as any other provided
GET or POST parameter.

.. code-block:: python

    @expose()
    def save_movie(self, **kw):
        return str(kw)

Validating Fields
=====================

ToscaWidgets2 is able to use any `FormEncode` validator for validation of
both fields and forms. More validators are also provided inside the
``tw2.core.validators`` module.

To start using validation we have to declare the validator for each form field.
For example to block submission of our previous form when no title or director
is provided we can use the ``tw2.core.Required`` validator:

.. code-block:: python

    class MovieForm(twf.Form):
        class child(twf.TableLayout):
            title = twf.TextField(validator=twc.Required)
            director = twf.TextField(value="Default Director", validator=twc.Required)
            genres = twf.CheckBoxList(options=['Action', 'Comedy', 'Romance', 'Sci-fi'])

        action = '/save_movie'

Now the forms knows how to validate the title and director fields,
but those are not validated in any way.
To enable validation in TurboGears we must use the **tg.validate** decorator
and place it at our form action:

.. code-block:: python

    @expose()
    @validate(MovieForm, error_handler=index)
    def save_movie(self, *args, **kw):
        return str(kw)

Now every submission to */save_movie* url will be validated against
the *MovieForm* and if it doesn't pass validation will be redirected
to the *index* method where the form will display an error for each field
not passing validation.

More about TurboGears support for validation is available inside the
:ref:`validation` page.

Validating Compound Fields
============================

Suppose that you are afraid that people might enter a wrong director name
for your movies. The most simple solution would be to require them to
enter the name two times to be sure that it is actually the correct one.

How can we enforce people to enter two times the same name inside our form?
Apart from fields, ToscaWidgets permits to set validators to forms.
Those can be used to validate form fields together instead of one by one.
To check that our two directors equals we will use the
``formencode.validators.FieldsMatch`` validator:

.. code-block:: python

    import tw2.core as twc
    import tw2.forms as twf
    from formencode.validators import FieldsMatch

    class MovieForm(twf.Form):
        class child(twf.TableLayout):
            title = twf.TextField(validator=twc.Required)
            director = twf.TextField(value="Default Director", validator=twc.Required)
            director_verify = twf.TextField()
            genres = twf.CheckBoxList(options=['Action', 'Comedy', 'Romance', 'Sci-fi'])

        action = '/save_movie'
        validator = FieldsMatch('director', 'director_verify')

Nothing else of our code needs to be changed, our */save_movie* controller
already has validation for the *MovieForm* and when the form is submitted
after checking that there is a title and director will also check that
both *director* and *director_verify* fields equals.

Relocatable Widget Actions
==========================

Whenever you run your application on a mount point which is not the root of
the domain name your actions will have to poin to the right path inside the
mount point.

In TurboGears2 this is usually achieved using the ``tg.url`` function which
checks the `SCRIPT_NAME` inside the request environment to see where
the application is mounted. The issue with widget actions is that widgets
actions are globally declared and ``tg.url`` cannot be called outside of
a request.

Calling ``tg.url`` while declaring a form and its action will cause a crash
to avoid this TurboGears provides a lazy version of the url method which
is evaluated only when the widget is displayed (``tg.lurl``):

.. code-block:: python

    from tg import lurl

    class MovieForm(twf.Form):
        class child(twf.TableLayout):
            title = twf.TextField(validator=twc.Required)
            director = twf.TextField(value="Default Director", validator=twc.Required)
            genres = twf.CheckBoxList(options=['Action', 'Comedy', 'Romance', 'Sci-fi'])

        action = lurl('/save_movie')

Using ``tg.lurl`` the form action will be correctly written depending on
where the application is mounted.

Please pay attention that usually when registering resources on ToscaWidgets (both
tw1 and tw2) it won't be necessary to call neither ``tg.url`` or ``tg.lurl`` as
all the ``Link`` subclasses like ``JSLink``, ``CSSLink`` and so on will already
serve the resource using the application mount point.

Automatic Form Generation
===========================

TurboGears provides support for forms autogeneration from models using ``Sprox``.

Those features are documented inside the :ref:`form-basics` page.

Back to ToscaWidgets1
======================

Some projects may still want to rely on ToscaWidgets1 due to legacy code or
due to external packages which are not available on ToscaWidgets2.

If you want to switch back your entire project to ToscaWidgets1, just remove the:

.. code-block:: python

    base_config.prefer_toscawidgets2 = True

from your `config/app_cfg.py`.

If you want to use both ToscaWidgets2 and ToscaWidgets1 remove the *prefer_toscawidgets2* line
and replace it with:

.. code-block:: python

    base_config.use_toscawidgets = True
    base_config.use_toscawidgets2 = True

Please keep in mind that recent versions of `sprox`, `tgext.crud` and `tgext.admin`
all rely on ToscaWidgets2 if it is available inside your virtualenv so remember to have
ToscaWidgets2 enabled inside your project or remove it from your virtual environment
if you want to use those modules.