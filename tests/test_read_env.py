# This file is part of the django-environ-2.
#
# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
# Copyright (C) 2013-2021 Daniele Faraglia <daniele.faraglia@gmail.com>
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import logging
import os
import pathlib

import pytest

from environ import Env, Path


def test_read_env_priority(simple_env_file, monkeypatch):
    """Values obtained from the os.environ should have a higher priority."""
    monkeypatch.setenv('EMAIL', 'dev@acme.localhost')

    env = Env()
    env.read_env(simple_env_file)

    # In env_file: EMAIL=sales@acme.com
    assert os.environ['EMAIL'] == 'dev@acme.localhost'


def test_read_env_overrides(env_file):
    """Additional keywords should be added to the environment."""
    env = Env()

    assert 'SECRET' not in env.ENVIRON
    assert 'SECRET' not in os.environ

    env.read_env(env_file=env_file, SECRET='top_secret')

    assert env.ENVIRON['SECRET'] == 'top_secret'
    assert os.environ['SECRET'] == 'top_secret'


def test_read_env_override_os(env_file, monkeypatch):
    """Additional keywords should override vars from the os.environ."""
    monkeypatch.setenv('SECRET_KEY', 'enigma')
    env = Env()

    env.read_env(env_file=env_file, SECRET_KEY='top_secret')

    assert env.ENVIRON['SECRET_KEY'] == 'top_secret'
    assert os.environ['SECRET_KEY'] == 'top_secret'


@pytest.mark.parametrize(
    'file_path',
    [
        os.path.join(os.path.dirname(__file__), 'test_env.txt'),
        Path(os.path.join(os.path.dirname(__file__), 'test_env.txt')),
        pathlib.Path(__file__).parent.joinpath('test_env.txt'),
        pathlib.Path(__file__).parent / 'test_env.txt'
    ],
)
def test_read_env(file_path, caplog):
    """Ability to use environ.Path, pathlib.Path or just string in read_env."""
    env = Env()
    with caplog.at_level(logging.DEBUG):
        env.read_env(file_path)
    assert 'Read environment variables from:' in caplog.text


def test_read_env_no_file(caplog):
    """Log warning if there is no env file."""
    env = Env()

    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'environ.tests.settings'
    )

    with caplog.at_level(logging.WARN):
        env.read_env(env_file=None)
    expected_message = (
        "Environment file doesn't exist - if you're not configuring "
        "your environment separately, create one."
    )
    assert expected_message in caplog.text


def test_read_and_overwrite_env(simple_env_file, monkeypatch):
    """Make sure we able overwrite existing environment variables."""
    monkeypatch.setenv('DB_NAME', 'user')
    monkeypatch.setenv('DB_USER', 'password')

    env = Env()

    env.read_env(env_file=simple_env_file, overwrite=True)

    assert os.environ['DB_NAME'] == 'dev_db'
    assert os.environ['DB_USER'] == 'dev_user'
