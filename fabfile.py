from os.path import dirname, abspath

from fabric.api import local
from fabric.api import lcd


BASE_DIR = dirname(abspath(__file__))


def manage(command, args=''):
    local('{}/manage.py {} {}'.format(BASE_DIR, command, args))


def test():
    with lcd(BASE_DIR):
        local('pip install tox')
        local('tox')


def run():
    local('{}/manage.py runserver 8000'.format(BASE_DIR))


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
    bootstrap_sql = kwargs['sql'] if 'sql' in kwargs else None
    psql("DROP DATABASE IF EXISTS mfl", no_sudo)
    psql("DROP USER IF EXISTS mfl", no_sudo)
    psql("CREATE USER mfl WITH SUPERUSER CREATEDB "
         "CREATEROLE LOGIN PASSWORD 'mfl'", no_sudo)
    psql('CREATE DATABASE mfl', no_sudo)
    manage('migrate')
