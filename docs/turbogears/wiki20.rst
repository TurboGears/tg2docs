.. _wiki20:

=========================================
Full Stack TurboGears: Wiki in 20 Minutes
=========================================

This tutorial builds a small reStructuredText wiki with TurboGears 2.5.1.
It starts with the generated full-stack project, keeps the generated demo and
authentication routes, and mounts the wiki below ``/wiki``. A page is a
``Page`` with a ``pagename`` and ``data``; ``FrontPage`` is the first page.

The result is intentionally small: CamelCase ``WikiWords`` become links,
missing pages open an edit form, and the page list shows every saved page. It
is a learning path through a model, controller, database setup, and Kajiki
views, not a complete wiki product.

.. warning::

   **Run this sample on localhost only.** It intentionally omits
   authentication and authorization for wiki actions, CSRF protection,
   POST-only enforcement, input validation, and complete HTML sanitization.
   Do not expose or deploy it. In particular, generated debug mode (including
   ``--debug`` and its detailed error pages) must never be public.

Scope and checkpoints
=====================

You will make one ``Page`` model, one ``/wiki`` subcontroller, three views,
and one focused HTTP test. The checkpoints below make it clear when each
stage is complete. Do not start the server until the **final files** stage.

* **Project:** the virtual environment is active and the full-stack project
  installs with its development extras.
* **Database:** ``setup-app`` completes and creates ``FrontPage``.
* **Final files:** the wiki controller and all three wiki templates have
  replaced their scaffolds; the test file is also in place.
* **Running app:** ``/wiki`` shows ``FrontPage`` and ``/demo`` still shows the
  generated demo.

Prerequisites and project setup
===============================

Use Python **3.10 or newer**. Work from an explicit directory so it is easy
to distinguish the outer project directory from the inner Python package.
The commands below use a POSIX shell; on Windows, activate the environment
with ``.venv\\Scripts\\activate`` instead of ``. .venv/bin/activate``.

.. code-block:: bash

    $ python3 --version
    $ mkdir -p ~/src/turbogears-tutorial
    $ cd ~/src/turbogears-tutorial
    $ python3 -m venv .venv
    $ . .venv/bin/activate
    $ python -m pip install --upgrade pip
    $ python -m pip install tg.devtools
    $ gearbox quickstart wiki20
    $ cd wiki20

The outer project directory is now ``~/src/turbogears-tutorial/wiki20``. Run
project commands from there unless a later command says otherwise. The
quickstart's default options provide SQLAlchemy, Alembic migrations, Kajiki,
and generated authentication routes. Keep those generated routes; the wiki
is added beside them rather than replacing the root controller.

The generated project has two levels. The outer files describe and operate
the project; the inner ``wiki20/`` directory is the importable application
package:

.. code-block:: text

    wiki20/                                  # outer project: run commands here
    ├── pyproject.toml                       # dependencies and project metadata
    ├── development.ini                     # local server/database configuration
    ├── test.ini                             # generated test configuration
    ├── migration/                           # Alembic migration environment
    └── wiki20/                              # inner Python application package
        ├── config/                          # application configuration
        ├── controllers/                     # URL tree and request actions
        │   ├── demo.py                      # generated demo; keep it
        │   ├── error.py                     # generated error pages; keep it
        │   ├── root.py                      # add the /wiki mount here
        │   └── wiki.py                      # replace with the wiki controller
        ├── i18n/                            # translation catalogs
        ├── lib/                             # shared application helpers
        ├── model/                           # SQLAlchemy models
        │   ├── __init__.py                  # register Page at the bottom
        │   └── page.py                      # create this Page model
        ├── public/                          # static assets
        ├── templates/                       # Kajiki views
        │   ├── edit.xhtml                   # replace the edit view
        │   ├── page.xhtml                   # replace the display view
        │   └── pagelist.xhtml               # replace the list view
        ├── tests/                            # pytest/WebTest tests
        │   └── functional/test_wiki.py      # replace the generated test
        └── websetup/                         # setup and bootstrap hooks
            └── bootstrap.py                  # add the initial FrontPage

The paths in this tutorial are relative to the outer ``wiki20`` project
unless a path begins with ``wiki20/`` as shown above.

Add the rendering dependency
============================

The wiki stores reStructuredText and renders it with Docutils, so Docutils
must be an application dependency. Open ``pyproject.toml`` and add **only**
``"docutils",`` to the existing ``[project]`` ``dependencies`` list. Do not
replace the generated list with an abbreviated one: it contains the runtime
packages selected by quickstart.

