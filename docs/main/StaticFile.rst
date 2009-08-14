
Serving Static Files (Css, Javascript, Images, etc.)
====================================================


Place any static files in the 'public' folder.  Files there will be
served up just as they would in a "normal" web server. You might want
to consider putting all static files in a static directory, so that
you can use apache/nginx to serve up these static files for you when
you go into production, or later when your traffic requires it.


Getting Rid Of The Static File Middleware
-----------------------------------------

If your app is running in production, and Apache or another web server
is handling this static content, edit config/middleware.py and
remove::

  javascripts_app = StaticJavascripts()
  static_app = StaticURLParser(config['pylons.paths']['static_files'])
  app = Cascade([static_app, javascripts_app, app])

Reference
---------

Upload File
 
 * http://wiki.pylonshq.com/display/pylonscookbook/Hacking+Pylons+for+handling+large+file+upload
 * http://kelpi.com/script/06fff7
