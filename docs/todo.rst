.. _todolist:

=============================
All To Do Items From The Docs
=============================
For the doc sprint, todo items have been given three categories:

* Easy. Simple definitions, maybe couple of paragraphs. Expected work time: <15 minutes
* Medium. Reorganization, reformatting, taking existing notes and making them coherent (for instance: Google groups threads). Expected work time: <1 hour
* Hard. Everything else. Expected work time: Unknown (but likely a couple of hours)

.. todolist::

Questions
---------

* Where i can find the good tutorial about genshi other than  it's home page?

Useful Links:
-------------

* http://groups.google.com/group/turbogears/browse_thread/thread/70c14ac308563af5
* http://www.imagebin.ca/view/65iqpnZ.html
* http://www.blog.pythonlibrary.org/?p=210
* http://wiki.github.com/GothAlice/YAPWF/how-to-multiple-database-connections
* http://www.blog.pythonlibrary.org/?p=230

Testing Notes and Links
-----------------------

* http://showmedo.com/videos/video?name=2910000&fromSeriesID=291 
* http://code.google.com/p/pythontutorials/source/browse/
* Coverage of testing: http://nedbatchelder.com/code/coverage/


From Admin Through Creating Your Own Widgets
--------------------------------------------

* http://turbogears.org/2.1/docs/main/Extensions/Admin/index.html
* http://turbogears.org/2.1/docs/main/Extensions/Crud/index.html
* http://turbogears.org/2.1/docs/main/RestControllers.html?highlight=moviedemo
* http://turbogears.org/2.1/docs/main/ToscaWidgets/forms.html
* http://www.sprox.org/tutorials/table.html
* http://www.sprox.org/tutorials/form.html
* http://code.google.com/p/pythontutorials/source/browse/docs/twtut/ajax_tutorial.rst

Repoze Docs
-----------

* http://static.repoze.org/whatdocs
* Understand __nozero__ better
* which does this Predicate.__nonzero__ = lambda self: self.is_met(request.environ) which is thread unsafe (according to Gustavo) which is bad because it's using the environ.  and therefore it shouldn't be used because you need the env.

20 Minute Wiki Issues
---------------------

The existing tutorial is great marketing ... very compelling. However, it's
pedagogically weak.  It's too rushed and assumes far too much familiarity
with the ORM ... and the overall conceptual basis for web development
frameworks. For example there's no explanation of MVC and not discussion of
how a new developer would recognize the separation semantics.

Apache/mod_wsgi
---------------
Make sure to discuss mod_wsgi more fully
< peep1> should tg2/mod_wsgi work slower than stock paste/pylons installation?
< peep2> yea, tg2 will be somewhat slower than stock pylons
< peep2> genshi is not as fast as mako
< peep2> there's a couple more pre-loaded wsgi middleware components, etc
< peep2> if you use mako they get pretty close together

Root Url of app is in environ, SCRIPT_PATH

Sprox Disabling 'id' Field Editing When Using AddRecordForm
-----------------------------------------------------------

Don't use AddRecordForm, use FormBase instead.  AddRecordForm
automatically disables the primary key fields.  The only other
difference between AddRecordForm and FormBase is the assignment of the
__check_if_unique__ property to True.

Q: How can I enable editing of the 'id' field on a Sprox AddRecordForm?
A: Override _do_get_disabled_fields(self) in your subclass and return self.__disable_fields__[:].
By default it excludes the field(s) returned by self.__provider__.get_primary_field(self.__entity__)
Or, since that is the only feature added by AddRecordForm, don't use AddRecordForm.  XD
From the docstrings: """Override this function to define how"""

Using tg.config Variables
-------------------------

the tg.config variable is created when middlware.py does the
load_environment call well, not created, but updated with the ini file
values, etc you can't use it before that.  But all the ini values are
passed in to the make_middlware call in middlware.py so you can use
them there if you need to

On Spawning New Processes and Threads
-------------------------------------

< peep1> hey all, i'm using TG1, and wondering what my options are for making an asynchronous HTTP request from a controller method
< peep1> i want the controller to return ASAP, and don't care about callbacks from the (long-running) HTTP request
< peep1> threads don't seem to work (they get killed off when the controller method exits), and i'd prefer not to go down the rabbit warren of twisted or similar
< peep1> calling curl from subprocess seems my best option at the moment, but seems to be The Wrong Solution - any other ideas?
< peep2> I'd look into threads, and find out why the thread gets killed, and then fix that.
< peep1> ah, rather than started threads directly from the controller, I'll put a queue in there, see if it helps
< peep3> goodgracious: you pretty much need to fork in some way. threads will be no good as the webserver will recycle it as you found out.

On Adding Robots.txt
--------------------

< peep1> where should one place robots.txt in a tg2 installation?
< peep1> ./public ?
< peep2> that should work
< peep2> according to pylons docs, public is searched *before* going through controllers
< peep2> I assume this still applies with turbogears
< peep1> y, that worked

On How To Limit Routes To Specific Languages
--------------------------------------------

< peep> map.connect('/{lang}/{controller}/', requirements=dict(lang='bg|en|ro|ru'))


google search!    including search key related sites:   tosca, sqlalchemy, 
   genshi, etc...
should we link more directly to toscawidget tutorials?   
   either ask them to upgrade tutorials to tg2, or provide them a patch?


Serving Specific File Types
---------------------------

.. code-block:: python

    from tg.controllers import CUSTOM_CONTENT_TYPE

    class FilesController(RestController):

        @@expose(content_type=CUSTOM_CONTENT_TYPE)
            def get_one(self, file_type, *file_path):
	            file_path = list(file_path)
		    if pylons.request.response_ext:
		        file_path[-1]+=pylons.request.response_ext
    		    pylons.response.headers['Content-Type'] = 'text/plain'
		    pylons.response.headers['Content-Disposition'] = 'attachment; filename="'+file_path[-1]+'"'
		    return file(file_path, "r").read()
							    
