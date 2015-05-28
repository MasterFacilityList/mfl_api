import glob

from os import path
from multiprocessing import Pool
from contextlib import closing

from django.core.management import BaseCommand, call_command
from django.conf import settings


def load_data_file(file_path):
    # print file_path
    call_command('bootstrap', file_path)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--setup',
            action='store_true',
            dest='test',
            default=False,
            help='Provide this if you want to load setup data only')

    def handle(self, *args, **options):

        set_data_folder = path.join(
            settings.BASE_DIR, 'data/data/0001_setup_data')
        contacts_data_folder = path.join(
            settings.BASE_DIR, 'data/data/0002_contacts')
        facilities_data_folder = path.join(
            settings.BASE_DIR, 'data/data/0003_facilities')
        chews_data_folder = path.join(
            settings.BASE_DIR, 'data/data/0006_chews')
        fl_data_folder = path.join(
            settings.BASE_DIR, 'data/data/0006_facility_links')
        ward_data_folder = path.join(
            settings.BASE_DIR, 'data/data/0003_wards')
        chul_data_folder = path.join(
            settings.BASE_DIR, 'data/data/0005_chuls')

        def get_json_files(folder):
            json_files = folder + "/*.json"
            data_files = glob.glob(json_files)
            return data_files

        def load_setup_data():
            data_files = get_json_files(set_data_folder)
            with closing(Pool(processes=100)) as pool:
                pool.map(load_data_file, data_files)
            # pool.join()

        def load_contacts_data():
            data_files = get_json_files(contacts_data_folder)
            with closing(Pool(processes=100)) as pool:
                pool.map(load_data_file, data_files)

        def load_wards_data():
            data_files = get_json_files(ward_data_folder)
            with closing(Pool(processes=100)) as pool:
                pool.map(load_data_file, data_files)

        def load_facilities_data():
            data_files = get_json_files(facilities_data_folder)
            with closing(Pool(processes=100)) as pool:
                pool.map(load_data_file, data_files)

        def load_chul_data():
            data_files = get_json_files(chul_data_folder)
            with closing(Pool(processes=100)) as pool:
                pool.map(load_data_file, data_files)

        def load_chews_data():
            data_files = get_json_files(chews_data_folder)
            with closing(Pool(processes=100)) as pool:
                pool.map(load_data_file, data_files)

        def load_facility_throughs_data():
            data_files = get_json_files(fl_data_folder)
            with closing(Pool(processes=100)) as pool:
                pool.map(load_data_file, data_files)

        load_setup_data()
        load_contacts_data()
        load_wards_data()
        load_facilities_data()
        load_chul_data()
        load_chews_data()
        load_facility_throughs_data()
        self.stdout.write("Done loading the data")
