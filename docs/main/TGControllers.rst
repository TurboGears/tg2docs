The TGController Class 
===========================

The TGController is the basic controller class that provides an easy method
for nesting of controller classes to map URL hierarchies.  There are however
a few methods which provide a slightly different method for dispatch.  They are
described below.

The Default Method
-----------------------

Explanation of how the default method works here.

The Lookup Method
--------------------------

``Lookup`` and ``default`` are called in identical situations: when "normal"
object traversal is not able to find an exposed method, it begins
popping the stack of "not found" handlers.  If the handler is a
"default" method, it is called with the rest of the path as positional
parameters passed into the default method.

The not found handler stack can also contain "lookup" methods, which
are different, as they are not actual controllers.

A lookup method takes as its argument the remaining path elements and
returns an object (representing the next step in the traversal) and a
(possibly modified) list of remaining path elements.  So a blog might
have controllers that look something like this::

  class BlogController(BaseController):

     @expose()
     def lookup(self, year, month, day, id, *remainder):
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
BlogController's lookup method, which would lookup the date, instantiate
a new BlogEntryController object (blog_entry), and pass that blog_entry object
back to the object dispatcher,  which uses the remainder do continue dispatch,
finding the edit method. And of course the edit method would have access to self.entry,
which was looked up and saved in the object along the way.


In other situations,
you might have a several-layers-deep "lookup" chain, e.g. for
editing hierarchical data (/client/1/project/2/task/3/edit).

The benefit over "default" handlers is that you *return* an object that acts
as a sub-controller and continue traversing rather than *being* a controller
and stopping traversal altogether.  This allows you to use actual objects with
data in your controllers.

Plus, it makes RESTful URLs much easier than they were in TurboGears 1.

.. todo:: Review this file for todo items.

