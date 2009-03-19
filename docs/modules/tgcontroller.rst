:mod:`tg.controllers` -- Controllers
========================================

.. automodule:: tg.controllers

Common Controller Classes
----------------------------

There are two main methods for defining controllers in a TG2 system.  The first method is
ObjectDispatch-based, and is similar to the way TG1 dispatch worked.  RootControllers should
be defined with this class.  This will allow the normal nested-style dispatch of URLS as is
expected with TG1.

The second controller is RestController, which defines a RESTful interface for URL dispatch.
This provides Controller-Specific methods which are unique to dispatch using REST architecture.
RestControllers may be inter-twined with "regular" controllers to provide any mix of
dispatch the developer desires.

Controller classess along with the redirect function, and the special url function for constructing URL's 
constitutes the main functionality of the Controllers part of MVC.

.. autoclass:: TGController
   :show-inheritance:
   :members: __before__, __after__
   
.. autoclass:: RestController
   :show-inheritance:
   :members: __before__, __after__
   
Useful Methods
----------------

.. autofunction:: redirect

.. autofunction:: url

Other Classes
---------------


The ObjectDispatchController, and 
DecoratedController provide controllers that can be used as endpoints for users who are using 
Routes -- either in addition to object dispatch, or as an alternative.


.. autoclass:: DecoratedController
   :show-inheritance:

.. autoclass:: ObjectDispatchController
   :show-inheritance:

.. autoclass:: WSGIAppController
   :show-inheritance:

