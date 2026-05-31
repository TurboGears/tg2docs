=====================================
Creating and Managing Wiki Pages
=====================================

If you correctly quickstarted your project with SQLAlchemy database support and authentication
you should end up having a ``model`` directory which contains database layer initialization and
*User*, *Group* and *Permission* models.

Those are the standard TurboGears2 authentication models. You can freely customize them, but for
now we will stick to the standard ones.

To manage our pages we are going to add model that represents a Wiki Page with attributes to store
the *title* of the page, page *data* and last time the page got modified.

WikiPage Model
-----------------

To define the model we are going to add a ``wiki.py`` file inside the ``wikir/model`` directory
which contains the model definition itself::

    # -*- coding: utf-8 -*-
    from datetime import datetime

    from sqlalchemy import Column
    from sqlalchemy.types import DateTime, Integer, Unicode

    from wikir.model import DeclarativeBase

    class WikiPage(DeclarativeBase):
        __tablename__ = 'wiki_page'

        uid = Column(Integer, primary_key=True)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        title = Column(Unicode(255), nullable=False, unique=True)
        data = Column(Unicode(4096), nullable=False, default='')

Now to let TurboGears know that our model exists we must make it available inside the ``wikir/model/__init__.py``
file just by importing it at the end::

    # Import your model modules here.
    from wikir.model.auth import User, Group, Permission
    from wikir.model.wiki import WikiPage

Enabling the Admin Controller
--------------------------------------------

The current quickstart does not mount ``/admin`` by default. This tutorial uses
the TurboGears admin extension to create and edit wiki pages, so add the admin
packages to ``pyproject.toml`` before you continue::

    [project]
    dependencies = [
      # keep the dependencies created by quickstart here...
      "tgext.admin >= 0.7.4",
      "tgext.crud >= 0.9.2",
      "tw2.forms >= 2.2.6",
    ]

Then reinstall the project so those packages are available::

    (tgenv)$ python -m pip install -e .

Finally mount the admin controller in ``wikir/controllers/root.py``. Add the
import near the other controller imports and add the ``admin`` attribute inside
``RootController``::

    from tgext.admin import AdminController

    class RootController(BaseController):
        secc = SecureController()
        admin = AdminController(model, DBSession)
        error = ErrorController()

Creating Tables and setting up Application
--------------------------------------------

Now that our model is recognized by TurboGears we must create the table that it is going to use
to store its data. By default TurboGears will automatically create tables for each model it is aware of.
This is performed during the application setup phase.

To setup your application you simply need to run the ``gearbox setup-app`` command where your application
configuration file is available (usually the root of the project)::

    (tgenv)$ gearbox setup-app
    Running setup_app() from wikir.websetup
    Creating tables

The Application setup process, apart from creating tables for the known models, will also execute the
``wikir/websetup/bootstrap.py`` module, which by default is going to create an administrator
user for our application.

Managing Pages through the Admin
===========================================

Through the *manager* user that has been created during the setup phase it is possible to get access
to the TurboGears Admin at http://localhost:8080/admin.
The first time the page is accessed it will ask for authentication. Simply provide the username and password
of the user that the setup-app command created for us::

    Username: manager
    Password: managepass

You should end up being redirected to the administration page. One of the links on the page should
point to ``WikiPages`` administration page http://localhost:8080/admin/wikipages/

On this page a list of the existing pages is provided with a link to create a **New WikiPage**.

.. note::
    If you don't find the WikiPages link on the administrator page, make sure you correctly
    imported the WikiPage model at the end of ``wikir/model/__init__.py``, mounted the admin
    controller in ``wikir/controllers/root.py``, and ran the setup-app command again.

Customizing Management
--------------------------------

Now that we have a working administration page for our WikiPages, we are going to tune a bunch
of things to improve it.

First of all we are going to hide the **updated_at** fields.
This will get automatically updated to the current time, so we don't really want to let users
modify it.

Then if you tried to click the **New WikiPage** link you probably saw that for the title of our
web page a TextArea is used, probably a TextField would be a better match to make more clear
that the user is supposed to provide a short single line title.

Last but not least we are going to provide a bit more space for the page data, to make it easier
to edit the page.

All these changes can be made from our model by specifying a special attribute called ``__sprox__``
which will be used by the administrative interface to tune the look and feel of the tables and
forms it is going to generate::

    # -*- coding: utf-8 -*-
    """Wiki Page module."""
    from datetime import datetime

    from sqlalchemy import Column
    from sqlalchemy.types import DateTime, Integer, Unicode

    from wikir.model import DeclarativeBase

    class WikiPage(DeclarativeBase):
        __tablename__ = 'wiki_page'

        uid = Column(Integer, primary_key=True)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        title = Column(Unicode(255), nullable=False, unique=True)
        data = Column(Unicode(4096), nullable=False, default='')

        class __sprox__(object):
            hide_fields = ['updated_at']
            field_widget_args = {'data': {'rows': 15}}

Going back to our administration page at http://localhost:8080/admin/wikipages/ and clicking
on the **New WikiPage** link you will see a form with just a single line entry field for the
title and a wide textarea for the page data.

Feel free to add as many pages as you like; we are going to see later how to display them.
