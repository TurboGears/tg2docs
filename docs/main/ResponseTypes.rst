Content Types and Request Extensions
========================================

Content Types and Request Extensions are supported by both :class:`tg.controllers.TGController` and :class:`tg.controllers.RestController`.
Request extensions allow the user to provide a specifier at the end of their data stream which specifies how
they would like their data retrieved, using a dot operator.  

A simple Json Example
-------------------------
TurboGears Controllers gives the developer the ability to attach a mime-type to their methods to express
data in using different protocols.  The most common usage for this is with json, a standard protocol used
for Asynchronous JavaScript.  Consider the following code snippet::

    users = "sally", "dave", "john"

    class Forum(TGController):

        @expose('json')
        def users(self):
            return {'users':users}

This allows you to map a URL like /forum/users.json
            
            
Cascading exposes to provide Web Services
-------------------------------------------
Sometimes you want a controller to return content based on the extension provided by the user, or the
lack-there-of.  You can cascade multiple expose decorators to accomplish this.  Consider this example:
you have a page which lists the user in a table which is generated using JavaScript.  JS makes an asynchronous
call to your web application to fill the data.  It makes sense to fetch the data for the Json call, but
not for the rendering of the HTML template used to render the data.  Here is the users example again which
expresses this use case::

    users = "sally", "dave", "john"

    class Forum(TGController):

        @expose(myproject.templates.forum.users)
        @expose('json')
        def users(self):
            if pylons.request.response_type == 'application/json':
                return {'users':users}
            return {}

The users method will service both /forum/users/ and /forum/users.json.  Simply provide the JavaScript
code with a link to users.json and you are good to go.  This makes providing your users with RESTful
URLs much simpler.  You could imagine using this capability to expose your application's resources 
for SOAP, or XML-RPC.


Application-Specific Mime-type Configuration
-------------------------------------------------
By default, only json/application and text/html are defined mimetypes.  If you would like to use additional mime-types you must
register them with your application's config.  You can accomplish this by adding the following code your your app_cfg.py file::

    base_config.mimetype_lookup = {'.ext':'my-mimetype'}


Custom Content Types
----------------------
Setting the Content-Type for your return data is often used to tell the web browser how to display that data to the user.
For instance, if you want the browser to open an Excel file as such, you need to tell the browser that the data coming back
is in Excel format.  Sometimes we want to set the content-type for our response within the controller method.  
By providing the @expose decorator with a "CUSTOM_CONTENT_TYPE" indicator we are able to accomplish this.  
Here is an example of how to return a simple .csv file that the browser will treat as an attachment::


    from tg import request, response
    from tg.controllers import CUSTOM_CONTENT_TYPE
 
    class MyController:
        @expose(content_type=CUSTOM_CONTENT_TYPE)
        def stats(self):
            response.content_type = 'text/csv'
            response.headerlist.append(('Content-Disposition','attachment;filename=stats.csv'))
            return '1,2,3'

.. todo:: Review this file for todo items.

