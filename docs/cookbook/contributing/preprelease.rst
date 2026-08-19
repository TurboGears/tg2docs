===================================
 Preparing a Release of TurboGears
===================================

.. warning::

   Release tagging, package publishing, documentation publishing, and release
   announcements are maintainer-only actions. Contributors should stop after
   preparing and validating a change, then submit it for maintainer review.

Prerequisites
=============

Before preparing release material, you need:

#. Python 3 and an isolated virtual environment.
#. Working Git checkouts of `TG2 Core`_, `TG2 Devtools`_, and `TG2 Docs`_.
#. The testing dependencies installed with the editable-install workflow in
   :doc:`prepenv`.
#. Familiarity with Git and the repository's current contribution workflow.

Package publishing requires maintainer permission for `PyPI`_. The release
process does not grant or describe permissions.

Release overview
================

A release normally requires these activities:

#. Review and validate the changes in the relevant repositories.
#. Prepare version metadata, changelogs, and release documentation.
#. Build and check the documentation and package distributions.
#. Have maintainers perform the repository merge, release tagging, and package
   or documentation publishing steps required by the project.
#. Complete the release announcement and post-release repository cleanup.

The exact branch promotion and publishing order is maintained by the project
maintainers. Do not infer a release branch or create release tags from this
page alone.

Review and prepare the repositories
===================================

Review the changes since the previous release in `TG2 Core`_, `TG2 Devtools`_,
and `TG2 Docs`_. Confirm that tests pass and that the documentation describes
the released behavior. Work on the current integration branch, normally
``development``, until maintainers give different release instructions.

Prepare changelog entries from the relevant commit history. This command gives
a starting point; review and edit the output rather than copying every commit::

    $ git log --no-merges --format="* %s" LAST_RELEASE_TAG..HEAD

Update each package's version metadata in its ``pyproject.toml`` and update
any corresponding release notes or dependency constraints required by the
maintainer-approved release plan. Use the packaging workflow configured by
``pyproject.toml`` for package operations.

Build and validate
==================

From the root of each Python package, install the package and its test
extra in editable mode, then run pytest::

    $ python -m pip install -e ".[testing]"
    $ python -m pytest

From the ``tg2docs`` repository root, build strict HTML documentation and check
external links::

    $ python -m sphinx -W --keep-going -b html docs docs/_build/html
    $ python -m sphinx -W --keep-going -b linkcheck docs docs/_build/linkcheck

Build source distributions and wheels with the packaging workflow configured
by each project's ``pyproject.toml``. Inspect the resulting distributions
before any maintainer publishes them.

Maintainer publishing steps
===========================

After review and validation, maintainers perform the project-specific steps to
merge approved release changes, create the release tag, publish package
distributions to `PyPI`_, and publish the corresponding documentation. These
steps depend on current project permissions and release infrastructure and are
not specified here.

Maintainers should also publish the approved release announcement, update the
relevant `GitHub`_ milestone or issue tracking, and complete any repository
cleanup required by the release plan.

Repository links
================

.. _GitHub: https://github.com/TurboGears/tg2/issues
.. _PyPI: https://pypi.org/
.. _TG2 Core: https://github.com/TurboGears/tg2
.. _TG2 Devtools: https://github.com/TurboGears/tg2devtools
.. _TG2 Docs: https://github.com/TurboGears/tg2docs
