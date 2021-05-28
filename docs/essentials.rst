==========
Essentials
==========

``Env.read_env()``
==================

Typically usage of ``django-environ-2`` starts with ``environ.Env.read_env()``.
This method is responsible for reading key-value pairs from the ``.env`` file
and adding them to environment variables.

``read_env()`` expects a path to the ``.env`` file. If one is not provided, it
will attempt to use the ``django.BASE_DIR`` constant from the Django ``settings``
module. If an ``ImportError`` or ``NameError`` is encountered while it attempts
to do this, ``read_env()`` will assume there's no ``.env`` file to be found, log
a WARN-level log message to that effect, and continue on.

.. note::
    The ``.env`` file doesn't have to be called that way. This could be for
    example ``settings.sh``, or any other name up to you.

Considering the above, here are some typical use cases of ``read_env()``:

.. code-block:: python

    import environ
    import os

    # Set the project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Take environment variables from .env file
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    # Take environment variables from settings.env file
    environ.Env.read_env(os.path.join(BASE_DIR, 'settings.env'))

    # Attempt to use the django.BASE_DIR to load .env file from
    # os.path.join(BASE_DIR, '.env').
    environ.Env.read_env()

The following things should also be mentioned:

* The values read in from the ``.env`` file are overridden by any that already
  existed in the environment. This means that environment variables obtained
  from the ``os.environ`` will have a higher priority.
* ``read_env()`` also takes an additional overrides list. Any additional keyword
  arguments provided directly to ``read_env`` will be added to the environment.
  If the key matches an existing environment variable, the value will be overridden.
* ``read_env()`` updates ``os.environ`` directly, rather than just that particular
  ``environ.Env`` instance.

The following example demonstrates the above:

**.env file**:

.. code-block:: shell

   # .env file contents
   DJANGO_SETTINGS_MODULE=settings.prod
   EMAIL=sales@acme.com
   DEBUG=on


**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ

   os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev'

   assert 'SECRET_KEY' not in os.environ
   assert 'DEBUG' not in os.environ


   overrides = {
       'SECRET_KEY': 'Enigma',
       'EMAIL': 'dev@acme.localhost',
   }

   # Take environment variables from .env file using
   # os.path.join(BASE_DIR, '.env'). Also take the overrides list.
   environ.Env.read_env(**overrides)

   assert os.environ['SECRET_KEY'] == 'Enigma'
   assert os.environ['DJANGO_SETTINGS_MODULE'] == 'settings.dev'
   assert os.environ['EMAIL'] == 'dev@acme.localhost'

   assert 'DEBUG' in os.environ
