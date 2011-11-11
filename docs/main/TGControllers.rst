The TGController Class
======================

The TGController is the basic controller class that provides an easy
method for nesting of controller classes to map URL hierarchies.
There are however a few methods which provide a slightly different
method for dispatch.  They are described below.

The Default Method
------------------

The developer may decide to provied a ``_default`` method within their
controller which is called when the dispatch mechanism cannot find
an appropriate method in your controllers to call.  This 
_default method might look something like this::

    class WikiController(BaseController):
    
      @expose('mytgapp.wiki.new)
      def _default(self, *args):
        """
          Return a page to prompt the user to create a new wiki page."""
        """
        return dict(new_page_slug=args)s


The Lookup Method
-----------------

``_lookup`` and ``_default`` are called in identical situations: when
"normal" object traversal is not able to find an exposed method, it
begins popping the stack of "not found" handlers.  If the handler is a
"_default" method, it is called with the rest of the path as positional
parameters passed into the default method.

The not found handler stack can also contain "lookup" methods, which
are different, as they are not actual controllers.

A lookup method takes as its argument the remaining path elements and
returns an object (representing the next step in the traversal) and a
(possibly modified) list of remaining path elements.  So a blog might
have controllers that look something like this::

  class BlogController(BaseController):

     @expose()
     def _lookup(self, year, month, day, id, *remainder):
        dt = date(int(year), int(month), int(day))
        blog_entry = BlogEntryController(dt, int(id))
        return blog_entry, remainder

  class BlogEntryController(object):

     def __init__(self, dt, id):
         self.entry = model.BlogEntry.get_by(date=dt, id=id)

     @expose(...)
     def index(self):
        ...
     @expose(...)
     def edit(self):
         ...

     @expose()
     def update(self):
        ....

So a URL request to .../2007/6/28/0/edit would map first to the
BlogController's _lookup method, which would lookup the date,
instantiate a new BlogEntryController object (blog_entry), and pass
that blog_entry object back to the object dispatcher, which uses the
remainder do continue dispatch, finding the edit method. And of course
the edit method would have access to self.entry, which was looked up
and saved in the object along the way.

In other situations, you might have a several-layers-deep "_lookup"
chain, e.g. for editing hierarchical data
(/client/1/project/2/task/3/edit).

The benefit over "_default" handlers is that you *return* an object
that acts as a sub-controller and continue traversing rather than
*being* a controller and stopping traversal altogether.  This allows
you to use actual objects with data in your controllers.

Plus, it makes RESTful URLs much easier than they were in TurboGears 1.


Mount Points and Dispatch
---------------------------

Since TurboGears 2.1.4 it is possible to ask for various informations
about the request dispatchment and controllers mount points.

Those informations can be useful when writing controllers that
you plan to reuse in multiple applications or mount points,
making possible for example to generate all the urls knowing
where they are mounted.

For statically mounted controllers the exposed informations are:

* The ``mount_point`` property of a controller. If statically mounted
  it will return where the controller is mounted. This is the
  url to call when you want to access that controller.
* The ``mount_steps`` property of a controller. If statically mounted
  it will return the complete list of parents of that controller.

In the case you are dispatching the request yourself, for example
through a ``_lookup`` method, the ``mount_point`` and ``mount_steps``
informations won't be available. In this case you can rely
on some other functions exposed by TG:

* The ``tg.request.controller_state`` object keeps track of all
  the steps provided to dispatch the request.
* The ``tg.dispatched_controller()`` method when called inside
  a request will return the last statically mounted controller.
  This can be useful to detect which controller finished the
  request dispatch using the ``_lookup`` method.

The application ``RootController`` can usually be retrieved from
``tg.config['application_root_module'].RootController``
