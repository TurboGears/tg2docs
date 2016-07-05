.. -*- mode: rst; encoding: utf-8 -*-

.. _kajiki-language:

========================
Kajiki Template Language
========================

Kajiki provides a XML-based template language that is heavily inspired by Kid_,
and Genshi_ which in turn was inspired by a number of existing template languages, namely
XSLT_, TAL_, and PHP_.

.. _kid: http://kid-templating.org/
.. _genshi: https://genshi.edgewall.org/
.. _python: http://www.python.org/
.. _xslt: http://www.w3.org/TR/xslt
.. _tal: http://www.zope.org/Wikis/DevSite/Projects/ZPT/TAL
.. _php: http://www.php.net/

This document describes the template language and will be most useful as
reference to those developing Kajiki XML templates. Templates are XML files of
some kind (such as XHTML) that include processing directives_ (elements or
attributes identified by a separate namespace) that affect how the template is
rendered, and template expressions that are dynamically substituted by
variable data.

.. _`directives`:

-------------------
Template Directives
-------------------

Directives are elements and/or attributes in the template that are identified
by the namespace ``py:``. They can affect how the
template is rendered in a number of ways: Kajiki provides directives for
conditionals and looping, among others.

All directives can be applied as attributes, and some can also be used as
elements. The ``if`` directives for conditionals, for example, can be used in
both ways:

.. code-block:: genshi

  <html>
    ...
    <div py:if="foo">
      <p>Bar</p>
    </div>
    ...
  </html>

This is basically equivalent to the following:

.. code-block:: genshi

  <html>
    ...
    <py:if test="foo">
      <div>
        <p>Bar</p>
      </div>
    </py:if>
    ...
  </html>

The rationale behind the second form is that directives do not always map
naturally to elements in the template. In such cases, the ``py:strip``
directive can be used to strip off the unwanted element, or the directive can
simply be used as an element.


Conditional Sections
====================

.. _`py:if`:

``py:if``
---------

The element and its content is only rendered if the expression evaluates to a
truth value:

.. code-block:: genshi

  <div>
    <b py:if="foo">${bar}</b>
  </div>

Given the data ``foo=True`` and ``bar='Hello'`` in the template context, this
would produce:

.. code-block:: xml

  <div>
    <b>Hello</b>
  </div>

But setting ``foo=False`` would result in the following output:

.. code-block:: xml

  <div>
  </div>

This directive can also be used as an element:

.. code-block:: genshi

  <div>
    <py:if test="foo">
      <b>${bar}</b>
    </py:if>
  </div>

.. _`py:switch`:
.. _`py:case`:
.. _`py:else`:

``py:switch``
-------------

The ``py:switch`` directive, in combination with the directives ``py:case``
and ``py:else`` provides advanced conditional processing for rendering one
of several alternatives. The first matching ``py:case`` branch is rendered, or,
if no ``py:case`` branch matches, the ``py:else`` branch is rendered.

The nested ``py:case`` directives will be tested for equality to the
parent ``py:switch`` value:

.. code-block:: genshi

  <div>
    <py:switch="1">
      <span py:case="0">0</span>
      <span py:case="1">1</span>
      <span py:else="">2</span>
    </py:switch>
  </div>

This would produce the following output:

.. code-block:: xml

  <div>
    <span>1</span>
  </div>

.. note:: The `py:switch` directive can only be used as a standalone tag
          and cannot be applied as an attribute of a tag.

Looping
=======

.. _`py:for`:

``py:for``
----------

The element is repeated for every item in an iterable:

.. code-block:: genshi

  <ul>
    <li py:for="item in items">${item}</li>
  </ul>

Given ``items=[1, 2, 3]`` in the context data, this would produce:

.. code-block:: xml

  <ul>
    <li>1</li><li>2</li><li>3</li>
  </ul>

This directive can also be used as an element:

.. code-block:: genshi

  <ul>
    <py:for each="item in items">
      <li>${item}</li>
    </py:for>
  </ul>


Snippet Reuse
=============

.. _`py:def`:
.. _`macros`:

``py:def``
----------

The ``py:def`` directive can be used to create macros, i.e. snippets of
template code that have a name and optionally some parameters, and that can be
inserted in other places:

.. code-block:: genshi

  <div>
    <p py:def="greeting(name)" class="greeting">
      Hello, ${name}!
    </p>
    ${greeting('world')}
    ${greeting('everyone else')}
  </div>

The above would be rendered to:

.. code-block:: xml

  <div>
    <p class="greeting">
      Hello, world!
    </p>
    <p class="greeting">
      Hello, everyone else!
    </p>
  </div>

If a macro doesn't require parameters, it can be defined without the 
parenthesis. For example:

.. code-block:: genshi

  <div>
    <p py:def="greeting" class="greeting">
      Hello, world!
    </p>
    ${greeting()}
  </div>

