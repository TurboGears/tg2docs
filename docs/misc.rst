==============================
Misc To Do Items From The Docs
==============================


Configuration
-----------------

.. todo:: Difficulty: Medium. Understand "variable_provider": you define
          tg.config['variable_provider'] = callable and that returns a
          dict with all the variables you want in all templates.

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/7db400f92f652fd4/95c256ac817a5102?hl=en
          How can I configure genshi?


Authorization/Authentication
------------------------------

.. todo:: Difficulty: Medium. add in notes regarding how to use repoze.who's user_checker

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/c2aa4cb5ed07f52d?hl=en
          Everything there is to know about the current auth/identity in TG2

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/3afbc13d88af57d3?hl=en TG2
          repoze.who and multiple auth sources

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/f3c2c616f5530426?hl=en
          Help with Authentication

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/54306a9fd9b76a7d?hl=en
          How to check if the user is authorized for a controller or action

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/f6c61b5f1668e6d3?hl=en
          Auth can now be configured via config [ini] files
          percious: priority high

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ba405adcabf4f78f?hl=en
          Configuring LDAP authentication on turbogears2
          percious: priority high on this one

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/4a87b275876647b6?hl=en
          list of connected users?

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/9fab648428c20761?hl=en
          login_handler

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/f35ef3d347793682?hl=en
          What's wrong with predicates being "booleanized"


ToscaWidgets
---------------

.. todo:: Difficulty: Hard. TW2 usage documentation

.. todo:: Difficulty: Easy. Add note for "validator=Schema(allow_extra_fields=True)" for ToscaWidgets and RestController classes

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/33a64a06ee4020ce?hl=en
          Upload images to a TG2 app with Dojo (Ajax style)

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/bb07ff87d38367f0?hl=en
          Best way to add fields on the fly to TW Forms?

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ca5ddeabdc7cb517?hl=en
          trying to inject Dojo resources with ToscaWidgets

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/72e106fc6512b1cb?hl=en
          Toscawidgets form with multiple buttons
          priority: low

.. todo:: Difficulty: Hard. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/a691ae9d3b31138d?hl=en
          Flash Widget

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/7d5a07b4a21d7226?hl=en
          Visitor IP & pre-populated toscawidget field from database

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/be2939380bfe0f2b?hl=en
          Using ImageButton() as submit throws an error

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/c721e2d15bb2c134?hl=en
          Return to form after custom validation and keep form data?

Controllers
--------------

.. todo:: Difficulty: Medium. Document @restrict decorator, restricts request types that a given method will respond to

.. todo:: Difficulty: Medium. incorporate custom routes docs from here http://simplestation.com/locomotion/routes-in-turbogears2/
          percious: There is a better way of doing this by overriding _dispatch in 2.0
          so I would wait until I re-write RoutedController with _dispatch before documenting this

.. todo:: Difficulty: Hard. RestController requires that all data come in as a key/value pair, can't just get raw POST body.
          percious: not sure what you mean by this.  You want to provide RestController with just a blob of data?
          jorge: yes, this was the complain from europe74 this goes against the atom protocol http://tools.ietf.org/html/rfc5023#section-9.2
          I think that this needs to be a trac ticket, not a doc todo

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ad87eeef701ed1b1?hl=en
          exception object in ErrorController

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_thread/thread/3ba7ca9d35fd9d75?fwc=1
          mounting test-controllers/getting root-controller instance?

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/b97ee4faeb6acd53?hl=en
          CRC does wacky pluralization
          percious: this should probably be a trac ticket, not a doc todo.

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/d4635f5eb2ad1dc4?hl=en
          how could a controller method know whether it's invoked as an error_handler or directly

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/9b451d82b410f844?hl=en
          TG2 serveFile equivalent?

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/1c4158ad3035082c?hl=en
          Secure Static Files TG2

Installation
---------------

.. todo:: Difficulty: Medium. http://turbogears.org/2.0/docs/main/DownloadInstall.html references
          ttp://www.turbogears.org/2.0/downloads/current/tg2-bootstrap.py and this needs to be updated.
          Or does it? request from percious, the code to generate the installer currently has
          tg.devtools/scripts/_installer.py and it's fixed at 2.0 only update needed is to hg

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/263233e9a8081c7a?hl=en
          easy_install and offline installation in virtualenv og TG2
          percious: we need to add an offline install section to deployment.  This should not be very difficult, it's basically 2 commands.

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/bbf8c847e77ca740?hl=en
          TG2 on Webfaction - Make TG not see the extra part of the URL

