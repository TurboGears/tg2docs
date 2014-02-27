.. _tgext.crud.restapi:


Rapid Prototyping REST API
=====================================

TurboGears provides a great way to rapidly prototype rest APIS using the
:ref:`EasyCrudRestController <tgext.crud.reference>`.

Defining a basic ready to use API is as simple as::

    from tgext.crud import EasyCrudRestController

    class APIController(EasyCrudRestController):
        pagination = False
        model = model.Permission

    class RootController(BaseController):
        permissions = APIController(model.DBSession)

Accessing the ``/permissions.json`` URL you should get::

    {
        value_list: [
            {
                permission_id: 1,
                description: "This permission give an administrative right to the bearer",
                permission_name: "manage"
            }
        ]
    }

Blocking non JSON requests
--------------------------------

The first side effect is that accessing the url without the ``.json``
extension you will get the CRUD page. This is usually something you
don't want when exposing an API and can be easily prevented by blocking
requests which are not in JSON format::

    from tgext.crud import EasyCrudRestController
    from tg import abort

    class APIController(EasyCrudRestController):
        pagination = False
        model = model.Permission

        def _before(self, *args, **kw):
            if request.response_type != 'application/json':
                abort(406, 'Only JSON requests are supported')

            super(APIController, self)._before(*args, **kw)

Accessing the HTML page will now report a `Not Acceptable` error while
JSON output will still be accepted.

Getting Relationships
-----------------------------

You probably noticed that even though our permissions are related to groups
we didn't get the list of groups the permission is related to.

This is due to the fact that for performance reasons the ``EasyCrudRestController``
doesn't automatically resolve relationships when providing responses for APIs.

To enable this behavior it is sufficient to turn on the ``json_dictify`` option::

    class APIController(EasyCrudRestController):
        pagination = False
        json_dictify = True
        model = model.Permission

        def _before(self, *args, **kw):
            if request.response_type != 'application/json':
                abort(406, 'Only JSON requests are supported')

            super(APIController, self)._before(*args, **kw)

Reloading the ``/permissions.json`` page will now provide the list of groups
each Permission is related to with a response like::

    {
        value_list: [
            {
                permission_id: 1,
                description: "This permission give an administrative right to the bearer",
                groups: [
                    1
                ],
                permission_name: "manage"
            }
        ]
    }

Leveraging your REST API on AngularJS
---------------------------------------

One of the main reasons to rapidly prototype a REST api is to join it with a
frontend framework to perform logic and templating on client side.

The following is an example of a working **AngularJS** application
that permits creation and deletion of ``Permission`` objects through
the previously created API:

.. note::
    Please note the custom **$resource** to adapted tgext.crud responses to the
    style expected by AngularJS

.. note::
    Pay attention to the double **$$** required to escape the dollar sign on Genshi

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:py="http://genshi.edgewall.org/"
          xmlns:xi="http://www.w3.org/2001/XInclude">

      <xi:include href="master.html" />

    <head>
      <title>AngularTG</title>
      <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.12/angular.min.js"></script>
      <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.12/angular-resource.min.js"></script>
      <style>
        .ng-cloak {
          display: none !important;
        }
      </style>
    </head>

    <body>
      <div class="row">
        <div class="col-md-12">
         <div ng-app="myApp" class="ng-cloak">
           <div ng-controller="PermissionsCtrl">
            <h1>Permissions</h1>

            <form ng-submit="addPermission(newPerm)">
                <input placeholder="Create Permission" ng-model="newPerm.permission_name" autofocus="true"/>
            </form>

            <div ng-repeat="perm in permissions">
              <span ng-click="delPermission($$index)">X</span>
              {{perm.permission_name}}
              <p>{{perm.description}}</p>
            </div>
           </div>
         </div>
       </div>
      </div>
      <script>
    //<![CDATA[
        var myApp = angular.module('myApp', ['ngResource']);

        myApp.factory('Permissions', ['$$resource', function($$resource) {
          return $$resource("${tg.url('/permissions/:id.json')}", {'id': "@permission_id"}, {
            query: {
              method: 'GET',
              isArray: true,
              transformResponse: function (data) {
                var data = angular.fromJson(data);
                return data.value_list;
              }
            },
            save: {
              method: 'POST',
              transformResponse: function(data) {
                var data = angular.fromJson(data);
                return data.value;
              }
            }
           });
        }]);

        myApp.controller('PermissionsCtrl', ['$$scope', 'Permissions',
                function ($$scope, Permissions) {
          $$scope.permissions = Permissions.query();

          $$scope.addPermission = function(permData) {
            var perm = new Permissions(permData);
            permData.permission_name = "";
            perm.$$save(function(data) {
              $$scope.permissions.push(new Permissions(data));
            });
          }

          $$scope.delPermission = function(index) {
            perm = $$scope.permissions[index];
            perm.$$delete(function(data) {
              $$scope.permissions.splice(index, 1);
            });
          }
        }]);
    //]]>
      </script>
    </body>
    </html>


