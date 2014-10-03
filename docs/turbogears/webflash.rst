.. _webflash:

================================
Displaying Flash/Notice Messages
================================

TurboGears provides a way to display short messages inside the current
or next page. This works by using the WebFlash module which stores
short text messages inside a cookie so that it can be retrieved
when needed.

Default Setup
=============

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
======================

Flash messages can be stored using the ``tg.flash`` command
this allows to store a message with a status option to configure
the flash style.

.. code-block:: python

    tg.flash('Message', 'status')

If the method that called flash performs a redirect the flash
will be visible inside the redirected page.
If the method directly exposes a template the flash will be
visible inside the template itself.

Caching with Flash Messages
===========================

When using ``tg_cache`` variable in rendered templates (:ref:`prerendered-templates-cache`)
the flash will get into the cached template causing unwanted messages to be displayed.

To solve this issue the ``tg.flash_obj.render`` method provides the ``use_js`` option.
By default this option is set at False inside the template, changing it to True
will make the flash message to be rendered using javascript. This makes so that the same
template is always rendered with a javascript to fetch the flash message and display it
due to the fact that the template won't change anymore it will now be possible to
correctly cache it.

Customizing Flash
=================

CSS Styling
-----------

By default `warning`, `error`, `info`, `ok` statuses
provide a style in ``public/css/style.css`` for quickstarted applications.

Any number of statuses can be configured using plain css:

.. code-block:: css

    #flash > .warning {
      color: #c09853;
      background-color: #fcf8e3;
      border-color: #fbeed5;
    }

    #flash > .ok {
      color: #468847;
      background-color: #dff0d8;
      border-color: #d6e9c6;
    }

    #flash > .error {
      color: #b94a48;
      background-color: #f2dede;
      border-color: #eed3d7;
    }

    #flash > .info {
      color: #3a87ad;
      background-color: #d9edf7;
      border-color: #bce8f1;
    }

Flash Options
-------------

Flash messages support can be styled using options inside the ``flash.`` namespace,
those are documented in :class:`.TGFlash` and can be specified in ``config/app_cfg.py``
or in your ``.AppConfig`` instance.

For example to change the default message status (when status is omitted) you can use the
``flash.default_status`` option and set it to any string. To change the default flash template
you can use ``flash.template`` and set it to a string with the HTML that should be displayed
to show the flash (note that ``flash.template`` only works for static rendered flash, not for
JS version).

Custom Flash HTML
~~~~~~~~~~~~~~~~~

For example to render the flash using the **toastr** library you might want to remove the
``py:with`` code block from your ``master.html`` and move it to the bottom of your ``<body>``
right after the usage of bootstrap and jquery libraries:

.. code-block:: html+genshi

    <body>
      <!-- YOUR CURRENT BODY CONTENT -->
      <script src="http://code.jquery.com/jquery.js"></script>
      <script src="${tg.url('/javascript/bootstrap.min.js')}"></script>

      <py:with vars="flash=tg.flash_obj.render('flash')">
        <py:if test="flash">${Markup(flash)}</py:if>
      </py:with>
    </body>

This will ensure that we can provide custom Javascript that depends on JQuery inside our
flash template.
Now we can switch flash template to use the toastr library to display our flash by setting
inside your ``app_cfg.py``::

    base_config['flash.default_status'] = 'success'
    base_config['flash.template'] = '''\
        <script src="//cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/js/toastr.min.js"></script>
        <script>toastr.$status("$message");</script>
    '''

This will ensure that each time the flash is displayed the toastr library with the given status
is used.

Last, to correctly display the flash with the right look and feel, don't forget to add the
toastr CSS to the head of your ``master.html``:

.. code-block:: html

  <link rel="stylesheet" type="text/css" media="screen"
        href="//cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/css/toastr.min.css" />

If everything is correct you should see your flash messages as baloon into the top-right corner
of your webpage.

Custom Flash JavaScript
~~~~~~~~~~~~~~~~~~~~~~~

Javascript based flashes are usually common when Caching is involved, so the cached version
of the webpage will not have the flash inside but you still want to be able to display
the flash messages. In this case instead of providing a custom ``flash.template`` you
should provide a custom ``flash.js_call`` which is the javascript code used to display the
message.

For example to use the toastr library you might want to ensure toastr CSS and JS are available
and add the following to your ``app_cfg.py``::

    base_config['flash.default_status'] = 'success'
    base_config['flash.js_call'] = '''\
        var payload = webflash.payload();
        if(payload) { toastr[payload.status](payload.message); }
    '''

The webflash object is provided by :class:`.TGFlash` itself and the ``webflash.payload()``
method will fetch the current message for you.