Keep every generated dependency and add this one line inside the existing
``dependencies = [...]`` list; do not replace the list with a shortened
example:

.. code-block:: toml

    "docutils",

Install the project, its development dependencies, and the new Docutils
requirement from the outer project directory:

.. code-block:: bash

    $ python -m pip install -e '.[development]'

A quick check is useful before editing application files:

.. code-block:: bash

    $ python -c "import docutils, tg; print('TurboGears and Docutils are ready')"

MVC, routing, and Kajiki in one page
====================================

TurboGears follows Model-View-Controller (MVC):

* The **model** maps ``Page`` objects to database rows.
* The **controller** receives a URL, reads or changes a page, and returns
  template variables.
* The **view** is a Kajiki template that turns those variables into HTML.

TurboGears represents URLs as a tree of controller objects. Mounting
``WikiController()`` as ``RootController.wiki`` means the ``wiki`` path is
consumed first; the remaining path is dispatched inside that subcontroller.
``@expose`` makes a method reachable through HTTP. ``index`` handles the
controller's default URL, while ``_default`` catches an otherwise unmatched
path and receives the remaining URL segment.

An exposed action can return a dictionary. Its keys become variables with the
same names in the selected template, so ``{"content": html, "wikipage": page}``
provides ``content`` and ``wikipage`` to the view. Kajiki templates use
``py:`` directives such as ``py:extends`` for inheritance, ``py:content`` or
``py:replace`` for values, ``py:for`` for loops, and ``py:if`` for conditions.
The generated ``master.xhtml`` supplies the common page layout.

The finished URL/action map is:

.. list-table:: Wiki routes
   :header-rows: 1
   :widths: 35 35 30

   * - URL
     - Action
     - Purpose
   * - ``/wiki``
     - ``WikiController.index``
     - Display ``FrontPage``
   * - ``/wiki/<pagename>``
     - ``WikiController._default``
     - Display a page or redirect to its edit form
   * - ``/wiki/edit?pagename=<pagename>``
     - ``WikiController.edit``
     - Show an edit form without creating a row
   * - ``/wiki/save`` (form POST)
     - ``WikiController.save``
     - Create or update a page, then redirect
   * - ``/wiki/pagelist``
     - ``WikiController.pagelist``
     - List pages alphabetically

Scaffold the wiki files
=======================

From the outer project directory, use the generated scaffold templates:

.. code-block:: bash

    $ gearbox scaffold controller wiki
    $ gearbox scaffold controller_test wiki
    $ gearbox scaffold template page
    $ gearbox scaffold template edit
    $ gearbox scaffold template pagelist

The controller command creates ``wiki20/controllers/wiki.py``. The
``controller_test`` command creates
``wiki20/tests/functional/test_wiki.py``. The three template commands create
``wiki20/templates/page.xhtml``, ``wiki20/templates/edit.xhtml``, and
``wiki20/templates/pagelist.xhtml``.

The scaffold does **not** create ``wiki.xhtml``. That is expected: the final
controller below exposes ``page.xhtml``, ``edit.xhtml``, and
``pagelist.xhtml``. Do not run the server or visit ``/wiki`` yet. Replace the
controller and all three templates first, otherwise the application can start
with an incomplete route/template set.

Create and register the model
=============================

Create ``wiki20/model/page.py``:

.. code-block:: python

    """Wiki page model."""

    from sqlalchemy import Column
    from sqlalchemy.types import Integer, Text

    from wiki20.model import DeclarativeBase


    class Page(DeclarativeBase):
        """A reStructuredText page in the wiki."""

        __tablename__ = "page"

        id = Column(Integer, primary_key=True)
        pagename = Column(Text, unique=True, nullable=False)
        data = Column(Text, nullable=False)

At the **bottom** of the generated ``wiki20/model/__init__.py``, after its
existing model imports, add ``Page`` and export it. Keeping this import at the
bottom lets the generated model setup exist before the new mapped class is
registered:

.. code-block:: python

    from wiki20.model.todo import TodoItem
    from wiki20.model.auth import User, Group, Permission
    from wiki20.model.page import Page

    __all__ = ('TodoItem', 'User', 'Group', 'Permission', 'Page')

Leave the generated session, metadata, and ``init_model`` code unchanged.

Seed the first page
===================

The generated ``wiki20/websetup/bootstrap.py`` already creates its example
authentication users. In its existing SQLAlchemy ``try`` block, immediately
after ``model.DBSession.add(u1)`` and before the generated ``flush`` and
``commit``, add the initial page:

.. code-block:: python

    model.DBSession.add(model.Page(
        pagename="FrontPage",
        data="Welcome to the **FrontPage**. Create a NewPage.",
    ))

