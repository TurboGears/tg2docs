Contributing To TurboGears 2
============================

If you want to help out, we want to help you help out! The goal of
this document is to help you get started and answer any questions you
might have. The `Project Philosophy`_ document has a more high-level
view, whereas this document is nuts-and-bolts. The `TurboGears team`_
page lists who is responsible for what (a little outdated don't trust
it much).

.. _Project Philosophy: TG2Philosophy.html
.. _TurboGears team: http://docs.turbogears.org/TurboGearsTeam

Installation and Tools
----------------------

To contribute to core, you will want to do a :ref:`sourceinstall` so that
you can use Mercurial (hg) to generate patches.  You may want
to review :ref:`bitbucket_tutorial` if you would like to use the BitBucket
service to collaborate with other developers easily.

Communication Channels
----------------------

 * Internet Relay Chat (IRC) is the primary channel for collaboration and
   communication for the core developers.  `Freenode's TurboGears Channel`_
   is the primary channel for getting interactive answers to questions.
 * If you want to post a piece of code, a traceback, or any significant
   piece of text in the IRC channel, consider using a
   `PasteBin`_ service.
 * The `TurboGears mailing list`_ allows for asking longer-form questions
   and can be accessed without an IRC client, such as when you are behind
   a corporate firewall.

.. _`TurboGears mailing list`: http://groups.google.com/group/turbogears
.. _`PasteBin`: http://pastebin.ca/
.. _`Freenode's TurboGears Channel`: irc://freenode.net/#turbogears

Source Layout
-------------

TurboGears 2 is composed of two core packages.

* tg package is TurboGears 2 core.
* tg.devtools is a set of tools used for developing turbogears
    applications but not needed for running them.

Coding Style
------------

Since it's hard to argue with someone who's already written a code
style document, TurboGears 2 follows `PEP 8`_ conventions. The only
rule we do not enforce is the 80 characters per line, as templates and
other web related files simply don't fit into 80 chars in a natural
way.

To ensure that files in the TurboGears source code repository have
proper line-endings, you must configure your Subversion client. Please
see the `patching guidelines`_ for details.

.. _PEP 8: http://www.python.org/peps/pep-0008.html

Testing
-------

Automated unit tests are essential to make the future growth of the
project as error free as possible.  Please see :ref:`testing_core`
for more information about how to set up your environment with
TurboGears for testing.

Documenting Changes
-------------------

The `TurboGears Trac`_ is mostly used for tracking upcoming changes
and tasks required before release of a new version. The changelog_
provides the human readable list of changes.

.. _TurboGears Trac: http://trac.turbogears.org/
.. _changelog: http://trac.turbogears.org/wiki/2.0/changelog

Updating the changelog right before a release just slows down the
release. Please **update the changelog as you make changes**, and this
is **especially** critical for **backwards incompatibilities**.

How To Submit A Patch
---------------------

Please make sure that you read and follow the `patching guidelines`_.

.. _patching guidelines: http://docs.turbogears.org/patching_guidelines

Documentation
-------------

As mentioned in the `Project Philosophy`_ document, a feature doesn't
truly exist until it's documented. Tests can serve as good
documentation, because you at least know that they're accurate. But,
it's also nice to have some information in English.

There are two kinds of docs, and both have their useful place:

**API reference**
    These are generated with sphinx and normally include both TG docs
    and the sphinx sources of all upstream packages (that use sphinx)

**Manual**
    The TurboGears |version| documentation is online at
    http://turbogears.org/2.1/docs/

Please document your own work. It doesn't have to be Shakespeare, but
the editors don't enjoy writing documentation any more than you do
(we'd rather be coding) and it's much easier to edit an existing doc
than it is to figure out your code and write something from scratch.

.. todo:: Difficulty: Medium. More doc types will be defined here when doc templates are
    brought online.

Contributing Documentation
----------------------------

Please see the document :ref:`building_docs` for detailed instructions
on how to submit documentation to the TurboGears project.
