from django.core.management import BaseCommand
from django.db.models import get_app, get_models
from django.conf import settings

from search.search_utils import index_instance, confirm_model_is_indexable


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            dest='test',
            default=False,
            help='Provide this if you want to create a test index')

    def handle(self, *args, **options):
        # optimize this to index in bulk

        apps_lists = settings.LOCAL_APPS

        for app_name in apps_lists:
            app = get_app(app_name)
            for model in get_models(app):
                if model and confirm_model_is_indexable(model):
                    all_instances = model.objects.all()[0:100] \
                        if options.get('test') else model.objects.all()
                    [
                        index_instance(
                            obj._meta.app_label,
                            obj.__class__.__name__,
                            str(obj.id))
                        for obj in all_instances]
                    message = "Indexed {} {}".format(
                        all_instances.count(),
                        model._meta.verbose_name_plural.capitalize())
                    self.stdout.write(message)
                else:
                    message = "Not indexing model {}".format(
                        model.__name__)
                    self.stdout.write(message)

        self.stdout.write("Finished indexing")
