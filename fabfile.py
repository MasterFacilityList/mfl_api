#! /usr/bin/env python
from os.path import dirname, abspath
from config.settings import base
from fabric.api import local


BASE_DIR = dirname(abspath(__file__))


def manage(command, args=''):
    local('{}/manage.py {} {}'.format(BASE_DIR, command, args))


def test():
    local('python setup.py check')
    local('pip install tox')
    local('tox -r -c tox.ini')


def run():
    local('{}/manage.py runserver 8000'.format(BASE_DIR))


def deploy():
    """
    Should be run only by the release manager
    """
    test()
    local('python setup.py sdist upload -r slade')


def psql(query, no_sudo=False, is_file=False):
    sudo = 'sudo -u postgres'
    if no_sudo:
        sudo = ''

    if is_file:
        local('{} psql < {}'.format(sudo, query))
    else:
        local('{} psql -c "{}"'.format(sudo, query))


def setup(*args, **kwargs):
    no_sudo = True if 'no-sudo' in args else False
    kwargs['sql'] if 'sql' in kwargs else None
    db_name = base.DATABASES.get('default').get('NAME')
    db_user = base.DATABASES.get('default').get('USER')
    db_pass = base.DATABASES.get('default').get('PASSWORD')

    psql("DROP DATABASE IF EXISTS {}".format(db_name), no_sudo)
    psql("DROP USER IF EXISTS {}".format(db_user), no_sudo)
    psql("CREATE USER {0} WITH SUPERUSER CREATEDB "
         "CREATEROLE LOGIN PASSWORD '{1}'".format(db_user, db_pass), no_sudo)
    psql('CREATE DATABASE {}'.format(db_name), no_sudo)
    psql('CREATE EXTENSION postgis')
    psql('CREATE EXTENSION postgis_topology')
    manage('migrate users')
    manage('migrate')
