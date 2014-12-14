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
class inside which you just need to import inside ``model/__init__.py``
to make it available inside your app.

Creating All Together
---------------------

Multiple scaffolds can be created together, so in case you
need to create a new model with a controller to handle it
and an index page you can run::

    $ gearbox scaffold model controller template photo

Which will create a new controller with the associated page
and model. To start using the controller mount it inside
your application ``RootController``.

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
a photo package where multiple templates can be placed.