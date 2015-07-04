from django.conf import settings
import csv
import os
import json

file_path = os.path.join(
    settings.BASE_DIR, 'data/csvs/facility_services_through_yn.csv')

bc_file_path = os.path.join(
    settings.BASE_DIR, 'data/csvs/facility_services_through_bc.csv')


keph_file_path = os.path.join(
    settings.BASE_DIR, 'data/csvs/facility_services_through_keph.csv')
from facilities.models import Facility


def read_csv_yn_file():
    service_options = []
    facility_services = []
    with open(file_path, 'r') as csv_file:
        fs_reader = csv.reader(csv_file)
        # col_names = [
        #     "ID_FACILITY", "svcId", "svcName",
        # "Facility_Code", "Facility_Name"]
        index = 0
        for row in fs_reader:

            # Create the service options
            # import pdb
            # pdb.set_trace()
            if len(row) == 5:
                b_templete_dict = {
                    "option": {
                        "value": "Yes"
                    },
                    "service": {
                        "name": str(unicode(row[2], errors='ignore'))
                    }
                }
                c_templete_dict = {
                    "option": {
                        "value": "No"
                    },
                    "service": {
                        "name": str(unicode(row[2], errors='ignore'))
                    }
                }
                if b_templete_dict not in service_options:
                    service_options.append(b_templete_dict)
                if c_templete_dict not in service_options:
                    service_options.append(c_templete_dict)

                # create the facility services
                selected_option_template_dict = {
                    "selected_option": b_templete_dict,
                    "facility": {
                        "name": str(unicode(row[4], errors='ignore'))
                    }
                }
                try:
                    Facility.objects.get(
                        name=str(unicode(row[4], errors='ignore')))

                    if (
                            selected_option_template_dict not in
                            facility_services):
                        facility_services.append(
                            selected_option_template_dict)
                    # print row[4]
                    print index
                except Facility.DoesNotExist:
                    pass
                    # print "Facility {} does not exist".format(row[4])
                index = index + 1

            else:
                pass
        return service_options, facility_services


def read_csv_bc_file():
    service_options = []
    facility_services = []
    with open(bc_file_path, 'r') as csv_file:
        fs_reader = csv.reader(csv_file)
        # col_names = [
        #     "ID_FACILITY", "svcId", "svcName",
        # "Facility_Code", "Facility_Name"]
        index = 0
        for row in fs_reader:

            # Create the service options
            # import pdb
            # pdb.set_trace()
            if len(row) == 5:
                b_templete_dict = {
                    "option": {
                        "value": "Basic"
                    },
                    "service": {
                        "name": str(unicode(row[2], errors='ignore'))
                    }
                }
                c_templete_dict = {
                    "option": {
                        "value": "Comprehensive"
                    },
                    "service": {
                        "name": str(unicode(row[2], errors='ignore'))
                    }
                }
                if b_templete_dict not in service_options:
                    service_options.append(b_templete_dict)
                if c_templete_dict not in service_options:
                    service_options.append(c_templete_dict)

                # create the facility services
                selected_option_template_dict = {
                    "selected_option": b_templete_dict,
                    "facility": {
                        "name": str(unicode(row[4], errors='ignore'))
                    }
                }
                try:
                    Facility.objects.get(
                        name=str(unicode(row[4], errors='ignore')))

                    if (
                            selected_option_template_dict not in
                            facility_services):
                        facility_services.append(
                            selected_option_template_dict)
                    # print row[4]
                    print index
                except Facility.DoesNotExist:
                    pass
                    # print "Facility {} does not exist".format(row[4])
                index = index + 1

            else:
                pass
        return service_options, facility_services


def read_csv_keph_file():
    service_options = []
    facility_services = []
    with open(bc_file_path, 'r') as csv_file:
        fs_reader = csv.reader(csv_file)
        # col_names = [
        #     "ID_FACILITY", "svcId", "svcName",
        # "Facility_Code", "Facility_Name"]
        index = 0
        for row in fs_reader:

            # Create the service options
            # import pdb
            # pdb.set_trace()
            if len(row) == 5:
                b_templete_dict = {
                    "option": {
                        "value": "Basic"
                    },
                    "service": {
                        "name": str(unicode(row[2], errors='ignore'))
                    }
                }
                c_templete_dict = {
                    "option": {
                        "value": "Comprehensive"
                    },
                    "service": {
                        "name": str(unicode(row[2], errors='ignore'))
                    }
                }
                if b_templete_dict not in service_options:
                    service_options.append(b_templete_dict)
                if c_templete_dict not in service_options:
                    service_options.append(c_templete_dict)

                # create the facility services
                selected_option_template_dict = {
                    "selected_option": b_templete_dict,
                    "facility": {
                        "name": str(unicode(row[4], errors='ignore'))
                    }
                }
                try:
                    Facility.objects.get(
                        name=str(unicode(row[4], errors='ignore')))

                    if (
                            selected_option_template_dict not in
                            facility_services):
                        facility_services.append(
                            selected_option_template_dict)
                    # print row[4]
                    print index
                except Facility.DoesNotExist:
                    pass
                    # print "Facility {} does not exist".format(row[4])
                index = index + 1

            else:
                pass
        return service_options, facility_services

def write_to_file():
    options, facility_services = read_csv_yn_file()
    with open('service_options.txt', 'w+') as service_option_file:
        service_option_file.write(json.dumps(options))
    with open('facility_services.txt', 'w+') as fs_file:
        fs_file.write(json.dumps(facility_services))
    print "Nimemaliza kuchonga hizo files"


def write_bcs_to_file():
    options, facility_services = read_csv_bc_file()
    with open('service_options_bc.txt', 'w+') as service_option_file:
        service_option_file.write(json.dumps(options))
    with open('facility_services_bc.txt', 'w+') as fs_file:
        fs_file.write(json.dumps(facility_services))
    print "Nimemaliza kuchonga hizo files"
