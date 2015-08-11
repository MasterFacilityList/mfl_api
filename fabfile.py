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
    data_files = join(BASE_DIR, 'data/data/0*.json')
    manage('bootstrap', data_files)
    manage('load_groups')
    # Needs to occur after base setup data has been loaded
    load_gis_data()
    manage("createinitialrevisions")
    manage("load_service_groups")


def load_gis_data(*args, **kwargs):
    """Load boundary data from stored GeoJSON files"""
    manage('load_world_boundaries')
    manage('load_kenyan_administrative_boundaries')


def create_search_index(*args, **kwargs):
    """
    Creates the search index in elastic search
    """
    manage('setup_index')


def remove_search_index(*args, **kwargs):
    """
    Deletes the search index in elastic search
    """
    manage('remove_index')


def build_search_index(*args, **kwargs):
    """Creates the entire search index"""
    manage('build_index')


def recreate_search_index(*args, **kwargs):
    remove_search_index()
    create_search_index()
    build_search_index()


def setup_db(*args, **kwargs):
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


def clear_cache():
    local('redis-cli flushall')


def warmup_cache(
        server_location, username, password, client_id, client_secret):
    """Warm up the cache"""
    import requests
    import logging
    logging.basicConfig(level=logging.DEBUG)

    def _get_url(stub):
        return "{}{}".format(server_location, stub)

    def login():
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret
        }
        headers = {
            'Accept': 'application/json'
        }
        resp = requests.request(
            "POST", url=_get_url("/o/token/"), data=data,
            headers=headers
        )
        if resp.status_code == 200:
            data = resp.json()
            return "{} {}".format(data['token_type'], data['access_token'])
        else:
            raise ValueError(resp.content)

    def prod_api(token):
        non_gzipped_headers = {
            'Authorization': token,
            'Accept': 'application/json, */*'
        }
        gzipped_headers = {
            'Authorization': token,
            'Accept': 'application/json, */*',
            'Accept-Encoding': 'gzip'
        }
        urls = [
            "/api/gis/coordinates/",
            "/api/gis/county_boundaries/",
            "/api/gis/ward_boundaries/",
            "/api/gis/constituency_boundaries/",
            "/api/common/filtering_summaries/"
            "/api/facilities/facilities/",
            "/api/facilities/facilities_list/",
            "/api/facilities/facilities_list/?format=excel"
        ]
        for i in urls:
            # warmup non-gzip encoded content
            requests.request(
                "GET", url=_get_url(i), headers=non_gzipped_headers
            )

            # warmup gzip encoded content
            requests.request("GET", url=_get_url(i), headers=gzipped_headers)

    prod_api(login())
