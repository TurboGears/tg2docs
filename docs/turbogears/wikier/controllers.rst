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

To create links to the pages and display their content we are going to add url
and html_content properties to the page model. The first property will create
the slug for the model and provide the url where the page is available, while
the second will give back the page content parsed accordingly to the
`Markdown <http://en.wikipedia.org/wiki/Markdown>`_ language.

To generate the slugs we are going to use ``tgext.datahelpers``, so
the first thing we are going to do is add it to our project ``setup.py``
file inside the ``install_requires`` list::

    install_requires=[
        "TurboGears2 >= 2.2.0",
        "Genshi",
        "zope.sqlalchemy >= 0.4",
        "sqlalchemy",
        "sqlalchemy-migrate",
        "repoze.who",
        "repoze.who-friendlyform >= 1.0.4",
        "tgext.admin >= 0.5.1",
        "repoze.who.plugins.sa",
        "tw2.forms",
        "webhelpers",
        "tgext.datahelpers",
        ]

Then we need to run again ``pip install -e .`` to install our new
project dependency::

    (tg22env)$ pip install -e .
    Successfully installed tgext.datahelpers wikir PIL
    Cleaning up...

.. note::
    As tgext.datahelpers also provides support for attachments and
    thumbnails generation it is going to bring in the Python Imaging Library (PIL).
    For now we are just going to ignore it as we don't need it, but it's good
    to know that it's available.

Now that we installed the datahelpers we can add the **url** and **html_content**
properties to our WikiPage model. Our model should end up looking like::

    #all the other sqlalchemy imports here...
    import tg
    from tgext.datahelpers.utils import slugify
    from webhelpers.html.converters import markdown

    class WikiPage(DeclarativeBase):
        __tablename__ = 'page'

        uid = Column(Integer, primary_key=True)
        updated_at = Column(DateTime, default=datetime.now, nullable=False)
        title = Column(Unicode(255), nullable=False, unique=True)
        data = Column(Unicode(4096), nullable=False, default='')

        @property
        def url(self):
            return tg.url('/'+slugify(self, self.title))

        @property
        def html_content(self):
            return markdown(self.data)

        class __sprox__(object):
            hide_fields =  ['updated_at']
            field_widget_types = {'title':TextField}
            field_widget_args = {'data': {'rows':15, 'cols':50}}
            field_attrs = {'data': {'style':'width:auto'}}

Index Controller
------------------------

Now that we are able to retrieve the url for each wiki page,
we need to retrieve the list of the wiki pages with their urls
so that our index page can display the sidebar.

Our index page is a wiki page itself, so we are also going to load up
it's content from the page titled "index".

To do so we must edit the ``RootController`` class inside the ``wikir/controllers/root.py``
file and look for the **index** method. When you found it change it to look like::


    @expose('wikir.templates.index')
    def index(self):
        wikipages = [(w.url, w.title) for w in DBSession.query(model.WikiPage).filter(model.WikiPage.title!='index')]

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
at TurboGears2 documentation about `how controllers work <http://www.turbogears.org/2.2/docs/main/Controllers.html>`_
and try to understand how *Object Dispatch* routing works.

Index Template
-------------------------

Now, if you reloaded to your index page you probably already noticed that nothing
changed. This is because our controller retrieved the wiki pages, but we didn't
expose them in the index template in any place.

The index template is available as ``wikir/templates/index.html`` which is exactly
the same path written inside the @expose decorator but with */* replaced by dots and
without the template extension.

We are going to provide a really simple template, so what is currently
available inside the file is going to just be removed and replaced with:

.. code-block:: html+genshi

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:py="http://genshi.edgewall.org/"
          xmlns:xi="http://www.w3.org/2001/XInclude">

      <xi:include href="master.html" />

    <head>
      <title>TurboGears2 Wikier Index</title>
    </head>

    <body>
      <div class="row">
        <div class="span3">
          <ul>
           <li py:for="url, title in wikipages">
              <a href="${url}">${title}</a>
           </li>
          </ul>
        </div>
        <div class="span9">
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
``wikir/templates/page.html``. The content of our template will look like:

.. code-block:: html+genshi

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:py="http://genshi.edgewall.org/"
          xmlns:xi="http://www.w3.org/2001/XInclude">

      <xi:include href="master.html" />

    <head>
      <title>${title}</title>
    </head>

    <body>
      <div class="row">
        <div class="span12">
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
turbogears will call if it's unable to find the exact method request
by the url.

As our wiki pages have a all different names they will all end up
in _default and we will be able to serve them from there. Just
edit ``wikir/controller/root.py`` and add the ``_default`` method
to the ``RootController``::

    from tg import validate
    from tgext.datahelpers.validators import SQLAEntityConverter
    from tgext.datahelpers.utils import fail_with

    @expose('wikir.templates.page')
    @validate({'page':SQLAEntityConverter(model.WikiPage, slugified=True)},
              error_handler=fail_with(404))
    def _default(self, page, *args, **kw):
        return dict(page_id=page.uid, title=page.title, content=page.html_content)

The ``@validate`` decorator makes possible to apply validators
to the incoming parameters and if validation fails the specified
error_handler is called. In this case we are checking if there
is a web page with the given slug. If it fails to find one
it will just return a 404 page.

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
