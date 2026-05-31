==================================
Serving Wiki Pages
==================================

We are now able to create, edit and delete Wiki Pages, but we are still unable
to serve them.

Without serving pages our wiki is actually useless, so we are going to add
a controller and template to make them available.

WebSite Index
======================

To make our wiki navigable we are going to create a new index page with
a sidebar containing all the available wiki pages, so the user can easily move around.

Pages Slug and Content
-----------------------

To create links to the pages and display their content we are going to add url,
slug, and html_content properties to the page model. The slug gives each page a
stable URL-friendly path segment, while html_content gives back the page content
parsed accordingly to the `Markdown <http://en.wikipedia.org/wiki/Markdown>`_
language.

To process **markdown** we are going to use the ``Markdown`` library. Add it to
our project ``pyproject.toml`` file inside the ``[project].dependencies`` list::

    [project]
    dependencies = [
      # keep the dependencies already listed here...
      "Markdown",
    ]

Then we need to run again ``python -m pip install -e .`` to install our new
project dependency::

    (tgenv)$ python -m pip install -e .

Now that we installed Markdown we can add the **slug**, **url** and
**html_content** properties to our WikiPage model. Our model should end up
looking like::

    # -*- coding: utf-8 -*-
    from datetime import datetime
    import re
    import unicodedata

    import tg
    from markdown import markdown
    from sqlalchemy import Column
    from sqlalchemy.types import DateTime, Integer, Unicode

    from wikir.model import DeclarativeBase

    _slug_pattern = re.compile(r'[^a-z0-9]+')

    def slugify(value):
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = _slug_pattern.sub('-', value.lower()).strip('-')
        return value or 'page'

    class WikiPage(DeclarativeBase):
        __tablename__ = 'wiki_page'

        uid = Column(Integer, primary_key=True)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        title = Column(Unicode(255), nullable=False, unique=True)
        data = Column(Unicode(4096), nullable=False, default='')

        @property
        def slug(self):
            return slugify(self.title)

        @property
        def url(self):
            return tg.url('/' + self.slug)

        @property
        def html_content(self):
            return markdown(self.data)

        class __sprox__(object):
            hide_fields = ['updated_at']
            field_widget_args = {'data': {'rows': 15}}

Index Controller
------------------------

Now that we are able to retrieve the url for each wiki page,
we need to retrieve the list of the wiki pages with their urls
so that our index page can display the sidebar.

Our index page is a wiki page itself, so we are also going to load up
its content from the page titled "index".

To do so we must edit the ``RootController`` class inside the ``wikir/controllers/root.py``
file and look for the **index** method. When you found it change it to look like::


    @expose('wikir.templates.index')
    def index(self):
        wikipages = [(w.url, w.title) for w in DBSession.query(model.WikiPage).filter(model.WikiPage.title != 'index')]

        indexpage = DBSession.query(model.WikiPage).filter_by(title='index').first()
        if not indexpage:
            content = 'Index page not available, please create a page titled index'
        else:
            content = indexpage.html_content

        return dict(page='index', wikipages=wikipages, content=content)

TurboGears2 controllers are just plain python methods with an ``@expose`` decorator.
The @expose decorator tells to TurboGears2 which template the controller is going to display
and make so that all the data that our controller returns will be available inside
the template itself.

If you are still asking yourself why connecting to http://localhost:8080/ you ended
up being served by the **RootController.index** method you probably want to take a look
at TurboGears2 documentation about :ref:`writing_controllers`
and try to understand how *Object Dispatch* routing works.

Index Template
-------------------------

Now, if you reloaded to your index page you probably already noticed that nothing
changed. This is because our controller retrieved the wiki pages, but we didn't
expose them in the index template in any place.

The index template is available as ``wikir/templates/index.xhtml``. This is the
same path written inside the @expose decorator but with */* replaced by dots and
without the ``.xhtml`` template extension.

We are going to provide a really simple Kajiki template, so what is currently
available inside the file is going to just be removed and replaced with:

.. code-block:: xml

    <html py:extends="master.xhtml" py:strip="True">
    <head py:block="head" py:strip="True">
        <title py:block="master_title">Wikier Index</title>
    </head>

    <body py:block="body" py:strip="True">
      <div class="row">
        <div class="col-md-3">
          <ul>
           <li py:for="url, title in wikipages">
              <a href="${url}">${title}</a>
           </li>
          </ul>
        </div>
        <div class="col-md-9">
          <div>
           ${Markup(content)}
          </div>
        </div>
      </div>
    </body>
    </html>

Serving all Wiki pages
==========================

If you tried clicking on any link in our sidebar your probably noticed that
they all lead to a 404 page. This is because we still haven't implemented any
controller method that is able to serve them.

Page Template
---------------------------

First we are going to create a template for our wiki pages and save it as
``wikir/templates/page.xhtml``. The content of our template will look like:

.. code-block:: xml

    <html py:extends="master.xhtml" py:strip="True">
    <head py:block="head" py:strip="True">
        <title py:block="master_title">${title}</title>
    </head>

    <body py:block="body" py:strip="True">
      <div class="row">
        <div class="col-md-12">
          <h2>${title}</h2>
          ${Markup(content)}
          <a py:if="request.identity and 'managers' in request.identity['groups']"
             href="${tg.url('/admin/wikipages/%s/edit' % page_id)}">
             edit
          </a>
        </div>
      </div>
    </body>
    </html>

Page Controller
----------------------

Now that we have our template we just need to bind it a controller
which is going to render the page. To do this we are going to use
the special ``_default`` controller method. This is a method that
TurboGears will call if it's unable to find the exact method requested
by the url.

As our wiki pages have all different names they will all end up
in _default and we will be able to serve them from there. Just
edit ``wikir/controllers/root.py`` and add the ``_default`` method
to the ``RootController``::

    from tg import abort

    @expose('wikir.templates.page')
    def _default(self, slug, *args, **kw):
        page = next((w for w in DBSession.query(model.WikiPage).all() if w.slug == slug), None)
        if page is None:
            abort(404)
        return dict(page_id=page.uid, title=page.title, content=page.html_content)

The ``_default`` method receives the requested path segment, looks for a wiki
page with the same slug, and returns a 404 response when no page matches.

If the page is available the page instance is returned, so
our controller ends just returning the data of the page to
the template.

If you now point your browser to the index and click any of the
links in the sidebar you will see that they now lead to the
linked page instead of failing with a 404 like before.

.. note::

    If you don't have any links in the left bar, just go to the
    admin page and create as many pages as you like.

Our wiki is actually finished, but in the upcoming sections
we are going to see how we can improve it by introducing caching.
