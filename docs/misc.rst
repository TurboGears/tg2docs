==============================
Misc To Do Items From The Docs
==============================

.. todo:: Difficulty: Hard. TW2 usage documentation

.. todo:: Difficulty: Easy. base_config.use_sqlalchemy=false <-- needs documentation

.. todo:: Difficulty: Medium. http://turbogears.org/2.0/docs/main/DownloadInstall.html references http://www.turbogears.org/2.0/downloads/current/tg2-bootstrap.py and this needs to be updated. Or does it? request from percious, contradiction from elpargo. Clarify with them before change.

.. todo:: Difficulty: Medium. critique the toc, and other organization. 

.. todo:: Difficulty: Medium. add a "what is turbogears"/faq - very early on. first?   

.. todo:: Difficulty: Hard. Include navigation links (previous, next, index) on all pages

.. todo:: Difficulty: Hard. add prerequisites to all pages - well, especially tutorials

.. todo:: Difficulty: Medium. include links to "read more" - especially true of tutorials that just scratch the surface  (this kind of replaces the "more linky" todo)

.. todo:: Difficulty: Medium. parts is parts:   the text on the frontgage of a quickstart says:  "standing on the shoulders of giants, since 2007" - provide a main place to see what components are used (by default) in turbogears.   don't be afraid to mention TG2 is built on pylons now, and link to the pylonsbook for more info

.. todo:: Difficulty: Hard. add (or find) exploration of quickstart - want to show how the pieces we are given "out of the box" fit together.   Possibly expanding upon mramm/percious' pycon-tg-tutorial:  http://bitbucket.org/mramm/pycon-tg-tutorial/, particularly the pages:   quickstart, looking_around, genshi_in_10, sqlalchemy_in_10

.. todo:: Difficulty: Hard. only after showing the default components - show what components can be easily switched in TG2, and how

.. todo:: Difficulty: Medium. Add lifecycle of TG project.

.. todo:: Difficulty: Medium. highlight the test suite:  and the goodness of test driven development.

.. todo:: Difficulty: Hard. Compare Our Docs to `Django Docs <http://docs.djangoproject.com/en/dev/`, see where we can do better.   Also compare to pylons book!

.. todo:: Difficulty: Medium. Understand "variable_provider": you define tg.config['variable_provider'] = callable and that returns a dict with all the variables you want in all templates.

.. todo:: Difficulty: Easy. Add note for "validator=Schema(allow_extra_fields=True)" for ToscaWidgets and RestController classes

.. todo:: Difficulty: Medium. Add shell script which validates environment for building docs

.. todo:: Difficulty: Easy. Add better notes in README.txt for setting up the virtual environment for this

.. todo:: Difficulty: Medium. Add docs for adding jquery, mochikit, and other resources to pages.

.. todo:: Difficulty: Medium. laurin is following the tutorial path.   right now, I created a tutorials directory under _static.   perhaps, all tutorial images, etc should go in there?   just a thought.   

.. todo:: Difficulty: Medium. clean up old tutorial static stuff:   hello-oops.jpg, hello-evalexception.jpg both seem to be old and not be exactly what the text is talking about.   Wiki20_final.zip is empty, and is now replaced by _static/tutorials/Wiki-20.zip.     There are probably more "old" files...    

.. todo:: Difficulty: Medium. make sure that override_template is more visible, and provide a tutorial on how to use it

.. todo:: Difficulty: Medium. port http://docs.turbogears.org/1.0/FileUploadTutorial to TG2

.. todo:: Difficulty: Medium. add in notes regarding how to use repoze.who's user_checker

.. todo:: Difficulty: Medium. port http://docs.turbogears.org/1.0/SQLAlchemy#id13

.. todo:: Difficulty: Medium. http://code.google.com/p/tgtools/source/browse/projects/tgext.admin/trunk/tgext/admin/tgadminconfig.py#114 << how to override tgext.admin controllers properly

.. todo:: Difficulty: Medium. incorporate custom routes docs from here http://simplestation.com/locomotion/routes-in-turbogears2/

.. todo:: Difficulty: Easy. Note that RestController is REST + forms, not for webservices

.. todo:: Difficulty: Easy. RestController requires that all data come in as a key/value pair, can't just get raw POST body

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/9b07a8d34611f5d7?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/c2aa4cb5ed07f52d?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://www.blog.pythonlibrary.org/?p=210

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/4023f34fd114121e?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/f35ef3d347793682?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/3afbc13d88af57d3?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/46d8fa413a0c97d8?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_thread/thread/6b44420129281259

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/31c4268417c5033c?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/1c4158ad3035082c?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/55d6bb9704b3127a?hl=en

.. todo:: Difficulty: Medium. Include these docs: http://groups.google.com/group/turbogears/browse_frm/thread/a02d64756fb0aa24?hl=en

.. todo:: Difficulty: Medium. Incorporate the info from this pic: http://imagebin.ca/view/P969Fr.html

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ae89ea2b3a354bc2?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/9fab648428c20761?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ade704ec2fb9f2bb?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/c721e2d15bb2c134?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/24683a03895e264a?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/b718855725da557d?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/0d804df13f2299b1?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/bbf8c847e77ca740?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/be2939380bfe0f2b?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/da4789ff0e246f8b?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ed539bc52198115b?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/4fc2abf3b91b9ce3?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/8fc49a69e9971290?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/d64d27b2cf54bb2e?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/1b82fa2b4a95957e?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/33a64a06ee4020ce?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/1f9853eac52decd5?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/7d5a07b4a21d7226?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/2e9737544409c8e9?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/42950271275c25ba?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/b258fe5a1f788c0c?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/094cf0138bd33e2c?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/daf8db234df8105b?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/4a87b275876647b6?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ba405adcabf4f78f?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/f6c61b5f1668e6d3?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/263233e9a8081c7a?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/d4635f5eb2ad1dc4?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/d3f40bf1bdf2cc98?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/a60d30766006f58d?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/5dd5b090eb0d4c49?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/a691ae9d3b31138d?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/626ff97e4b3a1dfd?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/72e106fc6512b1cb?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/b97ee4faeb6acd53?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/92581851b407cdd6?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/57229bc8677f0e6b/a9843e77e67af793?hl=en#a9843e77e67af793

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/7db400f92f652fd4/95c256ac817a5102?hl=en#95c256ac817a5102

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_thread/thread/3ba7ca9d35fd9d75?fwc=1

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/54306a9fd9b76a7d?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ad87eeef701ed1b1?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/ca5ddeabdc7cb517?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/f3c2c616f5530426?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/2d425ea3ab159cfd?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/bb07ff87d38367f0?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_frm/thread/9b451d82b410f844?hl=en

.. todo:: Difficulty: Medium. Incorporate these docs: http://groups.google.com/group/turbogears/browse_thread/thread/1174aad1b3350b5c

.. todo:: Difficulty: Hard. Resolve all tickets that match this query: http://trac.turbogears.org/query?status=new&status=assigned&status=reopened&component=Documentation&order=id

.. todo:: Difficulty: Medium. Document @restrict decorator, restricts request types that a given method will respond to


