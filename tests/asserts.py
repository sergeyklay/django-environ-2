# This file is part of the django-environ.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (C) 2013-2021 Daniele Faraglia
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

def assert_type_and_value(type_, expected, actual):
    assert isinstance(actual, type_)
    assert actual == expected
