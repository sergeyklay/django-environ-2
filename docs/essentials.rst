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
  existed in the environment. This means that variables that are already defined
  in the environment take precedence over those in your ``.env`` file.
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
   import os

   os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.dev'

   assert 'SECRET_KEY' not in os.environ
   assert 'DEBUG' not in os.environ


   overrides = {
       'SECRET_KEY': 'Enigma',
       'EMAIL': 'dev@acme.localhost',
   }

   # Take environment variables from .env file and the overrides list.
   environ.Env.read_env(**overrides)

   assert os.environ['SECRET_KEY'] == 'Enigma'
   assert os.environ['DJANGO_SETTINGS_MODULE'] == 'settings.dev'
   assert os.environ['EMAIL'] == 'dev@acme.localhost'

   assert 'DEBUG' in os.environ


Interpolate Environment Variables
=================================

An environment value or default can reference another environ value by referring
to it with a ``$`` sign. Values that being with a ``$`` can be interpolated, but
it is turned off by default. Pass ``interpolate=True`` to ``environ.Env()`` to
enable this feature:

The following example demonstrates the above:

**.env file**:

.. code-block:: shell

   # .env file contents
   PROXIED_VAR=$STR_VAR
   STR_VAR=bar

**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ

   # Take environment variables from .env file and enable interpolation
   env = environ.Env(interpolate=True)
   env.str('PROXIED_VAR')  # 'bar'
   env.str('NON_EXISTENT_VAR', default='$STR_VAR')  # 'bar'

   # Take environment variables from .env file and do not enable interpolation
   env = environ.Env()
   env.str('PROXIED_VAR')  # '$STR_VAR'
   env.str('NON_EXISTENT_VAR', default='$STR_VAR')  # '$STR_VAR'


However, expanding variables automatically on a read usually is an anti-pattern.
Variable expansion by the shell should only be done when the value is inserted
into the environment, but the value should be treated as opaque data. Any processing
or interpretation of the variable should be done by the application, not by the
access method.

If you get an infinite recursion when using environ most likely you have an
unresolved and perhaps unintentional proxy value in an environ string. For example,
consider the following use case:

**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ

   # Take environment variables from .env file and enable interpolation
   env = environ.Env(interpolate=True)

   env('not_present', default='$@u#c4w=%k')

In the example above the environment variable ``not_present`` does not exist
and the default value happens to start with a ``$``.  This is assumed to be a
"proxy variable" and looked up (using the same value as default again), which
leads to an infinite recursion.

Interpolation of environment variables on read is a very risky behavior. Even
if there's a valid use case for it. That's why it is disabled by default.
