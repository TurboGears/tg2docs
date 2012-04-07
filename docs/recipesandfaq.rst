.. _recipes-and-faq:

================
Tips and Recipes
================

This page collects documentation which describes how to work with
TurboGears to accomplish an effect.  Normally you should have completed
a few :ref:`tutorials` so that you have a feel for the general workflow
within TurboGears before you dive into these documents.

Core: Read These Pages!
=======================

These pages are the most useful pages for a new TurboGears developer
to read after going through the tutorials. Reading the material
here will help make you a more productive developer with TurboGears.

We cannot stress this enough: Read These Pages!

..  toctree::
    :maxdepth: 1

    main/Auth/index
    main/Validation
    main/Controllers
    main/Templates/Genshi
    main/Config
    main/LogSetup
    main/Internationalization

.. todo:: link repoze.who, repoze.what, and the other key middleware

Modeling Your Application
--------------------------

SQLAlchemy is the default data-storage layer for TurboGears |version|.
Ming is supported as the alternative storage layer for MongoDB.
The SQLAlchemy-migrate project is the officially supported mechanism
for updating and migrating your database.

..  toctree::
    :maxdepth: 1

    main/SQLAlchemy
    main/DatabaseMigration
    main/Config/MasterSlave
    main/Ming
    main/Config/SQLAlchemy
    main/MultipleDatabases

.. todo:: Document initial DB setup in websetup.py
.. todo:: Link DB setup (MySQL, PostgreSQL, etceteras) docs
.. todo:: document the transaction module, part of the repoze.tm package, introduction for implementers here... http://repoze.org/tmdemo.html

Handling HTTP Requests (Controllers)
------------------------------------

..  toctree::
    :maxdepth: 1

    main/Controllers
    main/Session
    main/Validation
    main/FormBasics
    main/Pagination/index

    main/Auth/index
    main/Auth/OpenID
    modules/thirdparty/webob
    modules/tgflash
    modules/tgdecorators

    main/ResponseTypes
    main/RequestFlow

    main/Caching
    main/RoutesIntegration

    modules/thirdparty/webhelpers_feedgenerator

.. todo:: Document "community" sites; user-signup mechanisms (e.g. tgext.registration2), OpenID,
   Recaptcha, etceteras as sub-section

Automatic Forms/Controllers
---------------------------

The TurboGears Admin system is built on top of the Sprox and tgext.crud
system.  You can use the same automatically generated forms and
controllers to help you quickly prototype your applications.  The
:ref:`Movie Tutorial <movie-tutorial>` introduces this usage of
`Sprox`_.

..  toctree::
    :maxdepth: 1

    main/RestControllers
    main/Extensions/Crud/index
    main/Extensions/Admin/index

.. _`Sprox`: http://www.sprox.org

Templates/Views
---------------

By default your TurboGears |version| project will be configured to use the
:ref:`Genshi <genshi>` templating language.  TurboGears allows for the
use of alternate templating languages.

Note: most new users do not need to choose an alternate templating language.

..  toctree::
    :maxdepth: 1

    main/Templates/Genshi
    main/Templates/index
    main/Templates/Mako
    main/Templates/Jinja

Javascript Libraries
--------------------

Modern web-sites are dynamic, flexible, Javascript-code-heavy pieces
of software.  You will almost certainly want to use one of the major
Javascript libraries to make the process of creating your sites less
painful.  The ToscaWidgets package provides plug-ins for each of the
three major libraries, JQuery, Dojo and Ext, as well as the older
Mochikit package which was the default in TurboGears 1.x.

..  toctree::
    :maxdepth: 1

    main/GlobalJSLib

.. todo:: JQuery, Dojo, EXT usage doc-links
.. todo:: Link documentation for doing JSON RPC/Ajax here

Old Recipes
----------------------

..  toctree::
    :maxdepth: 1

    deprecated/master_html
    deprecated/ToscaWidgets/ToscaWidgets
    deprecated/ToscaWidgets/forms
    deprecated/ToscaWidgets/Cookbook
    deprecated/ToscaWidgets/Cookbook/ReCaptcha
    deprecated/ToscaWidgets/Cookbook/FlexiGrid
    deprecated/ToscaWidgets/Cookbook/Flot
    deprecated/ToscaWidgets/Cookbook/JQueryTreeView
    deprecated/ToscaWidgets/Cookbook/JQueryAjaxForm
    deprecated/Wiki20/JSONMochiKit


Testing
=======

..  toctree::
    :maxdepth: 2

    main/Testing/index


Installation and Deployment
===========================

..  toctree::
    :maxdepth: 2

    main/DownloadInstall
    main/AltInstall
    main/Deployment/index

.. todo:: Difficulty Medium: document how to "freeze" applications (PIP, zc.buildout, etceteras) for re-deployment with precisely the same software on each machine (no downloads etceteras)
.. todo:: document use of Nginx beyond just saying you can do it
.. todo:: (maybe) document use of Twisted WSGI wrapper?

Tools
=====

..  toctree::
    :maxdepth: 1

    main/Profile
    main/ToolBox
    main/CommandLine
    main/Config
    main/LogSetup
    main/CLIScript
    main/Extensions/Scheduling

.. todo: Difficulty Easy: document Debugging

Special Effects and Extensions
==============================

..  toctree::
    :maxdepth: 1

    main/TGandPyAMF
    main/TGandFirePython
    main/AuthorizeTutorial
    main/Extensions/Geo/index

.. todo:: Document use of `Ming`_ and `MongoDB`_ with TurboGears

.. _`Ming`: http://merciless.sourceforge.net/
.. _`MongoDB`: http://www.mongodb.org/

Real-time Web
-------------

.. toctree::
    :maxdepth: 1

    main/Realtime/index
    main/Realtime/moksha

Performance and optimization
============================

.. toctree::
    :maxdepth: 1

    main/Profile
    main/Performance/TemplatePerformance
    main/Caching

.. todo:: Difficulty: Medium. optimization tips for SQLAlchemy usage

.. todo:: Difficulty: Easy. Validate that toctree maxdepth values are appropriate

.. todo:: Difficulty: Easy. Explain usage of tgscheduler and how to use SQLAlchemy in a task

Next Steps
----------

* :ref:`getting-to-know` -- learn how TurboGears |version| works, changes since the 1.x release, and how to contribute to the project
