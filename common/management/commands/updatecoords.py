import os, sys, csv, re
import shutil

from random import randint

from rest_framework.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from tempfile import NamedTemporaryFile
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry

from facilities.models.facility_models import Facility
from mfl_gis.models import FacilityCoordinates

abc = 'abcdefghijklmnopqrstuvwxyz'
letters = abc + abc.upper()

ALLOWED_CHARS = '0123456789' + letters
NUMBER_OF_CODE_POINTS = len(ALLOWED_CHARS) - 1
NUMBER_OF_SUB_CODE_POINTS = len(letters) - 1
CODE_SIZE = 15
CODE_PATTERN = re.compile(r"[a-zA-Z]{1}[a-zA-Z0-9]{14}")

fields = [
    'MFL Code',
    'Facility',
    'County',
    'Sub County',
    'Ward',
    'Latitude',
    'Longitude',
    'Status'
]

temp_file = NamedTemporaryFile(mode='w', delete=False)


def progress_bar(value, end_value, task, bar_length=50):
    percent = float(value) / end_value
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r" + str(task) + ": [{0}] {1}% ({2})".format(arrow + spaces, int(round(percent * 100)), value))
    sys.stdout.flush()


def generate_uid():
    """
        Courtesy of DHIS2 src ('https://dhis2.github.io/d2/src_uid.js.html)
    """
    random_chars = letters[randint(0, NUMBER_OF_SUB_CODE_POINTS)]
    for i in range(1, CODE_SIZE):
        random_chars += ALLOWED_CHARS[randint(0, NUMBER_OF_CODE_POINTS)]
    return random_chars


class Command(BaseCommand):
    help = 'Updates facility coordinates from specified .csv file'

    def __init__(self):
        super(Command, self).__init__()
        self.strict = False
        self.nocode = False
        self.failed_counter = 0

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)
        parser.add_argument('--strict', nargs='+', type=str)
        parser.add_argument('--nocode', nargs='+', type=str)

    def handle(self, *args, **options):

        if options.get('strict', None):
            _strict = str(options['strict'][0]).lower()
            if _strict == 'y':
                self.strict = True

        if options.get('nocode', None):
            _nocode = str(options['nocode'][0]).lower()
            if _nocode == 'y':
                self.nocode = True

        if options.get('file', None):
            path_to_csv = options['file'][0]

            if os.path.isfile(path_to_csv):
                row_count = sum(1 for line in open(path_to_csv))
                print('\n\nStrict Mode: ' + str(self.strict))
                print('\n\nConsidering MFL Code: ' + str(self.nocode))
                print('Parsing ' + path_to_csv + '. Please wait...\n\n')
                try:
                    with open(path_to_csv, 'rb') as csvfile, temp_file:
                        reader = csv.DictReader(csvfile, fieldnames=fields)
                        writer = csv.DictWriter(temp_file, fieldnames=fields)
                        self.update_coords(row_count, reader, writer)

                        shutil.move(temp_file.name, path_to_csv)

                except Exception as e:
                    print('Error: ' + str(e))
            else:
                raise CommandError('(' + path_to_csv + ') does not exist.')
        else:
            raise CommandError('Provide csv file')

    def update_coords(self, row_count, reader, writer):

        counter = 0
        self.failed_counter = 0

        for row in reader:
            facility_code = str(row['MFL Code']).strip()
            facility_name = str(row['Facility']).strip().lower()
            facility_county = str(row['County']).strip().lower().replace(' county', '').replace('county', '')
            facility_sub_county = str(row['Sub County']).strip().lower() \
                .replace(' sub county', '').replace('sub county', '') \
                .replace(' subcounty', '').replace('subcounty', '')
            facility_ward = str(row['Ward']).strip().lower().replace(' ward', '').replace('ward', '')
            facility_latitude = str(row['Latitude']).strip()
            facility_longitude = str(row['Longitude']).strip()

            progress_bar(counter + 1, row_count, 'Progress')

            row['Status'] = generate_uid()

            try:
                if facility_code != 'NULL' and facility_code != 'MFL Code' and not self.nocode:
                    facility = Facility.objects.get(code=facility_code)
                    row['Status'] = self.update(facility, facility_latitude, facility_longitude)
                    row['MFL Code'] = facility.code
                else:
                    if self.strict:

                        facility = Facility.objects.get(
                            Q(name__iexact=facility_name) | Q(official_name__iexact=facility_name))

                        if str(facility.ward_name).lower() != facility_ward:
                            row['Status'] = 'Facility Ward Mismatch. ' \
                                            'Found ' + facility.ward_name + ' instead'
                            self.failed_counter += 1
                            counter += 1
                            writer.writerow(row)
                            continue

                        if str(facility.get_constituency).lower() != facility_sub_county:
                            row['Status'] = 'Facility Constituency / Sub County Mismatch. ' \
                                            'Found ' + facility.get_constituency + ' instead'
                            self.failed_counter += 1
                            counter += 1
                            writer.writerow(row)
                            continue

                        if str(facility.get_county).lower() != facility_county:
                            row['Status'] = 'Facility County Mismatch. ' \
                                            'Found ' + facility.get_county + ' instead'
                            self.failed_counter += 1
                            counter += 1
                            writer.writerow(row)
                            continue

                        row['Status'] = self.update(facility, facility_latitude, facility_longitude)
                        row['MFL Code'] = facility.code

                    else:
                        facility = Facility.objects.get(
                            Q(name__iexact=facility_name) | Q(official_name__iexact=facility_name))
                        row['Status'] = self.update(facility, facility_latitude, facility_longitude)
                        row['MFL Code'] = facility.code

            except Facility.MultipleObjectsReturned:
                row['Status'] = 'Multiple Facilities Returned'
                self.failed_counter += 1
            except Facility.DoesNotExist:
                row['Status'] = 'Facility Not Found'
                self.failed_counter += 1

            writer.writerow(row)
            counter += 1

        updated = row_count - self.failed_counter

        print('\n\nCompleted!\n')
        print('STATS')
        print('*************')
        print('Updated - ' + str(updated) + ' (' + str((updated / float(row_count)) * 100) + '%)')
        print('Failed - ' + str(self.failed_counter) + ' (' + str((self.failed_counter / float(row_count)) * 100) + '%)')
        print('*************\n')

    def update(self, facility, lat, long):

        if lat == 'NULL' or long == 'NULL':
            self.failed_counter += 1
            return "Coordinates NOT Complete!"
        else:
            try:

                facility_coordinates = FacilityCoordinates.objects.get(facility=facility)
                facility_coordinates.coordinates = GEOSGeometry('POINT('+long+' '+lat+')')
                # facility_coordinates = FacilityCoordinates(
                #     facility=facility,
                #     coordinates=GEOSGeometry('POINT('+long+' '+lat+')')
                # )
                facility_coordinates.save()
            except Exception as e:
                self.failed_counter += 1
                error = "Error: "+str(e).replace(",", " ")
                return error

            return "UPDATED ("+str(facility.code)+")"
