Installation
============

Install GDAPS in your Python virtual environment. If you want to create plugins, install cookiecutter too.

.. code-block:: bash

    pip install gdaps cookiecutter


Create a Django application as usual: ``django-admin startproject myproject``.

First, set a variable named ``PROJECT_NAME``.

.. code-block:: python

    PROJECT_NAME = "myproject"

This is a (machine) name for your project. Django itself does not provide such a name. It will be used in various places. Must be a valid python identifier.

.. note::

    ``PROJECT_NAME`` is roughly what Django means with ``ROOT_URLCONF[0]``, but GDAPS requires it to be set explicitly.

Now add "gdaps" to the ``INSTALLED_APPS`` section, and add a special line below it:

.. code-block:: python

    from gdaps.pluginmanager import PluginManager

    INSTALLED_APPS = [
        # ... standard Django apps and GDAPS
        "gdaps",
    ]
    # The following line is important: It loads all plugins from setuptools
    # entry points and from the directory named 'myproject.plugins':
    INSTALLED_APPS += PluginManager.find_plugins(PROJECT_NAME + ".plugins")

You can use whatever you want for your plugin path, but we recommend that you use "**<PROJECT_NAME>.plugins**" here to make things easier. Basically, this is all you really need so far, for a minimal working GDAPS-enabled Django application. See :doc:`usage` for how to use GDAPS.

URL handling
------------
Now add the URL path for GDAPS, so it can add plugins' URLs automatically to the global urlpattern.

.. code-block:: python

    # urls.py
    from gdaps.pluginmanager import PluginManager

    urlpatterns = PluginManager.urlpatterns() + [
        # ... add your fixed URL patterns here, like "admin/", etc.
    ]

This way each plugin can have an `urlpatterns` variable in `urls.py`, and all are merged together. However, by now, the plugin order is not determined, so urlpatterns too are not in a deterministically determined order. This could lead to problems, depending on your application design, so keep that in mind when designing plugins.

Logging
-------
Django does not write loggings to the command line automatically. GDAPS uses various levels of logging. It is recommended that you create a LOGGING section in settings.py for GDAPS:

.. code-block:: python

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {"console": {"class": "logging.StreamHandler"}},
        "loggers": {
            "gdaps": {"handlers": ["console"], "level": "INFO", "propagate": True},
        },
    }

This will output all GDAPS log messages to the console.

