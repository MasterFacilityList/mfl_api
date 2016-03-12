#! /usr/bin/env python
from common.constants import TRUTH_NESS
import json
import os
import datetime
import time
import logging
import math

from filechunkio import FileChunkIO
from config.settings import base
from fabric.api import local
from fabric.context_managers import lcd
from boto.s3.connection import S3Connection
from boto.s3.key import Key


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER = logging.getLogger(__name__)


def manage(command, args=''):
    """Dev only - a convenience"""
    local('{}/manage.py {} {}'.format(BASE_DIR, command, args))


def reset_migrations(*args, **kwargs):
    """Neccessary for circle ci to be able to run tests"""

    del_facility_migrations = ""\
        "cd facilities/migrations && ls | grep -v" \
        "set_facility_code_sequence_min_value.py | xargs rm" \
        "cd common/migrations && ls | grep -v admin_unit_codes.py | xargs rm"

    local(del_facility_migrations)
    local('rm -r chul/migrations')
    local('rm -r mfl_gis/migrations')
    local('rm -r users/migrations')

    manage('makemigrations users')
    manage('makemigrations facilities')
    manage('makemigrations common')
    manage('makemigrations chul')
    manage('makemigrations mfl_gis')


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
    with lcd(os.path.join(BASE_DIR, 'playbooks')):
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
    """Loads data through fixture"""
    manage("loaddata", "mfl_fixture.json")


def load_demo_data_from_scratch(*args, **kwargs):
    """Loads demo data for testing purpose. Do not use this in production"""
    data_files_1 = os.path.join(BASE_DIR, 'data/data/setup/*.json')
    data_files_2 = os.path.join(BASE_DIR, 'data/data/admin_units/*.json')
    data_files_3 = os.path.join(BASE_DIR, 'data/data/v2_data/*.json')
    data_files_4 = os.path.join(BASE_DIR, 'data/data/demo/*.json')
    data_files_5 = os.path.join(BASE_DIR, 'data/data/facilities/*.json')
    data_files_6 = os.path.join(BASE_DIR, 'data/data/geocodes/*.json')
    data_files_7 = os.path.join(BASE_DIR, 'data/data/approvals/*.json')
    data_files_8 = os.path.join(BASE_DIR, 'data/data/last/*.json')
    data_files_11 = os.path.join(BASE_DIR, 'data/data/mcul/*.json')
    data_files_10 = os.path.join(
        BASE_DIR, 'data/data/facility_services/*.json')

    manage('bootstrap', data_files_1)
    manage('bootstrap', data_files_2)
    manage('bootstrap', data_files_3)
    manage('bootstrap', data_files_4)
    manage('bootstrap', data_files_5)
    manage('load_groups')
    manage('sample_users')
    # Needs to occur after base setup data has been loaded
    load_gis_data()
    manage('bootstrap', data_files_6)
    manage('bootstrap', data_files_7)
    manage('bootstrap', data_files_8)
    manage('approve_facilities')
    manage('bootstrap', data_files_10)
    manage('bootstrap', data_files_11)
    manage('update_hours_of_operation')
    manage('link_officers_to_facilities')
    manage("createinitialrevisions")


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
    manage('index_material_records')


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


def migrate(*args, **kwargs):
    """
    Updates the migrations which do not require a database setup
    """
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


def start_celery_worker(*args, **kwargs):
    """
    Starts the celery worker
    """
    local("celery -A config worker -l info")


def start_celery_beat(*args, **kwargs):
    """
    Starts the celery beat to retry indexing failed records and
    resend emails that were not successfully sent to users
    """
    local("celery -A config beat -l info")