Limiting API Results
------------------------------

The previous API returns all the Permissions available, which is the most
simple case but not always what you are looking for. It is often needed
to filter the results by a constraint, for example it is common to get only
the objects for a specific user.

While this can be easily achieved by passing any filter to the API itself
when it is called: ``/permissions.json?groups=1``. It is common to need to
perform this on server side.

If we want to permanently only get the permissions for the manage groups
we can make it by extending the ``get_all`` method::

    from tgext.crud import EasyCrudRestController
    from tg import abort

    class APIController(EasyCrudRestController):
        pagination = False
        json_dictify = True
        model = model.Permission

        def _before(self, *args, **kw):
            if request.response_type != 'application/json':
                abort(406, 'Only JSON requests are supported')

            super(APIController, self)._before(*args, **kw)

        @expose(inherit=True)
        def get_all(self, *args, **kw):
            kw['groups'] = 1
            return super(APIController, self).get_all(*args, **kw)

If you point your browser to ``/permissions.json`` and had multiple
permissions you will se that only those for the ``managers`` group
are now reported.

Now if you tried to use the filtered controller with the previously
created **AngularJS** application your probably noticed that the new
permissions you create are not listed back when you reload the page.
This is because they are actually created without a group, so they don't
match our *managers* group filter.

To avoid this we can also force the group on creation by extending
also the ``post`` method::

    from tgext.crud import EasyCrudRestController
    from tg import abort

    class APIController(EasyCrudRestController):
        pagination = False
        json_dictify = True
        model = model.Permission

        def _before(self, *args, **kw):
            if request.response_type != 'application/json':
                abort(406, 'Only JSON requests are supported')

            super(APIController, self)._before(*args, **kw)

        @expose(inherit=True)
        def get_all(self, *args, **kw):
            kw['groups'] = 1
            return super(APIController, self).get_all(*args, **kw)

        @expose(inherit=True)
        def post(self, *args, **kw):
            kw['groups'] = [1]
            return super(APIController, self).post(*args, **kw)

This will now correctly create all the new permissions for the *managers*
group.


Custom Queries when fetching data
-------------------------------------

While extending the ``get_all`` method is quick and easy, you are limited
to the filtering possibilities that **sprox** exposes you.

For more advanced filtering or even custom queries it is possible to
declare your own TableFiller with a totally custom query::

    from tgext.crud import EasyCrudRestController
    from sprox.fillerbase import TableFiller
    from tg import abort

    class APIController(EasyCrudRestController):
        pagination = False
        json_dictify = True
        model = model.Permission

        class table_filler_type(TableFiller):
            __entity__ = model.Permission

            def _do_get_provider_count_and_objs(self, **kw):
                manager_group = model.DBSession.query(model.Group).filter_by(group_name='managers').first()
                results = model.DBSession.query(model.Permission).filter(model.Permission.groups.contains(manager_group)).all()
                return len(results), results

        def _before(self, *args, **kw):
            if request.response_type != 'application/json':
                abort(406, 'Only JSON requests are supported')

            super(APIController, self)._before(*args, **kw)