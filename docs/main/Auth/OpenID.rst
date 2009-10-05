.. _openid:

Adding OpenID Support
=====================

As an example of what you can do with a custom configuration when 
:ref:`using-who.ini`, let's add the ability to use OpenID to our 
`repoze.who` configuration.  We need to install the 
`repoze.who.plugins.openid` package:

.. code-block:: bash

    easy_install repoze.who.plugins.openid 

and then we need to alter our `who.ini` like so:

.. code-block:: ini

    [plugin:openid]
    use = repoze.who.plugins.openid:make_identification_plugin

    store = file
    store_file_path = %(here)s/sstore
    openid_field = openid
    came_from_field = came_from
    error_field = error
    session_name = beaker.session
    login_form_url = /login
    login_handler_path = /openid_login_handler
    logout_handler_path = /logout_handler
    logged_in_url = /
    logged_out_url = /
    rememberer_name = auth_tkt

    ...
    [general]
    request_classifier = repoze.who.classifiers:default_request_classifier
    challenge_decider = repoze.who.plugins.openid.classifiers:openid_challenge_decider

    [identifiers]
    # We can decide who the user is trying to identify as using either 
    # a fresh form-post, or the session identifier cookie
    plugins =
        friendlyform;browser
        openid
        auth_tkt

    [authenticators]
    plugins =
        openid
        sqlauth

    [challengers]
    plugins =
        openid
        friendlyform;browser

and lastly, we provide an OpenID form on our login page to allow the user 
to enter their OpenID and log in:

.. code-block:: html

    <form action="${tg.url('/openid_login_handler', came_from = came_from.encode('utf-8'), __logins = login_counter.encode('utf-8'))}" method="POST" class="openid-login">
        <input type="text" id="openid" name="openid" class="text" value="http://"></input>
        <input type="submit" id="submit" value="Login with OpenID" />
            <input type="hidden" value="/" name="returnto"/>
            <input type="hidden" value="claim_openid" name="op"/>
            <input type="hidden" value="1" name="openid_login"/>    
            <div class="get-an-openid">
                <a href="http://openid.net/get-an-openid/">Get an OpenID</a>
            </div>
    </form>

which you should style appropriately with CSS to match the OpenID standards.

Adding Some Style
-----------------

OpenID provides a logo suitable for use as a background for text-boxes.
We can download this logo to our project's `public/images` directory:

.. code-block:: bash

    wget http://wiki.openid.net/f/openid-16x16.gif

And then reference it from our css stylesheet `public/css/style.css` 
to get a reasonable looking and somewhat compact login form:

.. code-block:: css

    form.openid-login {
        border: thin solid #f7931e;
        padding: .25em;
    }
    form.openid-login input[type="text"] {
        padding-left: 16px;
        background: url('/images/openid-16x16.gif') top left no-repeat;
        width: 10em;
    }
    form.openid-login input[type="submit"] {
        background-color: #f7931e;
        color: white;
    }

.. todo:: Difficulty Medium/Hard: document how to provide group/permission
          support when using an OpenID Authentication provider.
.. todo:: Difficulty Hard: document how to store OpenID identifiers in 
          SQLAlchemy (i.e. add records for each new OpenID identity)

References
----------

 * :ref:`using-who.ini` -- describes the process to switching to `who.ini` 
   from quickstart
 * `Get an OpenID`_ -- describes how to get an OpenID URI via various services,
   you may already have an OpenID provider.  If not `myopenid.com` can be used 
   to set up a new ID
 * `Repoze.who.plugins.openid`_ -- documentation for the plugin

.. _`Repoze.who.plugins.openid` : http://quantumcore.org/docs/repoze.who.plugins.openid/
.. _`Get an OpenID` : http://openid.net/get-an-openid/
