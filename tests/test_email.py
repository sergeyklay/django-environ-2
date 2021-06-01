# This file is part of the django-environ-2.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (C) 2013-2021 Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from environ import Env


@pytest.mark.parametrize(
    'url,backend,expected',
    [
        ('smtps://user@domain.com:password@smtp.example.com:587',
         None,
         {
             'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
             'EMAIL_HOST': 'smtp.example.com',
             'EMAIL_HOST_PASSWORD': 'password',
             'EMAIL_HOST_USER': 'user@domain.com',
             'EMAIL_PORT': 587,
             'EMAIL_USE_TLS': True,
             'EMAIL_FILE_PATH': ''
         }
        ),
        ('smtp+ssl://user@ukr.net:secret@smtp.ukr.net:465',
         'my.email.backend.Class',
         {
             'EMAIL_BACKEND': 'my.email.backend.Class',
             'EMAIL_HOST': 'smtp.ukr.net',
             'EMAIL_HOST_PASSWORD': 'secret',
             'EMAIL_HOST_USER': 'user@ukr.net',
             'EMAIL_PORT': 465,
             'EMAIL_USE_SSL': True,
             'EMAIL_FILE_PATH': ''
         }
        ),
        ('consolemail://user@gmail.com:secret@smtp.gmail.com:587',
         None,
         {
             'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
             'EMAIL_HOST': 'smtp.gmail.com',
             'EMAIL_HOST_PASSWORD': 'secret',
             'EMAIL_HOST_USER': 'user@gmail.com',
             'EMAIL_PORT': 587,
             'EMAIL_FILE_PATH': ''
         }
        ),
    ],
)
def test_smtp_parsing(url, backend, expected):
    actual = Env.email_url_config(url, backend=backend)

    assert len(actual) == len(expected)
    assert actual == expected
