from rest_framework import generics
from django.db.models.deletion import Collector, ProtectedError


def delete_child_instances(instance):
    try:
        collector = Collector(using='default')
        collector.collect(objs=[instance], collect_related=True)
    except ProtectedError as error:
        protected_objects = error.protected_objects
        for obj in protected_objects:
            delete_child_instances(obj)
            obj.deleted = True
            obj.save()


class CustomDestroyModelMixin(object):

    def perform_destroy(self, instance):
        delete_child_instances(instance)
        instance.deleted = True
        instance.save()


class CustomRetrieveUpdateDestroyView(
        CustomDestroyModelMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
