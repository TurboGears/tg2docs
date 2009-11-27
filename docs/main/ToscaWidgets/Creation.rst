.. _developing_toscawidgets:

Developing Toscawidgets
=======================

Widgets Are Stateless
---------------------

ToscaWidgets use stateless widgets in order to maintain a low memory
footprint during execution.  What this means is that all instances
of a widget reside in the same execution thread on the server.  For
this reason, no modifications can be made to the widgets at runtime
because the results may be propogated across multiple requests
to the server, resulting in thread safety issues, along with potential
security risks.  A simple way to say this is that widgets are stateless,
that is you may not change their attributes after their initial creation.


Role of data in your widget
---------------------------

Because widgets are stateless, data for their attributes must only be
provided at start time.  However, that is not to say that widgets cannot
provide dynamic data.  Display data may be passed into the widget's 
``display()`` call such that it can provide dynamic data for the user.
The other way to moodify a widgets rendering data is to modify a widget's
``update_params()`` method, but that will be discussed later.

Parameters
----------

Parameters are defined in a widget's definition.  These are variables
that can be passed into a widgets's ``display()`` method at render time.
These parameters are then passed onto the widget's display template
for use inrendering.  Here is how you would define parameters for a 
TextArea widget::

    class TextArea(Widget):
        params = ['rows', 'cols']
        rows=10
        cols=30

It's easy as that, ``rows`` and ``cols`` will now be added to your template's
namespace upon rendering.  It would be easy enough to create a new widget
with a call as follows::
    
    my_text_area = TextArea(rows=38, cols=38)
    
This would override the defaults provided by the widget and set the row and
column values to 38.

Parameters are collected from a widget's parameter, so that if you have
a parameter defined in one widget, widgets that subclass that widget will
automatically add the parameters to the parameter list.  This makes mixins
fairly easy to create as in this example::

    class MyField(Widget):
        params = ['css_class', 'name', 'value']
        css_class = 'my-field-class'
        name = None
        value = None
        
    
    class MyTextArea(MyField)
        params = ['rows', 'cols']
        rows=10
        cols=30
        
Now MyTextArea widgets will have the default css_class value unless overridden,
and also obtain the name and value parameters.  Now you can instantiate the widget
with name and value parameters and they will be made available to the widget's
template at render time.

Update Params
---------------

As mentioned earlier, update_params gives the developer an oportunity to modify
parameters of the widget before it is rendered.  For example, you may want to populate
the options of a select field from the database at runtime.  Here is what the code
for that would look like::

    from tw.forms import SingleSelectField
    from myapp.model import User, DBSession
    
    class UserSelectField(SingleSelectField)
        def update_params(self, d):
            options = [user.user_name, user.display_name for user in DBSession.query(User).all()]
            if self.nullable:
                options.append([None,"-----------"])
            if len(options) == 0:
                return d
            d['options']= options
            return d

``update_params`` is called with a dictionary representing the values of the widget parameters.
It is here where you can modify them before final rendering.

JavaScript Callbacks
----------------------
.. todo:: Difficulty: Medium. add section about the javascript callbacks


Typical Widget Components
-------------------------

 * Template code
 * Resources
 * Server-side code

Template Code
~~~~~~~~~~~~~

 * TW supports all the template engines supported by Buffet_ 
 * Templates are usually kept in separate files, although it is
   possible to inline in code.
 * The variables available in the template are: parameters defined for
   the widget (see below); TW built-in functions (args_for, value_for,
   display_child, css_class) and any provided by the user-defined
   functions update_params and get_extra_vars.

Resources
~~~~~~~~~

 * Once a resource is defined, the TW middleware serves that as a
   static directory.
 * Widgets specify their JS and CSS dependencies, and links are
   automatically inserted into appropriate points in the document
   (e.g. the HEAD section). There are two mechanisms for doing this:

    * Widgets are detected in variables passed from the controller to
      templates, and the resource requirements are collected. The
      site-wide master template includes code to render the
      requirements appropriately.
    * There is an experimental mode to rewrite the output document
      with links; this avoids the widgets needing to be passed to the
      template.

Server-side code
~~~~~~~~~~~~~~~~

 * Defines widget parameters, and default values for parameters.
 * Can run code at hook points; the main one is update_params, called
   just before display.
 * Having the template code call Python functions is discouraged; such
   code is better included in update_params.

Compound Widgets
----------------

All ToscaWidgets are in fact compound widgets. This means that every
widget can contain child widgets which get rendered at the same time
as the parent widget, without explicit instruction to do so.  This
gives ToscaWidgets the following functionality:

 * Parent / child relationships
 * Repeating widgets
 * Generation of compound IDs
 * Decoding nested dictionaries for values and parameters
 * Utility functions, e.g. ichildren_hidden

Compound IDs are generated by going through the tree from root to the
node, joining all the names (and numbers for repeaters) into a
globally unique name. The generated IDs need to match the validation
schema.

A compound widget takes a dictionary as it's value when ``display()`` is 
called, and passes individual values to child widgets. A similar system
works for parameters, but you have to do .child_args.

.. todo:: Difficulty: Easy. check this (.child_args), it's been a while

.. _Buffet: http://projects.dowski.com/projects/buffet


