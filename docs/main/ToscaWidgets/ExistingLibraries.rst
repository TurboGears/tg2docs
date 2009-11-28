.. _existing_toscawidgets_packages:

Existing ToscaWidgets Packages
==============================

ToscaWidgets has been around for a few years and has grown a significant
set of widget libraries.  TW has grown from it's simple roots defining
Form widgets to include a full suite of ajax enabled capabilities.
Recent versions of TW even support on-widget controllers which makes
it easy to encapsulate both server and client side code in the same
object.  In addition to form functionality nearly every major JavaScript 
library is wrapped in someway by ToscaWidgets.



Form Libraries
--------------------

tw.forms
++++++++++++++++++++++
The form library that started it all.  This library allows you to create
forms and fields with objects instead of raw html.  Coupled with FormEncode
validation, this library provides a powerful tool for the creation of 
validated forms for your application.

maintainers: Alberto Valverde, Chris Perkins,  Diez B. Roggisch, Christoph Zwerschke

Notable Widgets:

 * TableForm
 * InputField
 * CalendarPicker

tw.dynforms
++++++++++++++++++++++
This add-on for tw allows for more dynamic forms on your
web pages.  This widget allows for some functionality like
autocompletion fields, as well as allowing for sub-forms
with the capability to grow or shrink based on user
needs.

maintainers: Paul Johnston, Chris Perkins, Joseph Tate

Notable Widgets:

 * HidingTableForm
 * AjaxLookupField
 * GrowingTableFieldSet


JavaScript wrapping Libraries
--------------------------------
Although most people associate ToscaWidgets with the ability
to create forms, the brunt of the development has gone into
wrapping existing JS libraries, making them easily available
to pages for further development.  Here are a few JavaScript
libraries that you can use for this purpose.


tw.jquery
++++++++++
A wrapper for the popular jquery library.  This library gives
you the ability to use jquery on your pages, and implements
a number of widgets to make it easier to render jquery enabled
components.

maintainers: Luke Macken, Christoph Zwerschke

Notable Widgets:
 * ActiveForm
 * AutoCompleteField
 * FlotWidget
 * DynaTree
 * TreeView
 * UIDatePicker


tw.mootools
+++++++++++++
Mootools is a JavaScript library that took off from the Prototype
JavaScript library.  Jonathan Schemoul has contributed a considerable
amout of functionality, some of which is used in his `Paris Envies`_ site.

maintainer: Jonathan Schemoul

Notable Widgets:

 * SortableWidget
 * KwickWidget
 * SimpleGridWidget
 * CalendarWidget

.. _`Paris Envies`: http://www.parisenvies.com/

tw.extjs
+++++++++
This library wraps the 2.0.2 version of extjs.  It is locked at this
version for licensing reasons and is not likely to change any time soon.
Use of this library is cautioned as there is no clear upgrade path.

maintainer: Chris Perkins

tw.yui
+++++++++
This is a wrapper for the popular YUI javascript library.  This library
wraps the version 2.x code and is periodically updated.  There are limited
widgets for this library available, as it is mostly used for it's ability
to inject YUI links into a page.

maintainer: Chris Perkins

Notable Widgets:

 * AutoCompleteField

tw.openlayers
++++++++++++++
OpenLayers is a JavaScript library especially good for handling
the needs of Geospacial web pages.  This library helps you to put
meaningful maps on your page.  Coupled with TileCache, you can render
maps and data assocaited data much more easily.

Notable widgets:
 * Map
 * Layer
 * Navigation
 * LayerSwitcher

maintainer: Sanjiv Singh

tw.prototype
+++++++++++++
needs maintainer

tw.mochikit
+++++++++++++
needs maintiner

JavaScript Testing Libraries
_______________________________

tw.yui
+++++++++
Again, yui is provided as a means to inject JavaScript resources into your
page.  One of those resources is the yuitest framework, which is an excellent
way to unit test your client side JavaScript.

maintainer: Chris Perkins


tw.jsunit
++++++++++++
A simple wrapper for the jsunit code that you may use to load the JS
framework required for getting your unit tests started.

maintainer: Sanjiv Singh


Simile Libraries
-----------------
Simile is a library from MIT that helps display time-based data. We have
created a few libraries to make this process a bit easier.


tw.timeline
+++++++++++++
Wraps the timeline library, which can plot events over time whether
the time for the events is continuous or point-related.


maintainer: Chris Perkins

tw.timeplot
+++++++++++++++
Wraps the timeplot library, which can plot datapoints over time.

maintainer: Chris Perkins

One-Off Libraries
---------------------

tw.recaptcha
++++++++++++++
ReCaptcha packaged as ToscaWidgets

tw.rating
++++++++++++
Ajax star rating system

tw.analytics.google
++++++++++++++++++++
Google Analytics wrapped by ToscaWidgets
