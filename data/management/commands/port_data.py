#!/usr/bin/env python

import os
import json
import logging

from django.conf import settings
from django.template import loader, Context

import sqlalchemy as sa


DEFAULT_DB = "mssql+pyodbc://mfl:Saitan2@192.168.56.101:1433/tiba_public?driver=freetds"  # NOQA
LOGGER = logging.getLogger(__name__)

BASE_DIR = '/home/titan/savannah/mfl_api'


class Database(object):
    def _init__(self, connection_string=DEFAULT_DB):
        self.engine = sa.create_engine(connection_string)

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
            json_file.write(json_data)

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


SETUP_DATA_CONFIG = [
    {
        "resource_name": "Job Titles",
        "mfl_v1_object_name": "lkpJobTitles",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "ttlShortName",
                "v2": "abbreviation",
                "v1_pos": 1
            },
            {
                "v1": "ttlName",
                "v2": "name",
                "v1_pos": 2
            }
        ],
        "file_name": "0000_job_titles.json",
        "folder": "setup",
        "model_name": "facilities.JobTitle",
        "unique_fields": ['name'],
        "data": []
    },
    {
        "resource_name": "Contact Types",
        "mfl_v1_object_name": "N/A",
        "mfl_v1_v2_fields_map": [],
        "file_name": "0001_contact_types.json",
        "folder": "setup",
        "model_name": "common.ContactType",
        "unique_fields": ["name"],
        "data": [
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
    },
    {
        "resource_name": "Facility Operation Statuses",
        "mfl_v1_object_name": "lkpFacilityStatus",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "staShortName",
                "v1_pos": 1,
                "v2": "name"
            }
        ],
        "file_name": "0002_facility_operation_status.json",
        "folder": "setup",
        "model_name": "facilities.FacilityStatus",
        "unique_fields": ["name"],
        "data": []
    },
    {
        "resource_name": "Facility Types",
        "mfl_v1_object_name": "lkpFacilityTypes",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "typName",
                "v2": "name",
                "v1_pos": 1
            },
            {
                "v1": "typShortName",
                "v2": "abbreviation",
                "v1_pos": 2
            }
        ],
        "file_name": "0003_facility_types.json",
        "folder": "setup",
        "model_name": "facilities.RE",
        "unique_fields": ["name"],
        "data": []
    },
    {
        "resource_name": "Facility Owner Types",
        "mfl_v1_object_name": "lkpFacilityOwners",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "ownName",
                "v2": "name",
                "v1_pos": 1
            },
            {
                "v1": "ownShortName",
                "v2": "abbreviation",
                "v1_pos": 2
            }
        ],
        "file_name": "0004_facility_owner_types.json",
        "folder": "setup",
        "model_name": "facility.OwnerType",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT * from lkpFacilityOwners where ownId > 99",
    },
    {
        "resource_name": "Facility Owners",
        "mfl_v1_object_name": "lkpFacilityOwners",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "ownName",
                "v2": "name",
                "v1_pos": 1
            },
            {
                "v1": "ownShortName",
                "v2": "abbreviation",
                "v1_pos": 2
            },
            {
                "v1": "ownName",
                "v2": "owner_type",
                "v1_pos": 2,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0005_facility_owners.json",
        "folder": "setup",
        "model_name": "facility.Owner",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT * from lkpFacilityOwners where ownId < 100",
    },
    {
        "resource_name": "Regulators",
        "mfl_v1_object_name": "lkpRegulators",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "regName",
                "v1_pos": 2,
                "v2": "name"
            },
            {
                "v1": "regshortName",
                "v1_pos": 1,
                "v2": "abbreviation"
            },
            {
                "v1": "regFunctionVerb",
                "v1_pos": 8,
                "v2": "regulation_verb"
            },
            {
                "v1": "regDefaultStatus",
                "v1_pos": 6,
                "v2": "default_status",
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }

        ],
        "file_name": "0006_regulatory_bodies.json",
        "folder": "setup",
        "model_name": "facility.RegulatingBody",
        "unique_fields": ["name"],
        "data": []
    },
    {
        "resource_name": "KEPH levels",
        "mfl_v1_object_name": "lkpKephLevels",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "kphName",
                "v1_pos": 2,
                "v2": "name"
            }
        ],
        "file_name": "0007_keph_levels.json",
        "folder": "setup",
        "model_name": "facility.OwnerType",
        "unique_fields": ["name"],
        "data": []
    },
    {
        "resource_name": "Geo CodeMethods",
        "mfl_v1_object_name": "lkpGeoCodeMethod",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "geoName",
                "v1_pos": 2,
                "v2": "name"
            }
        ],
        "file_name": "0008_geo_code_methods.json",
        "folder": "setup",
        "model_name": "mfl_gis.GeoCodeMethod",
        "unique_fields": ["name"],
        "data": []
    },
    {
        "resource_name": "Geo CodeSources",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Source_of_Geo_Code",
                "v1_pos": 0,
                "v2": "name"
            }
        ],
        "file_name": "0009_geo_code_sources.json",
        "folder": "setup",
        "model_name": "mfl_gis.GeoCodeMethod",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT DISTINCT Source_of_GeoCode from qryFacilities"
    },
    {
        "resource_name": "Regulation Statuses",
        "database": "mssql+pyodbc://mfl:Saitan2@192.168.56.101:1433/tiba_regulator?driver=freetds", # NOQA
        "mfl_v1_object_name": "lkpRegulatorStatus",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "regStatusName",
                "v1_pos": 1,
                "v2": "name"
            }
        ],
        "file_name": "0010_regulatory_statuses.json",
        "folder": "setup",
        "model_name": "facilities.RegulationStatus",
        "unique_fields": ["name"],
        "data": []
    },
    {
        "resource_name": "Counties",
        "mfl_v1_object_name": "N/A",
        "mfl_v1_v2_fields_map": [],
        "file_name": "0011_counties.json",
        "folder": "setup",
        "model_name": "common.County",
        "unique_fields": ["code"],
        "data": [],
        "data_file_path": os.path.join(
            settings.BASE_DIR, 'data/data/0001_counties.json')
    },
    {
        "resource_name": "Constituencies",
        "mfl_v1_object_name": "N/A",
        "mfl_v1_v2_fields_map": [],
        "file_name": "0012_constituencies.json",
        "folder": "setup",
        "model_name": "common.Constituency",
        "unique_fields": ["code"],
        "data": [],
        "data_file_path": os.path.join(
            settings.BASE_DIR, 'data/data/0002_constituencies.json')
    },
    {
        "resource_name": "Wards",
        "mfl_v1_object_name": "N/A",
        "mfl_v1_v2_fields_map": [],
        "file_name": "0013_wards.json",
        "folder": "setup",
        "model_name": "common.Ward",
        "unique_fields": ["code"],
        "data": [],
        "data_file_path": os.path.join(
            settings.BASE_DIR, 'data/data/0009_wards.json')
    },
    {
        "resource_name": "Towns",
        "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Facility_Nearest_Town",
                "v2": "name",
                "v1_pos": 0
            }
        ],
        "file_name": "0014_towns.json",
        "folder": "demo",
        "model_name": "common.Town",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT Facility_Nearest_Town from tblFacilities"
    },
    {
        "resource_name": "physical addresses",
        "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Facility_Nearest_Town",
                "v2": "town",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]

            },
            {
                "v1": "Facility_Plot_Number",
                "v2": "plot_number",
                "v1_pos": 1
            },
            {
                "v1": "Location_Description",
                "v2": "location_desc",
                "v1_pos": 2

            }
        ],
        "file_name": "0015_physical_addresses.json",
        "folder": "demo",
        "model_name": "common.PhysicalAddress",
        "unique_fields": ["name"],
        "data": [],
        "select": "SELECT Facility_Nearest_Town, Facility_Plot_Number, Location_Description from tblFacilities"  # NOQA
    },
    {
        "resource_name": "Facilities",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Facility_Code",
                "v2": "code",
                "v1_pos": 0
            },
            {
                "v1": "Facility_Name",
                "v2": "name",
                "v1_pos": 1
            },
            {
                "v1": "Facility_Official_Name",
                "v2": "official_name",
                "v1_pos": 2
            },
            {
                "v1": "many fields",
                "v2": "physical_address",
                "v1_pos": 3,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            },
            {
                "v1": "Date_Added",
                "v2": "created",
                "v1_pos": 8
            },
            {
                "v1": "Date_Modified",
                "v2": "updated",
                "v1_pos": 9
            },
            {
                "v1": "Num_Bed",
                "v2": "number_of_beds",
                "v1_pos": 10
            },
            {
                "v1": "Num_Cots",
                "v2": "number_of_cots",
                "v1_pos": 11
            },
            {
                "v1": "typName",
                "v2": "facility_type",
                "v1_pos": 12,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            },
            {
                "v1": "ownName",
                "v2": "owner",
                "v1_pos": 13,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            },
            {
                "v1": "kphName",
                "v2": "keph_level",
                "v1_pos": 14,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            },
            {
                "v1": "regName",
                "v2": "regulatory_body",
                "v1_pos": 15,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            },
            {
                "v1": "staDisplayName",
                "v2": "operation_status",
                "v1_pos": 15,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }


        ],
        "file_name": "0016_facilities.json",
        "folder": "setup",
        "model_name": "common.Ward",
        "unique_fields": ["code", "name"],
        "data": [],
        "sql": ("SELECT Facility_Code, Facility_Code, Facility_Name,"
            "Facility_Official_Name, Facility_Nearest_Town,"
            "Facility_Plot_Number, Location_Description, Open24Hours,"
            "OpenWeekends, Date_Added, Date_Modified, Num_Beds, Num_Cots,"
            "typName, ownName, kphName, regName,"
            "staDisplayName from qryFacilities")
    },
    {
        "resource_name": "Services Categories",
        "mfl_v1_object_name": "lkpFacilityServices",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "svcName",
                "v2": "name",
                "v1_pos": 1
            },
            {
                "v1": "svcShortName",
                "v2": "abbreviation",
                "v1_pos": 2
            }
        ],
        "file_name": "0017_services.json",
        "folder": "demo",
        "model_name": "facilities.ServiceCategory",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT svcId,svcName,svcShortName, svcParent from lkpFacilityServices  WHERE svcParent = 0"  # NOQA
    },
    {
        "resource_name": "Services",
        "mfl_v1_object_name": "lkpFacilityServices",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "svcName",
                "v2": "name",
                "v1_pos": 1
            },
            {
                "v1": "svcShortName",
                "v2": "abbreviation",
                "v1_pos": 2
            },
            {
                "v1": "svcParent",
                "v2": "category",
                "v1_pos": 3,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0017_services.json",
        "folder": "demo",
        "model_name": "facilities.Service",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT svcId, svcName,svcShortName,svcParent from lkpFacilityServices  WHERE svcId <> 0"  # NOQA
    },
    {
        "resource_name": "Facility Email Contacts non linked",
         "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Official_Email",
                "v2": "contact",
                "v1_pos": 0
            },
            {
                "v1": "N/A",
                "v2": "contact_type",
                "v1_pos": 0,
                "v2_value": "EMAIL",
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0018_facility_emails_contacts.json",
        "folder": "demo",
        "model_name": "common.Contact",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT Official_Email from tblFacilities where Official_Email <> NULL"  # NOQA
    },
    {
        "resource_name": "Facility Email Contacts linked",
        "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Facility_Code",
                "v2": "facility",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "code"
                    }
                ]
            },
            {
                "v1": "Official_Email",
                "v2": "contact",
                "v1_pos": 1,
                "fk_map": [
                    {
                        "field_name": "contact"
                    }
                ]
            }
        ],
        "file_name": "0019_facility_emails_contacts_linked.json",
        "folder": "demo",
        "model_name": "facilities.FacilityContact",
        "unique_fields": ["facility", "contact"],
        "data": [],
        "sql": "SELECT Facility_Code, Official_Email from tblFacilities where Official_Email <> NULL"  # NOQA
    },
    {
        "resource_name": "Facility Landline Contacts non linked",
         "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Official_Landline",
                "v2": "contact",
                "v1_pos": 0
            },
            {
                "v1": "N/A",
                "v2": "contact_type",
                "v1_pos": 0,
                "v2_value": "LANDLINE",
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0020_facility_landline_contacts.json",
        "folder": "demo",
        "model_name": "common.Contact",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT Official_Landline from tblFacilities WHERE Official_Landline <> NULL"  # NOQA
    },
    {
        "resource_name": "Facility Landline Contacts linked",
        "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Facility_Code",
                "v2": "facility",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "code"
                    }
                ]
            },
            {
                "v1": "Official_Landline",
                "v2": "contact",
                "v1_pos": 1,
                "fk_map": [
                    {
                        "field_name": "contact"
                    }
                ]
            }
        ],
        "file_name": "0021_facility_landline_contacts_linked.json",
        "folder": "demo",
        "model_name": "facilities.FacilityContact",
        "unique_fields": ["facility", "contact"],
        "data": [],
        "sql": "SELECT Facility_Code, Official_Landline from tblFacilities WHERE Official_Landline <> NULL"  # NOQA
    },
    {
        "resource_name": "Facility FAX Contacts non linked",
         "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Official_Fax",
                "v2": "contact",
                "v1_pos": 0
            },
            {
                "v1": "N/A",
                "v2": "contact_type",
                "v1_pos": 0,
                "v2_value": "FAX",
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0022_facility_fax_contacts.json",
        "folder": "demo",
        "model_name": "common.Contact",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT Official_Fax from tblFacilities WHERE Official_Fax <> NULL"  # NOQA
    },
    {
        "resource_name": "Facility FAX Contacts linked",
        "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Facility_Code",
                "v2": "facility",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "code"
                    }
                ]
            },
            {
                "v1": "Official_Fax",
                "v2": "contact",
                "v1_pos": 1,
                "fk_map": [
                    {
                        "field_name": "contact"
                    }
                ]
            }
        ],
        "file_name": "0023_facility_fax_contacts_linked.json",
        "folder": "demo",
        "model_name": "facilities.FacilityContact",
        "unique_fields": ["facility", "contact"],
        "data": [],
        "sql": "SELECT Facility_Code, Official_Fax from tblFacilities where Official_Fax <> NULL"  # NOQA
    },
    {
        "resource_name": "Facility MOBILE Contacts non linked",
         "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Official_MOILE",
                "v2": "contact",
                "v1_pos": 0
            },
            {
                "v1": "N/A",
                "v2": "contact_type",
                "v1_pos": 0,
                "v2_value": "MOBILE",
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0024_facility_mobile_contacts.json",
        "folder": "demo",
        "model_name": "common.Contact",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT Official_Mobile from tblFacilities WHERE Official_Mobile <> NULL"  # NOQA
    },
    {
        "resource_name": "Facility MOBILE Contacts linked",
        "mfl_v1_object_name": "tblFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "Facility_Code",
                "v2": "facility",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "code"
                    }
                ]
            },
            {
                "v1": "Official_Mobile",
                "v2": "contact",
                "v1_pos": 1,
                "fk_map": [
                    {
                        "field_name": "contact"
                    }
                ]
            }
        ],
        "file_name": "0025_facility_mobile_contacts_linked.json",
        "folder": "demo",
        "model_name": "facilities.FacilityContact",
        "unique_fields": ["facility", "contact"],
        "data": [],
        "sql": "SELECT Facility_Code, Official_Mobile from tblFacilities WHERE Official_Mobile <> NULL"  # NOQA
    },
    {
        "resource_name": "Officers",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "In_Charge_Name",
                "v2": "name",
                "v1_pos": 0
            },
            {
                "v1": "In_Charge_National_ID",
                "v2": "id_number",
                "v1_pos": 2
            },
            {
                "v1": "ttlName",
                "v2": "job_title",
                "v1_pos": 1,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0026_officers.json",
        "folder": "demo",
        "model_name": "facilities.Officer",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT In_Charge_Name,ttlName, In_Charge_National_ID from qryFacilities WHERE In_Charge_Name <> NULL"   # NOQA
    },
    {
        "resource_name": "Facility Officers",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "In_Charge_Name",
                "v2": "name",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "officer"
                    }
                ]
            },
             {
                "v1": "Facility_Code",
                "v2": "facility",
                "v1_pos": 3,
                "fk_map": [
                    {
                        "field_name": "code"
                    }
                ]
            }

        ],
        "file_name": "0027_facility_officers.json",
        "folder": "demo",
        "model_name": "facilities.FacilityOfficer",
        "unique_fields": ["name"],
        "data": [],
        "sql": "SELECT In_Charge_Name,ttlName, In_Charge_National_ID, Facility_Code from qryFacilities WHERE In_Charge_Name <> NULL AND Facility_Code <> NULL"   # NOQA
    },
    {
        "resource_name": "Officer Mobile Non Linked",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "In_Charge_Mobile",
                "v1_pos": 0,
                "v2": "contact"
            },
            {
                "v1": "N/A",
                "v2": "contact_type",
                "v1_pos": 0,
                "v2_value": "MOBILE",
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0028_officer_mobile_contacts.json",
        "folder": "demo",
        "model_name": "common.Contact.",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT In_Charge_Mobile from qryFacilities WHERE In_Charge_Name <> NULL and In_Charge_Mobile <> NULL"   # NOQA
    },
    {
        "resource_name": "Officer Mobile  Linked",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "In_Charge_Mobile",
                "v2": "contact",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "contact"
                    }
                ]
            },
            {
                "v1": "In_Charge_Name",
                "v2": "officer",
                "v1_pos": 1,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0029_officer_mobile_contacts_linked.json",
        "folder": "demo",
        "model_name": "facilities.OfficerContact.",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT In_Charge_Mobile, In_Charge_Name from qryFacilities WHERE In_Charge_Name <> NULL and In_Charge_Mobile <> NULL"   # NOQA
    },
    {
        "resource_name": "Officer EMAIL Non Linked",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "In_Charge_EMAIL",
                "v1_pos": 0,
                "v2": "contact"
            },
            {
                "v1": "N/A",
                "v2": "contact_type",
                "v1_pos": 0,
                "v2_value": "EMAIL",
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0030_officer_email_contacts.json",
        "folder": "demo",
        "model_name": "common.Contact.",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT In_Charge_EMAIL from qryFacilities WHERE In_Charge_Name <> NULL and In_Charge_EMAIL <> NULL"   # NOQA
    },
    {
        "resource_name": "Officer EMAIL  Linked",
        "mfl_v1_object_name": "qryFacilities",
        "mfl_v1_v2_fields_map": [
            {
                "v1": "In_Charge_Email",
                "v2": "contact",
                "v1_pos": 0,
                "fk_map": [
                    {
                        "field_name": "contact"
                    }
                ]
            },
            {
                "v1": "In_Charge_Name",
                "v2": "officer",
                "v1_pos": 1,
                "fk_map": [
                    {
                        "field_name": "name"
                    }
                ]
            }
        ],
        "file_name": "0031_officer_email_contacts_linked.json",
        "folder": "demo",
        "model_name": "facilities.OfficerContact.",
        "unique_fields": ["contact", "contact_type"],
        "data": [],
        "sql": "SELECT In_Charge_Email, In_Charge_Name from qryFacilities WHERE In_Charge_Name <> NULL and In_Charge_Email <> NULL"   # NOQA
    },


]


