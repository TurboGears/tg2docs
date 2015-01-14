=============================================
Advanced Admin Customizations
=============================================

TurboGears admin configurations work through the ``TGAdminConfig`` class, which
makes it possible to change the behavior for each model. We are going to use the
EasyCrudRestController to perform quick tuning of our administrative interface.

Displaying the Slug
======================

Right now our admin shows us the page id and title, but doesn't provide a link
to the page itself, so it's hard to see how a page looks after we edit it.

To solve this issue we are going to replace the page id with a link to the page
itself inside the administration table.

Custom Admin Config
----------------------

The first step is provide a custom admin config which removes the page id field.
We are going to add this in ``wikir/controllers/root.py``::

    from tgext.crud import EasyCrudRestController
    from tgext.admin.config import CrudRestControllerConfig

    class WikiPageAdminController(EasyCrudRestController):
        __table_options__ = {'__omit_fields__':['uid']}

    class CustomAdminConfig(TGAdminConfig):
        class wikipage(CrudRestControllerConfig):
            defaultCrudRestController = WikiPageAdminController

Once you declared your custom admin config, inside your ``RootController``
there should be a line which looks like::

    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

Replace that one with::

    admin = AdminController(model, DBSession, config_type=CustomAdminConfig)

When you reload the wiki pages administration table you should see that the
page uid is not there anymore.

The Slug Column
------------------------

We are now going to replace the previous **uid** field with a **url** column
which contains a link to the page.

To do so we have to tell our table that there an html type column (so its
content doesn't get escaped) and how to generate the content for that column.
This can be done inside the ``WikiPageAdminController`` that we just declared::

    class WikiPageAdminController(EasyCrudRestController):
        __table_options__ = {
            '__omit_fields__':['uid'],
            '__field_order__':['url'],
            '__xml_fields__':['url'],

            'url': lambda filler, row: '<a href="%(url)s">%(url)s</a>' % dict(url=row.url)
        }

.. note::

    The ``__field_order__`` option is necessary to let the admin know that we
    have a ``url`` field that we want to show. Otherwise it will just know
    how to show it thanks to the ``__xml_fields__`` and ``slug`` properties
    but won't know where it has to be displayed.

Extending the Admin Further
---------------------------

If you want to further customize the admin behaviour have a look at the
:ref:`tgadmin` documentation.
