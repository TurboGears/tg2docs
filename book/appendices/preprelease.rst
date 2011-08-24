===================================
 Preparing a Release of TurboGears
===================================

Prerequisites
=============

 1. You have a working knowledge of how to use a `virtualenv`_.
 2. You have shell access to the `turbogears`_ site.
 3. You have permissions to update configuration and run builds on
    `Jenkins`_
 4. You know how to run the nosetests on your local git clones of
    TurboGears.
 5. You have to have a working knowledge of git, and how to do merging
    and branching.
 6. You need permission to update the TurboGears2 and tg.devtools
    packages on `PyPI`_

With those prerequisites in mind, this document will not cover all the
command lines that you could run. Instead, we will specify steps as
"activate your virtualenv" or "run nosetests" or the like.

Summary of Steps
================

Preparing a release of TurboGears is going to take some time and
effort. It is unlikely to be completed in a mere day or two, so please
plan on taking some time to work through it all.

The steps for the release, in summary, are as follows:

 1. Ticket System Triage
 2. Repository Branching
 3. Closing Remaining Tickets
 4. Upgrading All Local Packages As High As Possible
 5. Testing Jenkins With The Upgraded Packages And Code
 6. Finalizing Changes On 'next' Branch
 7. Preparing Changelog And Release Announcement
 8. Preparing Packages And The Documentation
 9. Uploading The Documentation
 10. Making The Source Distribution For The New Eggbasket
 11. Making The New Eggbasket The Current On Turbogears.org
 12. Pushing to `PyPI`_
 13. Publishing Release Annoucement And Closing Milestones
 14. Final Cleanup

Below, we discuss each of these steps in detail.

Ticket System Triage
====================

Open the ticket system on `SourceForge`_. Click "Edit Milestones", and
create the milestone that will be worked on *after* the milestone you
are now working on releasing. For example, if you are working on
release 2.1.1, you will create milestone 2.1.2. Also, make sure that
there exists a major milestone after the current one. For example, if
you are working on 2.1.1, make sure that 2.2.0 exists.

Next, you need to work your way through all of the open tickets on
`SourceForge`_ and determine where they belong. This really does mean
*all* open tickets. Tickets for the next major milestone could have
been resolved in the current milestone. Tickets in the current
milestone could be postponed to the next minor or major milestone. As
a result, *all* open tickets must be visited and verified for which
milestone they belong to. 

Once this process has been completed, it would be wise to post an
announcement to the `TG ML`_ and the `TG-Dev ML`_ informing people
that any new tickets should only be placed against the next milestone
(and what it is).

Repository Branching
====================

We have three main repositories: `TG2`_, `TG2Devtools`_, and
`TG2Docs`_. Each of them functions in a similar fashion for this
process:

 1. Clone the repository
 2. Checkout the development branch
 3. Branch development and make a "next" branch

Once the "next" branch is made, this is where you will do all work
until the release is done.

Closing Remaining Tickets
=========================

Working exclusively on the "next" branch in any of the relevant
repositories, close out any remaining open tickets for this
milestone. This particular step is likely to be the step that takes
the greatest amount of time. To make it worse, we can't give guidance
in this document on how to do this. Each ticket is different.

The one thing we can say is this: Make sure you are running your
tests. `Jenkins`_ will be watching any commits you push, and running
tests. Don't break him!

Upgrading all local packages as high as possible
================================================

This part is fairly involved. As you will be uploading the result onto
the `TurboGears`_ site, it is highly recommended that you have shell
access to it.

Preparing Your Environment
--------------------------

Create a new virtual environment, and get "basketweaver" and "yolk"
installed. You will need them both. They will be used later to find
the eggs that can be updated, download the .tar.gz files, and prepare
an eggbasket for public consumption.

Finally, you will need to make sure you have a copy of Python 2.4 and
Python 2.6 installed and ready to work.

Mirroring the Current Packages
------------------------------

In order to mirror the current version of the `eggbasket`_, the
easiest way is to use a command similar to this:

.. code-block:: bash

   user@host:~> rsync -avPL user@turbogears.org:/home/turbogearsorg/var/static/2.1/downloads/2.1/ ${HOME}/eggbasket/
   user@host:~> chmod -R 0755 ${HOME}/eggbasket

Change the version from 2.1 to whatever it needs to be to correspond
to the latest and greatest version of TurboGears.

