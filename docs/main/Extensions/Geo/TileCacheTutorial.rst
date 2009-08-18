
tgext.geo TileCache Tutorial
============================


Introduction
------------

TileCache is a python WSGI (Web Services Gateway Interface) App that
implements the WMS-C (Web Map Service - Cached) spec for generation
and serving of WMS tiles. This improves the performance of a WMS
service substantially by generating / querying tiles and locally
caching them to serve subsequent tile requests. tgext.geo includes
paster commands for creating controller code that mounts TileCache as
a WSGI App.


About This Tutorial
-------------------

In this tutorial we will create a TG2 app and use tgext.geo extension
to mount the TileCache WSGI App. We will also modify the template code
for *index* method to create an OpenLayers Map that will render the
tiles.


Installation
------------

It is assumed that a fresh virtualenv has been created and TG2
installed following the :ref:`downloadinstall`. Install tgext.geo
using easy_install::

    (tg2env)$ easy_install -i http://www.turbogears.org/2.0/downloads/current/index tgext.geo


Creating A New TG2 App
----------------------

Create a new TG2 app using the paster command and change into the
newly created project folder::

    (tg2env)$ paster quickstart TilesApp
    (tg2env)$ cd TilesApp


Add tgext.geo Paster Plugin
---------------------------

Open the paster plugins file viz. TilesApp.egg-info/paster_plugins.txt
and add a line containing ``tgext.geo`` .


Create A TileCache Config
-------------------------

Create a TileCache config in the file tilecache.cfg in the project
folder and add the necessary configuration. Details of this
configuration can be found in the `TileCache Documentation
<http://tilecache.org/readme.html#configuration>`_. A sample
tilecache.cfg file can be downloaded from
http://svn.tilecache.org/trunk/tilecache/tilecache.cfg . For example,
a standard WMS tile service would have the following config::

    [cache]
    type=Disk
    base=/tmp/tilecache

    # Rendering VMAP0 data with WMS
    [basic]
    type=WMS
    url=http://labs.metacarta.com/wms/vmap0
    extension=png

Sections for all the required tilecache layers should be added to this
file. For example, the following lines should be added in order to
have a :term:`Mapnik` Tiles layer using the OpenStreetMap_ (OSM) data::

    # Rendering OpenStreetMap data with Mapnik
    [osm]
    type=Mapnik
    mapfile=/home/user/osm-mapnik/osm.xml
    spherical_mercator=true
    bbox=-20037508.34,-20037508.34,20037508.34,20037508.34
    resolutions=156543.0,78271.5,39135.75,19567.875,9783.9375,4891.96875,2445.984375,1222.9921875,611.49609375,305.748046875,152.874023438,76.4370117188,38.2185058594,19.1092529297,9.55462646484,4.77731323242,2.38865661621,1.19432830811,0.597164154053,0.298582077026
    metaTile="yes"
    metaBuffer=40


Creating The Tiles Controller
-----------------------------

Once the tilecache.cfg file is ready, the new controller containing
the TileCache WSGI App can be created using the following paster
command::

    (tg2env)$ paster geo-tilecache tiles

where tiles is the new controller. Now edit the root controller
(package/controllers/root.py) to import and mount the controller:

.. code-block:: python


    from tilesapp.controllers.tiles import TilesController

    class RootController(BaseController):
        tiles = TilesController()

The tiles controller should now be accessible at the url location
`http://<host>:<port>/tiles`.

Start the server and point your browser to the above url. You should
be able to see the TileCache Capabilities document, which an xml
document describing the service.


Rendering The Tiles In An OpenLayers Map
----------------------------------------


Adding The Javascript Code
~~~~~~~~~~~~~~~~~~~~~~~~~~

The tiles accessible through the TileCache definition above can be
rendered in an OpenLayers Map as a WMS layer. Modify the index
template to add the following javascript code in the head section:

.. code-block:: javascript

    <script src="/javascript/OpenLayers.js"></script>
    <script type="text/javascript">
        var map, layer;
        function init(){
            map = new OpenLayers.Map( $('map'), {'maxResolution': 360/512});
            layer = new OpenLayers.Layer.WMS( "VMap0", 
                    "http://localhost:8080/tiles", {layers: 'basic', format: 'image/png' } );
            map.addLayer(layer);
            if (!map.getCenter()) map.zoomToMaxExtent();
        }
    </script>

When using the OSM Layer, use exactly the same projection, extents and
resolution settings as defined in the tilecache config:

.. code-block:: javascript

    <script src="/javascript/OpenLayers.js"></script>
    <script type="text/javascript">
        var map, layer;
        function init(){
         options = {controls:[
                new OpenLayers.Control.LayerSwitcher(),
                new OpenLayers.Control.PanZoomBar()
                ]};

         options = OpenLayers.Util.extend({
            maxExtent: new OpenLayers.Bounds(-20037508.34,
                -20037508.34,20037508.34,20037508.34),
            maxResolution: 156543.0339,
            projection: new OpenLayers.Projection("EPSG:900913"),
            displayProjection: new OpenLayers.Projection("EPSG:4326"),
            transitionEffect: "resize"
        }, options);

        map = new OpenLayers.Map('map', options);

        layer = new OpenLayers.Layer.WMS("osm", "http://localhost:8080/tiles/",
                {layername: "osm", type: "png"});
        map.addLayer(layer);
        map.setCenter(new OpenLayers.LonLat(2.3, 48.86).transform(
                new OpenLayers.Projection("EPSG:4326"),
                new OpenLayers.Projection("EPSG:900913")), 15);
    }
    </script>

Download OpenLayers javascript mapping toolkit from the OpenLayers_
site and unzip / untar the archive. Copy the OpenLayers.js file and
the img folder in the archive to project/public/javascript folder.


Adding The Style Code
~~~~~~~~~~~~~~~~~~~~~

The following stylesheet code may be added to suite the map display:

.. code-block:: css

    <style type="text/css">
        #map {
            width: 100%;
            height: 100%;
        }
    </style>


Add The HTML Code
~~~~~~~~~~~~~~~~~

The following HTML code should be sufficient to show the map:

.. code-block:: html

    <body onload="init();">
      <div id="map"/>
      <div class="clearingdiv" />
      <div class="notice"> Thank you for choosing TurboGears.</div>
    </body>

See TileCache In Action
-----------------------

Its time to see TileCache in action now. Run the paster command to
start the local HTTP server::

    (tg2env)$ paster serve --reload development.ini

Point your browser to http://localhost:8080 to view the map. The first
time you see the map and zoom in the tile would be generated and
rendered. In the subsequent requests the response is much faster as
tiles cached earlier are served up.


.. glossary::

    Mapnik_
        Mapnik is a C++ toolkit with python bindings for rendering
	maps. OpenStreetMap is a free geographic data set containing street
	maps. A document describing the rendering of OSM maps using Mapnik can
	be found `here <http://wiki.openstreetmap.org/index.php/Mapnik>_`. The
	metaTile param causes mapnik to make use of PIL for rendering the
	maps.

.. _OpenStreetMap: http://www.openstreetmap.org/
.. _OpenLayers: http://www.openlayers.org/
.. _Mapnik: http://www.mapnik.org/