Do not remove the generated user setup or its ``IntegrityError`` handling.
For a fresh database, initialize the tables and bootstrap data now:

.. code-block:: bash

    $ gearbox setup-app -c development.ini

**Checkpoint:** setup completes without an import or database error. A fresh
application now has the ``page`` table and ``FrontPage`` row, but the wiki
routes are not ready until the remaining files are replaced.

Mount the subcontroller without replacing RootController
==========================================================

Open ``wiki20/controllers/root.py``. Add only this import with the existing
imports:

.. code-block:: python

    from wiki20.controllers.wiki import WikiController

Add this attribute alongside the generated ``demo`` and ``error`` attributes:

.. code-block:: python

    wiki = WikiController()

Keep the generated ``DemoController`` and ``ErrorController`` imports and
attributes, the ``index`` redirect, and all generated login/logout methods.
Do not replace ``RootController`` wholesale: the generated ``/demo`` and auth
routes should continue to work, while the new attribute adds the ``/wiki``
branch to the controller tree.

Final controller: display, edit, save, and list
===============================================

Now replace **all** of ``wiki20/controllers/wiki.py`` with the following
controller. This replacement must happen before serving the application.

.. code-block:: python

    """Wiki controller."""

    import re

    from docutils.core import publish_parts
    from sqlalchemy import select
    from tg import expose, redirect, url

    from wiki20.lib.base import BaseController
    from wiki20.model import DBSession, Page

    wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)\b")


    class WikiController(BaseController):
        """Display and edit pages below ``/wiki``."""

        @expose("wiki20.templates.page")
        def index(self):
            """Display FrontPage."""
            return self._display("FrontPage")

        @expose("wiki20.templates.page")
        def _default(self, pagename):
            """Display the page named by the final URL segment."""
            return self._display(pagename)

        @expose("wiki20.templates.edit")
        def edit(self, pagename):
            """Display an edit form without creating a page."""
            page = DBSession.scalar(select(Page).where(Page.pagename == pagename))
            if page is None:
                page = Page(pagename=pagename, data="")
            return {"wikipage": page}

        @expose()
        def save(self, pagename, data):
            """Create or update a page, then show it."""
            page = DBSession.scalar(select(Page).where(Page.pagename == pagename))
            if page is None:
                page = Page(pagename=pagename, data=data)
                DBSession.add(page)
            else:
                page.data = data
            redirect(url("/wiki/" + pagename))

        @expose("wiki20.templates.pagelist")
        def pagelist(self):
            """List all pages alphabetically."""
            pages = DBSession.scalars(select(Page).order_by(Page.pagename)).all()
            return {"pages": pages}

        def _display(self, pagename):
            page = DBSession.scalar(select(Page).where(Page.pagename == pagename))
            if page is None:
                redirect(url("/wiki/edit", params={"pagename": pagename}))

            content = publish_parts(
                page.data,
                writer_name="html",
                settings_overrides={
                    "raw_enabled": False,
                    "file_insertion_enabled": False,
                },
            )["html_body"]
            content = wikiwords.sub(
                lambda match: '<a href="{}">{}</a>'.format(
                    url("/wiki/" + match.group(1)), match.group(1)
                ),
                content,
            )
            return {"content": content, "wikipage": page}

The SQLAlchemy 2 style is deliberate: ``select()`` constructs a statement,
``DBSession.scalar()`` returns one ``Page`` or ``None``, and
``DBSession.scalars()`` returns the ordered collection. A request-time
controller uses ``url()`` so the application mount point is included. The
current generated ``RootController`` also uses ``lurl('/')`` for default
arguments such as ``came_from``. ``lurl()`` is lazy: it defers URL resolution
until the value is used, because Python evaluates default arguments before a
request exists. Do not mechanically replace generated ``lurl()`` with
``url()`` or ``tg.url()``. Use ``url()`` in request-time controller code and
``tg.url()`` in templates; each resolves the application mount point in its
request context, while ``lurl()`` preserves that handling for values declared
before the request. The ``redirect()`` call is intentionally invoked directly;
it ends the request instead of returning a template.

Display the rendered page
=========================

Replace ``wiki20/templates/page.xhtml`` with this ``html+genshi`` template.
It inherits the generated master layout and receives ``wikipage`` and
``content`` from ``_display``:

