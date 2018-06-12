import os
import glob


from django.core.management import BaseCommand

from ...bootstrap import process_json_file


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('data_file', nargs='+', type=str)

    def handle(self, *args, **options):
        for suggestion in options['data_file']:
            # if it's just a simple json file
            if os.path.exists(suggestion) and os.path.isfile(suggestion):

                process_json_file(suggestion)
            else:
                # check if it's a glob
                for filename in glob.glob(suggestion):
                    process_json_file(filename)

        self.stdout.write("Done loading")
