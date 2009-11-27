.. _FastCGI:

FastCGI/WSGI -- Running TG2 behind Apache 
========================================= 
 
:status: Draft 
 
Under many conditions, native support for Python in the form of mod_wsgi 
or mod_python will not be available.  Furthermore, you will not be able to 
run CherryPy as a webserver, since your webhost insists that everything pass 
through port 80... which is being served by Apache.  Because TurboGears 
implements the WSGIServer interface, we can use flup to interface between 
FastCGI and CherryPy.  We'll also show you how to use virtualenv in this 
setup. 
 
This document is closely analogous to _Pylon's instructions for CGI: 
http://wiki.pylonshq.com/display/pylonscookbook/Production+Deployment+Using+Apache,+FastCGI+and+mod_rewrite 
but have a number of key differences. 
 
 
Apache configuration 
-------------------- 
 
Discussing what Apache directives should be set is beyond the scope of this 
document, but `mod_fastcgi` and `mod_rewrite` should be enabled.  Most webhosts 
have the latter enabled by default; some require you to explicitly enable 
FastCGI via their control panel (Dreamhost is one such host). 
 
 
Installation 
------------ 
 
If you setup your own virtualenv according to the instructions on the 
installation page, you will need to install flup, with:: 
 
    $ setuptools -i flup 
 
If you are not using virtualenv, check to see if flup is installed or not 
with `import flup`. 
 
 
Dispatch scripts 
---------------- 
 
Keeping your TurboGears install in a web-accessible directory is strictly 
unnecessary; the only files we will need to add to forward FastCGI are 
`dispatch.fcgi` and an `.htaccess` file. 
 
dispatch.fcgi 
~~~~~~~~~~~~~ 
 
In the `dispatch.fcgi` file, you will need the following boilerplate code:: 
 
    #!/usr/bin/env python 
    turbogears = '/path/to/turbogears' 
    inifile = 'development.ini' 
    import sys, os 
    sys.path.insert(0, turbogears) 
    from paste.deploy import loadapp 
    wsgi_app = loadapp('config:' + turbogears + '/' + inifile 
    if __name__ == '__main__': 
        from flup.server.fcgi import WSGIServer 
        WSGIServer(wsgi_app).run() 
 
There are three locations in this file that you may need to edit: 
 
1. The `turbogears` variable should be set to the location of your 
   TurboGears codebase, i.e. where you can find such files as `development.ini` 
   and `setup.py` 
 
2. The `inifile` variable should be set to the name of the configuration file 
   you would like to be loaded on this server. 
 
3. The shebang line (`#!/usr/bin/env python`) should be modified to use 
   the virtualenv Python interpreter, if you are using such an environment. 
 
This loader file is different from the Pylons flup file, please be careful! 
Also, you need to make this file executable, with:: 
 
    $ chmod 0755 dispatch.fcgi 
 
.htaccess 
~~~~~~~~~ 
 
You will need to add the following lines to your `.htaccess` file:: 
 
    Options +ExecCGI 
    AddHandler fastcgi-script .fcgi 
    RewriteEngine On 
    RewriteRule   ^(dispatch\.fcgi/.*)$  - [L] 
    RewriteRule   ^(.*)$  dispatch.fcgi/$1 [L] 
 
You can also setup static content with an extra RewriteRule before the 
last line: 
 
    RewriteRule   ^(static/.*)$ - [L] 
 
The first two lines (Options and AddHandler) are not strictly necessary, 
depending on your webserver's configuration. 
 
Pylons tweaking 
~~~~~~~~~~~~~~~ 
 
Using this method, Turbogears/Pylons wrongly thinks that dispatch.fcgi 
is a part of the URL. One fix for this known to work is to add this 
Middleware (see config/middleware.py) to your install:: 
 
    class FastCGIFixMiddleware(object): 
        """Remove dispatch.fcgi from the SCRIPT_NAME 
         
        mod_rewrite doesn't do a perfect job of hiding it's actions to the 
        underlying script, which causes TurboGears to get confused and tack 
        on dispatch.fcgi when it really shouldn't. This fixes that problem as a 
        Middleware that fiddles with the appropriate environment variable 
        before any processing takes place. 
        """ 
        def __init__(self, app, global_conf=None): 
            self.app = app 
        def __call__(self, environ, start_response): 
            environ['SCRIPT_NAME'] = environ['SCRIPT_NAME'].replace('/dispatch.fcgi', '') 
            return self.app(environ, start_response) 
 
And then, below, in `make_app()`:: 
 
    app = FastCGIFixMiddleware(app, global_conf) 
 
Maintenance 
----------- 
 
Checking if it worked 
~~~~~~~~~~~~~~~~~~~~~ 
 
The most obvious metric for success is whether or not your site displays 
on your browser. However, you can also check with `ps aux | grep dispatch` 
to see if your FastCGI executable is still running. 
 
Rebooting 
~~~~~~~~~ 
 
Because FastCGI processes are persistent, even when you update your Python 
files the old code will still be running.  Usually, the following command 
from your shell will be sufficient to kill the process:: 
 
    $ killall -u username dispatch.fcgi 
 
If dispatch.fcgi is running as the Apache user, i.e. www-data, you'll need 
to create a short Python stub script to call from the web in order to execute 
this command. (Also, your host is doing it wrong.) 
 
Debugging 
~~~~~~~~~ 
 
FastCGI is notoriously difficult to debug. There are variants of dispatch.fcgi 
which add lots of informative debugging output; you can also rename the file 
to dispatch.cgi and run as a CGI module (it will not be as fast, but will be 
reloaded every request). 
 