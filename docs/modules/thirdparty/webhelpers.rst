.. _webhelpers:

==========
WebHelpers
==========

WebHelpers is a package designed to ease common tasks developers need
that are usually done for formatting or displaying data in templates.

Helpers available by module:


.. module:: webhelpers.date

Date
====

.. autofunction:: distance_of_time_in_words
.. autofunction:: time_ago_in_words


    

.. module:: webhelpers.html.converters

Converters
==========

Functions that convert from text markup languages to HTML

.. autofunction:: markdown
.. autofunction:: textilize


Tags
====

.. automodule:: webhelpers.html.tags

Form Tags
---------

.. autofunction:: checkbox
.. autofunction:: end_form
.. autofunction:: file
.. autofunction:: form
.. autofunction:: hidden
.. autofunction:: password
.. autofunction:: radio
.. autofunction:: select
.. autofunction:: submit
.. autofunction:: text
.. autofunction:: textarea
.. autoclass:: ModelTags
    :members:
    
    .. automethod:: __init__

Hyperlinks
----------

.. autofunction:: link_to
.. autofunction:: link_to_if
.. autofunction:: link_to_unless

Other Tags
----------

.. autofunction:: image

Head Tags
---------

.. autofunction:: auto_discovery_link
.. autofunction:: javascript_link
.. autofunction:: stylesheet_link

Utility
-------

.. autofunction:: convert_boolean_attrs


.. module:: webhelpers.html.tools

Tools
=====

Powerful HTML helpers that produce more than just simple tags.

.. autofunction:: auto_link
.. autofunction:: button_to
.. autofunction:: highlight
.. autofunction:: mail_to
.. autofunction:: strip_links


.. module:: webhelpers.mimehelper

MIMEType Helper
===============

The MIMEType helper assists in delivering appropriate content types
for a single action in a controller, based on several requirements:

1) Does the URL end in a specific extension? (.html, .xml, etc.)
2) Can the client accept HTML?
3) What Accept headers did the client send?

If the URL ends in an extension, the mime-type associated with that is
given the highest preference. Since some browsers fail to properly set
their Accept headers to indicate they should be served HTML, the next
check looks to see if its at least in the list. This way those
browsers will still get the HTML they are expecting.

Finally, if the client didn't include an extension, and doesn't have
HTML in the list of Accept headers, than the desired mime-type is
returned if the server can send it.

.. autoclass:: MIMETypes
    :members:


.. module:: webhelpers.number

Number
======

Number formatting and calculation helpers.

.. autofunction:: format_number
.. autofunction:: mean
.. autofunction:: median
.. autofunction:: percent_of
.. autofunction:: standard_deviation
.. autoclass:: Stats
.. autoclass:: SimpleStats


Misc
====

.. automodule:: webhelpers.misc

.. autofunction:: all
.. autofunction:: any
.. autofunction:: no
.. autofunction:: count_true
.. autofunction:: convert_or_none


.. module:: webhelpers.pylonslib

Pylons-specific
===============

.. autoclass:: Flash
    :members:
    
    .. automethod:: __init__
    .. automethod:: __call__


Text
====

.. automodule:: webhelpers.text

.. autofunction:: chop_at
.. autofunction:: excerpt
.. autofunction:: lchop
.. autofunction:: plural
.. autofunction:: rchop
.. autofunction:: strip_leading_whitespace
.. autofunction:: truncate
.. autofunction:: wrap_paragraphs

Submodules
==========
..  toctree::
    :maxdepth: 1

    webhelpers_paginate
    webhelpers_feedgenerator
    
