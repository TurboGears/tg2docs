.. _scaffolding:

Scaffolding
===========

Scaffolding is the process of creating a new component of your
web application through a template or preset.

Creating new Controllers, Models and Templates
----------------------------------------------

On TurboGears this is provided by the ``gearbox scaffold``
command which will look for ``.template`` files inside your
project directory to create new scaffolds for your web app.

Since version 2.3.5 projects quickstarted by TurboGears provide
``.template`` files for *model*, *controller* and *template* so
new models, controllers and templates can be easily created
in your project by running ``gearbox scaffold``.

For example to create a new **Photo** model simply run::

    $ gearbox scaffold model photo

It will create a ``model/photo.py`` file with a ``Photo``
class inside. Import that class inside ``model/__init__.py`` and add
it to ``__all__`` to make it available inside your app::

    from myapp.model.photo import Photo

    __all__ = ('User', 'Group', 'Permission', 'Photo')

Creating All Together
---------------------

Multiple scaffolds can be created together, so in case you
need to create a new model with a controller to handle it
and an index page you can run::

    $ gearbox scaffold model controller template photo

Which will create a new controller with the associated page
and model. To start using the controller, import and mount it inside
your application ``RootController``::

    from myapp.controllers.photo import PhotoController

    class RootController(BaseController):
        photo = PhotoController()

If you are following each example in the same project, use a different
scaffold name for each example or start from a fresh quickstart; the
examples are alternatives and reuse ``photo`` for readability.

Creating Packages
-----------------

There are cases when your controllers, templates and model
might become complex and be better managed by a python package
instead of a simple module. This is common for templates which
will usually be more than one for each controller and so
are usually grouped in a package for each controller.

To create scaffold in a package just provide the
``-s [PACKAGE]`` option to the scaffold command::

    $ gearbox scaffold -s photo controller template photo

This will create a photo controller and template inside
a photo package where multiple templates can be placed. The generated
controller lives in the nested module, so import and mount it from
there::

    from myapp.controllers.photo.photo import PhotoController

    class RootController(BaseController):
        photo = PhotoController()

The packaged template is created at ``templates/photo/photo.xhtml``.
If the generated controller exposes ``myapp.templates.photo``, update
that exposure to the packaged template path::

    @expose('myapp.templates.photo.photo')

Existing output files are refused with exit status ``1``; use ``--force`` to
overwrite deliberately. Use ``--dry-run`` to report the output without writing.
