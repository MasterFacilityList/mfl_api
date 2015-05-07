#! /usr/bin/env python
import json

from os.path import dirname, abspath, join
from config.settings import base
from fabric.api import local
from fabric.context_managers import lcd


BASE_DIR = dirname(abspath(__file__))


def manage(command, args=''):
    """Dev only - a convenience"""
    local('{}/manage.py {} {}'.format(BASE_DIR, command, args))


def test():
    """Dev and release - run the test suite"""
    local('python setup.py check')
    local('pip install tox')
    local('tox -r -c tox.ini')


def deploy():
    """Release only - publish to PyPi"""
    test()
    local('python setup.py sdist upload -r slade')


def server_deploy():
    """Production - run the deployment Ansible playbook"""
    with lcd(join(BASE_DIR, 'playbooks')):
        local(
            "ansible-playbook site.yml -v --extra-vars '{}'".format(
                json.dumps({
                    "base_dir": BASE_DIR,
                    "database_name": base.DATABASES.get('default').get('NAME'),
                    "database_user": base.DATABASES.get('default').get('USER'),
                    "database_password":
                        base.DATABASES.get('default').get('PASSWORD')
                })
            )
        )


def reset_migrations():
    """Development only - remove and recreate all migration"""
    for app_name in base.LOCAL_APPS:
        local('rm -f {}/migrations/ -r'.format(app_name))

    for app_name in base.LOCAL_APPS:
        manage('makemigrations {}'.format(app_name))

    local('git add . --all')


def graph_models():
    """Dev only - visualize the current model relationships"""
    manage(
        'graph_models common facilities chul mfl_gis -d '
        '-x=created,updated,created_by,updated_by -E -X=AbstractBase '
        '-o  mfl_models_graph.png')
    local('eog mfl_models_graph.png')


def psql(query, no_sudo=False, is_file=False):
    """Dev only - used by the setup function below"""
    sudo = 'sudo -u postgres'
    if no_sudo:
        sudo = ''

    if is_file:
        local('{} psql < {}'.format(sudo, query))
    else:
        local('{} psql -c "{}"'.format(sudo, query))


def load_demo_data(*args, **kwargs):
    """Loads demo data for testing purpose. Do not use this in production"""
    data_files = join(BASE_DIR, 'data/data/*')
    data_files = '/home/titan/savannah/mfl_api/0015_regulation_statuses.json'

    manage('bootstrap', data_files)


def load_gis_data(*args, **kwargs):
    """Load boundary data from stored GeoJSON files"""
    manage('load_world_boundaries')
    manage('load_kenyan_administrative_boundaries')


def create_search_index(*args, **kwargs):
    """
    Creates the search index in elastic search
    """
    manage('setup_index')


def create_entire_index(*args, **kwargs):
    """Creates the entire search index"""
    manage('build_index')


def setup(*args, **kwargs):
    """Dev only - clear and recreate the entire database"""
    # needs to come first to as to index data as it is being loaded
    create_search_index()
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
    manage('migrate')

    if base.DEBUG:
        load_demo_data()
        create_entire_index()

    # Needs to occur after base setup data has been loaded
    load_gis_data()
