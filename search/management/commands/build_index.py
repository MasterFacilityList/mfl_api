from django.core.management import BaseCommand
from django.db.models import get_app, get_models
from django.conf import settings
from search.search_utils import index_instance


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
        non_indexable_models = settings.SEARCH.get('NON_INDEXABLE_MODELS')
        non_indexable_models_classes = []
        non_indexable_models_names = []
        for app_model in non_indexable_models:
            app_name, cls_name = app_model.split('.')
            non_indexable_models_names.append(cls_name)
            app = get_app(app_name)
            app_models = get_models(app)

            for model_cls in app_models:
                if model_cls.__name__ in non_indexable_models_names:
                    non_indexable_models_classes.append(model_cls)
        non_indexable_models_classes = list(set(non_indexable_models_classes))

        for app_name in apps_lists:
            app = get_app(app_name)
            for model in get_models(app):
                if model not in non_indexable_models_classes:
                    all_instances = model.objects.all()[0:3] \
                        if options.get('test') else model.objects.all()
                    [index_instance(obj) for obj in all_instances]
                    message = "Indexed {} {}".format(
                        all_instances.count(),
                        model._meta.verbose_name_plural.capitalize())
                    self.stdout.write(message)
                else:
                    message = "Not indexing model {}".format(
                        model.__name__)
                    self.stdout.write(message)

        self.stdout.write("Finished indexing")
