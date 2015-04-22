#! /usr/bin/env python
from os.path import dirname, abspath, join
from config.settings import base
from fabric.api import local
from fabric.context_managers import lcd


BASE_DIR = dirname(abspath(__file__))


def manage(command, args=''):
    local('{}/manage.py {} {}'.format(BASE_DIR, command, args))


def test():
    local('python setup.py check')
    local('pip install tox')
    local('tox -r -c tox.ini')


def run():
    local('gunicorn -w 3 config.wsgi')


def deploy():
    """
    Should be run only by the release manager
    """
    test()
    local('python setup.py sdist upload -r slade')


def server_deploy():
    """
    Deploy to the staging and prod servers
    """
    with lcd(join(BASE_DIR, 'playbooks')):
        local(
            'ansible-playbook site.yml -v --extra-vars "base_dir={}"'.format(
                BASE_DIR
            )
        )


def reset_migrations():
    """
    A development only task; got sick of typing the same commands repeatedly
    """
    local('rm -f users/migrations/ -r')
    local('rm -f common/migrations/ -r')
    local('rm -f facilities/migrations/ -r')
    manage('makemigrations users')
    manage('makemigrations common')
    manage('makemigrations facilities')
    local('git add . --all')


def graph_models():
    """Another dev only task"""
    manage(
        'graph_models common facilities -g -d '
        '-x=created,updated,created_by,updated_by -E -X=AbstractBase '
        '-o  mfl_models_graph.png')
    local('eog mfl_models_graph.png')


def psql(query, no_sudo=False, is_file=False):
    sudo = 'sudo -u postgres'
    if no_sudo:
        sudo = ''

    if is_file:
        local('{} psql < {}'.format(sudo, query))
    else:
        local('{} psql -c "{}"'.format(sudo, query))


def setup(*args, **kwargs):
    """Do not use this in production!"""
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
    psql('CREATE EXTENSION IF NOT EXISTS postgis')
    manage('migrate users')
    manage('migrate')
