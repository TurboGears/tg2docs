.. _tw2forms:

===============
Widgets & Forms
===============

TurboGears relies on ToscaWidgets2 for Widgets and Forms definition.
Widgets are small reusable HTML components with attached values, and
a form is a collection of one or more widgets (one for each field) that
display the fields.

ToscaWidgets2 Widgets provide:

    * Templating support to generate the HTML
    * Support for widget configuration options
    * Resources declaration and injection (for css & JS required by the widget)

Widgets
=======

Creating Widgets
----------------

Widgets can be created by subclassing :class:`tw2.core.Widget` and defining
a ``template`` argument for it. By default the template argument has to be
the dotted format path of a template file (same syntax you provide to ``@expose``),
but an ``inline_engine_name`` option can be provided to tell ToscaWidgets2
that the template argument is actually the template itself.

.. code-block:: python

    import tw2.core as twc

    class UserAvatarWidget(twc.Widget):
        inline_engine_name = 'kajiki'
        template = '<div class="username">${w.name}</div>'

To display the widget just call the ``.display(**kwargs)`` method of the
widget passing any parameter you want to provide to the widget:

.. code-block:: python

    >>> UserAvatarWidget.display(name='John Doe')
    Markup(u'<div class="username">John Doe</div>')

The passed ``name`` is available inside the template as ``w.name``.
All the arguments passed to the :meth:`tw2.core.Widget.display` function will be available
as properties of the widget instance inside the template itself.

Widgets Parameters
------------------

While our previous example worked as expected, you probably noticed that when
the ``name`` argument to display is omitted it will lead to a crash and we
didn't provide any detail to developers that they must provide it.

to solve this ToscaWidgets provides parameters support through the :class:`tw2.core.Param`
class.

To make the ``name`` parameter explicit and provide a default value for it we
can add it to the widget as a ``Param``:

.. code-block:: python

    import tw2.core as twc

    class UserAvatarWidget(twc.Widget):
        name = twc.Param(default='Unknown User', description='Name of the logged user')

        inline_engine_name = 'kajiki'
        template = '<div class="username">${w.name}</div>'

Trying to display the widget without a ``name`` argument will now just provide the
default value instead of leading to a crash:

.. code-block:: python

    >>> UserAvatarWidget.display()
    Markup(u'<div class="username">Unknown User</div>')

    >>> UserAvatarWidget.display(name='John Doe')
    Markup(u'<div class="username">John Doe</div>')

The passed value will be available inside the template as properties
of the widget instance and the widget instance will be available as ``w``.
So in the previous example the user name was available as ``w.name``.

.. note:: Whenever you need to know which options a widget provides you want
          to have a look at its parameters. They will usually provide a short
          description of the parameter purpose.

Widgets Resources
-----------------

To implement more advanced widgets you will probably need to add styling
and javascript to them. This can easily be done through **resources**
support provided by ToscaWidgets.

A resource is an instance of :class:`tw2.core.JSLink`, :class:`tw2.core.JSSource`,
:class:`tw2.core.CSSLink` and :class:`tw2.core.CSSSource`, which allow to provide
access to a CSS and Javascript file or to inline code for the widget.

Resources are injected for you in the ``<head>`` tag by a middleware that
handles resources injection for widgets. Each resource has an ``id`` attribute
so the same resource won't be injected twice as far as all instances of the
resources share the same ``id``.

The following example adds an inline CSS to make user avatars bold and provides
*jQuery* as a dependency to add a *click* function that shows a dialog with the
username inside when clicked:

.. code-block:: python

    import tw2.core as twc


    class UserAvatarWidget(twc.Widget):
        name = twc.Param(default='Unknown User', description='Name of the logged user')

        inline_engine_name = 'kajiki'
        template = '''
            <div class="useravatar" id="${w.id}">
                <div class="username">${w.name}</div>
                <script>$('#${w.id}').click(function() { alert('${w.name}') })</script>
            </div>
        '''
        resources = [
            twc.CSSSource(id='useravatarstyle',
                          src='.useravatar .username { font-weight: bold; }'),
            twc.JSLink(id='jquery',
                       link='https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js')
        ]

Calling ``UserAvatarWidget.display`` will generate the short html snippet:

.. code-block:: html

    <div class="useravatar" id="id_a9a9fbba90744ff2a894f5ea5ae99f44">
        <div class="username">John Doe</div>
        <script>$('#id_a9a9fbba90744ff2a894f5ea5ae99f44').click(function() { alert('John Doe') })</script>
    </div>

but will also inject the required resources into the ``head`` tag:

.. code-block:: html

    <head>
        <style type="text/css">.useravatar .username { font-weight: bold; }</style>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js" type="text/javascript" id="jquery"></script>
        <meta content="width=device-width, initial-scale=1.0" name="viewport">
        ...
    </head>

Note that display the widgets twice on the page won't inject the resources twice. That's
because ToscaWidgets will recognize that ``useravatarstyle`` and ``jquery`` resources already
got injected and won't insert them again.

Widgets also provide an ``.id`` attribute automatically generated by ToscaWidgets2
(it can be overwritten at display time), this allows to uniquely identify
each widget instance from any javascript injected into the page.

In the previous example we leveraged this feature to point *jQuery* to each specific
widget instance through ``$('#${w.id}')``. If you display two ``UserAvatarWidget``
with different names on the same page, you will notice that clicking each one of them
will properly show the right name thanks to this.


