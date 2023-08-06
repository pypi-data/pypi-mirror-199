.. _Routers:

Routers Django Rest Framework
=============================

DRF offers great router classes, but implementations always assume that your main urls.py knows about all of your apps. GDAPS lets you define one `SimpleRouter` for each of your apps, and automatically collects them into one global `DefaultRouter`.

In your global `urls.py` add:

.. code-block:: python

    router = PluginManager.router()
    urlpatterns = [
        # ...
        path("api/", include(router.urls)),
    ]

In your apps' urls.py, similar to urlpatterns, create a `router` variable:

.. code-block:: python

    from rest_framework.routers import SimpleRouter

    router = SimpleRouter()
    router.register(r"app", AppListViewSet)

...where AppListViewSet is your DRF ViewSet. That's all, GDAPS takes care of the merging.
