=============================================
Wiki Page Generation Caching
=============================================

This section of the tutorial will show how to use the updated_at field of our models
for different kinds of caching that can greatly speed up our website.

Updating updated_at
======================

Right now the updated_at field of our models will only contain the time they get created,
because we are never updating it. We could add a SQLAlchemy event that updates it
each time the WikiPage object is updated, and that would probably be the suggested way
to handle this.

As that solution would be out of scope for this tutorial, we are
going to perform the same by customizing the TurboGears Admin.

To do so we have to customize the ``WikiPageAdminController.put`` method::

    from tgext.admin.config import CrudRestControllerConfig
    from datetime import datetime

    class WikiPageAdminController(EasyCrudRestController):
        __table_options__ = {'__omit_fields__':['uid'],
                             '__field_order__':['url'],
                             '__xml_fields__':['url'],

                             'url': lambda filler, row: '<a href="%(url)s">%(url)s</a>' % dict(url=row.url)
        }

        @expose(inherit=True)
        def put(self, *args, **kw):
            kw['updated_at'] = datetime.utcnow()
            return super(WikiPageAdminController, self).put(*args, **kw)

This way each time a wiki page is modified its updated_at field will be updated
accordingly.

Caching Page
===================

Now that we know when the page got updated we can use it speed up our wiki
by caching wiki page generation.

The first thing we need to do is move the html content generation inside our template
instead of using it directly from the controller. This can easily be done by
updating our ``RootController._default`` method accordingly::

    @expose('wikir.templates.page')
    @validate({'page':SQLAEntityConverter(model.WikiPage, slugified=True)},
              error_handler=fail_with(404))
    def _default(self, page, *args, **kw):
        return dict(wikipage=page)

Our controller now just retrieves the page and passes it to our template,
so we have to do some minor tuning to the ``wikir/templates/page.html`` template
too:

.. code-block:: html+genshi

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:py="http://genshi.edgewall.org/"
          xmlns:xi="http://www.w3.org/2001/XInclude">

      <xi:include href="master.html" />

    <head>
      <title>${wikipage.title}</title>
    </head>

    <body>
      <div class="row">
        <div class="span12">
          <h2>${wikipage.title}</h2>
          ${Markup(wikipage.html_content)}
          <a py:if="request.identity and 'managers' in request.identity['groups']"
             href="${tg.url('/admin/wikipages/%s/edit' % wikipage.uid)}">
             edit
          </a>
        </div>
      </div>
    </body>
    </html>

Now that the work of converting the page markdown content to HTML is done
by our template we can simply cache the template rendering process.

This way we will both skip the template generation phase and the page content
conversion phase at once. TurboGears2 provides a great tool for template caching.
You just need to generate a cache key and provide it inside the ``tg_cache`` dictionary
returned by your controller::

    @expose('wikir.templates.page')
    @validate({'page':SQLAEntityConverter(model.WikiPage, slugified=True)},
              error_handler=fail_with(404))
    def _default(self, page, *args, **kw):
        cache_key = '%s-%s' % (page.uid, page.updated_at.strftime('%Y%m%d%H%M%S'))
        return dict(wikipage=page, tg_cache={'key':cache_key, 'expire':24*3600, 'type':'memory'})

This will keep our template cached in memory up to a day and will still regenerate
the page whenever our wikipage changes as we are using the ``updated_at`` field
to generate our cache key.

Page Caching Performances Gain
----------------------------------

By just the minor change of caching the template the throughput of the applications
on my computer greatly increased. A quick benchmark can give the idea of the
impact of such a change::

    $ /usr/sbin/ab -c 1 -n 500 http://127.0.0.1:8080/this-is-my-first-page-1
    Requests per second:    97.55 [#/sec] (mean)

    $ /usr/sbin/ab -c 1 -n 500 http://127.0.0.1:8080/this-is-my-first-page-1
    Requests per second:    267.18 [#/sec] (mean)
