# This file is part of the django-environ-2.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (C) 2013-2021 Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import os
import sys

import pytest

from environ import Path
from environ.compat import ImproperlyConfigured


def test_str(volume):
    root = Path('/home')

    if sys.platform == 'win32':
        assert str(root) == f'{volume}home'
        assert str(root()) == f'{volume}home'
        assert str(root('dev')) == f'{volume}home\\dev'
    else:
        assert str(root) == '/home'
        assert str(root()) == '/home'
        assert str(root('dev')) == '/home/dev'


def test_path_class():
    root = Path(__file__, '..', is_file=True)
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

    assert root() == root_path
    assert root.__root__ == root_path

    web = root.path('public')
    assert web() == os.path.join(root_path, 'public')
    assert web('css') == os.path.join(root_path, 'public', 'css')


def test_repr(volume):
    root = Path('/home')
    if sys.platform == 'win32':
        assert root.__repr__() == f'<Path:{volume}home>'
    else:
        assert root.__repr__() == '<Path:/home>'


def test_comparison():
    root = Path('/home')
    assert root.__eq__(Path('/home'))
    assert root in Path('/')
    assert root not in Path('/other/path')

    assert Path('/home') == Path('/home')
    assert Path('/home') != Path('/home/dev')

    assert Path('/home/foo/').rfind('/') == str(Path('/home/foo')).rfind('/')
    assert Path('/home/foo/').find('/home') == \
           str(Path('/home/foo/')).find('/home')
    assert Path('/home/foo/')[1] == str(Path('/home/foo/'))[1]
    assert Path('/home/foo/').__fspath__() == str(Path('/home/foo/'))
    assert ~Path('/home') == Path('/')


def test_concatenation():
    """Make sure Path correct handle __add__."""
    assert Path('/') + Path('/home') == Path('/home')
    assert Path('/') + Path('/home/public') == Path('/home/public')

    assert Path('/') + 'home' == Path('/home')
    assert Path('/') + '/home/public' == Path('/home/public')


def test_subtraction():
    """Make sure Path correct handle __sub__."""
    assert Path('/home/dev/public') - 2 == Path('/home')
    assert Path('/home/dev/public') - 'public' == Path('/home/dev')


def test_subtraction_not_int():
    """Subtraction with an invalid type should raise TypeError."""
    with pytest.raises(TypeError) as excinfo:
        Path('/home/dev/') - 'not int'
    assert str(excinfo.value) == (
        "unsupported operand type(s) for -: '<class 'environ.environ.Path'>' "
        "and '<class 'str'>' unless value of <class 'environ.environ.Path'> "
        "ends with value of <class 'str'>"
    )


def test_required_path():
    root = Path('/home')
    with pytest.raises(ImproperlyConfigured) as excinfo:
        root('dev', 'not_existing_dir', required=True)
    assert "Create required path:" in str(excinfo.value)

    with pytest.raises(ImproperlyConfigured) as excinfo:
        Path('/not/existing/path/', required=True)
    assert "Create required path:" in str(excinfo.value)


def test_complex_manipulation(volume):
    root = Path('/home')
    public = root.path('public')
    assets, scripts = public.path('assets'), public.path('assets', 'scripts')

    if sys.platform == 'win32':
        assert public.__repr__() == f'<Path:{volume}home\\public>'
        assert str(public.root) == f'{volume}home\\public'
        assert str(public('styles')) == f'{volume}home\\public\\styles'
        assert str(assets.root) == f'{volume}home\\public\\assets'
        assert str(scripts.root) == f'{volume}home\\public\\assets\\scripts'

        assert (~assets).__repr__() == f'<Path:{volume}home\\public>'
        assert str(assets + 'styles') == (
            f'{volume}home\\public\\assets\\styles'
        )
        assert (assets + 'styles').__repr__() == (
            f'<Path:{volume}home\\public\\assets\\styles>'
        )
    else:
        assert public.__repr__() == '<Path:/home/public>'
        assert str(public.root) == '/home/public'
        assert str(public('styles')) == '/home/public/styles'
        assert str(assets.root) == '/home/public/assets'
        assert str(scripts.root) == '/home/public/assets/scripts'

        assert str(assets + 'styles') == '/home/public/assets/styles'
        assert (~assets).__repr__() == '<Path:/home/public>'
        assert (assets + 'styles').__repr__() == (
            '<Path:/home/public/assets/styles>'
        )
