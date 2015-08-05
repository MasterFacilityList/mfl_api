import os
import json
import logging

from django.conf import settings
from django.template import loader, Context

import sqlalchemy as sa


DEFAULT_DB = "mssql+pyodbc://mfl:Saitan2@192.168.56.101:1433/tiba_public?driver=freetds"  # NOQA
LOGGER = logging.getLogger(__name__)


class Database(object):
    def _init__(self, connection_string=DEFAULT_DB):
        self.engine = sa.engine(connection_string)

    def read_db_object(self, sql):
        return self.engine.execute(sql)


class CreateJsonFiles(object):
    """
    A class that creates the json data files from MFL version 1.

    These data files will be consumed in data bootstrap where
    they will be loaded into the db.
    """
    database = Database()

    def _help_create_file(
            self, folder_type, file_name, model_name, unique_fields, data):
        """
        Helper method to create json files

        Removes a file if it exists and recreates it again
        """
        file_path = os.path.join(folder_type, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w+') as json_file:
            template = loader.get_template('json_file_template.txt')
            context = Context(
                {
                    "model_name": model_name,
                    "unique_fields": unique_fields,
                    "data": data
                }
            )
            json_data = template.render(context)
            json_file.write(json.dumps(json_data))

    def create_single_json_file(
            self, file_name, folder, model_name, unique_fields, data,
            in_v1=True):
        """
        Creates a single json file
        """
        demo_folder = os.path.join(settings.BASE_DIR, "data/new_data/demo")
        setup_folder = os.path.join(settings.BASE_DIR, "data/new_data/setup")
        if folder == "demo":
            self._help_create_file(
                demo_folder, file_name, model_name, unique_fields, data)
        elif folder == "setup":
            self._help_create_file(
                setup_folder, file_name, model_name, unique_fields, data)
        else:
            LOGGER.error("The folder was given does not exist")

    def create_job_titles_json(self):
        file_name = "0000_job_titles.json"
        folder = "setup"
        model_name = "facilities.JobTitle"
        unique_fields = ["name"]
        data = []
        self.create_single_json_file(
            file_name, folder, model_name, unique_fields, data)

    def create_contact_types(self):
        file_name = "0001_contact_types.json"
        folder = "setup"
        model_name = "common.ContactType"
        unique_fields = ["name"]
        data = [
            {
                "name": "EMAIL"
            },
            {
                "name": "MOBILE"
            },
            {
                "name": "LANDLINE"
            },
            {
                "name": "FAX"
            },
            {
                "name": "POSTAL"
            }
        ]
        self.create_single_json_file(
            file_name, folder, model_name, unique_fields, data, in_v1=False)

    def create_counties(self):
        pass

    def create_contituencies():
        pass

    def create_ged_code_methods():
        pass

    def create_facility_operation_status(self):
        pass

    def create_service_categories(self):
        pass

    def create_wards(self):
        pass

    def create_geo_code_source(self):
        pass
