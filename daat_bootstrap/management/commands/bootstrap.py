import os
import glob

from django.core.management import BaseCommand

from sil_data_bootstrap.bootstrap import process_json_file


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for suggestion in args:
            # if it's just a simple json file
            if os.path.exists(suggestion) and os.path.isfile(suggestion):
                process_json_file(suggestion)
            else:
                # check if it's a glob
                for filename in glob.glob(suggestion):
                    process_json_file(filename)
        print "Done loading"