The above would be rendered to:

.. code-block:: xml

  <div>
    <p class="greeting">
      Hello, world!
    </p>
  </div>

This directive can also be used as an element:

.. code-block:: genshi

  <div>
    <py:def function="greeting(name)">
      <p class="greeting">Hello, ${name}!</p>
    </py:def>
  </div>

Variable Binding
================

.. _`with`:

``py:with``
-----------

The ``py:with`` directive lets you assign expressions to variables, which can
be used to make expressions inside the directive less verbose and more
efficient. For example, if you need use the expression ``author.posts`` more
than once, and that actually results in a database query, assigning the results
to a variable using this directive would probably help.

For example:

.. code-block:: genshi

  <div>
    <span py:with="y=7; z=x+10">$x $y $z</span>
  </div>

Given ``x=42`` in the context data, this would produce:

.. code-block:: xml

  <div>
    <span>42 7 52</span>
  </div>

This directive can also be used as an element:

.. code-block:: genshi

  <div>
    <py:with vars="y=7; z=x+10">$x $y $z</py:with>
  </div>

Structure Manipulation
======================

.. _`py:attrs`:

``py:attrs``
------------

This directive adds, modifies or removes attributes from the element:

.. code-block:: genshi

  <ul>
    <li py:attrs="foo">Bar</li>
  </ul>

Given ``foo={'class': 'collapse'}`` in the template context, this would
produce:

.. code-block:: xml

  <ul>
    <li class="collapse">Bar</li>
  </ul>

Attributes with the value ``None`` are omitted, so given ``foo={'class': None}``
in the context for the same template this would produce:

.. code-block:: xml

  <ul>
    <li>Bar</li>
  </ul>

.. note:: This directive can only be used as an attribute.


.. _`py:content`:

``py:content``
--------------

This directive replaces any nested content with the result of evaluating the
expression:

.. code-block:: genshi

  <ul>
    <li py:content="bar">Hello</li>
  </ul>

Given ``bar='Bye'`` in the context data, this would produce:

.. code-block:: xml

  <ul>
    <li>Bye</li>
  </ul>

This directive can only be used as an attribute.


.. _`py:replace`:

``py:replace``
--------------

This directive replaces the element itself with the result of evaluating the
expression:

.. code-block:: genshi

  <div>
    <span py:replace="bar">Hello</span>
  </div>

Given ``bar='Bye'`` in the context data, this would produce:

.. code-block:: xml

  <div>
    Bye
  </div>

This directive can also be used as an element (since version 0.5):

.. code-block:: genshi

  <div>
    <py:replace value="title">Placeholder</py:replace>
  </div>



.. _`py:strip`:

``py:strip``
------------

This directive conditionally strips the top-level element from the output. When
the value of the ``py:strip`` attribute evaluates to ``True``, the element is
stripped from the output:

.. code-block:: genshi

  <div>
    <div py:strip="True"><b>foo</b></div>
  </div>

This would be rendered as:

.. code-block:: xml

  <div>
    <b>foo</b>
  </div>

As a shorthand, if the value of the ``py:strip`` attribute is empty, that has
the same effect as using a truth value (i.e. the element is stripped).

.. _includes:

Includes
========

To reuse common snippets of template code, you can include other files using
py:include_ and py:import_.

.. _`py:include`:

py:include
----------

Includes the text of another template verbatim.  The precise semantics of this
tag depend on the `TemplateLoader` being used, as the `TemplateLoader` is used to
parse the name of the template being included and render its contents into the
current template.  For instance, with the `FileLoader`, you might use the
following:

.. code-block:: xml

    <py:include href="path/to/base.txt"/>

whereas in the `PackageLoader` you would use

.. code-block:: xml

    <py:include href="package1.package2.base"/>

.. _`py:import`:

py:import
---------

With `py:import`, you can make the functions defined in another template available
without expanding the full template in-place.  Suppose that we saved the
following template in a file `lib.xml`:

.. code-block:: xml

    <py:def function="evenness(n)">
       <py:if test="n%2==0">even</py:if><py:else>odd</py:else>
    </py:def>

Then (using the `FileLoader`) we could write a template using the `evenness`
function as follows:

.. code-block:: xml

    <div>
       <py:import hef="lib.xml" alias="lib"/>
       <ul>
          <li py:for="i in range(sz)">$i is ${lib.evenness(i)}</li>
       </ul>
    </div>

-------------------------------------
Converting Genshi Templates to Kajiki
-------------------------------------

Kajiki is a fast template engine which is 90% compatible with Genshi,
all of Genshi directives_ work in Kajiki too apart those involved in templates
inheritance as Kajiki uses **blocks** instead of **XInclude** and **XPath**.

