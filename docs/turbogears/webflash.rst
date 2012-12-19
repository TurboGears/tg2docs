.. _webflash:

=================================
Displaying Flash/Notice Messages
=================================

TurboGears provides a way to display short messages inside the current
or next page. This works by using the WebFlash module which stores
short text messages inside a cookie so that it can be retrieved
when needed.

Default Setup
================

By Default the `master.html` of a quickstarted project provides a div
where flash messages will be displayed, this is achieved with the
following lines of code:

.. code-block:: html+genshi

    <py:with vars="flash=tg.flash_obj.render('flash', use_js=False)">
        <div py:if="flash" py:replace="Markup(flash)" />
    </py:with>

The ``tg.flash_obj`` is the WebFlash object which is available inside
any rendered template. This object permits to retrieve the current
flash message and display it.

Storing Flash Messages
==========================

Flash messages can be stored using the ``tg.flash`` command
this allows to store a message with a status option to configure
the flash style.

.. code-block:: python

    tg.flash('Message', 'status')

If the method that called flash performs a redirect the flash
will be visible inside the redirected page.
If the method directly exposes a template the flash will be
visible inside the template itself.

Styling the Flash
==========================

By default `warning`, `error`, `info`, `ok` statuses
provide a style. Any number of statuses can be configured
using plain css:

.. code-block:: css

    #flash .ok {
        background:#d8ecd8 url(../images/ok.png) no-repeat scroll 10px center;
    }

    #flash .warning {
        background:#fff483 url(../images/warning.png) no-repeat scroll 10px center;
    }

    #flash .error {
        background:#f9c5c1 url(../images/error.png) no-repeat scroll 10px center;
    }

    #flash .info {
        background:#EEEEFF url(../images/info.png) no-repeat scroll 10px center;
    }


Caching with Flash Messages
=============================

When using ``tg_cache`` variable in rendered templates (:ref:`prerendered-templates-cache`)
the flash will get into the cached template causing unwanted messages to be displayed.

To solve this issue the ``tg.flash_obj.render`` method provides the ``use_js`` option.
By default this option is set at False inside the template, changing it to True
will make the flash message to be rendered using javascript. This makes so that the same
template is always rendered with a javascript to fetch the flash message and display it
due to the fact that the template won't change anymore it will now be possible to
correctly cache it.
