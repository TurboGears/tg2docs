===================================
 Preparing a Release of TurboGears
===================================

Prerequisites
=============

 1. You have a working knowledge of how to use a `virtualenv`_.
 2. You have shell access to the `turbogears`_ site.
 3. You know how to run the ``nosetests`` on your local git clones of TurboGears.
 4. You have to have a working knowledge of git, and how to do merging and branching.
 5. You need permission to update the TurboGears2 and tg.devtools packages on `PyPI`_

With those prerequisites in mind, this document will not cover all the
command lines that you could run. Instead, we will specify steps as
"activate your virtualenv" or "run nosetests" or the like.

Summary of Steps
================

Preparing a release of TurboGears is going to take some time and
effort. It is unlikely to be completed in a mere day or two, so please
plan on taking some time to work through it all.

The steps for the release, in summary, are as follows:

 1. Repository Branching
 2. Finalizing Changes On 'next' Branch
 3. Preparing Changelog And Release Announcement
 4. Preparing Packages And The Documentation
 5. Uploading The Documentation
 6. Pushing to `PyPI`_
 7. Publishing Release Annoucement And Closing Milestones
 8. Final Cleanup

Below, we discuss each of these steps in detail.

Repository Branching
====================

We have three main repositories: `TG2`_, `TG2Devtools`_, and
`TG2Docs`_. Each of them functions in a similar fashion for this
process:

 1. Clone the repository
 2. Checkout the "development" branch and update it
 3. Checkout the "next" branch and merge development into it

Once the "next" branch is made, this is where you will do all work
until the release is done.

Finalizing Changes On 'next' Branch
===================================

After all the changes that you've made so far, the final changes are
simply to get the new version numbers into the distributed files.

 * In `TG2`_:
 
   * Update ``tg/release.py`` to have the new version number.
   * Update CHANGES.txt:

     * Add new release with changelog generate with:
       ``git log --no-merges --format="* %s" LAS_RELEASE_TAG..HEAD``
       (LAST_RELEASE_TAG is the tag of the previous release, like tg2.3.2).
       Please take only meaningful changes.
   
 * In `TG2Devtools`_:
 
   * Update setup.py:
   
     * Update the version number
     * Update the install requirements so that it requires TurboGears2
       >= the new version number
       
   * Update ``devtools/templates/turbogears/setup.py_tmpl`` and
     ``devtools/gearbox/tgext/template/setup.py_tmpl``:
   
     * Update the install requirements so that it requires TurboGears2
       >= the new version number

 * In `TG2Docs`_:

   * Update requirements.txt:

     * Change TurboGears dependency line from ``@development`` to
       current release (EX: ``@tg2.3.2``).

   * Update docs/confg.py:

     * Update the version number


Commit all of these changes, but do not push them public, not yet.

Preparing Changelog And Release Announcement
============================================

For each of the three repositories, you will need to review the commit
logs since the last release. Gather up the summaries for each one, and
prepare a new file. Use the standard `GNU Changelog`_ format. However,
instead of recording individual file changes, record only the
summaries. We don't need the file changes since Git records those
changes for us.

Review the `GitHub`_ tickets for this milestone, and record any
tickets that were closed for this repository but were not referenced
in the summaries you've already recorded.

The changelog files you've made will be the commit message for the
tags you are about to make.

In addition, prepare a release announcement. Anything I can say here
sounds condescending. You should prepare it, though, so that as soon
as you reach the "Publish" step, it's all done in a few minutes.

Preparing Packages And The Documentation
========================================

First, merge the branch "next" onto the branch "master". Then, **tag the
master branch** with the new version number, and use the changelog
you've generated as the commit message. The tag should be an annotated
tag (i.e.: ``git tag -a"``).

Do this for each of the three repositories.

Pushing master branch of documentation will automatically trigger a new
documentation build in ``readthedocs.org``.

Making The Source Distribution to `PyPI`_
=========================================

At this point, everything is prepared, with one exception: The source
distributions for TurboGears2 and tg.devtools must be placed in the
eggbasket. Enter your local repository directory for both ``TG2.x
Core`` and ``TG2.x DevTools`` and run ``python setup.py sdist upload``.

Publishing Release Annoucement And Closing Milestones
=====================================================

Publish your release announcement to the places of your choice. We
recommend your blog(s) and twitter. In addition, update the
`turbogears`_ "Current Status" page to reflect the new release.

Final Cleanup
=============

For each of the three repositories, merge the "master" branch to the
"development" branch.

You're done. Sit back and enjoy having accomplished a release.

.. _GitHub: https://github.com/TurboGears/tg2/issues
.. _eggbasket: http://www.turbogears.org/2.1/downloads/current/
.. _turbogears: http://www.turbogears.org/
.. _Jenkins: http://jenkins.turbogears.org/
.. _PyPI: http://pypi.python.org/
.. _SourceForge: https://sourceforge.net/p/turbogears2/tickets/
.. _TG2: https://github.com/TurboGears/tg2
.. _TG2Devtools: https://github.com/TurboGears/tg2devtools
.. _TG2Docs: https://github.com/TurboGears/tg2docs
.. _TG ML: http://groups.google.com/group/turbogears
.. _TG-Dev ML: http://groups.google.com/group/turbogears-trunk
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _GNU Changelog: http://www.gnu.org/prep/standards/html_node/Change-Logs.html
