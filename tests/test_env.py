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
from urllib.parse import quote

import pytest

from environ import Env, Path
from environ.compat import ImproperlyConfigured, DJANGO_POSTGRES
from .asserts import assert_type_and_value
from .fixtures import FakeEnv


class TestEnv:
    def setup_method(self, method):
        """
        Setup environment variables.

        Setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.old_environ = os.environ
        os.environ = Env.ENVIRON = FakeEnv.generateData()
        self.env = Env()

    def teardown_method(self, method):
        """
        Rollback environment variables.

        Teardown any state that was previously setup with a setup_method call.
        """
        assert self.old_environ is not None
        os.environ = self.old_environ

    def test_not_present_with_default(self):
        assert self.env('not_present', default=3) == 3

    @pytest.mark.parametrize(
        'env_file',
        [
            os.path.join(os.path.dirname(__file__), 'test_env.txt'),
            Path(os.path.join(os.path.dirname(__file__), 'test_env.txt')),
            pathlib.Path(__file__).parent.joinpath('test_env.txt'),
            pathlib.Path(__file__).parent / 'test_env.txt'
        ],
    )
    def test_read_env(self, env_file, caplog):
        env = Env()
        with caplog.at_level(logging.DEBUG):
            env.read_env(env_file)
        assert 'Read environment variables from:' in caplog.text

    def test_not_present_without_default(self):
        with pytest.raises(ImproperlyConfigured) as excinfo:
            self.env('not_present')
        assert str(excinfo.value) == 'Set the not_present environment variable'

    def test_contains(self):
        assert 'STR_VAR' in self.env
        assert 'EMPTY_LIST' in self.env
        assert 'I_AM_NOT_A_VAR' not in self.env

    @pytest.mark.parametrize(
        'var,val,multiline',
        [
            ('STR_VAR', 'bar', False),
            ('MULTILINE_STR_VAR', 'foo\\nbar', False),
            ('MULTILINE_STR_VAR', 'foo\nbar', True),
        ],
    )
    def test_str(self, var, val, multiline):
        assert isinstance(self.env(var), str)
        if not multiline:
            assert self.env(var) == val
        assert self.env.str(var, multiline=multiline) == val

    def test_bytes(self):
        assert_type_and_value(bytes, b'bar', self.env.bytes('STR_VAR'))

    def test_int(self):
        assert_type_and_value(int, 42, self.env('INT_VAR', cast=int))
        assert_type_and_value(int, 42, self.env.int('INT_VAR'))

    def test_int_with_none_default(self):
        assert self.env('NOT_PRESENT_VAR', cast=int, default=None) is None

    def test_float(self):
        assert_type_and_value(float, 33.3, self.env('FLOAT_VAR', cast=float))
        assert_type_and_value(float, 33.3, self.env.float('FLOAT_VAR'))

        assert_type_and_value(float, 33.3, self.env('FLOAT_COMMA_VAR', cast=float))
        assert_type_and_value(float, 123420333.3, self.env('FLOAT_STRANGE_VAR1', cast=float))
        assert_type_and_value(float, 123420333.3, self.env('FLOAT_STRANGE_VAR2', cast=float))

    def test_bool_true(self):
        assert_type_and_value(bool, True, self.env('BOOL_TRUE_VAR', cast=bool))
        assert_type_and_value(bool, True, self.env('BOOL_TRUE_VAR2', cast=bool))
        assert_type_and_value(bool, True, self.env.bool('BOOL_TRUE_VAR'))

    def test_bool_false(self):
        assert_type_and_value(bool, False, self.env('BOOL_FALSE_VAR', cast=bool))
        assert_type_and_value(bool, False, self.env('BOOL_FALSE_VAR2', cast=bool))
        assert_type_and_value(bool, False, self.env.bool('BOOL_FALSE_VAR'))

    def test_proxied_value(self):
        assert self.env('PROXIED_VAR') == 'bar'

    def test_int_list(self):
        assert_type_and_value(list, [42, 33], self.env('INT_LIST', cast=[int]))
        assert_type_and_value(list, [42, 33], self.env.list('INT_LIST', int))

    def test_int_tuple(self):
        assert_type_and_value(tuple, (42, 33), self.env('INT_LIST', cast=(int,)))
        assert_type_and_value(tuple, (42, 33), self.env.tuple('INT_LIST', int))
        assert_type_and_value(tuple, ('42', '33'), self.env.tuple('INT_LIST'))

    def test_str_list_with_spaces(self):
        assert_type_and_value(list, [' foo', '  bar'],
                              self.env('STR_LIST_WITH_SPACES', cast=[str]))
        assert_type_and_value(list, [' foo', '  bar'],
                              self.env.list('STR_LIST_WITH_SPACES'))

    def test_empty_list(self):
        assert_type_and_value(list, [], self.env('EMPTY_LIST', cast=[int]))

    def test_dict_value(self):
        assert_type_and_value(dict, FakeEnv.DICT, self.env.dict('DICT_VAR'))

    @pytest.mark.parametrize(
        'value,cast,expected',
        [
            ('a=1', dict, {'a': '1'}),
            ('a=1', dict(value=int), {'a': 1}),
            ('a=1,2,3', dict(value=[str]), {'a': ['1', '2', '3']}),
            ('a=1,2,3', dict(value=[int]), {'a': [1, 2, 3]}),
            ('a=1;b=1.1,2.2;c=3', dict(value=int, cast=dict(b=[float])),
             {'a': 1, 'b': [1.1, 2.2], 'c': 3}),
            ('a=uname;c=http://www.google.com;b=True',
             dict(value=str, cast=dict(b=bool)),
             {'a': "uname", 'c': "http://www.google.com", 'b': True}),
        ],
        ids=[
            'dict',
            'dict_int',
            'dict_str_list',
            'dict_int_list',
            'dict_int_cast',
            'dict_str_cast',
        ],
    )
    def test_dict_parsing(self, value, cast, expected):
        assert self.env.parse_value(value, cast) == expected

    def test_url_value(self):
        url = self.env.url('URL_VAR')
        assert url.__class__ == self.env.URL_CLASS
        assert url.geturl() == FakeEnv.URL
        assert self.env.url('OTHER_URL', default=None) is None

    def test_url_encoded_parts(self):
        password_with_unquoted_characters = "#password"
        encoded_url = "mysql://user:%s@127.0.0.1:3306/dbname" % quote(
            password_with_unquoted_characters
        )
        parsed_url = self.env.db_url_config(encoded_url)
        assert parsed_url['PASSWORD'] == password_with_unquoted_characters

    @pytest.mark.parametrize(
        'var,engine,name,host,user,passwd,port',
        [
            (Env.DEFAULT_DATABASE_ENV, DJANGO_POSTGRES, 'd8r82722',
             'ec2-107-21-253-135.compute-1.amazonaws.com', 'uf07k1',
             'wegauwhg', 5431),
            ('DATABASE_MYSQL_URL', 'django.db.backends.mysql', 'heroku_97681',
             'us-cdbr-east.cleardb.com', 'bea6eb0', '69772142', ''),
            ('DATABASE_MYSQL_GIS_URL', 'django.contrib.gis.db.backends.mysql',
             'some_database', '127.0.0.1', 'user', 'password', ''),
            ('DATABASE_ORACLE_TNS_URL', 'django.db.backends.oracle', 'sid', '',
             'user', 'password', None),
            ('DATABASE_ORACLE_URL', 'django.db.backends.oracle', 'sid', 'host',
             'user', 'password', '1521'),
            ('DATABASE_REDSHIFT_URL', 'django_redshift_backend', 'dev',
             'examplecluster.abc123xyz789.us-west-2.redshift.amazonaws.com',
             'user', 'password', 5439),
            ('DATABASE_SQLITE_URL', 'django.db.backends.sqlite3',
             '/full/path/to/your/database/file.sqlite', '', '', '', ''),
            ('DATABASE_CUSTOM_BACKEND_URL', 'custom.backend', 'database',
             'example.com', 'user', 'password', 5430),
        ],
        ids=[
            'postgres',
            'mysql',
            'mysql_gis',
            'oracle_tns',
            'oracle',
            'redshift',
            'sqlite',
            'custom',
        ],
    )
    def test_db_url_value(self, var, engine, name, host, user, passwd, port):
        config = self.env.db(var)

        assert config['ENGINE'] == engine
        assert config['NAME'] == name
        assert config['HOST'] == host
        assert config['USER'] == user
        assert config['PASSWORD'] == passwd

        if port is None:
            assert 'PORT' not in config
        else:
            assert config['PORT'] == port

    @pytest.mark.parametrize(
        'var,backend,location,options',
        [
            (Env.DEFAULT_CACHE_ENV,
             'django.core.cache.backends.memcached.MemcachedCache',
             '127.0.0.1:11211', None),
            ('CACHE_REDIS', 'django_redis.cache.RedisCache',
             'redis://127.0.0.1:6379/1',
             {'CLIENT_CLASS': 'django_redis.client.DefaultClient',
              'PASSWORD': 'secret'}),
        ],
        ids=[
            'memcached',
            'redis',
        ],
    )
    def test_cache_url_value(self, var, backend, location, options):
        config = self.env.cache_url(var)

        assert config['BACKEND'] == backend
        assert config['LOCATION'] == location

        if options is None:
            assert 'OPTIONS' not in config
        else:
            assert config['OPTIONS'] == options

    def test_email_url_value(self):
        email_config = self.env.email_url()
        assert email_config['EMAIL_BACKEND'] == (
            'django.core.mail.backends.smtp.EmailBackend'
        )
        assert email_config['EMAIL_HOST'] == 'smtp.example.com'
        assert email_config['EMAIL_HOST_PASSWORD'] == 'password'
        assert email_config['EMAIL_HOST_USER'] == 'user@domain.com'
        assert email_config['EMAIL_PORT'] == 587
        assert email_config['EMAIL_USE_TLS']

    def test_json_value(self):
        assert self.env.json('JSON_VAR') == FakeEnv.JSON

    def test_path(self):
        root = self.env.path('PATH_VAR')
        assert_type_and_value(Path, Path(FakeEnv.PATH), root)

    def test_smart_cast(self):
        assert self.env.get_value('STR_VAR', default='string') == 'bar'
        assert self.env.get_value('BOOL_TRUE_VAR', default=True)
        assert self.env.get_value('BOOL_FALSE_VAR', default=True) is False
        assert self.env.get_value('INT_VAR', default=1) == 42
        assert self.env.get_value('FLOAT_VAR', default=1.2) == 33.3

    def test_exported(self):
        assert self.env('EXPORTED_VAR') == FakeEnv.EXPORTED


class TestFileEnv(TestEnv):
    def setup_method(self, method):
        """
        Setup environment variables.

        Setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        super().setup_method(method)

        Env.ENVIRON = {}
        self.env.read_env(
            Path(__file__, is_file=True)('test_env.txt'),
            PATH_VAR=Path(__file__, is_file=True).__root__
        )


class TestSubClass(TestEnv):
    def setup_method(self, method):
        """
        Setup environment variables.

        Setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        super().setup_method(method)

        self.CONFIG = FakeEnv.generateData()

        class MyEnv(Env):
            ENVIRON = self.CONFIG

        self.env = MyEnv()

    def test_singleton_environ(self):
        assert self.CONFIG is self.env.ENVIRON