def port_data():
    create_engine = CreateJsonFiles()
    print "Fetching data from mfl_v1"
    for resource in SETUP_DATA_CONFIG:
        resource_name = resource.get("resource_name")
        print "Fetching {}".format(resource_name)
        resource_db = resource.get('database', None)
        if not resource_db:
            database = sa.create_engine(DEFAULT_DB)
        else:
            database = sa.create_engine(resource_db)

        mfl_v1_object_name = resource.get("mfl_v1_object_name")
        file_name = resource.get("file_name")
        folder = resource.get("folder")
        model_name = resource.get("model_name")
        unique_fields = resource.get("unique_fields")
        data = resource.get("data", None)
        field_map = resource.get("mfl_v1_v2_fields_map")
        resource_sql = resource.get("sql", None)
        data_path = resource.get("data_file_path", None)

        if not len(data) and mfl_v1_object_name != "N/A":
            sql = "SELECT * from {}".format(mfl_v1_object_name)

            sql = sql if not resource_sql else resource_sql

            clean_data = []

            for obj in database.connect().execute(sql):
                for field in field_map:
                    if not field.get("fk_map"):
                        row_data = {
                            field.get("v2"):

                                (obj[field.get("v1_pos")].decode('cp1251')
                                    if obj[field.get("v1_pos")]
                                    and isinstance(
                                        obj[field.get("v1_pos")], str) else "")
                        }
                        clean_data.append(row_data)
                    else:
                        fk = field.get("fk_map")[0]
                        row_data = {
                            field.get("v2"): {
                                fk.get("field_name"):
                                    (obj[field.get("v1_pos")].decode('cp1251')
                                        if obj[field.get("v1_pos")]
                                        and isinstance(
                                            obj[field.get("v1_pos")],
                                            str) else "")

                            }
                        }
                        clean_data.append(row_data)

            data = clean_data
        elif not len(data) and data_path:
            with open(data_path) as data_file:
                string_data = data_file.read()
                data = json.loads(string_data)[0].get("records")

        create_engine.create_single_json_file(
            file_name, folder, model_name, json.dumps(unique_fields),
            json.dumps(data)
        )

        print "{} {} Fetched".format(len(data), resource_name)


from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        port_data()
