

Routes Integration in TG2
=========================


TurboGears2 does URL dispatch with a combination of TG1 style object
dispatch, and built in Routes integration.  By default you don't need
to think about Routes at all, because the framework sets up a default
route to your RootController, which sees that the action is route, and
does object dispatch in the same way that TurboGears 1 did.

But if you want to create special routes that override Object
Dispatch, you can easily do that, just by providing your own function
to set up the routes map. You can update the routes defaults by
overriding the setup_routes method of the base_config object in
app_cfg.py.

The standard setup_routes method looks like this::

    def setup_routes(self):
        """Setup the default TG2 routes
    
        Override this and set up your own routes maps if you want to use routes.
        """
        map = Mapper(directory=config['pylons.paths']['controllers'],
                    always_scan=config['debug'])
        # Setup a default route for the root of object dispatch
        map.connect('*url', controller='root', action='routes_placeholder')
    
        config['routes.map'] = map
    

The key to the default TG2 setup is the one map.connect() call which
sets up a default route for all urls (via the * wildcard) and sticks
the rest of the path on in the ``url`` param, and sends that info to
the application's RootController in the root.py file in your project's
controllers folder.

When TurboGears loads the environment for your app, it will use this
setup_routes method to do it.

So, to create your own routes, all you need to do is create another
``map.connect`` call **above** the ``*url`` call that maps everything
to the root controller.  This can send you to a regular pylons
controller, or to a DecoratedController.  You can even break up your
app into separate object trees and map to each of them them explicitly
to go to various different ``ObjectDispatchController's
``routes_placeholder`` actions.

.. warning: 

  Due to the way ObjectDispatchController overides the standard pylons
  controller call mechanisms, you cannot explicitly route to
  individual actions/methods on an ObjectDispatch controller.

If you want to start object dispatch from a different root than '/'
all you need to do is change the `'*url'` line to mount something
somewhere else.

If you have a very large app, and you want to break down the object
dispatch tree for performance reasons, you can do that by defining
routes to objects further down the tree.

For more information about how to write routes, you might want to read:

http://routes.groovie.org/manual.html