Configuring to Install TurboGears from LocalHost
------------------------------------------------

In order to make the testing happen locally, you will need to make
some updates to your system's configuration. Edit your /etc/hosts file
(or %SYSTEMDIR%\etc\hosts.txt file on Windows), and add a reference
that points www.turbogears.org to your local machine.

After doing this, update your web server to tell it that the proper
path for the TurboGears files is your eggbasket. Assuming that your
eggbasket is being stored at /home/user/eggbasket, and you are using
Apache, a line similar to this (replacing the version as needed) in
your httpd.conf will do the trick:

.. code-block:: apache

   Alias /2.1/downloads/next /home/user/eggbasket

You are likely to need to restart your local webserver to make that
work properly.

Final Change to "next" branch
-----------------------------

For `TG2`_, `TG2DevTools`_, and `TG2Docs`_, you must make one change
in each of them: setup.py has a "dependency_links" attribute. Change
the word "current" to "next", and commit the change. Don't push the
change to the world yet, though. You're not ready for that just yet.

Make sure to change the template itself in
tg2devtools/devtools/templates/turbogears/setup.py_tmpl !

Installing Packages
-------------------

For both Python 2.4 and Python 2.6, create a new virtualenv and run
``python setup.py develop`` for each of the repositories.

Finding the Packages to Upgrade
-------------------------------

Using the following commands, you will get your environment prepared with all possible packages.

.. code-block:: bash

   user@host:~> cd ${HOME}/tg2
   user@host:~> python setup.py nosetests
   user@host:~> ls *.egg*

This will show you a complete list of the packages that were
downloaded but not placed into your site-packages directory. Since the
tool we use to scan for updated packages is only looking there, you
need to remove all the local .egg files (except for the TurboGears2
.egg), and then "easy_install" the eggs you removed. Do this until all
.egg files are replaced. Then, do the same for ${HOME}/tg2devtools .

Once done, the following commands should help you get new package
versions for all packages that have upgrades, and get ready to install
them. The following command will help you to upgrade all possible
packages.

.. code-block:: bash

   user@host:~> for pkg in `yolk -a -U | awk '{ print $1 }'` ; do echo Downloading ${pkg} ; yolk -F ${pkg}; done
   user@host:~> makeindex *

Complete the process, looking in the virtual environment's
site-packages directory. Use yolk to download any/all packages you
can, download the rest manually, and keep reiterating until yolk shows
nothing more than pip, distribute, and (optionally) virtualenvwrapper.

Testing the Upgraded Packages
-----------------------------

Once you complete the process to get all packages as upgraded as
possible, it's time to start the testing. This is likely to be very
easy. Make sure to test the installations with both Python 2.4 and
Python 2.6. Use ``python setup.py nosetests`` to run them.

Now, at any point, if a package will not work, you need to either find
a fix or revert to a previous version of that package. The choice must
be made on a case by case basis.

Testing Jenkins With The Upgraded Packages And Code
===================================================

Now that you have both Python 2.4 and Python 2.6 testing cleanly with
the next branch locally, it's time to take your eggbasket from your
machine, and place it on the `turbogears`_ server. A command similar
to this will help:

.. code-block:: bash

   rsync -avP ${HOME}/eggbasket/ user@turbogears.org:eggbasket/

Once done, you will need to make it visible to the world under the
downloads directory. Make sure that it matches the URL you placed in
setup.py. Also pay close attention to the permissions when you do so,
making sure that they are world-readable.

After doing this, visit `Jenkins`_ and update the build processes for
the tg-next packages. Ideally, they will become very simple. Even
still, verify all of the processes, and make sure that they work as
expected.

Once done, you can finally do ``git push`` on all of the
repositories. Run the actual builds for all of the tg-next packages,
and make sure they come out clean. If so, the real work is done
finally. The rest will only take you an hour or so. Otherwise,
determine the problem, fix it, update the build process, ``git push``
(if applicable), and re-run the builds until they do come out clean.

As you go through the configuration on `Jenkins`_, please remember
this one very important thing: We are looking to make the installation
process as easy as possible. Follow that guideline, so that we can
make the process easier for our users.

Finalizing Changes On 'next' Branch
===================================

After all the changes that you've made so far, the final changes are
simply to get the new version numbers into the distributed files.

 * In `TG2`_:
 
   * Update tg/release.py to have the new version number.
   * Update the dependency_links in setup.py to reference the
     "current" URL instead of "next" URL.
   
 * In `TG2Devtools`_:
 
   * Update setup.py:
   
     * Update the version number
     * Update the install requirements so that it requires TurboGears2
       >= the new version number
     * Update the dependency_links to reference the "current" URL
       instead of "next" URL.
       
   * Update devtools/templates/turbogears/setup.py_tmpl:
   
     * Update the dependency_links to reference the "current" URL
       instead of "next" URL.
     * Update the install requirements so that it requires TurboGears2
       >= the new version number

 * In `TG2Docs`_:
 
   * Update book/setup.py:

     * Update the version number
     * Update the dependency_links to reference the "current" URL
       instead of "next" URL.

Commit all of these changes, but do not push them public, not yet.

Preparing Changelog And Release Announcement
============================================

For each of the three repositories, you will need to review the commit
logs since the last release. Gather up the summaries for each one, and
prepare a new file. Use the standard `GNU Changelog`_ format. However,
instead of recording individual file changes, record only the
summaries. We don't need the file changes since Git records those
changes for us.

Review the `SourceForge`_ tickets for this milestone, and record any
tickets that were closed for this repository but were not referenced
in the summaries you've already recorded.

The changelog files you've made will be the commit message for the
tags you are about to make.

In addition, prepare a release announcement. Anything I can say here
sounds condescending. You should prepare it, though, so that as soon
as you reach the "Publish" step, it's all done in a few minutes.

Preparing Packages And The Documentation
========================================

First, merge the branch "next" onto the branch "master". Then, tag the
master branch with the new version number, and use the changelog
you've generated as the commit message. The tag should be an annotated
tag (i.e.: ``git tag -a"``).

Do this for each of the three repositories.

For the documentation, go into the appropriate directory, and type
``make html`` (either the docs or the book, whichever is needed to be
uploaded).

Uploading The Documentation
===========================

When you run ``make html``, it will create a directory
"_build/html". Upload the contents of that directory and replace the
current directory with it. For instance, if you used rsync to upload
to your user account on the server, and fixed the permissions so that
the website user could read the files, you could then do ``rsync -avP
--delete /path/to/new/docs /path/to/web/docs/directory`` and have
everything properly uploaded/visible to the users.

*Do not forget the book!* Enter the tg2docs/book folder, and run
 ``make html``. This will produce the necessary html files for the
 book. Upload the contents of the book/_build/html directory to the
 webserver. Use similar commands as were used for copying the older
 html docs to complete the process.

Making The Source Distribution For The New Eggbasket
====================================================

At this point, everything is prepared, with one exception: The source
distributions for TurboGears2 and tg.devtools must be placed in the
eggbasket. Enter your local repository directory for both ``TG2.x
Core`` and ``TG2.x DevTools`` and run ``python setup.py sdist``. In
both of them, you will produce a directory named ``dist`` with a
.tar.gz file for the new version. Copy these files to your
``${HOME}/eggbasket``, then go to ``${HOME}/eggbasket`` and run
``makeindex *``.

Using the steps in ``Testing Jenkins With The Upgraded Packages And
Code``, upload the updated (and finalized) eggbasket to the
turbogears.org web server.

Making The New Eggbasket The Current On Turbogears.org
======================================================

Log in to the `turbogears`_ website. Go into the directory where you
stored the "next" directory, and rename "next" to the version you are
releasing. Remove the "current" link, and then do a symbolic link from
the version being released to "current", like so: ``ln -s 2.1.1
current``

Pushing to `PyPI`_
==================

For all three repositories, do ``python setup.py upload``.

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

.. _eggbasket: http://www.turbogears.org/2.1/downloads/current/
.. _turbogears: http://www.turbogears.org/
.. _Jenkins: http://jenkins.turbogears.org/
.. _PyPI: http://pypi.python.org/
.. _SourceForge: https://sourceforge.net/p/turbogears2/tickets/
.. _TG2: https://sourceforge.net/p/turbogears2/tg2/
.. _TG2Devtools: https://sourceforge.net/p/turbogears2/tg2devtools/
.. _TG2Docs: https://sourceforge.net/p/turbogears2/tg2docs/
.. _TG ML: http://groups.google.com/group/turbogears
.. _TG-Dev ML: http://groups.google.com/group/turbogears-trunk
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _GNU Changelog: http://www.gnu.org/prep/standards/html_node/Change-Logs.html
