.. _recipes-and-faq:

=======================
Working with TurboGears
=======================

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
    main/ToscaWidgets/ToscaWidgets
    main/Config
    main/LogSetup
    main/StaticFile
    main/Internationalization

.. todo:: document for Genshi should be how-to, not "why"
.. todo:: link repoze.who, repoze.what, and the other key middleware

Modelling Your Application
--------------------------

SQLAlchemy is the default data-storage layer for TurboGears 2.x.
The SQLAlchemy-migrate project is the officially supported mechanism
for updating and migrating your database.

..  toctree::
    :maxdepth: 1
   
    main/SQLAlchemy
    main/Config/SQLAlchemy
    main/DatabaseMigration
    
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
    main/ToscaWidgets/ToscaWidgets
    main/ToscaWidgets/forms
    main/Pagination/index
    
    main/Auth/index
    modules/thirdparty/webob
    modules/tgflash
    modules/tgdecorators
    
    main/ResponseTypes
    main/RequestFlow    

    main/Caching
    main/RoutesIntegration
    
Automatic Forms/Controllers
---------------------------

The TurboGears Admin system is built on top of the Sprox and tg.ext.crud
system.  You can use the same automatically generated forms and
controllers to help you quickly prototype your applications.  The 
:ref:`Movie Tutorial <movie-tutorial>` introduces this usage of 
Sprox.

..  toctree::
    :maxdepth: 1
    
    main/RestControllers
    main/Extensions/Crud/index
    main/Extensions/Admin/index

.. todo:: Difficulty easy: link sprox here

Templates/Views
---------------

By default your TurboGears 2.x project will be configured to use the 
:ref:`Genshi <genshi>` templating language.  TurboGears allows for the
use of alternate templating languages.  

Note: most new users do not need to choose an alternate templating language.

..  toctree::
    :maxdepth: 1

    main/Templates/Genshi
    main/master_html
    main/Templates/index
    main/Templates/ChameleonGenshi
    main/Templates/Mako
    main/Templates/Jinja
    main/ToscaWidgets/Cookbook/ReCaptcha.html

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
    main/ToscaWidgets/Cookbook
    main/ToscaWidgets/Cookbook/FlexiGrid
    main/ToscaWidgets/Cookbook/TreeView
    main/ToscaWidgets/Cookbook/Flot
    main/ToscaWidgets/Cookbook/JQueryTreeView
    main/ToscaWidgets/Cookbook/JQueryAjaxForm
    main/Wiki20/JSONMochiKit
    main/StaticFile

.. todo:: JQuery, Dojo, EXT usage doc-links
.. todo:: Link documentation for doing JSON RPC/Ajax here

Installation and Deployment
===========================

..  toctree::
    :maxdepth: 2

    main/DownloadInstall
    main/Deployment
    main/Deployment/DeployWithAnEgg
    main/Deployment/ModProxy
    main/Deployment/modwsgi+virtualenv

.. todo:: Difficulty Medium: document how to "freeze" applications (PIP, zc.buildout, etceteras) for re-deployment with precisely the same software on each machine (no downloads etceteras)

Tools
=====

..  toctree::
    :maxdepth: 1

    main/Profile
    main/ToolBox 
    main/CommandLine
    main/Config
    main/LogSetup

.. todo: Difficulty Easy: document Debugging
    
Special Effects and Extensions
==============================

..  toctree::
    :maxdepth: 1

    main/MultipleDatabases
    main/TGandPyAMF
    main/TGandFirePython
    main/AuthorizeTutorial
    main/Extensions/Geo/index

.. todo:: Difficulty Easy: Cron/periodic/stand-alone tasks using the TurboGears machinery (basically can be copied from: http://blog.vrplumber.com/index.php?/archives/2384-TurboGears-offline-processes-crons,-command-line-commands,-etc.html )
    
Performance and optimization:
===============================

.. toctree::
    :maxdepth: 1
   
    main/Profile
    main/Performance/TemplatePerformance
    main/Caching

.. todo:: Difficulty: Medium. optimization tips for SQLAlchemy usage

.. todo:: Difficulty: Easy. Validate that toctree maxdepth values are appropriate

Next Steps
----------

 * :ref:`getting-to-know` -- learn how TurboGears 2.x works, changes since the 1.x release, and how to contribute to the project