def backup_mfl_db(*args, **kwargs):
    """
    Creates a backup of the database
    """

    # generate the backup file
    timestamp = time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    value = value.strftime('%Y-%m-%d-%H-%M-%S')
    file_name = '/tmp/mfl_dump_{0}'.format(value)
    command = 'sudo -u postgres pg_dump mfl > {0}.sql'.format(file_name)
    local(command)
    tar_command = "tar -czf {0}.tar.gz {1}.sql".format(
        file_name, file_name)
    local(tar_command)

    def save_the_db_backup_to_s3():
        # send the file generated to aws s3
        aws_key = os.environ.get('AWS_KEY')
        aws_secret = os.environ.get('AWS_SECRET')
        aws_connection = S3Connection(aws_key, aws_secret)

        try:
            bucket = aws_connection.create_bucket(
                os.environ.get('AWS_DB_BACKUP_BUCKET'))
        except:
            bucket = aws_connection.get_bucket(
                os.environ.get('AWS_DB_BACKUP_BUCKET'))

        k = Key(bucket)
        k.key = "{0}.tar.gz".format(file_name)

        # upload the file in chunks just in case its too big
        source_file_path = os.path.join(BASE_DIR, k.key)
        source_size = os.stat(source_file_path).st_size
        mp = bucket.initiate_multipart_upload(
            os.path.basename(source_file_path))

        chunk_size = 20971520  # 20 MB
        chunk_count = int(math.ceil(source_size / float(chunk_size)))

        for i in range(chunk_count):
            offset = chunk_size * i
            bytes = min(chunk_size, source_size - offset)
            with FileChunkIO(source_file_path, 'r', offset=offset,
                             bytes=bytes) as fp:
                mp.upload_part_from_file(fp, part_num=i + 1)

        mp.complete_upload()

    def test_generated_backup_file(*args, **kwargs):
        # check the file generated does not have errors in it
        no_sudo = True if 'no-sudo' in args else False
        kwargs['sql'] if 'sql' in kwargs else None
        db_name = 'mfl_backup_db'
        db_user = base.DATABASES.get('default').get('USER')
        psql("DROP DATABASE IF EXISTS {0}".format(db_name), no_sudo)
        psql('CREATE DATABASE {0}'.format(db_name), no_sudo)
        psql('CREATE EXTENSION IF NOT EXISTS postgis')
        psql('GRANT ALL on database {0} to {1}'.format(db_name, db_user))
        command = 'sudo -u postgres psql {0} < {1}.sql'.format(
            db_name, file_name)
        local(command)
        psql("DROP DATABASE IF EXISTS {0}".format(db_name), no_sudo)

    def remove_local_files():
        # remove the local files created during the backup process
        local('rm {0}.tar.gz'.format(file_name))
        local('rm {0}.sql'.format(file_name))

    test_generated_backup_file()
    save_the_db_backup_to_s3()
    remove_local_files()


def restore_db(*args, **kwargs):
    """
    Fetches the latest database backup file from AWS and restores it
    """
    # confirm the user wants to restore the database
    confirmation = raw_input(
        "This will remove the existing database and "
        "replace it with the latest backup. "
        "Do you wish to continue? [Y/N] \n"
    )

    # fetch the latest db and restore the db
    if confirmation in TRUTH_NESS:
        aws_key = os.environ.get('AWS_KEY')
        aws_secret = os.environ.get('AWS_SECRET')
        aws_connection = S3Connection(aws_key, aws_secret)
        bucket = aws_connection.get_bucket(
            os.environ.get('AWS_DB_BACKUP_BUCKET'))

        latest_file = reversed([obj for obj in bucket.list()]).next()

        # unzip the file
        LOGGER.info("Downloading the latest backup")
        latest_file.get_contents_to_filename('mfl_db_backup.tar.gz')
        filename = latest_file.key.split('.')[0]
        local('tar -xzf mfl_db_backup.tar.gz {0}.sql'.format(filename))

        db_name = base.DATABASES.get('default').get('NAME')
        no_sudo = True if 'no-sudo' in args else False
        kwargs['sql'] if 'sql' in kwargs else None

        # drop and create the mfl database
        psql("DROP DATABASE IF EXISTS {}".format(db_name), no_sudo)
        psql('CREATE DATABASE {}'.format(db_name), no_sudo)

        # restore the data and structure from the saved file
        command = 'sudo -u postgres psql {0} <{1}.sql'.format(
           db_name, filename)
        local(command)

        # remove the downloaded files
        local('rm {0}.tar.gz'.format('mfl_db_backup'))
        local('rm {0}.sql'.format(filename))
        LOGGER.info("Done")
    else:
        LOGGER.info("Exiting Bye!")