Forms
=====

Displaying Forms
----------------

Forms are actually a particular kind of Widget, actually a particular kind of
:class:`tw2.core.CompoundWidget` as they can contain more widgets inside themselves.

A Forms is actually a widget that provides a template to displays through a
``Layout`` all the other widgets that are provided inside the form.

To create a form you will have to declare it specifying:

    * the form action (where to submit the form data)
    * the form layout (how the form will be displayed)
    * the form fields

The *action* can be specified as an attribute of the form itself, while the *layout*
must be a class named **child** which has to inherit from :class:`tw2.forms.BaseLayout`.
Any of :class:`tw2.forms.TableLayout` or :class:`tw2.forms.ListLayout` will usually do, but you
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
Any field of the form can be filled using the ``value`` argument passed to the
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

.. _tw2_forms_validation:

Validating Fields
-----------------

ToscaWidgets2 is able to use any `FormEncode` validator for validation of
both fields and forms. More validators are also provided inside the
:mod:`tw2.core.validators` module.

To start using validation we have to declare the validator for each form field.
For example to block submission of our previous form when no title or director
is provided we can use the :class:`tw2.core.Required` validator:

.. code-block:: python

    class MovieForm(twf.Form):
        class child(twf.TableLayout):
            title = twf.TextField(validator=twc.Required)
            director = twf.TextField(value="Default Director", validator=twc.Required)
            genres = twf.CheckBoxList(options=['Action', 'Comedy', 'Romance', 'Sci-fi'])

        action = '/save_movie'

Now the forms knows how to validate the title and director fields,
but those are not validated in any way.
To enable validation in TurboGears we must use the :class:`.validate` decorator
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

.. note:: TurboGears keeps track of the form that failed validation
          when running the ``error_handler``, so if we display that
          form during the ``error_handler`` it will automatically
          display the validation error messages, nothing particular
          is required to show errors apart displaying the form after
          validation failed.

More about TurboGears support for validation is available inside the
:ref:`validation` page.

Validating Compound Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose that you are afraid that people might enter a wrong director name
for your movies. The most simple solution would be to require them to
enter the name two times to be sure that it is actually the correct one.

How can we enforce people to enter two times the same name inside our form?
Apart from fields, ToscaWidgets permits to set validators to forms.
Those can be used to validate form fields together instead of one by one.
To check that our two directors equals we will use the
:class:`formencode.validators.FieldsMatch` validator:

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

Manual Validation
~~~~~~~~~~~~~~~~~

Usually you will rely on the ``@validate`` decorator to check for form errors
on submission and display the form with proper error messages, but there might
be cases where you want to manually validate the form and then pass the errors
to it.

To validate a Form just call the :meth:`tw2.forms.Form.validate` method on it
with the dictionary of values to validate:

.. code-block:: python

    MovieForm.validate({})

That will raise a :class:`tw2.core.ValidationError` in case the validation failed,
the validation error itself will contain an instance of the widget already configured
to display the error messages:

.. code-block:: python

    try:
        MovieForm.validate(dict())
    except twc.ValidationError as e:
        # Display widget with error messages inside.
        e.widget.display()

Relocatable Widget Actions
--------------------------

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

Custom Layouts
--------------

While using ``tw2.forms.TableLayout`` and ``tw2.forms.ListLayout`` it's easy to perform
most simple styling and customization of your forms, for more complex widgets
a custom template is usually the way to go.

You can easily provide your custom layout by subclassing ``tw2.forms.widgets.BaseLayout``
and declaring a template for it inside your forms.

For example it is possible to create a name/surname form with a side field for notes
using the bootstrap CSS framework:

.. code-block:: python

    from tw2.core import Validator
    from tw2.forms.widgets import Form, BaseLayout, TextField, TextArea, SubmitButton

    class SubscribeForm(Form):
        action = '/submit'

        class child(BaseLayout):
            inline_engine_name = 'kajiki'
            template = '''
    <div py:strip="">
        <py:for each="c in w.children_hidden">
            ${c.display()}
        </py:for>

        <div class="form form-horizontal">
            <div class="form-group">
                <div class="col-md-7">
                    <div py:with="c=w.children.name"
                         class="form-group ${c.error_msg and 'has-error' or ''}">
                        <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                        <div class="col-md-9">
                            ${c.display()}
                            <span class="help-block" py:content="c.error_msg"/>
                        </div>
                    </div>
                    <div py:with="c=w.children.surname"
                         class="form-group ${c.error_msg and 'has-error' or ''}">
                        <label for="${c.compound_id}" class="col-md-3 control-label">${c.label}</label>
                        <div class="col-md-9">
                            ${c.display()}
                            <span class="help-block" py:content="c.error_msg"/>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 col-md-offset-1">
                    ${w.children.notes.display()}
                </div>
            </div>
        </div>
    </div>
    '''

        name = TextField(label=l_('Name'), validator=Validator(required=True),
                         css_class="form-control")
        surname = TextField(label=l_('Surname'), validator=Validator(required=True),
                            css_class="form-control")
        notes = TextArea(label=None, placeholder=l_("Notes"),
                         css_class="form-control", rows=8)

        submit = SubmitButton(css_class='btn btn-primary', value=l_('Create'))

