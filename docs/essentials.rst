==========
Essentials
==========


``Env.read_env()``
==================

Typically usage of ``django-environ-2`` starts with ``environ.Env.read_env()``.
This method is responsible for reading key-value pairs from the ``.env`` file
and adding them to environment variables.

``read_env()`` expects a path to the ``.env`` file. If one is not provided, it
will attempt to use the ``BASE_DIR`` constant from the Django ``settings``
module. If one of ``AttributeError``, ``ImportError`` or  ``NameError`` errors
encountered while it attempts to do this, ``Env.read_env()`` will assume there's
no ``.env`` file to be found, log a WARN-level log message to that effect, and
continue on.

.. note::
   The ``.env`` file doesn't have to be called that way. This could be for
   example ``settings.sh``, or any other name up to you.

Considering the above, here are some typical use cases of ``read_env()``:

.. code-block:: python

   import environ
   import os
   import pathlib

   # Set the project base directory
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

   # Setting 'settings.BASE_DIR' at early stage to prevent error like:
   #     AttributeError: 'Settings' object has no attribute 'BASE_DIR'
   # when calling 'Env.read_env()' without specifying 'env_file'.
   #
   # This can also be avoided by calling 'Env.read_env()' as follows:
   #    env.read_env(BASE_DIR / '.env')
   settings.BASE_DIR = BASE_DIR

   env = environ.Env()

   # Attempt to use the django.conf.settings.BASE_DIR to load .env
   # file from os.path.join(BASE_DIR, '.env').
   env.read_env()

   # Take environment variables from '.env' file using str object.
   env.read_env(os.path.join(BASE_DIR, '.env'))

   # Take environment variables from specified 'settings.env' file.
   env.read_env(os.path.join(BASE_DIR, 'settings.env'))

   # Take environment variables from '.env' file using pathlib's Path
   BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
   env.read_env(BASE_DIR / '.env')

The following things should also be mentioned:

* By default, the values read in from the ``.env`` file are overridden by any
  that already existed in the environment. This means that variables that are
  already defined in the environment take precedence over those in your ``.env``
  file.
* ``read_env()`` also takes an additional overrides list. Any additional keyword
  arguments provided directly to ``read_env`` will be added to the environment.
  If the key matches an existing environment variable, the value will be overridden.
* ``read_env()`` updates ``os.environ`` directly, rather than just that particular
  ``environ.Env`` instance.

The following example demonstrates the above:

**.env file**:

.. code-block:: shell

   # .env file contents
   FOO=buz
   EMAIL=sales@acme.com
   DEBUG=on


**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ
   import os

   os.environ['FOO'] = 'bar'

   assert 'SECRET_KEY' not in os.environ
   assert 'DEBUG' not in os.environ

   overrides = {
       'SECRET_KEY': 'Enigma',
       'EMAIL': 'dev@acme.localhost',
   }

   env = environ.Env()

   # Take environment variables from .env file and the overrides list.
   env.read_env('/path/to/.env', **overrides)

   assert os.environ['FOO'] == 'bar'
   assert os.environ['SECRET_KEY'] == 'Enigma'
   assert os.environ['EMAIL'] == 'dev@acme.localhost'

   assert 'DEBUG' in os.environ

Additionally, ``read_env()`` takes an optional ``overwrite`` parameter, which is
set to ``False`` by default. Setting it to ``True`` will force an overwrite of
existing environment variables. This is illustrated by the following example:

**.env file**:

.. code-block:: shell

   # .env file contents
   DB_NAME=dev_db
   DB_USER=dev_user


**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ
   import os

   os.environ['DB_NAME'] = 'acme_prod'
   os.environ['DB_USER'] = 'acme'
   env = environ.Env()

   # Take environment variables from .env file and
   # overwrite existing environment variables
   env.read_env('/path/to/.env', overwrite=True)

   assert os.environ['DB_NAME'] == 'dev_db'
   assert os.environ['DB_USER'] == 'dev_user'


Finally, you can specify the name of the encoding used to read and decode the
``.env`` file. If is not specified the encoding used is platform dependent:

**.env file**:

.. code-block:: shell

   # .env file contents

   # Whèthér to uŝe a sêcurë cookiè for thé şeśsion cookiê
   SESSION_COOKIE_SECURE=True


**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ

   env = environ.Env()

   # Read .env file using UTF-8 encoding.
   env.read_env('/path/to/.env', encoding='utf-8')

   assert env.bool('SESSION_COOKIE_SECURE') is True


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

Using URL-unsafe characters un URL-like variables
=================================================

Internally ``django-environ-2`` uses ``urllib`` to parse URL-like schemas.
In turn, ``urllib`` follows `RFC 3986 <https://datatracker.ietf.org/doc/html/rfc3986>`_
to parse URIs. Therefore, you should encode all unsafe characters in the
userinfo part to achieve the expected behavior from ``django-environ-2``.

Consider the following **wrong** example:

**.env file**:

.. code-block:: shell

   # .env file contents
   DATABASE_URL='postgres://user:#@host:5432/db'

**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ


   env = environ.Env()
   result = env.db('DATABASE_URL')

   assert result['NAME'] == ''
   assert result['USER'] == ''
   assert result['PASSWORD'] == ''
   assert result['HOST'] == 'user'
   assert result['PORT'] == ''
   assert result['ENGINE'] == 'django.db.backends.postgresql'

Here, the number sign (``#``) was passed as unencoded, raw value.  However,
according to `RFC 3986 #2.2 <https://datatracker.ietf.org/doc/html/rfc3986#section-2.2>`_,
the number sign character must be encoded:

::

   URIs include components and subcomponents that are delimited by
   characters in the "reserved" set.  These characters are called
   "reserved" because they may (or may not) be defined as delimiters by
   the generic syntax, by each scheme-specific syntax, or by the
   implementation-specific syntax of a URI's dereferencing algorithm.
   If data for a URI component would conflict with a reserved
   character's purpose as a delimiter, then the conflicting data must be
   percent-encoded before the URI is formed.

   reserved    = gen-delims / sub-delims

   gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"

   sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
               / "*" / "+" / "," / ";" / "="

Thus, to make this example valid, we have to fix it as follows:

**.env file**:

.. code-block:: shell

   # .env file contents
   DATABASE_URL='postgres://user:%23@host:5432/db'

**settings.py file**:

.. code-block:: python

   # settings.py file contents
   import environ

   env = environ.Env()
   result = env.db('DATABASE_URL')

   assert result['NAME'] == 'db'
   assert result['USER'] == 'user'
   assert result['PASSWORD'] == '#'
   assert result['HOST'] == 'host'
   assert result['PORT'] == 5432
   assert result['ENGINE'] == 'django.db.backends.postgresql'
