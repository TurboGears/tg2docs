=========================================
 Building Applications with TurboGears 2
=========================================

.. note:: This page is filled with notes about what each chapter should become. As the chapter gets filled in with a proper document, the notes will be removed, leaving only the clean table of contents. Until then, the notes are left in for future reference.

#########
 Preface
#########

* :doc:`preface/history`
* :doc:`preface/prereqs`

.. toctree::
   :hidden:
   :glob:

   preface/history
   preface/prereqs

###################
Part I - The Basics
###################

* :doc:`part1/wiki20`
* :doc:`part1/install`
* :doc:`part1/hiringpond`

.. toctree::
   :hidden:

   part1/wiki20
   part1/install
   part1/hiringpond

##########################
Part II - Making A Web App
##########################

* Configuring TurboGears - Where the main configuration files are, and what their values mean
* Initial Project Layout - What the developer gets from the quickstarted project
* Using SQL Alchemy - How to perform basic operations with your data model, and how to specify it
* Writing The Unit Tests - To show how to build in testing, so as to establish good habits for the rest of the book
* Alternate Authentication Mechanisms - Writing a plugin that handles authenticating in a different way than is expected by default TG2
* Using Sprox - Completing the basic application
* Using ToscaWidgets - When you need lower level tools than Sprox can provide
* AJAX - Making the web application feel more like an application, rather than a set of web pages
* Command Line Tools - Adding command line tools to perform specific behind the scenes tasks (such as cron jobs)
* Content Types and Web Services - Returning items other than HTML, providing pages to other web servers for their own consumption, rather than a browser

#############################
Part III - Deployment Methods
#############################

* Build the Installation Egg - How to package the specific app
* Build a local PyPI - How to make a local installation source to allow easy installation of the exact same app version later on a different machine
* Apache

  * mod_wsgi
  * CGI
  * mod_proxy
  
* Lighttpd web server
* NGINX web server
* Maintaining the application - Things to do to make sure the app stays up to date easily

#####################################
Part IV - Alternatives and Extensions
#####################################

* Alternate Templating Systems

  * Mako
  * Jinja2
  * Kajiki
  
* Storage Alternatives

  * MongoDB
  * Cassandra
  
* Building TurboGears extensions, complete with a small sample
* Extensive ToscaWidgets Guide

##########
Appendices
##########

* :doc:`appendices/commandline`
* Multiple Domains Served by Single TG2 Application Instance
* Testing and Debugging TG2 Applications
* External Tutorials
* Contributing

  * :doc:`appendices/contributing/prepenv`
  * :doc:`appendices/contributing/testingchanges`
  
* Maintainer's Guide

  * :doc:`appendices/preprelease`
  
.. toctree::
   :hidden:
   :glob:

   appendices/commandline
   appendices/contributing/prepenv
   appendices/contributing/testingchanges
   appendices/preprelease
   appendices/modules/*
   appendices/todo
   
* :doc:`appendices/todo`
* :ref:`Alphabetical Module Index <modindex>`
* :ref:`Index <genindex>`

   
