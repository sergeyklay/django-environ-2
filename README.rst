.. raw:: html

    <h1 align="center">django-environ-2</h1>
    <p align="center">
        <a href="https://pypi.python.org/pypi/django-environ-2">
            <img src="https://img.shields.io/pypi/v/django-environ-2.svg" alt="Latest version released on PyPi" />
        </a>
        <a href="https://coveralls.io/github/sergeyklay/django-environ-2">
            <img src="https://coveralls.io/repos/github/sergeyklay/django-environ-2/badge.svg" alt="Coverage Status" />
        </a>
        <a href="https://github.com/sergeyklay/django-environ-2/actions?workflow=CI">
            <img src="https://github.com/sergeyklay/django-environ-2/workflows/CI/badge.svg?branch=master" alt="CI Status" />
        </a>
        <a href="https://raw.githubusercontent.com/sergeyklay/django-environ-2/master/LICENSE.txt">
            <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="Package license" />
        </a>
    </p>

.. teaser-begin

``django-environ-2`` is the Python package that allows you to use
`Twelve-factor methodology <http://www.12factor.net/>`_ to configure your
Django application with environment variables.

.. teaser-end

For that, it gives you an easy way to configure Django application using
environment variables obtained from a file or provided by OS:

.. -code-begin-

.. code-block:: python

    import environ

    env = environ.Env(
        # set casting, default value
        DEBUG=(bool, False)
    )

    # reading .env file
    environ.Env.read_env()

    # False if not in os.environ because of casting above
    DEBUG = env('DEBUG')

    # Raises Django's ImproperlyConfigured
    # exception if SECRET_KEY not in os.environ
    SECRET_KEY = env('SECRET_KEY')

    # Parse database connection url strings
    # like psql://user:pass@127.0.0.1:8458/db
    DATABASES = {
        # read os.environ['DATABASE_URL'] and raises
        # ImproperlyConfigured exception if not found
        #
        # The db() method is an alias for db_url().
        'default': env.db(),

        # read os.environ['SQLITE_URL']
        'extra': env.db_url(
            'SQLITE_URL',
            default='sqlite:////tmp/my-tmp-sqlite.db'
        )
    }

    CACHES = {
        # Read os.environ['CACHE_URL'] and raises
        # ImproperlyConfigured exception if not found.
        #
        # The cache() method is an alias for cache_url().
        'default': env.cache(),

        # read os.environ['REDIS_URL']
        'redis': env.cache_url('REDIS_URL')
    }

.. -overview-

The idea of this package is to unify a lot of packages that make the same stuff:
Take a string from ``os.environ``, parse and cast it to some of useful python
typed variables. To do that and to use the `12factor <http://www.12factor.net/>`_
approach, some connection strings are expressed as url, so this package can parse
it and return a ``urllib.parse.ParseResult``. These strings from ``os.environ``
are loaded from a ``.env`` file and filled in ``os.environ`` with ``setdefault``
method, to avoid to overwrite the real environ.
A similar approach is used in `Two Scoops of Django <http://twoscoopspress.org/>`_
book and explained in `12factor-django <http://www.wellfireinteractive.com/blog/easier-12-factor-django/>`_
article.

Using ``django-environ-2`` you can stop to make a lot of unversioned
``settings_*.py`` to configure your app.
See `cookiecutter-django <https://github.com/pydanny/cookiecutter-django>`_ for
a concrete example on using with a Django project.

Feature Support:

* Fast and easy multi environment for deploy
* Fill ``os.environ`` with .env file variables
* Variables casting
* Url variables exploded to Django specific package settings

.. -project-information-

Project Information
===================

``django-environ-2`` was forked from the `django-environ <https://github.com/joke2k/django-environ>`_
initially written by `Daniele Faraglia <https://github.com/joke2k>`_ to breathe
new life into it and set a more dynamic pace of development.

``django-environ-2`` is released under the `MIT / X11 License <https://choosealicense.com/licenses/mit/>`__,
its documentation lives at `Read the Docs <https://django-environ-2.readthedocs.io/>`_,
the code on `GitHub <https://github.com/sergeyklay/django-environ-2>`_,
and the latest release on `PyPI <https://pypi.org/project/django-environ-2/>`_.

It’s rigorously tested on Python 3.6+, and officially supports
Django 1.11, 2.2, 3.0, 3.1 and 3.2.

If you'd like to contribute to ``django-environ-2`` you're most welcome!

.. -support-

Support
=======

Should you have any question, any remark, or if you find a bug, or if there is
something you can't do with the ``django-environ-2``, please
`open an issue <https://github.com/sergeyklay/django-environ-2/issues>`_.

.. -similar-projects-

Similar projects
================

There are some projects similar to ``django-environ-2`` you may be interested in:

* https://github.com/joke2k/django-environ
* https://github.com/theskumar/python-dotenv