.. code-block:: html+genshi

    <html py:extends="master.xhtml" py:strip="True">
      <head py:block="head" py:strip="True">
        <title py:block="master_title">${wikipage.pagename} - TurboGears Wiki</title>
      </head>

      <body py:block="body" py:strip="True">
        <section class="card">
          <div class="card-body">
            <h1 class="h3" py:content="wikipage.pagename">Page name</h1>
            <div py:replace="Markup(content)">Formatted content</div>
            <p class="mt-3">
              <a href="${tg.url('/wiki/edit', params={'pagename': wikipage.pagename})}">Edit this page</a>
              <a class="ms-3" href="${tg.url('/wiki')}">FrontPage</a>
              <a class="ms-3" href="${tg.url('/wiki/pagelist')}">View the page list</a>
            </p>
          </div>
        </section>
      </body>
    </html>

The ``tg.url()`` expression is the template URL helper; it is distinct from
the controller's request-time ``url()``. ``Markup(content)`` tells Kajiki to
insert the already-generated HTML rather than escape its tags. It is **not**
a sanitizer and does not make untrusted content safe.

Edit and save pages
===================

Replace ``wiki20/templates/edit.xhtml``:

.. code-block:: html+genshi

    <html py:extends="master.xhtml" py:strip="True">
      <head py:block="head" py:strip="True">
        <title py:block="master_title">Editing: ${wikipage.pagename}</title>
      </head>

      <body py:block="body" py:strip="True">
        <section class="card">
          <div class="card-body">
            <h1 class="h3">Editing: ${wikipage.pagename}</h1>
            <form action="${tg.url('/wiki/save')}" method="post">
              <input type="hidden" name="pagename" value="${wikipage.pagename}" />
              <textarea class="form-control" name="data" rows="10" py:content="wikipage.data"></textarea>
              <button class="btn btn-primary mt-3" type="submit">Save</button>
            </form>
          </div>
        </section>
      </body>
    </html>

``edit`` creates an unsaved ``Page`` object when the name is missing, only so
the form has a name and empty text. It does **not** add that object to
``DBSession``. A GET for a missing page therefore performs no write. The
``save`` action creates the row on submission, or updates its ``data`` when
the row already exists; TurboGears' request transaction persists it before
the redirect completes.

WikiWords and missing pages
===========================

The ``wikiwords`` expression recognizes a CamelCase word with at least two
capitalized parts, such as ``NewPage``. ``publish_parts`` first converts the
stored reStructuredText to an HTML body. The controller then turns matching
words in that body into links below ``/wiki``.

Docutils is a real runtime dependency because of ``publish_parts``. The
controller disables the raw directive and file insertion before rendering:

* ``raw_enabled=False`` prevents raw output directives.
* ``file_insertion_enabled=False`` prevents including local files.

Those settings reduce risk but do not provide complete sanitization. The
sample remains localhost-only, especially because ``Markup(content)`` inserts
the generated HTML as markup.

Following a ``NewPage`` link when no row exists calls ``_display`` and
redirects to ``/wiki/edit?pagename=NewPage``. Nothing is written during that
GET. Saving the form is the first write and then redirects to the newly
created page.

Page list
=========

Replace ``wiki20/templates/pagelist.xhtml``:

.. code-block:: html+genshi

    <html py:extends="master.xhtml" py:strip="True">
      <head py:block="head" py:strip="True">
        <title py:block="master_title">Page listing - TurboGears Wiki</title>
      </head>

      <body py:block="body" py:strip="True">
        <section class="card">
          <div class="card-body">
            <h1 class="h3">All Pages</h1>
            <ul>
              <li py:for="page in pages">
                <a href="${tg.url('/wiki/' + page.pagename)}" py:content="page.pagename">Page name</a>
              </li>
            </ul>
            <a href="${tg.url('/wiki')}">FrontPage</a>
          </div>
        </section>
      </body>
    </html>

The ``pagelist`` action passes ``pages`` from an ordered
``DBSession.scalars(select(Page).order_by(Page.pagename))`` query. Kajiki's
``py:for`` renders one list item per model object.

Functional HTTP test
====================

Replace the generated ``wiki20/tests/functional/test_wiki.py`` with this
focused test. It uses the generated ``TestController`` (which loads
``test.ini`` and provides a WebTest ``self.app``) and checks behavior through
public HTTP requests rather than private controller methods:

