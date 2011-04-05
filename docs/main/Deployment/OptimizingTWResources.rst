.. _optimize-twresources:

Optimizing Toscawidgets Resources
=====================================

Toscawidgets uses a lot of static files for its widgets. 
Having those files served by the middleware is quite inefficient and doesn't usually provide 
any extra feature, so it is usually a good idea to let a web server directly serve them.

Extracting static files
------------------------

People at Toscawidgets know this and have been so kind to provide a way to extract all the
static files needed by the widgets that your application is currently using and since
Turbogears 2.1.1 this command is directly exposed when you ``quickstart`` a new application.

Static resources can be extracted by using::

    python setup.py archive_tw_resources

By default the static files will be extracted to your project ``public`` directory, and if you
had properly configured your web server or are using a proxy server you should end up
having your public directory directly served by you webserver instead of passing through 
toscawidgets middleware.

Compressing static files
-------------------------

By default turbogears won't compress your static files, it will just extract them.
This is because static files compression requires a working java environment and the
YUICompressor tool.

If you want to enable extracted files compression you just have to modify your ``setup.cfg``
by uncommenting those two lines::

	#yuicompressor = /home/someuser/bin/yuicompressor.jar
	#compresslevel = 2

The first one must point to your YUICompressor executable and the second one can be used
to specify the compression level.
