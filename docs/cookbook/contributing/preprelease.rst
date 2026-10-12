===================================
 Preparing a Release of TurboGears
===================================

.. warning::

   Release tagging, package publishing, documentation publishing, and release
   announcements are maintainer-only actions. Contributors should stop after
   preparing and validating a change, then submit it for maintainer review.

Releases are prepared and published by the ``prepare_release.sh`` script in
the `TG2 Core`_ repository. The script is the only supported release process:
it validates the whole release before touching any remote repository and
refuses to proceed when something is missing. Do not run the release steps
by hand.

Usage
=====

From the root of a `TG2 Core`_ checkout::

    $ ./scripts/prepare_release.sh MAJOR.MINOR.PATCH[.devN] [--push]

Without ``--push`` the script prepares and validates the release locally
without touching any remote repository. It prints the path of the retained
workspace together with the prepared release commits, ``master`` merges, and
``tg<version>`` tags, so the result can be inspected before publishing.

With ``--push`` the script publishes the release once the validation
succeeds.

Prerequisites
=============

#. ``uv`` and ``twine`` on the command line, plus ``gh`` when using
   ``--push``. The script checks them before doing any work.
#. SSH access to GitHub and PyPI credentials for ``twine``.

Before running the script
=========================

#. Write the ``From <previous version> to <released version>`` chapter of
   ``docs/reference/upgrading.rst`` in the `TG2 Docs`_ repository and push it
   to the ``development`` branch. The script refuses to release without it.
   ``.devN`` releases are covered by the chapter of their base version.
#. Make sure the `TG2 Core`_ and `TG2 Devtools`_ ``development`` branches hold
   everything the release should ship and pass their test suites.

What the script does
====================

The script clones `TG2 Core`_, `TG2 Devtools`_, and `TG2 Docs`_ into a
temporary workspace and then:

#. Verifies that the upgrading guide has a chapter for the released version.
#. Bumps the version of both packages, which must already be aligned, updates
   the ``TurboGears2 >=`` constraint of the devtools and of the quickstart
   templates, fills the new change log section from the commit history since
   the previous release, and opens it in your editor for review; the
   reviewed section is committed together with the version bump.
#. Builds the source distribution and wheel of both packages with ``uv``.
#. Runs the devtools quickstart test suite against the built wheels and
   checks that the tests really installed the candidate version.
#. Prepares the release commits on ``development``, fast-forwards
   ``master``, and creates the annotated ``tg<version>`` tags in both
   repositories.

With ``--push`` the script additionally:

#. Re-checks the remote repositories, then pushes ``master``,
   ``development``, and the tag of both repositories.
#. Creates the GitHub releases of both repositories with auto-generated
   notes.
#. Publishes the wheels and source distributions to `PyPI`_ with ``twine``.
#. Waits until PyPI lists the released version.
#. Updates the latest release version, date, and download link of the
   `TG2 website`_ and pushes the change, which deploys the site through
   GitHub Pages. ``.devN`` releases skip the website.

When something fails
====================

A validation failure aborts the script before the first Git release
operation, so a failed run never leaves a half-published release behind.
When a failure happens after publishing has started, the script keeps the
workspace, reports what was already published, and prints the exact command
to finish the remaining step by hand.

After the release
=================

The maintainer curates the auto-generated GitHub release notes and publishes
the release announcement.

Repository links
================

.. _PyPI: https://pypi.org/
.. _TG2 Core: https://github.com/TurboGears/tg2
.. _TG2 Devtools: https://github.com/TurboGears/tg2devtools
.. _TG2 Docs: https://github.com/TurboGears/tg2docs
.. _TG2 website: https://github.com/TurboGears/tgwebsite
