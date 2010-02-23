.. module:: webhelpers.feedgenerator

Generating RSS and Atom Feeds
=============================

The `webhelpers.feedgenerator` module provides an API for
programmatically generating syndication feeds from a `Pylons`
application (your TurboGears |version| application is a particular
configuration of `Pylons`).

The feed generator is intended for use in controllers, and generates
an output stream. Currently the following feeds can be created by
using the appropriate class:

* RssFeed
* RssUserland091Feed
* Rss201rev2Feed
* Atom1Feed

All of these format specific Feed generators inherit from the
:meth:`~webhelpers.feedgenerator.SyndicationFeed` class and
you use the same API to interact with them.

Example controller method:

.. code-block:: python

    from helloworld.lib.base import BaseController
    from tg.controllers import CUSTOM_CONTENT_TYPE
    from webhelpers.feedgenerator import Atom1Feed
    from pylons import response
    from pylons.controllers.util import url_for

    class CommentsController(BaseController):

        @expose(content_type=CUSTOM_CONTENT_TYPE)
        def atom1( self ):
            """Produce an atom-1.0 feed via feedgenerator module"""
            feed = Atom1Feed(
                title=u"An excellent Sample Feed",
                link=url_for(),
                description=u"A sample feed, showing how to make and add entries",
                language=u"en",
            )
            feed.add_item(title="Sample post",
                          link=u"http://example.com/posts/sample",
                          description="Testing.")
            response.content_type = 'application/atom+xml'
            return feed.writeString('utf-8')

To have your feed automatically discoverable by your user's browser,
you will need to include a link tag to your template/document's head.
Most browsers render this as a small RSS icon next to the address bar
on which the user can click to subscribe.

.. code-block:: html

    <head>
        <link rel="alternate" type="application/atom+xml" href="./atom1" />
    </head>

Normally you will also want to include an in-page link to the RSS page
so that users who are not aware of or familiar with the automatic
discovery can find the RSS feed.  `FeedIcons`_ has a downloadable set
of icons suitable for use in links.

.. code-block:: html

    <a href="./atom1"><img src="/images/feed-icon-14x14.png" /> Subscribe</a>

.. _`FeedIcons`: http://www.feedicons.com/

The various feed generators will escape your content appropriately
for the particular type of feed.

.. autoclass:: SyndicationFeed
    :members:

    .. automethod:: __init__

.. autoclass:: Enclosure
    :members:
