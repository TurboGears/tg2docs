===================================
 Preparing a Release of TurboGears
===================================

Preparing a release of TurboGears is going to take some time and
effort. It is unlikely to be completed in a mere day or two, so please
plan on taking some time to work through it all.

The steps for the release, in summary, are as follows:

 1. Ticket system triage
 2. Repository branching
 3. Closing remaining tickets
 4. Upgrading all local packages as high as possible
 5. Testing Jenkins with the upgraded packages and code
 6. Preparing changelog and release announcement
 7. Finalizing and merging branches
 8. Pushing to `PyPI`_
 9. Publishing release annoucement and closing milestones

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

.. _Jenkins: http://jenkins.turbogears.org/
.. _PyPI: http://pypi.python.org/
.. _SourceForge: https://sourceforge.net/p/turbogears2/tickets/
.. _TG2: https://sourceforge.net/p/turbogears2/tg2/
.. _TG2Devtools: https://sourceforge.net/p/turbogears2/tg2devtools/
.. _TG2Docs: https://sourceforge.net/p/turbogears2/tg2docs/
.. _TG ML: http://groups.google.com/group/turbogears
.. _TG-Dev ML: http://groups.google.com/group/turbogears-trunk
