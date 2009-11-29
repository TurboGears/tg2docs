.. _mako:

Why Mako?
=========

Mako provides another template rendering solution for TurboGears, it has a
couple of advantages:

 * Is very fast! (as fast as some C engines).
 * Mako is supported by Jython (and therefore TG projects utilizing Mako will run on Jython).
 * Mako uses inheritance instead of matching to combine page tempates.   This is often easier
   for developers to understand and see where problems lie.
 * Mako provides namespaces that behaves just like regular python code.
 * Mako syntax is much closer to standard python than many XML-based languages like TAL or Genshi.
 * Mako contains callable blocks.
 * Mako can be be used to generate non-html markup as neither the template or the output needs to be valid html.
 * Mako is the default in Pylons, so Pylons users will feel at home with it's use.

For more information see http://www.makotemplates.org

However it has one major tradeoff. The main reason for it's speed gain over genshi is the lack of "(x)html" validation. Some see this as 
an advantage some as a disavantage. This tradeoff can be mitigated with the use of a validator during development.

TurboGears mako Support
------------------------

All major components of TurboGears now support mako, including the admin
and CrudRestController.  This means that if you prefer the speed that mako
offers right now over the possible speedups Genshi will offer in the future.
Additionally, you may choose to quickstart your TurboGears application with
mako and you will then get a master template that is compatible with the
tgext.admin template.

Using Mako in TG2
---------------------

TurboGears allows you to setup and use Mako templates by simply adding it to
the list of renderers to prepare in base_config::

  base_config.renderers.append('mako')

You can also set it as the default renderer by setting::

   base_config.default_renderer = "mako"

You do not need to set the default renderer to mako, but if your 
project will be using mako primarily, it is a good idea to do so.

Dotted Lookup Support
-----------------------
Since TurboGears relies on dotted template support for it's standard, this
standard also applies to Mako.  Therefore, all templates are referenced using
a dotted name, instead of slashes, and this applies to inherited/imported templates
within your template as well.

Local Support
--------------
Mako support also includes support for ``local:`` in your template name.  What this
allows you to do is to tell TurboGears to look for the referenced template in the 
locally executing namespace, as apposed to a fully-dotted name.  This allows you to
write extensions that can "plug in" to an existing TurboGears project by providing
direct access to a project's master template.  tgext.admin takes advantage of this; most
templates have the following code at the beginning of their files::

    <%inherit file="local:templates.master"/>


Exposing a mako template
-------------------------

If you have your project's default set to genshi, don't fret, you may still use 
mako within your app.  Simply preface your template name with mako, producing
an expose decorator that might look like this::
    
    @expose('mako:mytgapp.templates.my_awesome_mako_template')
    def my_awesome_controller_method(self, **kw):
        ...

References
-----------
The `Mako docs <http://www.makotemplates.org/docs/syntax.html>`_ cover template
syntax very well, so we'll not repeat it. Instead, we refer you to their site.