Database
----------

.. todo:: Difficulty: Hard. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/92581851b407cdd6?hl=en migrate
          priority: high

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/57229bc8677f0e6b/a9843e77e67af793?hl=en Problem
          with accessing attributes after transaction.commit()

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/d64d27b2cf54bb2e?hl=en
         Suggestion about how turbojson handle SQLAlchemy object circuit jorge: this seems like a feature request rather than a docs item

.. todo:: Difficulty: uncertain. Document how SA+TG+Transaction manager work together.


Templating
------------

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/4fc2abf3b91b9ce3?hl=en
          tg_template is now override_template

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_thread/thread/1174aad1b3350b5c
          TurboGears2: Overriding meta element on child template.


Review
------------

.. todo:: Difficulty: Medium. critique the toc, and other organization.

I think the toc has an airy aroma, with a hint of cherry and oak.  It is not yet
aged to perfection, but will mature as time goes on.  This todo will be open
for some time.

.. todo:: Difficulty: Medium: the TG logo is missing in the new theme.
          It's hard to find a place for it where it does not disturb in the new layout.

.. todo:: Difficulty: Hard. add prerequisites to all pages - well, especially tutorials

.. todo:: Difficulty: Hard. Compare Our Docs to `Django Docs <http://docs.djangoproject.com/en/dev/`,
          see where we can do better.   Also compare to pylons book!

.. todo:: Difficulty: Medium. laurin is following the tutorial path.
          right now, I created a tutorials directory under _static.
          perhaps, all tutorial images, etc should go in there?   just a thought.

.. todo:: Difficulty: Medium. make docs more linky.   provide link to pylons,
          and why tg2 is now based on it.   eventually, I'd really like to see
          links to pylonsbook for specific "more information", and how turbogears is different/expands upon it

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/1f9853eac52decd5?hl=en
          Rolling back transactions in TG2 (I think this is documented, need to double check)

.. todo:: Difficulty: Hard. Resolve all tickets that match this query: http://trac.turbogears.org/query?status=new&status=assigned&status=reopened&component=Documentation&order=id


General
---------------

.. todo:: Difficulty: Medium. include links to "read more" - especially true of
          tutorials that just scratch the surface  (this kind of replaces the "more linky" todo)

.. todo:: Difficulty: Medium. parts is parts:   the text on the frontgage of a quickstart says:
          "standing on the shoulders of giants, since 2007" - provide a main place to
          see what components are used (by default) in turbogears.
          don't be afraid to mention TG2 is built on pylons now, and link to the pylonsbook for more info

.. todo:: Difficulty: Hard. only after showing the default components - show what components can be easily switched in TG2, and how

.. todo:: Difficulty: Medium. Add lifecycle of TG project in the getting to know TG section.

.. todo:: Difficulty: Medium. make sure that override_template is more visible, and provide a tutorial on how to use it

.. todo:: Difficulty: Medium. https://github.com/TurboGears/tgext.admin/blob/master/tgext/admin/tgadminconfig.py << how to override tgext.admin controllers properly

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/9b07a8d34611f5d7?hl=en
          TG2 virtualenv MySQLdb ImportError.
          Should we be providing documentation to debug MySQLdb problems?  Seems out of scope.

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/5dd5b090eb0d4c49?hl=en
          List of Quickstarted files that are safe to remove
          percious: I think this is a terrible idea to document

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ae89ea2b3a354bc2?hl=en
          Lukasz Szybalski's docs: http://lucasmanual.com/mywiki/TurboGears2

.. todo:: Difficulty: Medium. Document the code_ext extension for Sphinx (docs/code_ext.py)
          TG documentation writers should be aware of this extension, and how to use it.


Other
-----------------------------

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/4023f34fd114121e?hl=en
          Trouble with WebHelpers

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/b718855725da557d?hl=en
          tgext and i18n

.. todo:: Difficulty: Hard. Performance deployment enhancements pretty much explain all the YSlow issues
            * serving static files from the frontent,  /config/app_cfg.py base_config.serve_static = False
            * compressing JS/html/CSS,etc

.. todo:: Difficulty: Medium. Add shell script which validates environment for building docs


.. todo:: Difficulty: Medium. main/ToscaWidgets/forms.rst uses the archive directive. This outputs an absolute path relative to root on the machine that builds the docs. Fix the code so it is relative to _build/html/_static
