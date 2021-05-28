===============
Getting Started
===============

Installation
============


Requirements
------------

* `Django <https://www.djangoproject.com/>`_ >= 1.11
* `Python <https://www.python.org/>`_ >= 3.6

Installing django-environ-2
___________________________

``django-environ-2`` is a Python-only package `hosted on PyPI <https://pypi.org/project/django-environ-2/>`_.
The recommended installation method is `pip <https://pip.pypa.io/en/stable/>`_-installing into a virtualenv:

.. code-block:: console

   $ python -m pip install django-environ-2

.. note::

   After installing ``django-environ-2``, no need to add it to ``INSTALLED_APPS``.

Then create a ``.env`` file. The file format can be understood from the example below:

.. code-block:: bash

    DEBUG=on
    SECRET_KEY=your-secret-key
    DATABASE_URL=psql://user:un-githubbedpassword@127.0.0.1:8458/database
    SQLITE_URL=sqlite:///my-local-sqlite.db
    CACHE_URL=memcache://127.0.0.1:11211,127.0.0.1:11212,127.0.0.1:11213
    REDIS_URL=rediscache://127.0.0.1:6379/1?client_class=django_redis.client.DefaultClient&password=ungithubbed-secret

And use it with ``settings.py`` as follows:

.. include:: ../README.rst
   :start-after: -code-begin-
   :end-before: -overview-

.. warning::

    Don't forget to add ``.env`` in your ``.gitignore``. You can also add
    ``.env.dist`` with a template of your variables to the project repo.

Unstable version
================

The master of all the material is the Git repository at https://github.com/sergeyklay/django-environ-2.
So, can also install the latest unreleased development version directly from the ``master`` branch on GitHub.
It is a work-in-progress of a future stable release so the experience might be not as smooth.:

.. code-block:: bash

   $ pip install -e git://github.com/sergeyklay/django-environ-2.git#egg=django-environ-2
   # OR
   $ pip install --upgrade https://github.com/sergeyklay/django-environ-2.git/archive/master.tar.gz

This command will download the latest version of ``django-environ-2`` from the
`Python Package Index <https://pypi.org/project/django-environ-2/>`_ and install it to your system.

.. note::

   The ``master`` branch will always contain the latest unstable version, so the experience
   might be not as smooth. If you wish to check older versions or formal, tagged release,
   please switch to the relevant `tag <https://github.com/sergeyklay/django-environ-2/tags>`_.

More information about ``pip`` and PyPI can be found here:

* `Install pip <https://pip.pypa.io/en/latest/installing/>`_
* `Python Packaging User Guide <https://packaging.python.org/>`_