.. code-block:: python

    """Functional tests for the wiki."""

    from wiki20.tests import TestController


    class TestWikiController(TestController):
        """Tests for wiki requests through the public application."""

        def test_wiki_journey(self):
            response = self.app.get("/wiki")
            response.mustcontain("FrontPage", "Welcome")

            response = self.app.post(
                "/wiki/save",
                {"pagename": "FrontPage", "data": "Visit NewPage."},
                status=302,
            )
            assert response.location.endswith("/wiki/FrontPage")
            response = response.follow()
            response.mustcontain("FrontPage", "Visit")
            assert 'href="/wiki/NewPage"' in response

            response = self.app.get("/wiki/NewPage", status=302)
            assert response.location.endswith("/wiki/edit?pagename=NewPage")
            response = response.follow()
            response.mustcontain("Editing: NewPage")

            response = self.app.get("/wiki/pagelist")
            assert "NewPage" not in response

            response = self.app.post(
                "/wiki/save",
                {"pagename": "NewPage", "data": "This is a new page."},
                status=302,
            )
            assert response.location.endswith("/wiki/NewPage")
            response = response.follow()
            response.mustcontain("NewPage", "This is a new page.")

            response = self.app.get("/wiki/pagelist")
            response.mustcontain("FrontPage", "NewPage")

Run the focused test first, then the generated suite:

.. code-block:: bash

    $ python -m pytest wiki20/tests/functional/test_wiki.py -q
    $ python -m pytest -q

The focused test proves the initial ``/wiki`` response, save/redirect/display,
WikiWord linking, missing-page edit behavior, no-write-on-GET behavior, a
successful new-page save/display, and ``/wiki/pagelist``. It does not attempt
to test authentication or security features that this sample intentionally
does not add.

Start the server only after the final files
===========================================

At this point ``wiki.py``, ``page.xhtml``, ``edit.xhtml``, and
``pagelist.xhtml`` have all replaced their scaffolds, and the functional test
is present. Only now start the local development server:

.. code-block:: bash

    $ gearbox serve -c development.ini --reload

Open these URLs:

* http://127.0.0.1:8080/wiki shows ``FrontPage``.
* http://127.0.0.1:8080/demo still shows the generated demo.
* Editing ``FrontPage`` with ``Visit NewPage.`` links to the missing-page edit
  form; saving it creates and displays ``NewPage``.
* http://127.0.0.1:8080/wiki/pagelist lists both pages.

The ``--reload`` option restarts the development server after source changes.
The generated development configuration binds to localhost. Do not change
that into a public debug server for this sample.

Existing databases: migration path
===================================

``setup-app`` is the convenient fresh-project path. Do not use it to alter an
existing database that already has application data. Create a migration for
the new ``page`` table instead; see :ref:`database_migration` for the full
Alembic workflow:

.. code-block:: bash

    $ gearbox migrate -c development.ini db_version
    $ gearbox migrate -c development.ini create "Add wiki page table"
    # Edit the generated migration/versions/*_add_wiki_page_table.py revision.
    $ gearbox migrate -c development.ini test
    $ gearbox migrate -c development.ini upgrade

Keep the generated ``revision`` and ``down_revision`` values in the revision
file. The migration should create the ``page`` table with the same columns as
``Page``. Bootstrap data is separate: insert ``FrontPage`` only when it is not
already present, according to your application's existing deployment policy.

Troubleshooting
===============

* **``No module named docutils``:** confirm that ``docutils`` was added to the
  existing dependency list, then rerun ``python -m pip install -e
  '.[development]'`` from the outer project directory.
* **``No module named wiki20`` or a missing ``gearbox`` command:** activate
  ``.venv`` and install the project with the exact editable-install command
  above.
* **Template not found or an error mentioning ``wiki.xhtml``:** the scaffold
  is incomplete. Confirm that the final controller exposes
  ``wiki20.templates.page``, ``edit``, and ``pagelist``, and that all three
  ``*.xhtml`` files were replaced before starting the server.
* **``FrontPage`` is missing:** on a fresh database, rerun
  ``gearbox setup-app -c development.ini`` after registering ``Page`` and
  adding the bootstrap row. On an existing database, apply the migration
  instead.
* **``/wiki`` is missing but ``/demo`` works:** confirm the ``WikiController``
  import and ``wiki = WikiController()`` attribute were added to the
  generated ``RootController``; keep the generated root methods.
* **A change is not visible:** use ``--reload`` during local development or
  restart ``gearbox serve`` after changing configuration.

Further exploration and security
================================

The generated ``/demo`` and authentication routes remain useful examples.
Next, read :ref:`writing_controllers`, :ref:`templating`,
:ref:`kajiki-language`, :ref:`testing`, and :ref:`database_migration`.
Before building a real wiki, add an explicit authentication/authorization
policy, CSRF protection, validation, POST enforcement, and a well-reviewed
sanitization strategy for stored markup. Do not treat this tutorial's
``Markup(content)`` usage or Docutils settings as that policy.
