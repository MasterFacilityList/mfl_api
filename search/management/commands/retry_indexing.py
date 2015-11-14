import pydoc

from django.core.management import BaseCommand
from common.models import ErrorQueue
from search.search_utils import index_instance


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        objects_with_errors = ErrorQueue.objects.filter(
            error_type='SEARCH_INDEXING_ERROR')
        for obj in objects_with_errors:
            obj_path = "{}.models.{}".format(obj.app_label, obj.model_name)
            model = pydoc.locate(obj_path)
            try:
                instance = model.objects.get(id=obj.object_pk)
                index_instance(instance)
                obj.delete()
            except:
                pass
