.. _master_html:

=================================
 Full Description of master.html
=================================

master.html is quite the important page for your site. In fact, it's
what drives your site and makes it work. However, what's actually in
it? What do you get?


.. code-block:: html

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

The above is the standard doctype header. Nothing new for any web developer yet.

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:py="http://genshi.edgewall.org/"
          xmlns:xi="http://www.w3.org/2001/XInclude"
          py:strip="">

The above is where things start to get interesting. The standard
namespace for xhtml is declared, and we also declare the genshi
namespace (xmlns:py), along with the XInclude namespace
(xmlns:py). The last bit, the `py:strip`_, is what allows you to
include the master.html in another template. With it written the way
it is, the html tag itself is removed from the output.

.. code-block:: html

        <xi:include href="header.html" />
        <xi:include href="sidebars.html" />
        <xi:include href="footer.html" />

The above segment includes three files, header.html, sidebars.html,
and footer.html. Each of these files defines a `Genshi macro`_ that is
called later in master.html. The macro is named the same as the file
name, minus .html (i.e.: header(), footer(), sidebar()).

.. code-block:: html

    <head py:match="head" py:attrs="select('@*')">

The above segment grabs all of the elements under this head tag, and
places them into the head tag of the calling page. Remember,
master.html is included in other pages.

.. code-block:: html

        <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
        <title py:replace="''">Your title goes here</title>
        <meta py:replace="select('*')"/>
	
The above segment is used to, basically, trick Genshi. Genshi wants to
see that the document it is examining is has those attributes, but we
don't want them output. to the user. By using `py:replace`_, we give
Genshi what it wants, and get what we want.

.. code-block:: html

        <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    </head>
    
The above segment gets the default TurboGears style sheet.

.. code-block:: html

    <body py:match="body" py:attrs="select('@*')">
      ${header()}

The above segment gets the body attribute from the calling document,
and adds the remaining tags in master.html to it. It then runs the
header() macro.

.. code-block:: html

      <ul id="mainmenu">
        <li class="first"><a href="${tg.url('/')}" class="${('', 'active')[defined('page') and page==page=='index']}">Welcome</a></li>

The above segment is a fairly busy chunk. First, it sets up list to be
used as the menu. It sets the first item in the list to be a link to
the root of the TurboGears project. Finally, it checks to see if the
variable ``page`` is defined, and if so, if that variable has the
value ``index``, which indicates that we are on the root page. If so,
it marks the class for the link as the ``active`` class.

.. code-block:: html

            <li><a href="${tg.url('/about')}" class="${('', 'active')[defined('page') and page==page=='about']}">About</a></li>

The above segment functions very similarly to the link for the index,
in the previous menu item.

.. code-block:: html

            <li py:if="tg.auth_stack_enabled"><a href="${tg.url('/auth')}" class="${('', 'active')[defined('page') and page==page=='auth']}">Authentication</a></li>

The above segment functions very similarly to the link for the index,
in the first menu item.

.. code-block:: html

            <li><a href="http://groups.google.com/group/turbogears">Contact</a></li>

The above segment simply sets up a link pointing to the TurboGears
Google group.

.. code-block:: html

        <span py:if="tg.auth_stack_enabled" py:strip="True">

The above segment sets up an `if statement`_, which allows the
template to only show the content of the span tag when the result of
the ``if`` statement is True. In this case, the contents of the span
tag will only be shown if authentication is enabled. I keep saying the
contents of the span tag, rather than the span tag, since the span tag
has the attribute `py:strip`_ set to ``True``, which will result in
the span tag itself being removed, but leaving the contents
behind. Combined with the ``if`` statement, if authentication is
disabled, this entire segment will be skipped, resulting in nothing
being sent to the browser from this segment.

.. code-block:: html

            <li py:if="not request.identity" id="login" class="loginlogout"><a href="${tg.url('/login')}">Login</a></li>

The above segment checks to see if the client has logged in. If not,
it presents a ``Login`` link. It does this using
``request.identity``. If this variable is not None, then the client
has logged in.

.. code-block:: html

            <li py:if="request.identity" id="login" class="loginlogout"><a href="${tg.url('/logout_handler')}">Logout</a></li>

The above segment checks to see if the client has logged in. If so, it
presents a ``Logout`` link. It does this using
``request.identity``. If this variable is not None, then the client
has logged in.

.. code-block:: html

            <li py:if="request.identity" id="admin" class="loginlogout"><a href="${tg.url('/admin')}">Admin</a></li>
        </span>
      </ul>

The above segment checks to see if the client has logged in. If so, it
presents a ``Admin`` link. It does this using ``request.identity``. If
this variable is not None, then the client has logged in. Note that
this means that any logged in user can see the ``Admin`` link. If you
wish to protect this from non-privileged users, you will want to look
further into :ref:`Authentication and Authorization <auth_and_auth>`.

.. code-block:: html

      <div id="content">
        <py:if test="defined('page')">

The above segment checks to see if the page knows about a variable named ``page``, enclosing the next segement in an ``if`` block. If the page is defined, the next segment will be shown.

.. code-block:: html

        <div class="currentpage">
         Now Viewing: <span py:replace="page"/>
         </div>

The above segment displays the name of the page being shown: ``index``, ``about``, etc.

.. code-block:: html

        </py:if>

The above segment closes the if block opened earlier.

.. code-block:: html

        <py:with vars="flash=tg.flash_obj.render('flash', use_js=False)">

The above segment uses the `py:with`_ construct to avoid re-rendering
the contents of the ``flash``. What happens here is that a new
variable, named ``flash``, is set to have the value of the output of
the function that will return the text that was flashed in a previous
method call (though possibly still on the same request). By doing this
once, it is possible to simply re-use the output, without having to
call it twice. Why to do this is next:

.. code-block:: html

            <div py:if="flash" py:content="XML(flash)" />
        </py:with>

The above segment uses the variable named ``flash`` above. If the
variable has any data, display it. If it does not, do nothing. Note
the use of the XML_ call around the variable flash. This is because
flash is assumed to already be XML, so that we can avoid having
``<b>My Text</b>`` become ``&lt;b&gt;My Text&lt;/b&gt;``.

.. code-block:: html

        <div py:replace="select('*|text()')"/>
        <!-- End of content -->

The above segment is what finally finishes inserting the body of
master.html into the calling document. The result is that the layout
defined in master.html is now wrapped around the body of the document
defined by the caller.

.. code-block:: html

        ${footer()}
      </div>
    </body>
    </html>

The above segment calls the footer function (from footers.html), and
closes out the page, completing what will be sent to the user.

.. _`Genshi macro`: http://genshi.edgewall.org/wiki/Documentation/xml-templates.html#snippet-reuse
.. _`py:replace`: http://genshi.edgewall.org/wiki/Documentation/xml-templates.html#id8
.. _`py:strip`: http://genshi.edgewall.org/wiki/Documentation/xml-templates.html#id9
.. _`if statement`: http://genshi.edgewall.org/wiki/Documentation/xml-templates.html#id1
.. _`py:with`: http://genshi.edgewall.org/wiki/Documentation/xml-templates.html#py-with
.. _XML: http://genshi.edgewall.org/wiki/Documentation/plugin.html#extra-implicit-objects
