.. _globaljslib:

Adding a JavaScript Library Include to Every Page
===============================================================

In TurboGears 1.0, you could easily drop MochiKit into every page.
You just added an entry to your .cfg file, and the script import
would appear.  In the past few years, a number of JavaScript libraries
have burst on the scene, and every developer has his or her
favorite.  For TG2, we decided to leave the JavaScript Library
choice up to you.

Luckily, TG has provided wrappers for all of the major JS libraries,
including:

    * JQuery
    * Dojo
    * Extjs
    * Yui
    * Mootools
    * and yes, Mochikit
  
The easiest way to take advantage of these ToscaWidget wrapper libraries is to
install them, and then inject the main JavaScript widget into the WSGI
environment for every page.  Let's see how we do this with Dojo.  First,
we need to install tw.dojo::
    
    easy_install tw.dojo
    
Then, we want to modify the base controller in our project so that it injects
the js file link on every page call. Open up the mytgapp/lib/base.py file. Add
the import for your selected JS app at the top of the file, in our case, this is
dojo_js::

   from tw.dojo import dojo_js
   
Next, modify the __call__ method of the BaseController.  Call the inject method
inside the __call__ method::

   dojo_js.inject()
   
You should now see a JavaScript link in your HTML::

<script type="text/javascript" src="/toscawidgets/resources/tw.dojo/static/1.3.2/min/dojo/dojo.js" djConfig="isDebug: false, parseOnLoad: true"></script>

That's pretty much it.  You have to figure out what library uses what name 
for thier js widgets, but most of them are fairly obvious.  The other alternative
is to put the file in your static directory, and add it directly to your master.html
template.