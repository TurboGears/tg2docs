==============================
Misc To Do Items From The Docs
==============================

.. todo:: critique the toc, and other organization. 

.. todo:: add a "what is turbogears"/faq - very early on. first?   

.. todo:: Include navigation links (previous, next, index) on all pages

.. todo:: add prerequisites to all pages - well, especially tutorials

.. todo:: include links to "read more" - especially true of tutorials that just scratch the surface  (this kind of replaces the "more linky" todo)

.. todo::  parts is parts:   the text on the frontgage of a quickstart says:  "standing on the shoulders of giants, since 2007" - provide a main place to see what components are used (by default) in turbogears.   don't be afraid to mention TG2 is built on pylons now, and link to the pylonsbook for more info

.. todo::  add (or find) exploration of quickstart - want to show how the pieces we are given "out of the box" fit together.   Possibly expanding upon mramm/percious' pycon-tg-tutorial:  http://bitbucket.org/mramm/pycon-tg-tutorial/, particularly the pages:   quickstart, looking_around, genshi_in_10, sqlalchemy_in_10

.. todo:: only after showing the default components - show what components can be easily switched in TG2, and how

.. todo:: Add lifecycle of TG project.   laurin:  I wonder what is meant by this?

.. todo:: highlight the test suite:  and the goodness of test driven development.   is this part of what is meant by "lifecycle"?

.. todo:: Update install docs, since we now use pypi

.. todo:: Compare Our Docs to `Django Docs <http://docs.djangoproject.com/en/dev/`, see where we can do better.   laurin: I say compare to pylons book!

.. todo:: Understand "variable_provider": you define tg.config['variable_provider'] = callable and that returns a dict with all the variables you want in all templates.

.. todo:: Add note for "validator=Schema(allow_extra_fields=True)" for ToscaWidgets and RestController classes

.. todo:: Add shell script which validates environment for building docs

.. todo:: Add better notes in README.txt for setting up the virtual environment for this

.. todo:: Add docs for adding jquery, mochikit, and other resources to pages.

.. todo:: laurin is following the tutorial path.   right now, I created a tutorials directory under _static.   perhaps, all tutorial images, etc should go in there?   just a thought.   

.. todo:: clean up old tutorial static stuff:   hello-oops.jpg, hello-evalexception.jpg both seem to be old and not be exactly what the text is talking about.   Wiki20_final.zip is empty, and is now replaced by _static/tutorials/Wiki-20.zip 
.. todo:: laurin is following the tutorial path.   right now, I created a tutorials directory under _static.   perhaps, all tutorial images, etc should go in there?   just a thought.   

.. todo:: clean up old tutorial static stuff:   hello-oops.jpg, hello-evalexception.jpg both seem to be old and not be exactly what the text is talking about.   Wiki20_final.zip is empty, and is now replaced by _static/tutorials/Wiki-20.zip.     There are probably more "old" files...    

.. todo:: document override_template for doing dynamic templates in a controller method

.. todo:: port http://docs.turbogears.org/1.0/FileUploadTutorial to TG2

.. todo:: make sure to explain how to use "paster --daemon"

.. tood:: add in notes regarding how to use repoze.who's user_checker
