=================================================
 tgext.geo: Geographic Extensions for TurboGears
=================================================

Overview
========

The Geographic Extensions for TurboGears makes is easy to add
GIS capabilities in a TurboGears2 application. A Web GIS application
typically consists of both server side and client side components.

Client Side Components
======================

The client side component typically consists of a Web2.0 based map
with rich Ajax capabilities for panning, zooming, layer selection, etc.
The tw.openlayers ToscaWidget library makes it really simple to add
a map on a TG2 application. However, if the client side application
becomes complex and involves a lot of javascript work, it is advisable
to use the the OpenLayers library directly for greater flexibility.

Server Side Components
======================

On the server side a GIS application needs to handle HTTP requests for
query, processing and manipulation of GIS objects. Several server side
GIS tools already exist in the python world and tgext.geo makes it easy
to integrate these tools for server side processing. The tools integrated
by tgext.geo are:

GeoAlchemy
~~~~~~~~~~

GeoAlchemy_ is  a SQLAlchemy extension for spatial databases.
Use this to define you model objects which have geometry fields.
The FeatureServer Tutorial explains the usage. For further details
refer to the GeoAlchemy docs.

FeatureServer
~~~~~~~~~~~~~

FeatureServer_ is a GIS server that supports publishing of GIS data
from multiple datasources including GeoAlchemy. FeatureServer can
publish GIS data in several formats such as JSON, GML, RSS, etc.

MapFish
~~~~~~~

MapFish_ is a pylons based GIS server. MapFish also has a rich client
library that uses the mapfish protocol. So, if you want a complete
WebGIS solution, MapFish is for you. MapFish model and controller
definitions can be added to TG2 application using the paster commands.
As of now MapFIsh model definitions do not use GeoAlchemy and support
only reflected tables. However, work is on for building future versions
of MapFish on GeoAlchemy.

TileCache
~~~~~~~~~

Serving raster data (satellite imagery, etc) is not supported by TG2 as
this is not a very common use case. Most of the time we are just
interested in requesting them from public / corporate servers and
displaying as background layers on our maps. However, in doing so we
could choose to cache the requested tiles (view elements) on our
servers (or in the cloud) in order to make our application more responsive.

TileCache_ is an excellent python library for achieving this. tgext.geo
provides a paster command to integrate TileCache in an existing TG2 app.
The details are available on the TileCache_ home page and on the TG2
TileCache Tutorial.

.. toctree::
   :maxdepth: 1

   commands
   FeatureServerTutorial
   MapFishTutorial
   TileCacheTutorial

.. _GeoAlchemy: http://geoalchemy.org
.. _FeatureServer: http://featureserver.org
.. _MapFish: http://mapfish.org
.. _TileCache: http://tilecache.org
