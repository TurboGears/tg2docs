.. _recipes-and-faq:

=======================
Working with TurboGears
=======================

This page collects documentation which describes how to work with 
TurboGears to accomplish an effect.  Normally you should have completed 
a few :ref:`tutorials` so that you have a feel for the general workflow 
within TurboGears before you dive into these documents.

.. toctree::
    :maxdepth: 1
    
    main/Auth/index
    main/Validation
    main/StaticFile
    main/Controllers
    main/Templates/Genshi
    main/master_html
    main/ToscaWidgets/ToscaWidgets
    main/RestControllers
    main/Extensions/Crud/index
    main/Extensions/Admin/index
    main/DatabaseMigration
    main/MultipleDatabases
    main/Caching
    main/Config
    main/LogSetup
    main/Internationalization
    main/Session
    main/ResponseTypes
    main/RoutesIntegration
    main/RequestFlow
    main/CommandLine

.. todo:: Document initial DB setup in websetup.py
.. todo:: Difficulty Easy: Cron/periodic/stand-alone tasks using the TurboGears machinery (basically can be copied from: http://blog.vrplumber.com/index.php?/archives/2384-TurboGears-offline-processes-crons,-command-line-commands,-etc.html )
   
Extensions and Alternatives
===========================

TurboGears is a remarkably flexible framework that allows you to swap in 
new implementations for many of the pieces used by default.  Templating 
engines, Javascript libraries, authorization mechanisms, data-storage 
abstractions and the like can all be plugged in to suit your development 
methods.

.. toctree::
    :maxdepth: 1
    
    main/Templates/index
    main/Templates/Mako
    main/Templates/Jinja
    main/Templates/ChameleonGenshi
    main/Wiki20/JSONMochiKit
    main/ToscaWidgets/Cookbook/FlexiGrid
    main/ToscaWidgets/Cookbook/TreeView
    main/TGandPyAMF
    main/TGandFirePython
    main/AuthorizeTutorial
    main/Extensions/Geo/index

.. todo:: JQuery, Dojo, EXT usage doc-links

Installation and Deployment
===========================

.. toctree::
    :maxdepth: 2

    main/Deployment
    main/Deployment/DeployWithAnEgg
    main/Deployment/ModProxy
    main/Deployment/modwsgi+virtualenv


Performance and optimization:
===============================

.. toctree::
    :maxdepth: 2
   
    main/Profile
    main/Performance/TemplatePerformance
    main/Caching

.. todo:: Difficulty: Medium. optimization tips for SQLAlchemy usage

.. todo:: Difficulty: Easy. Validate that toctree maxdepth values are appropriate

.. todo:: Difficulty: Medium. Rearrange headers, condensing as appropriate