Simple templates hierarchies (like the one coming from TurboGears quickstart)
can be moved to Kajiki blocks in a matter of seconds through the Kajiki
``autoblocks`` feature. Autoblocks will automatically create inclusion blocks
whenever a tag with the given name is found. So in case of simple hierarchies
we can easily remove the ``py:match`` and rely on ``autoblocks``.

.. note::

  Please note that this guide only works on version ``2.3.6`` and greater.

.. note::

  It's suggested to try this steps on a newly quickstarted Genshi application
  and then test them on your real apps when you are confident with the
  whole process.

Enabling Autoblocks
===================

Enabling autoblocks in Kajiki involves adding the ``templating.kajiki.xml_autoblocks``
option to your ``app_cfg.py`` with the list of tags that should be considered
autoblocks::

  base_config.renderers.append('kajiki')
  base_config['templating.kajiki.xml_autoblocks'] = ['head', 'body']

  # Set the default renderer
  base_config.default_renderer = 'kajiki'

Restarting your web application you will probably lead to an ``IOError``
regarding TurboGears being unable to find your template. This is because
Kajiki uses ``.xml`` as the default templates extension, while Genshi used
``.html``. What we need to do is add the following line to make Kajiki load
templates from ``.html`` files::

  base_config['templating.kajiki.template_extension'] = '.html'

Adapting the Master Template
============================

The only template we will need to adapt by hand is our ``master.html``
template, everything else will be done automatically. So the effort
of porting an application from Genshi to Kajiki is the same independently
from the size of the application.

First of all let's adapt our ``head`` tag to make it so that the content
from templates that extend our master gets included inside it:

.. code-block:: html+genshi
  :emphasize-lines: 1, 5

  <head py:match="head" py:attrs="select('@*')">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta charset="${response.charset}" />
    <title py:if="False">Your generic title goes here</title>
    <meta py:replace="select('*')"/>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap.min.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
  </head>

should became:

.. code-block:: html+genshi
  :emphasize-lines: 1, 5

  <head py:autoblock="False">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta charset="${response.charset}" />
    <title py:if="False">Your generic title goes here</title>
    <py:blocks name="head"/>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap.min.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
  </head>

Then we do the same with the ``body`` tag by disabling it as a block and
placing a block with the same name inside of it:

.. code-block:: html+genshi
  :emphasize-lines: 1, 16

  <body py:match="body" py:attrs="select('@*')">
    <!-- Navbar -->
    [...]

    <div class="container">
      <!-- Flash messages -->
      <py:with vars="flash=tg.flash_obj.render('flash', use_js=False)">
        <div class="row">
          <div class="col-md-8 col-md-offset-2">
            <div py:if="flash" py:replace="Markup(flash)" />
          </div>
        </div>
      </py:with>

      <!-- Main included content -->
      <div py:replace="select('*|text()')"/>
    </div>
  </body>

Which should became:

.. code-block:: html+genshi
  :emphasize-lines: 1, 16

  <body py:autoblock="False">
    <!-- Navbar -->
    [...]

    <div class="container">
      <!-- Flash messages -->
      <py:with vars="flash=tg.flash_obj.render('flash', use_js=False)">
        <div class="row">
          <div class="col-md-8 col-md-offset-2">
            <div py:if="flash" py:replace="Markup(flash)" />
          </div>
        </div>
      </py:with>

      <!-- Main included content -->
      <py:blocks name="body"/>
    </div>
  </body>

What happened is that we replaced the ``head`` and ``body`` blocks in the
master template (which were created by the ``xml_autoblocks`` option) with
blocks with the same name inside the head and body tags.

Now your application will properly start, but you will get a broken page
due to missing layout, css and so on.

Upgrading Templates
===================

This is because Kajiki doesn't understand the ``xi:include`` command and
so it is not including the ``master.html`` at all. To solve this issue
we can rely on a simple but helpful ``gearbox`` command to patch all our
templates by replacing ``xi:include`` with ``py:extends`` which is used
and recognized by Kajiki.

Just move inside the root of your project and run::

  $ gearbox patch -R '*.html' xi:include -r py:extends

You should get an output similar to::

  7 files matching
  ! Patching /private/tmp/prova/prova/templates/about.html
  ! Patching /private/tmp/prova/prova/templates/data.html
  ! Patching /private/tmp/prova/prova/templates/environ.html
  ! Patching /private/tmp/prova/prova/templates/error.html
  ! Patching /private/tmp/prova/prova/templates/index.html
  ! Patching /private/tmp/prova/prova/templates/login.html
  x Patching /private/tmp/prova/prova/templates/master.html

Which means that all our templates apart from ``master.html`` got patched
properly and now correctly use ``py:extends``.

Restarting your application now should lead to a properly working page
equal to the original Genshi one.

Congratulations, you successfully moved your templates from Genshi
to Kajiki.