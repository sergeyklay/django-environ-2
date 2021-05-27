Changelog
=========

This file contains a brief summary of new features and dependency changes or
releases, in reverse chronological order.

2.1.0 (2021-XX-XX)
------------------


Breaking Changes
^^^^^^^^^^^^^^^^

- Removed no longer needed ``Env.unicode()`` shortcut.
- Removed no longer needed ``simplejson`` from the ``compat`` module.


Features
^^^^^^^^

* Allows use of ``pathlib.Path`` objects when reading env from the filesystem.
  This enables use of ``env.read_env(BASE_DIR / '.env')`` instead of
  ``read_env(os.path.join(BASE_DIR, '.env'))``.
* Added support for negative float strings.

Improvements
^^^^^^^^^^^^

* Changed additional groups of dependencies so that ``develop`` is superset
  now for ``testing`` and ``docs``.


Bug Fixes
^^^^^^^^^

* Added missed files to the package contents.
* Don't include ``tests`` package in wheel. Previously ``pip install django-environ-2``
  used to install a top-level package ``tests``. This was fixed.
* Fixed ``db_url_config`` to work the same for all postgres aliases.


----


2.0.1 (2021-05-25)
------------------

Bug Fixes
^^^^^^^^^

* Fixed changelog URL in package description.
* Added missed ``test_env.txt`` to the package contents.


Improved Documentation
^^^^^^^^^^^^^^^^^^^^^^

* Improved package documentation.
* Fixed misspellings in the documentation.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Added testing dependencies to ``setup.py``.


----


2.0.0 (2021-05-25)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* Renaming PyPI package from ``django-environ`` to ``django-environ-2`` due to
  the fork. Now package lives at `<https://pypi.org/project/django-environ-2>`_.
* Python < 3.6 is no longer supported.
* Django < 1.11 is no longer supported.
* Removed no longer used ``environ.VERSION``. Use ``environ.__version__`` instead.


Features
^^^^^^^^

* Added support for Django 2.1, 2.2, 3.0, 3.1 and 3.2.
* Added option to disable ``smart_cast``.
* Added support for ``rediss://`` cache URLs.
* Added secure redis backend and Django 1.11 db config.


Improvements
^^^^^^^^^^^^

* Added validation fro empty cache url and unknown cache scheme.
* Removes usage of ``basestring`` in favour of ``str``.


Bug Fixes
^^^^^^^^^

* Fixed various code linting errors added this check to CI.
* Added missed ``cast=str`` to ``Env.str()`` method.


Improved Documentation
^^^^^^^^^^^^^^^^^^^^^^

* Improved documentation and fixed misspellings.


Trivial/Internal Changes
^^^^^^^^^^^^^^^^^^^^^^^^

* Move CI/CD to GitHub Actions.
* Refactor tests to use pytest and follow DRY.
* Used tox for tests.
* Fixed spelling in example ``.env`` code block.


----


0.4.5 (2018-06-25)
------------------

Features
^^^^^^^^

* Provided support for Django 2.0.
* Provided support for smart casting.
* Provided support PostgreSQL unix domain socket paths.
* Tip: Multiple env files.


Bug Fixes
^^^^^^^^^

* Fixed parsing option values None, True and False.


Improvements
^^^^^^^^^^^^

* Order of importance of engine configuration in ``db_url_config``.
* Remove django and six dependencies.


----


0.4.4 (2017-08-21)
------------------

Features
^^^^^^^^

* Provided support for ``django-redis`` multiple locations (master/slave, shards).
* Provided support for ``Elasticsearch2``.
* Provided support for Mysql-connector.
* Provided support for ``pyodbc``.
* Added ``__contains__`` feature to ``Environ`` class.


Bug Fixes
^^^^^^^^^

* Fix ``Path`` subtracting.


----


0.4.3 (2017-08-21)
------------------


Bug Fixes
^^^^^^^^^

* Rollback the default ``Environ`` to ``os.environ``.


----


0.4.2 (2017-04-13)
------------------

Features
^^^^^^^^

* Confirmed support for Django 1.11.
* Provided support for Redshift database URL.


Bug Fixes
^^^^^^^^^

* Fixed uwsgi settings reload issue.


Improvements
^^^^^^^^^^^^

* Updated support for ``django-redis`` urls.


----


0.4.1 (2016-11-13)
------------------

Features
^^^^^^^^

* Added support for Django 1.10.


Bug Fixes
^^^^^^^^^

* Fixed for unsafe characters into URLs.
* Fixed support for Oracle urls.
* Fixed support for ``django-redis``.


Improvements
^^^^^^^^^^^^

* Clarifying warning on missing or unreadable file.


----


0.4.0 (2015-09-23)
------------------

Breaking Changes
^^^^^^^^^^^^^^^^

* ``redis_cache`` replaced by ``django_redis``.


Features
^^^^^^^^

* Added new email schemes - ``smtp+ssl`` and ``smtp+tls``
  (smtps would be deprecated).
* Added tuple support.
* Added LDAP url support for database.


Bug Fixes
^^^^^^^^^

* Fixed non-ascii values (broken in Python 2.x).
* Fixed psql/pgsql url.


----


0.3 (2014-06-03)
----------------

Features
^^^^^^^^

* Added cache url support.
* Added email url support.
* Added search url support.


Improved Documentation
^^^^^^^^^^^^^^^^^^^^^^

* Rewriting README.rst.


----


0.2.1 (2013-04-19)
------------------

Improvements
^^^^^^^^^^^^

* ``Env.__call__`` now uses ``Env.get_value`` instance method.


----


0.2 (2013-04-16)
----------------

Features
^^^^^^^^

* Added advanced float parsing (comma and dot symbols to separate thousands and decimals).


Improved Documentation
^^^^^^^^^^^^^^^^^^^^^^

* Fixed typos in documentation.


----


0.1 (2013-04-02)
----------------

Features
^^^^^^^^

* Initial release.
