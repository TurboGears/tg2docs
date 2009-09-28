Content Types and Request Extensions
====================================

Content Types and Request Extensions are supported by both
:class:`tg.controllers.TGController` and
:class:`tg.controllers.RestController`.  Request extensions allow the
user to provide a specifier at the end of their data stream which
specifies how they would like their data retrieved, using a dot
operator.

A Simple Json Example
---------------------

TurboGears Controllers gives the developer the ability to attach a
mime-type to their methods to express data in using different
protocols.  The most common usage for this is with json, a standard
protocol used for Asynchronous JavaScript.  Consider the following
code snippet::

    users = "sally", "dave", "john"

    class Forum(TGController):

        @expose('json')
        def users(self):
            return {'users':users}

This allows you to map a URL like /forum/users.json
            
            
Cascading Exposes To Provide Web Services
-----------------------------------------

Sometimes you want a controller to return content based on the
extension provided by the user, or the lack-there-of.  You can cascade
multiple expose decorators to accomplish this.  Consider this example:
you have a page which lists the user in a table which is generated
using JavaScript.  JS makes an asynchronous call to your web
application to fill the data.  It makes sense to fetch the data for
the Json call, but not for the rendering of the HTML template used to
render the data.  Here is the users example again which expresses this
use case::

    users = "sally", "dave", "john"

    class Forum(TGController):

        @expose(myproject.templates.forum.users)
        @expose('json')
        def users(self):
            if pylons.request.response_type == 'application/json':
                return {'users':users}
            return {}

The users method will service both /forum/users/ and
/forum/users.json.  Simply provide the JavaScript code with a link to
users.json and you are good to go.  This makes providing your users
with RESTful URLs much simpler.  You could imagine using this
capability to expose your application's resources for SOAP, or
XML-RPC.


Application-Specific Mime-type Configuration
--------------------------------------------

By default, only json/application and text/html are defined mimetypes.
If you would like to use additional mime-types you must register them
with your application's config.  You can accomplish this by adding the
following code your your app_cfg.py file::

    base_config.mimetype_lookup = {'.ext':'my-mimetype'}


Custom Content Types
--------------------

Setting the Content-Type for your return data is often used to tell
the web browser how to display that data to the user.  For instance,
if you want the browser to open an Excel file as such, you need to
tell the browser that the data coming back is in Excel format.
Sometimes we want to set the content-type for our response within the
controller method.  

By providing the @expose decorator with a content_type parameter we are 
able to accomplish this.

Here is an example of how to return a simple .csv file that the browser
will treat as an attachment::

    class MyController(BaseController):
        @expose(content_type='text/csv')
        def stats(self):
            return '1,2,3'

It is also possible to set this up with a template::

    class MyController(BaseController):
            @expose("mypackage.templates.sometemplate",content_type='text/csv')
            def stats(self):
                ...
                return dict(data = somedata)

Custom Content Types At Runtime
--------------------------------

Sometimes you will want to set the content type at runtime, the best example of 
this is when you want to restrict downloads behind auth and you will only know 
which file you are serving based on the request parameters.

This is done in the same way as plain old pylons.

.. warning :: due to bug `#2378 <http://trac.turbogears.org/ticket/2378>`_ we currently need to flag the controller as "setting the content type at runtime"

In this example we are flagging the content type::

    from tg import request, response
    from tg.controllers import CUSTOM_CONTENT_TYPE
 
    class MyController(BaseController):
        @expose(content_type=CUSTOM_CONTENT_TYPE)
        def stats(self):
            response.content_type = 'text/csv'
            response.headerlist.append(('Content-Disposition','attachment;filename=stats.csv'))
            return '1,2,3'

Ones the above bug is fixed all you will need is to set the content type at runtime by modifiying the headers::

    from tg import response

    class MyController(BaseController):
        @expose()
        def stats(self):
            response.headers['Content-type'] = 'text/csv'
            return '1,2,3'


